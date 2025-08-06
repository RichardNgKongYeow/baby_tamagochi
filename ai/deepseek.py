import subprocess
import time
import requests
import platform
import websocket


# === CORE UTILITY ===

def retry_operation(operation, max_attempts, delay, operation_name):
    attempts = 0
    while max_attempts is None or attempts < max_attempts:
        try:
            if operation():
                print(f"{operation_name} is ready!")
                return True
        except Exception as e:
            print(f"Attempt {attempts + 1}/{max_attempts or '∞'} - {operation_name} not ready: {e}")
        attempts += 1
        time.sleep(delay)
    print(f"Failed to get {operation_name} ready within {max_attempts} attempts.")
    return False


# === DEEPSEEK MODEL ===

def run_deepseek():
    print("🚀 Starting DeepSeek via Ollama...")
    try:
        result = subprocess.run(["ollama", "--version"], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Ollama not installed or not found.")
            return False
        subprocess.Popen(["ollama", "run", "deepseek-r1:8b"], shell=(platform.system() == "Windows"))
        time.sleep(10)
        return True
    except Exception as e:
        print(f"Failed to start DeepSeek: {e}")
        return False


def is_deepseek_running():
    try:
        r = requests.get("http://localhost:11434/api/tags", timeout=10)
        r.raise_for_status()
        models = r.json().get("models", [])
        if not any(m.get("name", "").startswith("deepseek-r1") for m in models):
            print("DeepSeek model not found in Ollama.")
            return False

        # Test generation
        r = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "deepseek-r1:8b", "prompt": "Hello", "stream": False},
            timeout=15
        )
        r.raise_for_status()
        return True
    except Exception as e:
        print(f"DeepSeek check failed: {e}")
        return False


def wait_for_deepseek(timeout=300):
    max_attempts = int(timeout / 5) if timeout else None
    return retry_operation(is_deepseek_running, max_attempts, 5, "DeepSeek")


def chat(prompt: str) -> str:
    try:
        r = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "deepseek-r1:8b",
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )
        r.raise_for_status()
        return r.json().get("response", "").strip()
    except Exception as e:
        return f"Error generating response: {str(e)}"


# === OPTIONAL: WEBUI DOCKER SECTION (RUN SEPARATELY) ===

def check_port_free(port):
    try:
        result = subprocess.run(["netstat", "-tuln"], capture_output=True, text=True)
        return f":{port}" not in result.stdout
    except Exception:
        return True


def is_webui_running():
    try:
        r = requests.get("http://localhost:3000/signin", timeout=10)
        r.raise_for_status()
        return True
    except Exception as e:
        print(f"WebUI check failed: {e}")
        return False


def is_websocket_alive():
    try:
        ws = websocket.WebSocket()
        ws.connect("ws://localhost:3000/ws/socket.io/?EIO=4&transport=websocket", timeout=5)
        ws.send('0')
        response = ws.recv()
        ws.close()
        return '"sid"' in response
    except Exception as e:
        print(f"WebSocket check failed: {e}")
        return False


def run_webui(userid, password):
    print("🧹 Cleaning up old WebUI container...")
    subprocess.run(["docker", "rm", "-f", "open-webui"], capture_output=True, text=True)

    if not check_port_free(3000):
        print("Port 3000 is in use. Please free it before running.")
        return False

    docker_command = [
        "docker", "run", "-d", "-p", "3000:8080",
        "-v", "open-webui:/app/backend/data",
        "--name", "open-webui",
        "--add-host=host.docker.internal:host-gateway",
        "-e", "OLLAMA_API_BASE_URL=http://127.0.0.1:11434",
        "-e", "WEBUI_AUTH=true",
        "-e", f"ADMIN_EMAIL={userid}",
        "-e", f"ADMIN_PASSWORD={password}",
        "--restart", "unless-stopped",
        "ghcr.io/open-webui/open-webui:main"
    ]

    try:
        subprocess.run(docker_command, check=True, capture_output=True, text=True)
        print("✅ Started WebUI container.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to start WebUI container: {e.stderr}")
        return False

    if not retry_operation(is_webui_running, 30, 5, "WebUI"):
        subprocess.run(["docker", "logs", "open-webui"])
        return False

    if not retry_operation(is_websocket_alive, 10, 3, "WebSocket"):
        subprocess.run(["docker", "logs", "open-webui"])
        return False

    print("✅ WebUI is running and reachable.")
    return True

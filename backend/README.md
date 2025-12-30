**Overview**
This folder contains a lightweight Flask backend that wraps a Lambda-style handler and exposes a `/chat` endpoint used by the frontend.

**Prerequisites**
- **Python:** Python 3.8 or newer installed.
- **Tools:** `git` and a POSIX shell (macOS/Linux) or PowerShell on Windows.

**Setup (macOS / Linux / zsh / Windows)**
- **Create venv:**
```sh
python3 -m venv .venv
```
- **Activate venv for macOS / Linux / zsh:**
```sh
source .venv/bin/activate
```
- **Activate venv for Windows powershell**
```sh
.\.venv\Scripts\Activate.ps1
```
- **Install requirements:**
```sh
pip install --upgrade pip
pip install -r requirements.txt
```

**Setup (Windows - PowerShell)**
```ps
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

**Run the server**
- Start the Flask server (default port 5000):
```sh
python server.py
```
- The server exposes `POST /chat` which the frontend calls. The request/response format is JSON.

**Quick test (curl)**
```sh
curl -X POST http://127.0.0.1:5000/chat \
	-H "Content-Type: application/json" \
	-d '{"message":"Hello"}'
```

**Files**
- **`server.py`:** Flask entrypoint — defines the `/chat` route and starts the local server.
- **`lambda_function.py`:** Core business logic and `lambda_handler` used by `server.py`.
- **`requirements.txt`:** Python dependencies required by the backend.

**Troubleshooting**
- **Port in use:** If port 5000 is already in use, stop the other process or change the port in `app.run(...)` inside `server.py`.
- **Missing packages:** Ensure the virtual environment is activated and run `pip install -r requirements.txt`.
- **CORS issues:** CORS is enabled in `server.py` so the Vite frontend (default port 5173) can call the backend; if you still see CORS errors, verify the frontend origin and the backend configuration.

**Notes**
- The backend implements a thin wrapper around the local Lambda-style handler in `lambda_function.py`. The frontend expects a JSON response with `message` (and optional `action`) fields.
- When sharing or deploying, remember to secure any secrets and follow environment-specific deployment practices.

**Contact**
- For questions about the backend implementation, inspect `server.py` and `lambda_function.py` in this folder.

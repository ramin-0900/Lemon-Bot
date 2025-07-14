from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import subprocess
import signal
import time

load_dotenv()

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BOT_SCRIPT_PATH = "main.py"
PID_FILE = "bot.pid"

def is_bot_running():
    if not os.path.exists(PID_FILE):
        return False
    try:
        with open(PID_FILE, "r") as f:
            pid = int(f.read().strip())
        os.kill(pid, 0)
    except (IOError, ValueError, OSError):
        return False
    else:
        return True

def start_bot_process():
    if not is_bot_running():
        process = subprocess.Popen(["python3", BOT_SCRIPT_PATH])
        with open(PID_FILE, "w") as f:
            f.write(str(process.pid))
        print(f"Bot started with PID: {process.pid}")
        return True
    return False

def stop_bot_process():
    if os.path.exists(PID_FILE):
        try:
            with open(PID_FILE, "r") as f:
                pid = int(f.read().strip())
            os.kill(pid, signal.SIGTERM)
            print(f"Sent SIGTERM to bot process with PID: {pid}")
            os.remove(PID_FILE)
            return True
        except (IOError, ValueError, OSError) as e:
            print(f"Error stopping bot: {e}. Cleaning up PID file.")
            os.remove(PID_FILE)
            return False
    return False

app.mount("/static", StaticFiles(directory="static", html=True), name="static_files")

@app.get("/")
async def root():
    return RedirectResponse("/index.html")

class TokenInput(BaseModel):
    token: str

@app.get("/status")
def get_status():
    return {
        "bot_running": is_bot_running(),
        "guilds": 5
    }

@app.post("/update-token")
def update_token(data: TokenInput):
    env_file = ".env"
    if not os.path.exists(env_file):
        with open(env_file, "w") as f:
            f.write(f"DISCORD_TOKEN={data.token}\n")
        return {"status": "created_and_updated"}
    
    try:
        lines = []
        token_found = False
        with open(env_file, "r") as f:
            lines = f.readlines()

        with open(env_file, "w") as f:
            for line in lines:
                if line.strip().startswith("DISCORD_TOKEN="):
                    f.write(f"DISCORD_TOKEN={data.token}\n")
                    token_found = True
                else:
                    f.write(line)
            if not token_found:
                f.write(f"DISCORD_TOKEN={data.token}\n")

        return {"status": "updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/restart")
def restart_bot():
    print("Restart command received.")
    if is_bot_running():
        print("Bot is running, attempting to stop...")
        stop_bot_process()
        time.sleep(2)
    
    print("Attempting to start bot...")
    if start_bot_process():
        return {"status": "restarted"}
    else:
        raise HTTPException(status_code=409, detail="Bot is already running or failed to start.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)

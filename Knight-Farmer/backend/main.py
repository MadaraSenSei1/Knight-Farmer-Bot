from fastapi import FastAPI, UploadFile, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from uuid import uuid4
from bot.travian_bot import TravianBot
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

ACCOUNTS = {}

class LoginData(BaseModel):
    username: str
    password: str
    server: str
    proxy: str

class IntervalConfig(BaseModel):
    uuid: str
    min: int
    max: int
    randomize: bool

@app.get("/")
async def get_root():
    return FileResponse("static/index.html")

@app.post("/api/login")
async def login(data: LoginData):
    uuid = str(uuid4())
    bot = TravianBot(
        username=data.username,
        password=data.password,
        server=data.server,
        proxy=data.proxy
    )
    success = bot.login()
    if not success:
        return JSONResponse(content={"error": "Login failed"}, status_code=401)

    ACCOUNTS[uuid] = bot
    return {"uuid": uuid}

@app.get("/api/farmlist/{uuid}")
async def get_farmlist(uuid: str):
    bot = ACCOUNTS.get(uuid)
    if not bot:
        return JSONResponse(content={"error": "Bot not found"}, status_code=404)
    farms = bot.get_farm_lists()
    return {"farmlists": farms}

@app.post("/api/start")
async def start_bot(config: IntervalConfig):
    bot = ACCOUNTS.get(config.uuid)
    if not bot:
        return JSONResponse(content={"error": "Bot not found"}, status_code=404)
    bot.start_farming(config.min, config.max, config.randomize)
    return {"status": "started"}

@app.post("/api/stop/{uuid}")
async def stop_bot(uuid: str):
    bot = ACCOUNTS.get(uuid)
    if bot:
        bot.stop()
    return {"status": "stopped"}

@app.get("/api/status/{uuid}")
async def get_status(uuid: str):
    bot = ACCOUNTS.get(uuid)
    if not bot:
        return {"running": False}
    return {"running": bot.is_running()}

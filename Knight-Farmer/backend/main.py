from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from uuid import uuid4
from typing import Optional
from bot.travian_bot import TravianBot

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
ACCOUNTS = {}

class ProxyData(BaseModel):
    ip: Optional[str] = ""
    port: Optional[str] = ""
    username: Optional[str] = ""
    password: Optional[str] = ""

class LoginData(BaseModel):
    username: str
    password: str
    server: str
    proxy: ProxyData

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
    try:
        proxy = data.proxy
        proxy_str = None
        if proxy and proxy.ip:
            proxy_str = f"{proxy.username}:{proxy.password}@{proxy.ip}:{proxy.port}" if proxy.username else f"{proxy.ip}:{proxy.port}"

        bot = TravianBot(data.username, data.password, data.server, proxy_str)
        success = bot.login()

        if not success:
            return JSONResponse(content={"error": "Login failed on Travian side"}, status_code=401)

        uuid = str(uuid4())
        ACCOUNTS[uuid] = bot
        farms = bot.get_farm_lists()
        return {"uuid": uuid, "farm_lists": farms}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/api/farmlist/{uuid}")
async def get_farmlist(uuid: str):
    bot = ACCOUNTS.get(uuid)
    if not bot:
        return JSONResponse(content={"error": "Bot not found"}, status_code=404)
    try:
        farms = bot.get_farm_lists()
        return {"farmlists": farms}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/api/start")
async def start_bot(config: IntervalConfig):
    bot = ACCOUNTS.get(config.uuid)
    if not bot:
        return JSONResponse(content={"error": "Bot not found"}, status_code=404)
    try:
        bot.start_farming(config.min, config.max, config.randomize)
        return {"status": "started"}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/api/stop/{uuid}")
async def stop_bot(uuid: str):
    bot = ACCOUNTS.get(uuid)
    if bot:
        try:
            bot.stop()
        except Exception as e:
            return JSONResponse(content={"error": str(e)}, status_code=500)
    return {"status": "stopped"}

@app.get("/api/status/{uuid}")
async def get_status(uuid: str):
    bot = ACCOUNTS.get(uuid)
    if not bot:
        return {"running": False}
    try:
        return {"running": bot.is_running()}
    except Exception:
        return {"running": False}

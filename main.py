from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from backend.api import data
from backend.api import auth
from backend.utils.exceptions_handlers import setup_exception_handlers


app = FastAPI()
setup_exception_handlers(app)

app.include_router(auth.auth_router)
app.include_router(data.data_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # для тестирования разрешаем все источники
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def status():
    return {"status":"ok"}

app.mount("/", StaticFiles(directory="frontend", html=True), name="static")

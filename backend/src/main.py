from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers.task_router import router as task_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(task_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}

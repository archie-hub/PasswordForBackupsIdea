"""
This needs to be behind a load balancer with some security and SSL at a minimum.
"""
from os import getenv
from fastapi import FastAPI, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from lambda_src.modules import generate_password


app = FastAPI()

origins = ["*"]
# WE should narrow this down for security. Work in progress

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter()

class PasswordRequest(BaseModel):
    string1: str
    string2: str

@router.post("/makeapassword")
async def makepassword(request: PasswordRequest):
    generated_seed = request.string1 + request.string2
    password = generate_password(generated_seed,
                                 length=15,
                                 defaultseed=getenv("STARTSEED")) #<= Reading this from podman env.
    return {"our_password": password}

@router.get("/", response_class=HTMLResponse)
async def get_index():
    with open("static/index.html", "r") as file:
        return file.read()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

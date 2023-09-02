from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from . import models
from .routers import post, user, auth, vote
from .config import settings
from alembic import config
from alembic import command
import os
print(settings.database_username)


# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

# current_directory = os.path.dirname(__file__)
# alembic_ini_path = os.path.join(current_directory, "../alembic.ini")
# alembic_cfg = config.Config(alembic_ini_path)
# command.upgrade(alembic_cfg, "head")

@app.get("/") # The Decorater: turns this into a path operation and makes endpoint
def root(): # The Function
    return {"message": "Kenzy Abozeed Enty Panda"}







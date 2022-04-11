from fastapi import FastAPI
from starlette.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from .routes import posts, users, auth
from . import models
from .database import engine

app = FastAPI()

# Handling CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


# Sets up database and its tables
models.Base.metadata.create_all(bind=engine)

# including the routes
app.include_router(posts.router);
app.include_router(users.router);
app.include_router(auth.router);

@app.get("/")
def main():
    return RedirectResponse(url="/docs/")
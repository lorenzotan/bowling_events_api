from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import events, locations

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:8100"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(events.router)
app.include_router(locations.router)

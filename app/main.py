from fastapi import FastAPI
from .routers import events, locations

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(events.router)
app.include_router(locations.router)

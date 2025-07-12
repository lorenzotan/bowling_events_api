from fastapi import APIRouter, FastAPI

app = FastAPI()
router = APIRouter()

@router.get("/events/", tags=["events"])
async def read_events():
    return [
        {"event": "League"},
        {"event": "Tournament"}
        ]
"""
JSON Response Template
{
    id: <event_id>
    name: <event_name>
    category: <category league|tournament>
    start_date: <start_date>
    end_date: <end_date>
    game_day: <game_day>
    game_time: <game_time>
    registration_url: <url>
    location: <location_name>
}
"""

app.include_router(router)
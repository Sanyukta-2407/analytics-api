from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = "ak_l5ya7qce7nzaz9jlads6rk7v"
EMAIL = "22f2001139@ds.study.iitm.ac.in"


class Event(BaseModel):
    user: str
    amount: float
    ts: int


class EventBatch(BaseModel):
    events: List[Event]


@app.get("/")
def root():
    return {"message": "Analytics API running"}


@app.post("/analytics")
def analytics(
    batch: EventBatch,
    x_api_key: str = Header(None),
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    total_events = len(batch.events)

    unique_users = len(set(event.user for event in batch.events))

    revenue = sum(event.amount for event in batch.events if event.amount > 0)

    user_totals = {}
    for event in batch.events:
        if event.amount > 0:
            user_totals[event.user] = user_totals.get(event.user, 0) + event.amount

    top_user = max(user_totals, key=user_totals.get) if user_totals else ""

    return {
        "email": EMAIL,
        "total_events": total_events,
        "unique_users": unique_users,
        "revenue": revenue,
        "top_user": top_user,
    }
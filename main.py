from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
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
    x_api_key: str = Header(None)
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401)

    total_events = len(batch.events)

    unique_users = len(set(e.user for e in batch.events))

    revenue = sum(e.amount for e in batch.events if e.amount > 0)

    totals = {}

    for e in batch.events:
        if e.amount > 0:
            totals[e.user] = totals.get(e.user, 0) + e.amount

    top_user = max(totals, key=totals.get) if totals else ""

    return {
        "email": EMAIL,
        "total_events": total_events,
        "unique_users": unique_users,
        "revenue": revenue,
        "top_user": top_user,
    }
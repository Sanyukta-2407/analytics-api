from fastapi import Header, HTTPException

API_KEY = "ak_l5ya7qce7nzaz9jlads6rk7v"

@app.post("/analytics")
def analytics(
    batch: EventBatch,
    x_api_key: str | None = Header(default=None, alias="X-API-Key")
):
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )

    total_events = len(batch.events)
    unique_users = len({e.user for e in batch.events})
    revenue = sum(e.amount for e in batch.events if e.amount > 0)

    totals = {}
    for e in batch.events:
        if e.amount > 0:
            totals[e.user] = totals.get(e.user, 0) + e.amount

    top_user = max(totals, key=totals.get) if totals else ""

    return {
        "email": "22f2001139@ds.study.iitm.ac.in",
        "total_events": total_events,
        "unique_users": unique_users,
        "revenue": revenue,
        "top_user": top_user,
    }
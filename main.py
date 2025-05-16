from fastapi import FastAPI
from api import converter, users
from db.operations import fetch_and_cache_supported_currencies
import asyncio

app = FastAPI()

app.include_router(users.router)
app.include_router(converter.router)


@app.on_event("startup")
async def startup_event():
    print("Fetching supported currencies...")
    success = await fetch_and_cache_supported_currencies()
    if success:
        print("Supported currencies fetched and cached successfully.")
    else:
        print("Failed to fetch and cache supported currencies.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
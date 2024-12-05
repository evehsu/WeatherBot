import logging
import os
from fastapi import FastAPI
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from subscribe import Subscription, check_weather_for_single_subscription, check_weather_for_subscribers
from database import init_db

logging.basicConfig(level=logging.INFO)

app = FastAPI()
scheduler = BackgroundScheduler()

@app.post("/subscribe")
async def subscribe(subscription: Subscription):
    # Test the subscription immediately
    try:
        await check_weather_for_single_subscription(subscription)
        return {"message": "Subscription successful and initial check completed"}
    except Exception as e:
        logging.error(f"Subscription added but initial check failed: {str(e)}")
        return {"message": "Subscription successful but initial check failed"}

# Main script
if __name__ == "__main__":
    load_dotenv(override=True)
    init_db()  # Initialize the database
    scheduler.add_job(check_weather_for_subscribers, 'interval', hours=24)
    scheduler.start()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


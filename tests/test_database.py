import pytest
from database import save_subscriber, get_subscriber_by_email, get_all_subscribers
from subscribe_objects import Subscriber

def test_save_and_retrieve_subscriber(test_db):

    # Create test subscriber
    subscriber = Subscriber(
        user_email="test_xxx@example.com",
        user_destination=["Seattle", "Portland"],
        sunny_threshold=[2, 2],
        time_window=[7, 7]
    )
    
    # Save subscriber
    save_subscriber(subscriber)
    
    # Retrieve subscriber
    retrieved = get_subscriber_by_email("test_xxx@example.com")
    assert retrieved is not None
    assert retrieved.user_email == subscriber.user_email
    assert retrieved.user_destination == subscriber.user_destination
    assert retrieved.sunny_threshold == subscriber.sunny_threshold
    assert retrieved.time_window == subscriber.time_window

def test_get_all_subscribers(test_db):

    # Create multiple test subscribers
    subscribers = [
        Subscriber(
            user_email=f"new{i}@example.com",
            user_destination=["Seattle"],
            sunny_threshold=[2],
            time_window=[7]
        )
        for i in range(3)
    ]
    
    # Save all subscribers
    for subscriber in subscribers:
        save_subscriber(subscriber)

    # Retrieve all subscribers
    retrieved = get_all_subscribers(verbose=True)
    assert len(retrieved) == 3 
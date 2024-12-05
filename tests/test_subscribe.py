import pytest
from subscribe import manage_subscription, check_weather_for_subscribers
from subscribe_objects import Subscription
import uuid

def test_manage_subscription(test_db):
    # Test creating new subscription
    new_user = str(uuid.uuid4())
    subscription = Subscription(
        email=f"{new_user}@example.com",
        locations=["Seattle", "Portland"],
        sunny_threshold=2,
        time_window=7
    )
    
    subscriber = manage_subscription(subscription)
    assert subscriber.user_email == subscription.email
    assert len(subscriber.user_destination) == 2
    
    # Test updating existing subscription
    new_subscription = Subscription(
        email=f"{new_user}@example.com",
        locations=["Miami"],
        sunny_threshold=3,
        time_window=14
    )
    
    updated_subscriber = manage_subscription(new_subscription)
    assert updated_subscriber.user_email == new_subscription.email
    assert "Miami" in updated_subscriber.user_destination
    assert len(updated_subscriber.user_destination) == 3
    
    another_subscription = Subscription(
        email=f"{new_user}@example.com",
        locations=["San Francisco"],
        sunny_threshold=3,
        time_window=14
    )
    updated_subscriber = manage_subscription(another_subscription)  # respect max locations
    assert "San Francisco" in updated_subscriber.user_destination
    assert "Seattle" not in updated_subscriber.user_destination

# def test_check_weather_for_subscribers(test_db, mock_weather_api, mock_email_sender):
#     # Create test subscription
#     subscription = Subscription(
#         email="test@example.com",
#         locations=["Seattle"],
#         sunny_threshold=2,
#         time_window=7
#     )
#     manage_subscription(subscription)
    
#     # Run weather check
#     check_weather_for_subscribers()
    
#     # Verify email was sent (because mock weather is sunny)
#     mock_email_sender.assert_called_once() 
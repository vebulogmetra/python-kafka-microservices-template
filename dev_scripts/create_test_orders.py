import requests
import json
import random

url = "http://127.0.0.1:5002/order"

for i in range(5):
    user_id = str(random.randint(1, 100))
    order_id = str(random.randint(1, 100))
    user_email = f"email{random.randint(1, 10)}@ml.com"
    price = random.randint(100, 200)
    quantity = random.randint(1, 10)

    data = {
        "user_id": user_id,
        "order_id": order_id,
        "user_email": user_email,
        "order_details": {"price": price, "quantity": quantity},
    }

    headers = {"accept": "application/json", "Content-Type": "application/json"}

    response = requests.post(url, headers=headers, data=json.dumps(data))

    print(f"Request {i+1} status code: {response.status_code}")

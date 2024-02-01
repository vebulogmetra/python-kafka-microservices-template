#!/bin/bash

url="http://127.0.0.1:5002/order"

for i in {1..5}
do
    user_id=$(shuf -i 1-100 -n 1)
    order_id=$(shuf -i 1-100 -n 1)
    user_email="email$(( RANDOM % 10 + 1 ))@ml.com"
    price=$(( RANDOM % 101 + 100 ))
    quantity=$(( RANDOM % 10 + 1 ))

    data='{"user_id": "'$user_id'", "order_id": "'$order_id'", "user_email": "'$user_email'", "order_details": {"price": '$price', "quantity": '$quantity'}}'
    
    curl -X 'POST' $url -H 'accept: application/json' -H 'Content-Type: application/json' -d "$data" -s -o /dev/null -w "Request $i status code: %{http_code}\n"
done
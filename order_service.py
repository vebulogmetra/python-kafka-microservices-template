import json
import uvicorn
from datetime import datetime

from kafka import KafkaProducer
from fastapi import FastAPI
from DTOs import OrderModel
from loggers import get_logger
from settings import (
    KAFKA_SERVER,
    KAFKA_TOPIC_ORDER,
    KAFKA_SECURITY_PROTOCOL,
    APP_DATETIME_STR_FORMAT,
    APP_ORDER_SERVICE_HOST,
    APP_ORDER_SERVICE_PORT,
)

logger = get_logger(__name__)


app = FastAPI()


producer = KafkaProducer(
    bootstrap_servers=[KAFKA_SERVER],
    security_protocol=KAFKA_SECURITY_PROTOCOL,
    value_serializer=lambda x: json.dumps(x).encode("utf-8"),
)


@app.post("/order")
def order_handler(order_data: OrderModel):
    order_data.created_at = datetime.now().strftime(APP_DATETIME_STR_FORMAT)
    order: dict = order_data.model_dump()

    producer.send(KAFKA_TOPIC_ORDER, order)
    logger.info(f"Sent message to kafka topic: {KAFKA_TOPIC_ORDER}")
    return order_data


if __name__ == "__main__":
    uvicorn.run(
        "order_service:app",
        host=APP_ORDER_SERVICE_HOST,
        port=APP_ORDER_SERVICE_PORT,
        reload=True,
    )

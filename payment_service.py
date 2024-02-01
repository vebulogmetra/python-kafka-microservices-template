import json
from kafka import KafkaConsumer, KafkaProducer
from DTOs import OrderModel
from loggers import get_logger
from settings import (
    KAFKA_SERVER,
    KAFKA_SECURITY_PROTOCOL,
    KAFKA_TOPIC_ORDER,
    KAFKA_TOPIC_PAYMENT,
)

logger = get_logger(__name__)


consumer = KafkaConsumer(
    KAFKA_TOPIC_ORDER,
    bootstrap_servers=[KAFKA_SERVER],
    security_protocol=KAFKA_SECURITY_PROTOCOL,
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
)
producer = KafkaProducer(
    bootstrap_servers=[KAFKA_SERVER],
    security_protocol=KAFKA_SECURITY_PROTOCOL,
    value_serializer=lambda x: json.dumps(x).encode("utf-8"),
)

while True:
    for message in consumer:
        logger.info(f"Received message from topic: {KAFKA_TOPIC_ORDER}")
        order = OrderModel(
            user_id=message.value["user_id"],
            order_id=message.value["order_id"],
            user_email=message.value["user_email"],
            order_details=message.value["order_details"],
            created_at=message.value["created_at"],
        )
        logger.info("Confirmation order foo...")
        order.status = "confirmed"

        order_confirmed = order.model_dump()

        producer.send(KAFKA_TOPIC_PAYMENT, order_confirmed)
        logger.info(f"Sent message to kafka topic: {KAFKA_TOPIC_PAYMENT}")

import json

from kafka import KafkaConsumer, KafkaProducer
from DTOs import OrderModel
from loggers import get_logger
from settings import (
    KAFKA_SERVER,
    KAFKA_SECURITY_PROTOCOL,
    KAFKA_TOPIC_PAYMENT,
    KAFKA_TOPIC_SENT_NOTIFY,
)

logger = get_logger(__name__)


producer = KafkaProducer(
    bootstrap_servers=[KAFKA_SERVER],
    security_protocol=KAFKA_SECURITY_PROTOCOL,
    value_serializer=lambda x: json.dumps(x).encode("utf-8"),
)

consumer = KafkaConsumer(
    KAFKA_TOPIC_PAYMENT,
    bootstrap_servers=[KAFKA_SERVER],
    security_protocol=KAFKA_SECURITY_PROTOCOL,
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
)


def send_email(user_email, order_details):
    logger.info(f"Sending email to: {user_email}. Order details: {order_details}")

    return True


while True:
    for message in consumer:
        logger.info(f"Received message from topic: {KAFKA_TOPIC_PAYMENT}")

        order = OrderModel(
            user_id=message.value["user_id"],
            order_id=message.value["order_id"],
            user_email=message.value["user_email"],
            order_details=message.value["order_details"],
            created_at=message.value["created_at"],
            status=message.value["status"],
        )

        is_sent = send_email(order.user_email, order.order_details)

        order.status = "sent" if is_sent else "failed"

        producer.send(KAFKA_TOPIC_SENT_NOTIFY, order.model_dump())
        logger.info(f"Sent message to kafka topic: {KAFKA_TOPIC_SENT_NOTIFY}")

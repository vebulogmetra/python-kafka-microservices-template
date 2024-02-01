import json

from kafka import KafkaConsumer, KafkaProducer
from loggers import get_logger
from settings import (
    KAFKA_SERVER,
    KAFKA_SECURITY_PROTOCOL,
    KAFKA_TOPIC_ANALYTIC,
    KAFKA_TOPIC_PAYMENT,
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

total_revenue = 0
total_orders_count = 0

while True:
    for message in consumer:
        logger.info(f"Received message from kafka topic: {KAFKA_TOPIC_PAYMENT}")

        order_details = message.value["order_details"]
        total_revenue += int(order_details["price"])
        total_orders_count += int(order_details["quantity"])

        analytics = {}
        analytics["total_revenue"] = total_revenue
        analytics["total_orders_count"] = total_orders_count
        producer.send(KAFKA_TOPIC_ANALYTIC, analytics)
        logger.info(f"Sent message to kafka topic: {KAFKA_TOPIC_ANALYTIC}")

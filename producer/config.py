import os
from dataclasses import dataclass


@dataclass(frozen=True)
class GeneratorConfig:
    cities: tuple[str, ...] = (
        "Bangalore",
        "Mumbai",
        "Delhi",
        "Hyderabad",
        "Chennai",
        "Pune",
        "Kolkata",
        "Kochi",
    )

    payment_methods: tuple[str, ...] = (
        "UPI",
        "CREDIT_CARD",
        "DEBIT_CARD",
        "NET_BANKING",
        "COD",
    )

    activity_types: tuple[str, ...] = (
        "PRODUCT_VIEW",
        "SEARCH",
        "ADD_TO_CART",
        "CHECKOUT",
    )

    warehouse_ids: tuple[str, ...] = (
        "WH-BLR-01",
        "WH-MUM-01",
        "WH-DEL-01",
        "WH-HYD-01",
    )

    product_count: int = 1_000
    customer_count: int = 100_000


@dataclass(frozen=True)
class KafkaConfig:
    bootstrap_servers: str = os.getenv(
        "KAFKA_BOOTSTRAP_SERVERS",
        "localhost:9092",
    )

    topic_orders: str = os.getenv(
        "KAFKA_TOPIC_ORDERS",
        "orders",
    )

    topic_payments: str = os.getenv(
        "KAFKA_TOPIC_PAYMENTS",
        "payments",
    )

    topic_inventory: str = os.getenv(
        "KAFKA_TOPIC_INVENTORY",
        "inventory",
    )

    topic_customer_activity: str = os.getenv(
        "KAFKA_TOPIC_CUSTOMER_ACTIVITY",
        "customer_activity",
    )

from producer.kafka_config import KafkaConfig


def test_default_kafka_configuration() -> None:
    config = KafkaConfig()

    assert config.bootstrap_servers
    assert config.client_id == "retail-event-producer"
    assert config.acks == "all"
    assert config.retries > 0
    assert config.enable_idempotence is True


def test_default_topics() -> None:
    config = KafkaConfig()

    assert config.topic_orders == "orders"
    assert config.topic_payments == "payments"
    assert config.topic_inventory == "inventory"
    assert config.topic_customer_activity == "customer_activity"

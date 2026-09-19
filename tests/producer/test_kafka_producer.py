import json

from producer.kafka_producer import RetailKafkaProducer


def test_event_serialization(generator) -> None:
    producer = RetailKafkaProducer()

    event = generator.generate_order()

    payload = producer._serialize(event)

    decoded = json.loads(payload.decode("utf-8"))

    assert decoded["event_id"] == event.event_id
    assert decoded["event_type"] == "ORDER_CREATED"
    assert decoded["order_id"] == event.order_id


def test_order_is_sent_to_orders_topic(generator) -> None:
    producer = RetailKafkaProducer()

    event = generator.generate_order()

    topic = producer._topic_for_event(
        event,
        producer.config,
    )

    assert topic == "orders"


def test_order_uses_order_id_as_partition_key(generator) -> None:
    producer = RetailKafkaProducer()

    event = generator.generate_order()

    key = producer._key_for_event(event)

    assert key == event.order_id

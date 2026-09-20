from unittest.mock import Mock

import pytest

from producer.kafka_producer import RetailKafkaProducer


def test_event_serialization(generator) -> None:
    kafka_client = Mock()

    producer = RetailKafkaProducer(kafka_client=kafka_client)

    event = generator.generate_order()

    payload = producer._serialize(event)

    assert isinstance(payload, bytes)

    decoded = payload.decode("utf-8")

    assert event.event_id in decoded
    assert event.order_id in decoded
    assert "ORDER_CREATED" in decoded


def test_order_uses_order_id_as_partition_key(generator) -> None:
    kafka_client = Mock()

    producer = RetailKafkaProducer(kafka_client=kafka_client)

    event = generator.generate_order()

    producer.publish(event)

    call_kwargs = kafka_client.produce.call_args.kwargs

    assert call_kwargs["key"] == event.order_id.encode("utf-8")


def test_order_is_sent_to_orders_topic(generator) -> None:
    kafka_client = Mock()

    producer = RetailKafkaProducer(kafka_client=kafka_client)

    event = generator.generate_order()

    producer.publish(event)

    kafka_client.produce.assert_called_once()
    kafka_client.poll.assert_called_once_with(0)

    call_kwargs = kafka_client.produce.call_args.kwargs

    assert call_kwargs["topic"] == "orders"
    assert call_kwargs["key"] == event.order_id.encode("utf-8")


def test_payment_is_sent_to_payments_topic(generator) -> None:
    kafka_client = Mock()
    producer = RetailKafkaProducer(kafka_client=kafka_client)

    order = generator.generate_order()
    event = generator.generate_payment(order)

    producer.publish(event)

    call_kwargs = kafka_client.produce.call_args.kwargs

    assert call_kwargs["topic"] == "payments"
    assert call_kwargs["key"] == order.order_id.encode("utf-8")


def test_inventory_is_sent_to_inventory_topic(generator) -> None:
    kafka_client = Mock()
    producer = RetailKafkaProducer(kafka_client=kafka_client)

    order = generator.generate_order()
    event = generator.generate_inventory(order)

    producer.publish(event)

    call_kwargs = kafka_client.produce.call_args.kwargs

    assert call_kwargs["topic"] == "inventory"
    assert call_kwargs["key"] == order.product_id.encode("utf-8")


def test_customer_activity_is_sent_to_customer_topic(generator) -> None:
    kafka_client = Mock()
    producer = RetailKafkaProducer(kafka_client=kafka_client)

    event = generator.generate_customer_activity()

    producer.publish(event)

    call_kwargs = kafka_client.produce.call_args.kwargs

    assert call_kwargs["topic"] == "customer_activity"
    assert call_kwargs["key"] == event.customer_id.encode("utf-8")


def test_unsupported_event_type_raises_error() -> None:
    kafka_client = Mock()
    producer = RetailKafkaProducer(kafka_client=kafka_client)

    unsupported_event = object()

    with pytest.raises(ValueError, match="Unsupported event type"):
        producer._topic_for_event(
            unsupported_event,
            producer.config,
        )

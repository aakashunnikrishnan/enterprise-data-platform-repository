import json


def test_order_can_be_serialized_to_json(generator) -> None:
    event = generator.generate_order()

    payload = event.model_dump(mode="json")

    serialized = json.dumps(payload)
    deserialized = json.loads(serialized)

    assert deserialized["event_id"] == event.event_id
    assert deserialized["event_type"] == "ORDER_CREATED"
    assert deserialized["order_id"] == event.order_id


def test_order_payment_and_inventory_share_business_context(generator) -> None:
    order = generator.generate_order()

    payment = generator.generate_payment(order)
    inventory = generator.generate_inventory(order)

    assert payment.order_id == order.order_id
    assert payment.customer_id == order.customer_id

    assert inventory.product_id == order.product_id


def test_generator_respects_customer_configuration(generator) -> None:
    events = [generator.generate_order() for _ in range(100)]

    for event in events:
        customer_number = int(event.customer_id.split("-")[1])

        assert 1 <= customer_number <= generator.config.customer_count


def test_generator_respects_product_configuration(generator) -> None:
    events = [generator.generate_order() for _ in range(100)]

    for event in events:
        product_number = int(event.product_id.split("-")[1])

        assert 1 <= product_number <= generator.config.product_count

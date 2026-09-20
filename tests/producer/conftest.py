import pytest

from producer.config import GeneratorConfig
from producer.generators import RetailEventGenerator


@pytest.fixture
def generator_config() -> GeneratorConfig:
    return GeneratorConfig(
        cities=("Bangalore", "Mumbai"),
        payment_methods=("UPI", "CREDIT_CARD"),
        activity_types=("PRODUCT_VIEW", "ADD_TO_CART"),
        warehouse_ids=("WH-BLR-01",),
        product_count=100,
        customer_count=1_000,
    )


@pytest.fixture
def generator(
    generator_config: GeneratorConfig,
) -> RetailEventGenerator:
    return RetailEventGenerator(generator_config)

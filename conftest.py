import sys
from pathlib import Path

import pytest

from producer.kafka_producer import RetailKafkaProducer

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@pytest.fixture
def generator():
    """Provide a RetailKafkaProducer instance for tests."""
    return RetailKafkaProducer()

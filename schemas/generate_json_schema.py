import json
from pathlib import Path

from schemas.event_schema import (
    CustomerActivityEventSchema,
    InventoryEventSchema,
    OrderEventSchema,
    PaymentEventSchema,
)

OUTPUT_DIR = Path(__file__).parent / "json_schema"


def generate_schema() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    schemas = {
        "order_created": OrderEventSchema.model_json_schema(),
        "payment_completed": PaymentEventSchema.model_json_schema(),
        "inventory_updated": InventoryEventSchema.model_json_schema(),
        "customer_activity": CustomerActivityEventSchema.model_json_schema(),
    }

    for name, schema in schemas.items():
        output_file = OUTPUT_DIR / f"{name}.schema.json"

        output_file.write_text(
            json.dumps(schema, indent=2),
            encoding="utf-8",
        )

        print(f"Generated {output_file}")


if __name__ == "__main__":
    generate_schema()

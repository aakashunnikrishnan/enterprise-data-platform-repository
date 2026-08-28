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

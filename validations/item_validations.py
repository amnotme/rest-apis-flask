from db import items


def valid_create_item(item_data):
    if (
        "price" not in item_data
        or "store_id" not in item_data
        or "name" not in item_data
    ):
        return False
    return True


def valid_item_for_store(item_data):
    return all(
        item_data["store_id"] != item["store_id"] and item_data["name"] != item["name"]
        for item in items.values()
    )


def valid_update_item(item_data):
    if "price" not in item_data or "name" not in item_data:
        return False
    return True

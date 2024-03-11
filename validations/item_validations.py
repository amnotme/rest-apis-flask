def valid_create_item(item_data):
    if (
        "price" not in item_data
        or "store_id" not in item_data
        or "name" not in item_data
    ):
        return False
    return True


def valid_update_item(item_data):
    if "price" not in item_data or "name" not in item_data:
        return False
    return True

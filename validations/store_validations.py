from db import stores


def valid_create_store(store_data):
    if "name" not in store_data:
        return False
    return True


def valid_store(store_data):
    return all(store_data["name"] != store["name"] for store in stores.values())

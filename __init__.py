import json

import products
from cart import dao
from products import Product


class Cart:
    def _init_(self, id: int, username: str, contents: list[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    @staticmethod
    def load(data):
        return Cart(data['id'], data['username'], data['contents'], data['cost'])


def get_cart(username: str) -> list:
    cart_details = dao.get_cart(username)
    if cart_details is None:
        return []
    
    # Directly parse the contents without eval, assuming 'contents' is a JSON-encoded list
    items = []
    for cart_detail in cart_details:
        # Assuming contents is a JSON-encoded string, use json.loads to parse it
        contents = json.loads(cart_detail['contents'])
        items.extend(contents)  # Flatten the list of contents

    # Fetch all products in one batch instead of looping and calling get_product each time
    products_batch = products.get_products(items)  # Assuming this function exists for batch retrieval
    return products_batch


def add_to_cart(username: str, product_id: int):
    dao.add_to_cart(username, product_id)


def remove_from_cart(username: str, product_id: int):
    dao.remove_from_cart(username, product_id)

def delete_cart(username: str):
    dao.delete_cart(username)
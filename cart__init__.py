import json
from cart import dao
from products import get_product, Product

class Cart:
    def __init__(self, id: int, username: str, contents: list[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    @staticmethod
    def load(data):
        return Cart(
            id=data['id'],
            username=data['username'],
            contents=json.loads(data['contents']),  # Use JSON parsing instead of eval
            cost=data['cost']
        )

def get_cart(username: str) -> list[Product]:
    cart_details = dao.get_cart(username)
    if not cart_details:
        return []

    items = []
    for cart_detail in cart_details:
        # Parse JSON safely instead of eval
        try:
            contents = json.loads(cart_detail['contents'])
        except json.JSONDecodeError:
            continue
        
        # Retrieve product details for each item
        items.extend([get_product(product_id) for product_id in contents])

    return items

def add_to_cart(username: str, product_id: int):
    dao.add_to_cart(username, product_id)

def remove_from_cart(username: str, product_id: int):
    dao.remove_from_cart(username, product_id)

def delete_cart(username: str):
    dao.delete_cart(username)

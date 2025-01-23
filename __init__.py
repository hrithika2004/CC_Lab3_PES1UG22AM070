from products import dao


class Product:
    def __init__(self, id: int, name: str, description: str, cost: float, qty: int = 0):
        self.id = id
        self.name = name
        self.description = description
        self.cost = cost
        self.qty = qty

    def load(data):
        return Product(data['id'], data['name'], data['description'], data['cost'], data['qty'])


#for browse optimization
def list_products() -> list[dict]:
    """
    Fetch and return all products as a list of dictionaries for direct rendering.
    This avoids unnecessary object creation for the purpose of browsing.
    """
    # Fetch products from the DAO in a single, efficient query
    products = dao.list_products()

    # Return the raw product data directly (no need for Product.load here)
    return products





def get_product(product_id: int) -> Product:
    return Product.load(dao.get_product(product_id))


def add_product(product: dict):
    dao.add_product(product)


def update_qty(product_id: int, qty: int):
    if qty < 0:
        raise ValueError('Quantity cannot be negative')
    dao.update_qty(product_id, qty)



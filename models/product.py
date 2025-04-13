class Product:
    def __init__(self, id, product_id, wishlist_id):
        self.id = id
        self.product_id = product_id
        self.wishlist_id = wishlist_id

    def to_dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "wishlist_id": self.wishlist_id
        }

from models.product import Product
import logging

class ProductService:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        query = "SELECT * FROM products"
        with self.db.get_connection() as conn:
            cursor = conn.execute(query)
            products = [Product(row[0], row[1], row[2]).to_dict() for row in cursor.fetchall()]
        return products

    def get_by_wishlist_id(self, wishlist_id):
        query = "SELECT * FROM products WHERE wishlist_id = ?"
        with self.db.get_connection() as conn:
            cursor = conn.execute(query, (wishlist_id,))
            products = [Product(row[0], row[1], row[2]).to_dict() for row in cursor.fetchall()]
        return products
    
    def get_by_product_id(self, wishlist_id, product_id):
        query = "SELECT * FROM products WHERE wishlist_id = ? AND product_id = ?"
        with self.db.get_connection() as conn:
            cursor = conn.execute(query, (wishlist_id, product_id,))
            row = cursor.fetchone()
            if row:
                return Product(row[0], row[1], row[2]).to_dict()
        return None

    def create(self, wishlist_id, product_id):
        query = "INSERT INTO products (product_id, wishlist_id) VALUES (?, ?)"
        with self.db.get_connection() as conn:
            cursor = conn.execute(query, (product_id, wishlist_id))
            conn.commit()
            return Product(cursor.lastrowid, product_id, wishlist_id).to_dict()

    def delete(self, wishlist_id, product_id):
        query = "DELETE FROM products WHERE product_id = ? AND wishlist_id = ?"
        with self.db.get_connection() as conn:
            cursor = conn.execute(query, (product_id, wishlist_id,))
            conn.commit()
            if cursor.rowcount > 0:
                return Product(product_id, None, None).to_dict()
        return None
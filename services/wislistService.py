from models.wishlist import Wishlist

class WishlistService:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        query = "SELECT * FROM wishlists"
        with self.db.get_connection() as conn:
            cursor = conn.execute(query)
            wishlist = [Wishlist(row[0], row[1]).to_dict() for row in cursor.fetchall()]
        return wishlist

    def get_by_title(self, title):
        query = "SELECT * FROM wishlists WHERE title = ?"
        with self.db.get_connection() as conn:
            cursor = conn.execute(query, (title,))
            row = cursor.fetchone()
            if row:
                return Wishlist(row[0], row[1]).to_dict()
        return None
    
    def create(self, title):
        query = "INSERT INTO wishlists (title) VALUES (?)"
        with self.db.get_connection() as conn:
            cursor = conn.execute(query, (title,))
            conn.commit()
            return Wishlist(cursor.lastrowid, title).to_dict()

    def update(self, bookId, title):
        query = "UPDATE wishlists SET title = ? WHERE id = ?"
        with self.db.get_connection() as conn:
            cursor = conn.execute(query, (title, bookId))
            conn.commit()
            if cursor.rowcount > 0:
                return Wishlist(bookId, title).to_dict()
        return None

    def delete(self, bookId):
        query = "DELETE FROM wishlists WHERE id = ?"
        with self.db.get_connection() as conn:
            cursor = conn.execute(query, (bookId,))
            conn.commit()
            if cursor.rowcount > 0:
                return Wishlist(bookId, None).to_dict()
        return None
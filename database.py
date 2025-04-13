import sqlite3

class SqliteDatabase:
    db_name = "database.db"

    def __init__(self, ):
        self._create_tables()

    def _create_tables(self):
        createWishlistTable = """
        CREATE TABLE IF NOT EXISTS wishlists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL
        );
        """

        createProductTable = """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            wishlist_id INTEGER NOT NULL,
            FOREIGN KEY (wishlist_id) REFERENCES wishlists(id)
        );
        """

        with self.get_connection() as conn:
            conn.execute(createWishlistTable)
            conn.execute(createProductTable)


    def get_connection(self):
        return sqlite3.connect(self.db_name)

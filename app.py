from pydantic import BaseModel

from flask_openapi3 import Info, Tag
from flask_openapi3 import OpenAPI

from flask import jsonify
from flask_cors import CORS

from services.wislistService import WishlistService
from services.productService import ProductService
import logging

from database import SqliteDatabase

# Create the database
dataBase = SqliteDatabase()

# Create the services
wishlistService = WishlistService(dataBase)
productService = ProductService(dataBase)

# Create the API
info = Info(title="wishlist API", version="1.0.0")
app = OpenAPI(__name__, info=info)

# Enable CORS
CORS(app)

# Create the tags for documentation
wishlist_tag = Tag(name="wishlist", description="Wishlist Routes")

# Create the wishlist DTOs
class WishlistBody(BaseModel):
    title: str 

class WishlistPath(BaseModel):
    id: int

# Create the wishlist routes
@app.get("/wishlists", tags=[wishlist_tag])
def get_wishlists():
    """Retorna todos as wishlists cadastrados
    Retorna todos os wishlists cadastrados
    """
    wishlists = wishlistService.get_all()
    return jsonify(wishlists), 200

@app.post('/wishlists', tags=[wishlist_tag])
def create_wishlist(body: WishlistBody):
    """Cadastra uma wishlist
    Cadastra uma wishlist
    """
    if not body.title:
        return jsonify({"message": "Titulo é obrigatório"}), 400
    
    exist = wishlistService.get_by_title(body.title)
    
    if exist and exist.get("title"):
        return jsonify({"message": "Wishlist já cadastrado"}), 400
    
    wishlist = wishlistService.create(body.title)
    return jsonify(wishlist), 201

@app.put("/wishlists/<id>", tags=[wishlist_tag])
def update_wishlist(path: WishlistPath, body: WishlistBody):
    """Atualiza uma wishlist
    Atualiza uma wishlist
    """
    if not body.title:
        return jsonify({"message": "Titulo é obrigatório"}), 400    
    
    wishlist = wishlistService.update(path.id, body.title)

    if wishlist:
        return jsonify(wishlist), 200
    
    return jsonify({"message": "Wishlist não encontrado"}), 404

@app.delete("/wishlists/<id>", tags=[wishlist_tag])
def delete_wishlist(path: WishlistPath):
    """Remove uma wishlist
    Remove uma wishlist
    """
    if not path.id:
        return jsonify({"message": "Id é obrigatório"}), 400
    
    book = wishlistService.delete(path.id)
    if book:
        return jsonify(book), 200

    return jsonify({"message": "Livro não encontrado"}), 404


product_tag = Tag(name="product", description="Product Routes")

# Create the products DTOs
class ProductBody(BaseModel):
    product_id: int 

class ProductPath(BaseModel):
    wishlist_id: int
    product_id: int

# Create the products routes
@app.get("/wishlists/<id>/products", tags=[product_tag])
def get_product(path: WishlistPath):
    """Lista os produtos de uma wishlist
    Lista os produtos de uma wishlist
    """
    products = productService.get_by_wishlist_id(path.id)
    return jsonify(products), 200

@app.post('/wishlists/<id>/products', tags=[product_tag])
def create_product(path: WishlistPath, body: ProductBody):
    """Cadastra um produto
    Cadastra um produto
    """
    if not body.product_id:
        return jsonify({"message": "Id do produto é obrigatório"}), 400
    """ add uma validação se o product_id ja existe na wishlist """

    products_in_wishlist = productService.get_by_product_id(path.id, body.product_id)

    if products_in_wishlist and products_in_wishlist.get("product_id"):
        return jsonify({"message": "Produto já cadastrado na wishlist"}), 400
            
    product = productService.create(path.id, body.product_id)
    return jsonify(product), 201


@app.delete("/wishlists/<wishlist_id>/products/<product_id>", tags=[product_tag])
def delete_product(path: ProductPath):
    """Remove um produto
    Remove um produto
    """
    if not path.wishlist_id:
        return jsonify({"message": "Id da wishlist é obrigatório"}), 400
    
    if not path.product_id:
        return jsonify({"message": "Id do produto é obrigatório"}), 400
    
    product = productService.delete(path.wishlist_id, path.product_id)
    if product:
        return jsonify(product), 200

    return jsonify({"message": "Produto não encontrado"}), 404


if __name__ == "__main__":
    app.run(debug=True)
from flask import (
    Blueprint, jsonify, request, abort
)
from flask_jwt_extended import jwt_required
from sqlalchemy import select
from flaskr.database import db
from flaskr.models import CartItem, CartItemResponse, Book
from flaskr.validation import verify_user_id

bp = Blueprint('cart', __name__, url_prefix='/cart')

@bp.route('/<int:userId>')
@jwt_required()
def get_cart(userId):
    verify_user_id(userId)
    cart = db.session.execute(select(CartItem, Book).join(Book, CartItem.productId == Book.id).where(CartItem.userId == userId))
    res = [CartItemResponse(row.Book, row.CartItem.quantity) for row in cart]
    return jsonify(res)

@bp.route('/<int:userId>/add', methods=('POST',))
@jwt_required()
def add_product(userId):
    verify_user_id(userId)
    data = request.get_json()
    productId = int(data['productId']) if 'productId' in data else None
    quantity = data['quantity'] if 'quantity' in data else None
    if not productId:
        return {'message': 'Product ID required'}, 400
    if not quantity:
        return {'message': 'Quantity required'}, 400
    product = db.get_or_404(Book, productId)
    cartItem = CartItem(userId=userId, productId=productId, quantity=quantity)
    try:
        db.session.add(cartItem)
        db.session.commit()
    except Exception:
        return {'message': 'DB insertion error'}, 500
    res = CartItemResponse(product, quantity)
    return jsonify(res)

@bp.route('/<int:userId>/addMany', methods=('POST',))
@jwt_required()
def add_products(userId):
    verify_user_id(userId)
    data = request.get_json()
    cartData = data['cartItems'] if 'cartItems' in data else []
    if len(cartData) == 0:
        return {'message': 'items required'}, 400
    for item in cartData:
        db.get_or_404(Book, int(item['productId']))
    cartItems = [CartItem(userId=userId, productId=int(item['productId']), quantity=item['quantity']) for item in cartData]
    try:
        db.session.add_all(cartItems)
        db.session.commit()
    except Exception:
        return {'message': 'DB insertion error'}, 500
    return get_cart(userId)
    
@bp.route('/<int:userId>/delete/<int:productId>', methods=('DELETE',))
@jwt_required()
def remove_product(userId, productId):
    verify_user_id(userId)
    cartItem = db.session.scalar(select(CartItem).where(CartItem.userId == userId).where(CartItem.productId == productId))
    product = db.get_or_404(Book, cartItem.productId)
    res = CartItemResponse(product, cartItem.quantity)
    try:
        db.session.delete(cartItem)
        db.session.commit()
    except Exception as e:
        print(e)
        return {'message': 'DB deletion error'}, 500
    return jsonify(res)

@bp.route('/<int:userId>/order', methods=('POST',))
@jwt_required()
def place_order(userId):
    verify_user_id(userId)
    cartItems = db.session.scalars(select(CartItem).where(CartItem.userId == userId)).all()
    try:
        for item in cartItems:
            db.session.delete(item)
        db.session.commit()
    except Exception as e:
        print(e)
        return {'message': 'DB deletion error'}, 500
    return {'message': 'order sent successfully'}

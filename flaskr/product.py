from flask import (
    Blueprint, jsonify, request, abort
)
from sqlalchemy import select
from flaskr.database import db
from flaskr.models import Book, BookResponse

bp = Blueprint('product', __name__, url_prefix='/product')

@bp.route('/')
def index():
    books = db.session.scalars(select(Book).order_by(Book.id)).all()
    res = [BookResponse(b) for b in books]
    return jsonify(res)

@bp.route('/<int:id>', methods=('GET', 'POST'))
def get_product(id):
    book = db.get_or_404(Book, id)
    res = BookResponse(book)
    return jsonify(res)

@bp.route('/create', methods=('POST',))
def create_product():
    if request.is_json:
        data = request.get_json()
        name = data['name'] if 'name' in data else None
        author = data['author'] if 'author' in data else None
        publisher = data['publisher'] if 'publisher' in data else None
        price = data['price'] if 'price' in data else None
        discount = data['discount'] if 'discount' in data else None
        imageUrl = data['imageUrl'] if 'imageUrl' in data else None
    else:
        name = request.form['name']
        author = request.form['author']
        publisher = request.form['publisher']
        price = request.form['price']
        discount = request.form['discount']
        imageUrl = request.form['imageUrl']
    if not name:
        return {'message': 'Name required'}, 400
    if not author:
        return {'message': 'Author required'}, 400
    if price is None:
        return {'message': 'Price required'}, 400
    book = Book(name=name, author=author, publisher=publisher, price=price, discount=discount, imageUrl=imageUrl)
    try:
        db.session.add(book)
        db.session.commit()
    except Exception:
        return {'message': 'DB insertion error'}, 500
    res = BookResponse(book)
    return jsonify(res)

@bp.route('/<int:id>/update', methods=('PUT', 'PATCH'))
def update_product(id):
    if request.is_json:
        data = request.get_json()
        name = data['name'] if 'name' in data else None
        author = data['author'] if 'author' in data else None
        publisher = data['publisher'] if 'publisher' in data else None
        price = data['price'] if 'price' in data else None
        discount = data['discount'] if 'discount' in data else None
        imageUrl = data['imageUrl'] if 'imageUrl' in data else None
    else:
        name = request.form['name']
        author = request.form['author']
        publisher = request.form['publisher']
        price = request.form['price']
        discount = request.form['discount']
        imageUrl = request.form['imageUrl']
    book = db.get_or_404(Book, id)
    try:
        if name is not None:
            book.name = name
        if author is not None:
            book.author = author
        if publisher is not None:
            book.publisher = publisher
        if price is not None:
            book.price = price
        if discount is not None:
            book.discount = discount
        if imageUrl is not None:
            book.imageUrl = imageUrl
        db.session.commit()
    except Exception:
        return {'message': 'DB update error'}, 500
    res = BookResponse(book)
    return jsonify(res)

@bp.route('/<int:id>/delete', methods=('DELETE',))
def remove_product(id):
    book = db.get_or_404(Book, id)
    res = BookResponse(book)
    try:
        db.session.delete(book)
        db.session.commit()
    except Exception as e:
        print(e)
        return {'message': 'DB deletion error'}, 500
    return jsonify(res)
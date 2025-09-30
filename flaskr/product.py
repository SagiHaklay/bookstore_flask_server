from flask import (
    Blueprint, jsonify, request, abort, current_app
)
import os
from werkzeug.utils import secure_filename
from sqlalchemy import select
from flask_jwt_extended import get_jwt, verify_jwt_in_request
from flaskr.database import db
from flaskr.models import Book, BookResponse
from flaskr.validation import admin_required

bp = Blueprint('product', __name__, url_prefix='/product')

UPLOAD_FOLDER = 'C://talpiot/bookstore_flask_server/flaskr/static'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 5 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def handle_file(id):
    if 'image' not in request.files:
        return {
            'message': 'No file provided',
            'filename': None
        }
    
    file = request.files['image']
    
    if file.filename == '':
        return {
            'message': 'No file selected',
            'filename': None
        }
    
    if not allowed_file(file.filename):
        return {'error': 'File type not allowed'}
    
    
    
    # filename = secure_filename(file.filename)
    filename = f'book{id}.{file.filename.rsplit('.', 1)[1]}'
    # file_path = os.path.join(UPLOAD_FOLDER, filename)
    file_path = f'{current_app.config['UPLOAD_FOLDER']}/{filename}'
    # dir_fd = os.open(UPLOAD_FOLDER, os.O_RDONLY)
    # def opener(path, flags):
    #     return os.open(path, flags, dir_fd=dir_fd)
    # with open(filename, 'wb', opener=opener) as f:
    #     file.save(f)
    # os.close(dir_fd)
    file.save(file_path)
    
    return {
        'message': 'File uploaded successfully',
        'filename': filename,
        'path': file_path
    }


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
@admin_required()
def create_product():
    if request.is_json:
        data = request.get_json()
        name = data['name'] if 'name' in data else None
        author = data['author'] if 'author' in data else None
        publisher = data['publisher'] if 'publisher' in data else None
        price = data['price'] if 'price' in data else None
        discount = data['discount'] if 'discount' in data else None
        # imageUrl = data['imageUrl'] if 'imageUrl' in data else None
    else:
        name = request.form.get('name', None)
        author = request.form.get('author', None)
        publisher = request.form.get('publisher', None)
        price = request.form.get('price', None)
        discount = request.form.get('discount', None)
        # imageUrl = request.form['imageUrl']
    if not name:
        return {'message': 'Name required'}, 400
    if not author:
        return {'message': 'Author required'}, 400
    if price is None:
        return {'message': 'Price required'}, 400
    
    
    book = Book(name=name, author=author, publisher=publisher, price=price, discount=discount)
    try:
        db.session.add(book)
        db.session.commit()
        file_result = handle_file(book.id)
        if 'error' in file_result:
            return jsonify(file_result), 400
        image_url = file_result['filename']
        book.imageUrl = image_url
        db.session.commit()
    except Exception as e:
        print(e)
        return {'message': 'DB insertion error'}, 500
    res = BookResponse(book)
    return jsonify(res)

@bp.route('/<int:id>/update', methods=('PUT', 'PATCH'))
@admin_required()
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
        publisher = request.form.get('publisher', None)
        price = request.form['price']
        discount = request.form.get('discount', None)
        imageUrl = request.form.get('imageUrl', None)
    file_result = handle_file(id)
    print(file_result)
    if 'error' in file_result:
        return jsonify(file_result), 400
    imageUrl = file_result['filename']
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
    except Exception as e:
        print(e)
        return {'message': 'DB update error'}, 500
    res = BookResponse(book)
    return jsonify(res)

@bp.route('/<int:id>/delete', methods=('DELETE',))
@admin_required()
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
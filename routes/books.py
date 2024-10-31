from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import Book, User

books = Blueprint('books', __name__)

@books.errorhandler(Exception)
def handle_error(error):
    return jsonify({'message': str(error)}), 500

@books.route('/', methods=['GET'])
@jwt_required()
def get_books():
    books = Book.query.all()
    return jsonify({
        'books': [{
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'isbn': book.isbn,
            'published_year': book.published_year
        } for book in books]
    }), 200

@books.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_book(id):
    book = Book.query.get_or_404(id)
    return jsonify({
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'isbn': book.isbn,
        'published_year': book.published_year
    }), 200

@books.route('/', methods=['POST'])
@jwt_required()
def create_book():
    data = request.get_json()
    
    if Book.query.filter_by(isbn=data['isbn']).first():
        return jsonify({'message': 'Book with this ISBN already exists'}), 400
        
    new_book = Book(
        title=data['title'],
        author=data['author'],
        isbn=data['isbn'],
        published_year=data['published_year']
    )
    
    db.session.add(new_book)
    db.session.commit()
    
    return jsonify({'message': 'Book created successfully', 'book_id': new_book.id}), 201

@books.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_book(id):
    book = Book.query.get_or_404(id)
    data = request.get_json()
    
    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    book.isbn = data.get('isbn', book.isbn)
    book.published_year = data.get('published_year', book.published_year)
    
    db.session.commit()
    
    return jsonify({'message': 'Book updated successfully'}), 200

@books.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    
    return jsonify({'message': 'Book deleted successfully'}), 200 
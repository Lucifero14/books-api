import pytest
from app import app, db
from models import Book

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_create_book(client):
    res = client.post('/books', json={
        "title": "Test Book",
        "author": "Tester",
        "year_published": 2023,
        "genre": "Test"
    })
    assert res.status_code == 201
    assert res.get_json()['title'] == "Test Book"

def test_get_books(client):
    # Add a book first
    client.post('/books', json={
        "title": "Book 1",
        "author": "Author 1",
        "year_published": 2000,
        "genre": "Fiction"
    })
    res = client.get('/books')
    assert res.status_code == 200
    assert isinstance(res.get_json(), list)
    assert len(res.get_json()) >= 1

def test_update_book(client):
    post_res = client.post('/books', json={
        "title": "Old Title",
        "author": "Old Author"
    })
    book_id = post_res.get_json()['id']
    res = client.put(f'/books/{book_id}', json={"title": "New Title"})
    assert res.status_code == 200
    assert res.get_json()['title'] == "New Title"

def test_delete_book(client):
    post_res = client.post('/books', json={
        "title": "Delete Me",
        "author": "Someone"
    })
    book_id = post_res.get_json()['id']
    del_res = client.delete(f'/books/{book_id}')
    assert del_res.status_code == 200
    assert del_res.get_json()['message'] == 'Book deleted'

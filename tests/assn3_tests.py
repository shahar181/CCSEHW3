import requests

base_url = "http://localhost:5001"

book1 = {"title": "Adventures of Huckleberry Finn", "ISBN": "9780520343641", "genre": "Fiction"}
book2 = {"title": "The Best of Isaac Asimov", "ISBN": "9780385050784", "genre": "Science Fiction"}
book3 = {"title": "Fear No Evil", "ISBN": "9780394558783", "genre": "Biography"}
book4 = {"title": "No such book", "ISBN": "0000001111111", "genre": "Biography"}
book5 = {"title": "The Greatest Joke Book Ever", "authors": "Mel Greene", "ISBN": "9780380798490", "genre": "Jokes"}

# Global variables for book IDs
id1 = None
id2 = None
id3 = None
id4 = None
id5 = None


def test_add_books():
    global id1, id2, id3
    response1 = requests.post(f"{base_url}/books", json=book1)
    response2 = requests.post(f"{base_url}/books", json=book2)
    response3 = requests.post(f"{base_url}/books", json=book3)

    assert response1.status_code == 201
    assert response2.status_code == 201
    assert response3.status_code == 201

    id1 = response1.json()['ID']
    id2 = response2.json()['ID']
    id3 = response3.json()['ID']

    assert id1 != id2 != id3


def test_get_book1():
    global id1
    if id1 is None:
        test_add_books()
    response = requests.get(f"{base_url}/books/{id1}")

    assert response.status_code == 200
    data = response.json()
    assert data['authors'] == "Mark Twain"


def test_get_all_books():
    global id1, id2, id3
    if id1 is None or id2 is None or id3 is None:
        test_add_books()

    response = requests.get(f"{base_url}/books")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3


def test_invalid_book4():
    global id4
    response = requests.post(f"{base_url}/books", json=book4)
    id4 = response.json().get('ID', None)
    assert response.status_code == 400 or response.status_code == 500


def test_delete_book2():
    global id2
    if id2 is None:
        test_add_books()

    response = requests.delete(f"{base_url}/books/{id2}")
    assert response.status_code == 200


def test_get_deleted_book2():
    global id2
    response = requests.get(f"{base_url}/books/{id2}")
    assert response.status_code == 404


def test_invalid_genre_book5():
    global id5
    response = requests.post(f"{base_url}/books", json=book5)
    id5 = response.json().get('ID', None)
    assert response.status_code == 422

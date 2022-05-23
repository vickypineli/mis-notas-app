from src.lib.utils import temp_file
from src.webserver import create_app
from src.domain.note import NotesRepository, Note


def test_should_save_note():
    notes_repository = NotesRepository(temp_file())
    app = create_app(repositories={"note": notes_repository})
    client = app.test_client()

    note = {
        "id": "note1",
        "title": "example1",
        "text": "Hola nena",
        "user_id": "Joseba_1",
        "id_cat": "cat-1"
    }

    response = client.post("/api/notes", json=note)

    assert response.status_code == 200

    response_get = client.get("/api/notes/note1",
                              headers={"Authorization": "Joseba_1"})
    assert response_get.json == {
        "id": "note1",
        "title": "example1",
        "text": "Hola nena",
        "user_id": "Joseba_1",
        "id_cat": "cat-1"
    }


def test_shouldnt_save_new_note_with_same_id():
    notes_repository = NotesRepository(temp_file())
    app = create_app(repositories={"note": notes_repository})
    client = app.test_client()

    note1 = {
        "id": "note1",
        "title": "example1",
        "text": "Hola nena",
        "user_id": "Joseba_1",
        "id_cat": "cat-1"
    }

    note2 = {
        "id": "note1",
        "title": "example2",
        "text": "Hola beba",
        "user_id": "Joseba_1",
        "id_cat": "cat-1"
    }

    response = client.post("/api/notes", json=note1)
    response2 = client.post("/api/notes", json=note2)

    assert response2.status_code != 200

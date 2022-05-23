from src.lib.utils import temp_file
from src.webserver import create_app
from src.domain.note import NotesRepository, Note


def test_should_return_empty_list_of_notes():
    notes_repository = NotesRepository(temp_file())
    app = create_app(repositories={"note": notes_repository})
    client = app.test_client()

    response = client.get("/api/notes")

    assert response.json == []


def test_should_return_list_of_notes():
    notes_repository = NotesRepository(temp_file())
    app = create_app(repositories={"note": notes_repository})
    client = app.test_client()

    note = Note(id="pepa", title="example1",
                text="text example", user_id="Joseba_1", id_cat="cat-1")
    notes_repository.insert_data_note(note)
    response = client.get("/api/notes", headers={"Authorization": "Joseba_1"})

    assert response.json == [
        {
            "id": "pepa",
            "title": "example1",
            "text": "text example",
            "user_id": "Joseba_1",
            "id_cat": "cat-1"
        }

    ]

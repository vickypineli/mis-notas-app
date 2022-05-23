from src.lib.utils import temp_file
from src.webserver import create_app
from src.domain.note import NotesRepository, Note


def test_shuld_return_existing_note_by_id():
    notes_repository = NotesRepository(temp_file())
    app = create_app(repositories={"note": notes_repository})
    client = app.test_client()
    note = Note(id="pepa", title="example1",
                text="text example", user_id="Joseba_1", id_cat="cat-1")
    notes_repository.insert_data_note(note)

    response = client.get("/api/notes/pepa",
                          headers={"Authorization": "Joseba_1"})

    assert response.status_code == 200
    assert response.json == {
        "id": "pepa",
        "title": "example1",
        "text": "text example",
        "user_id": "Joseba_1",
        "id_cat": "cat-1"
    }


def test_shuld_return_unauthorized_note_by_id():
    notes_repository = NotesRepository(temp_file())
    app = create_app(repositories={"note": notes_repository})
    client = app.test_client()

    note = Note(id="pepa", title="example1",
                text="text example", user_id="Joseba_1", id_cat="cat-1")

    notes_repository.insert_data_note(note)

    response = client.get("/api/notes/pepa",
                          headers={"Authorization": "Josu_1"})

    assert response.status_code == 403

from src.lib.utils import temp_file
from src.webserver import create_app
from src.domain.note import NotesRepository, Note


def test_method_should_modify_data():
    notes_repository = NotesRepository(temp_file())
    app = create_app(repositories={"note": notes_repository})
    client = app.test_client()

    original_note = Note(id="note-1", title="example1",
                         text="text example", user_id="Joseba_1", id_cat="null")

    notes_repository.insert_data_note(original_note)

    modified_note = Note(
        id="note-1", title="example1 modified", text="text example modified", user_id="Joseba_1", id_cat="cat-1")
    notes_repository.modify_data_note_by_id(modified_note)

    response_get_database = client.get("/api/notes/note-1",
                                       headers={"Authorization": "Joseba_1"})
    assert response_get_database.json == {
        "id": "note-1",
        "title": "example1 modified",
        "text": "text example modified",
        "user_id": "Joseba_1",
        "id_cat": "cat-1"
    }

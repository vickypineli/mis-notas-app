from src.lib.utils import temp_file
from src.webserver import create_app
from src.domain.note import NotesRepository, Note


def test_should_return_notes_deleted():
    notes_repository = NotesRepository(temp_file())
    app = create_app(repositories={"note": notes_repository})
    client = app.test_client()
    note = Note(id="note-1", title="example1",
                text="text example", user_id="Joseba_1", id_cat ="cat-1")
    notes_repository.insert_data_note(note)
    reponse_note_deleted = client.delete("/api/notes/note-1",
                                         headers={"Authorization": "Joseba_1"})
    response = client.get("/api/notes")

    assert response.json == []

from src.domain.note import NotesRepository, Note
from src.lib.utils import temp_file
from src.webserver import create_app
from src.domain.tags import TagsRepository, Tag

import json


def test_should_return_note_with_their_tags():
    notes_repository = NotesRepository(temp_file())
    tags_repository = TagsRepository(temp_file())

    app = create_app(
        repositories={'notes': notes_repository, "tags": tags_repository, })
    client = app.test_client()

    note_1 = Note(id="1", title="title", text="content",
                  user_id="1", id_cat="1")

    notes_repository.insert_data_note(note_1)

    tag_1 = Tag(note_id="1",
                tag=["#a", "#claudio"])

    tags_repository.save(tag_1)

    response = client.get(
        "/api/tags/1")

    assert response.status_code == 200
    assert response.json == [
        {"note_id": "1", "tag": "#a"},
        {"note_id": "1", "tag": "#claudio"}
    ]

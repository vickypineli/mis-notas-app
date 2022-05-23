from src.lib.utils import temp_file
from src.webserver import create_app
from src.domain.tags import TagsRepository, Tag
import json


def test_should_return_empty_list_of_tags():
    tags_repository = TagsRepository(temp_file())
    app = create_app(repositories={"tags": tags_repository})
    client = app.test_client()

    response = client.get("/api/tags")

    assert response.json == []


def test_should_return_list_of_tags():
    tags_repository = TagsRepository(temp_file())
    app = create_app(repositories={"tags": tags_repository})
    client = app.test_client()

    tag_1 = Tag(note_id="8c3a9762-bd8a-4459-a350-5a2f77d04efd",
                tag=["#a", "#claudio"])

    tags_repository.save(tag_1)
    response = client.get("/api/tags")

    assert response.json == [
        {"note_id": "8c3a9762-bd8a-4459-a350-5a2f77d04efd", "tag": "#a"},
        {"note_id": "8c3a9762-bd8a-4459-a350-5a2f77d04efd", "tag": "#claudio"}
    ]

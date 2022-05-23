from src.lib.utils import temp_file
from src.webserver import create_app
from src.domain.note import NotesRepository, Note


def test_should_return_all_categories():
    notes_repository = NotesRepository(temp_file())
    app = create_app(repositories={"note": notes_repository})
    client = app.test_client()

    notes_repository.save_a_new_category("cat-1", "Sports")
    notes_repository.save_a_new_category("cat-2", "Music")
    notes_repository.save_a_new_category("cat-3", "Shopping List")

    response = client.get("/api/categories")

    assert response.status_code == 200
    assert response.json == [
        {
            "id_cat": "cat-1",
            "name": "Sports"
        },
        {
            "id_cat": "cat-2",
            "name": "Music"
        },
        {
            "id_cat": "cat-3",
            "name": "Shopping List"
        }
    ]

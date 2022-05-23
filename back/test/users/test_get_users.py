from src.lib.utils import temp_file
from src.webserver import create_app
from src.domain.note import NotesRepository, Note
from src.domain.user import UserRepository, User


def test_should_return_empty_list_of_users():
    users_repository = UserRepository(temp_file())
    app = create_app(repositories={"user": users_repository})
    client = app.test_client()

    response = client.get("/api/user")

    assert response.json == []

from src.lib.utils import temp_file
from src.webserver import create_app
from src.domain.user import UserRepository, User


def setup():
    user_repository = UserRepository(temp_file())
    app = create_app(repositories={"user": user_repository})
    client = app.test_client()

    claudio = User(id="user-1", name="Claudio", password="password")
    user_repository.save(claudio)

    return client


def test_should_validate_login():
    client = setup()

    body = {"user": "user-1", "password": "password"}

    response = client.post("/auth/login", json=body)

    assert response.status_code == 200
    assert response.json == {"id": "user-1", "name": "Claudio"}


def test_should_fail_if_invalid_password():
    client = setup()

    body = {"user": "user-1", "password": "wrong-password"}

    response = client.post("/auth/login", json=body)

    assert response.status_code == 401


def test_should_fail_if_user_no_exist():
    client = setup()

    body = {"user": "user-no-exist", "password": "password"}

    response = client.post("/auth/login", json=body)

    assert response.status_code == 401

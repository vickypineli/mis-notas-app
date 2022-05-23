from flask import Flask, jsonify, request
from flask_cors import CORS
from src.lib.utils import object_to_json
from src.domain.note import Note
from src.domain.user import User
from src.domain.tags import Tag
import json


def create_app(repositories):
    app = Flask(__name__)
    CORS(app)

    @app.route("/auth/login", methods=["POST"])
    def login():
        body = request.json
        user = repositories["user"].get_by_id(body["user"])

        if user is None or (body["password"]) != user.password:
            return "", 401

        return user.to_dict(), 200

    @app.route("/", methods=["GET"])
    def hello_world():
        return "...magic!"

    @app.route("/api/info", methods=["GET"])
    def info():
        info = repositories["info"].get_info()
        return object_to_json(info)

    @app.route("/api/notes", methods=["GET"])
    def get_user_all_notes():
        user_id = request.headers.get("Authorization")
        notes = repositories["note"].search_by_user_id(user_id)
        return object_to_json(notes)

    # verificar que no pueda ir a notas sin haber escogido un usuario

    @app.route("/api/notes", methods=["POST"])
    def notes_post():
        data = request.json

        note = Note(**data)

        repositories["note"].insert_data_note(note)
        return ""

    @app.route("/api/notes/<id>", methods=["GET"])
    def notes_get_by_id(id):
        user_id = request.headers.get("Authorization")
        one_note_by_id = repositories["note"].get_by_id(id)
        if user_id == one_note_by_id.user_id:
            return object_to_json(one_note_by_id), 200
        else:
            return "", 403

    @app.route("/api/notes/<id>", methods=["DELETE"])
    def deleted_note_by_id(id):
        user_id = request.headers.get("Authorization")
        note_deleted_by_id = repositories["note"].note_deleted_by_id(id)
        return ""

    @app.route("/api/notes/<id>", methods=["PUT"])
    def modify_note_by_id(id):
        data = request.json
        note = Note(**data)
        repositories["note"].modify_data_note_by_id(note)
        return ""

    @app.route("/api/user", methods=["GET"])
    def users_get_all():
        all_users = repositories["user"].get_all_users()
        return object_to_json(all_users)

    @app.route("/api/tags", methods=["GET"])
    def tags_get_all():
        all_tags = repositories["tags"].get_all_tags()
        return object_to_json(all_tags)

    @app.route("/api/tags", methods=["POST"])
    def tags_post_all():
        data = request.json
        tag = Tag(**data)

        repositories["tags"].save(tag)
        return "", 200

    @app.route("/api/tags/<id>", methods=["GET"])
    def tags_get_by_id(id):
        tag_by_id = repositories["tags"].get_by_note_id(id)
        return object_to_json(tag_by_id)

    @app.route("/api/categories", methods=["GET"])
    def categories_get_all():
        all_categories = repositories["note"].get_all_categories()

        return jsonify(all_categories)

    return app

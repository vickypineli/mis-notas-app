import sqlite3
import json


class Tag:
    def __init__(self, note_id, tag):
        self.note_id = note_id
        self.tag = tag

    def to_dict(self):
        return {"note_id": self.note_id, "tag": self.tag}


class TagsRepository:
    def __init__(self, database_path):
        self.database_path = database_path
        self.init_tables()

    def create_conn(self):
        conn = sqlite3.connect(self.database_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_tables(self):
        sql = """
            CREATE TABLE IF NOT EXISTS tags (
                note_id VARCHAR,
                tag VARCHAR,
                FOREIGN KEY (note_id) REFERENCES notes(id)
            );

            """
        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()

    def get_all_tags(self):
        sql = """SELECT * FROM tags"""
        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        list_tag = []
        for item in data:
            print(item)
            tag_class = Tag(note_id=item["note_id"], tag=item["tag"])
            list_tag.append(tag_class)
        return list_tag

    def get_by_note_id(self, note_id):

        # get tag by note id
        sql = """SELECT * FROM tags WHERE note_id = :note_id"""
        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.execute(sql, {"note_id": note_id})
        data = cursor.fetchall()
        list_tag = []
        for item in data:
            print(item)
            tag_class = Tag(note_id=item["note_id"], tag=item["tag"])
            list_tag.append(tag_class)
        return list_tag

    def save(self, tags):
        sql = """INSERT INTO tags (note_id, tag) VALUES (
            :note_id, :tag
        ) """
        conn = self.create_conn()
        cursor = conn.cursor()
        str_tags = json.dumps(tags.to_dict())
        json_tags = json.loads(str_tags)
        for tag in json_tags['tag']:
            cursor.execute(sql, {"note_id": json_tags['note_id'], "tag": tag})
        conn.commit()

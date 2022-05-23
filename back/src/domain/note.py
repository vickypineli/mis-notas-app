import sqlite3


class Note:
    def __init__(self, id, user_id, title, text, id_cat):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.text = text
        self.id_cat = id_cat

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'text': self.text,
            'user_id': self.user_id,
            'id_cat': self.id_cat
        }


class NotesRepository:
    def __init__(self, database_path):
        self.database_path = database_path
        self.init_tables()

    def create_conn(self):
        conn = sqlite3.connect(self.database_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_tables(self):
        # notes -> no tiene foreign key(id_cat)
        # porque la relacion notes - categories es VOLUNTARIA
        sql_table_notes = """
            CREATE TABLE IF NOT EXISTS notes (
                id varchar NOT NULL PRIMARY KEY,
                title varchar,
                text varchar,
                user_id varchar,
                id_cat varchar,
                FOREIGN KEY (id_cat)
                    REFERENCES categories (id_cat) 
            )

        """
        sql_table_categories = """
                CREATE TABLE IF NOT EXISTS categories (
                id_cat varchar NOT NULL PRIMARY KEY,
                name varchar)"""
        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.execute(sql_table_notes)
        cursor.execute(sql_table_categories)
        conn.commit()

    def get_all_notes(self):
        notes_list = []
        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.execute("""select * from notes""")

        data = cursor.fetchall()

        for item in data:
            one_note = Note(
                id=item["id"], title=item["title"], text=item["text"], user_id=item["user_id"], id_cat=item["id_cat"]
            )
            notes_list.append(one_note)

        return notes_list

    def get_by_id(self, note_id):

        sql = """SELECT * FROM notes WHERE id= :id"""
        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.execute(sql, {"id": note_id})

        data = cursor.fetchone()
        one_note = Note(id=data["id"], title=data["title"],
                        text=data["text"], user_id=data["user_id"], id_cat=data["id_cat"])
        return one_note

    # get_all_notes_searching_by_user_id
    def search_by_user_id(self, user_id):

        sql = """SELECT * FROM notes WHERE user_id= :user_id ORDER BY lower(title) ASC"""
        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.execute(sql, {"user_id": user_id})
        data = cursor.fetchall()
        notes = []
        for item in data:
            note = Note(**item)
            notes.append(note)
        return notes

    def insert_data_note(self, note):
        sql = """insert into notes (id, title, text, user_id, id_cat) values (
            :id, :title, :text, :user_id, :id_cat
        ) """

        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.execute(
            sql,
            note.to_dict(),

        )
        conn.commit()

    # metodo save() cambiado de nombre

    def modify_data_note_by_id(self, modified_note):

        sql = """ UPDATE notes
                    SET title = :title, text= :text, user_id = :user_id, id_cat = :id_cat
                    WHERE id = :id; """
        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.execute(
            sql, modified_note.to_dict()
        )
        conn.commit()

    def note_deleted_by_id(self, note_deleted):
        sql = """ DELETE FROM notes
                    WHERE notes.id = :id """
        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.execute(
            sql, {"id": note_deleted}
        )
        conn.commit()
        cursor.close()

    def get_all_categories(self):
        sql = """ SELECT * FROM categories """

        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.execute(sql)
        data_list = cursor.fetchall()

        categories_list = []
        for category in data_list:

            category_dicc = {
                'id_cat': category["id_cat"], 'name': category["name"]}
            categories_list.append(category_dicc)

        cursor.close()
        return categories_list

    # terminar de construir
    def get_last_category_id(self):
        sql = """SELECT id_cat FROM categories
                ORDER BY id_cat DESC
                LIMIT 1"""
        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.execute(sql)
        data_last_id = cursor.fetchone()[0]

        return data_last_id

    # comprobar que funciona
    def save_a_new_category(self, id_category, name_category):
        sql = """insert into categories (id_cat, name) values (
            :id_cat, :name
        ) """
        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.execute(sql, {'id_cat': id_category, 'name': name_category})
        conn.commit()

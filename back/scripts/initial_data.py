import sys

sys.path.insert(0, "")
from src.domain.user import UserRepository, User
from src.domain.note import NotesRepository, Note
from src.domain.info import InfoRepository, Info
from src.domain.tags import Tag, TagsRepository


def main():

    database_path = "data/database.db"

    info_repository = InfoRepository(database_path)

    info_repository.save(Info(app_name="my-personal-notes"))

    notes_repository = NotesRepository(database_path)

    tag_repository = TagsRepository(database_path)


    # Guardar categorias en NOTE repository
    notes_repository.save_a_new_category("cat-0", "Sin categorias")
    notes_repository.save_a_new_category("cat-1", "Tareas")
    notes_repository.save_a_new_category("cat-2", "Musica")
    notes_repository.save_a_new_category("cat-3", "Compras")

    nota1 = Note(
        id="note-1",
        title="Lista de la compra:",
        text="Huevos, Leche, Cereales, Pollo",
        user_id="user-1",
        id_cat="cat-1",
    )
    nota2 = Note(
        id="note-2",
        title="comprar libro",
        text="El Quijote 22€",
        user_id="user-1",
        id_cat="cat-2",
    )

    notes_repository.insert_data_note(nota1)
    notes_repository.insert_data_note(nota2)

    print("last category id: ", notes_repository.get_last_category_id())

    # Repositorio de Usuarios

    user_repository = UserRepository(database_path)

    user_repository.save(User("user-1", "Ander", "0000"))
    user_repository.save(User("user-2", "Alba", "0000"))
    not_1 = Tag("note-1", ["Musica", "Cine"])
    not_2 = Tag("note-1", ["Compras", "Tarea"])
    tag_repository.save(not_1)
    tag_repository.save(not_2)
    print("Datos iniciales cargados (se ha ejecutado initial_data.py)")


main()

<template>
<main>
    <div class="title">
      <h2>{{ pageTitle }}</h2>
    </div>
    <section id="note-detail">
        <form v-on:submit.prevent="addNewNote" action="">
          <div class="form">
              <label for="title-form">Titulo: </label>
              <input
                v-model="noteTitle"
                type="text"
                name="title-form"
                placeholder="Escriba aqui su titulo..."
              />
          </div>
          <div class="form">
              <label for="description">Descripciòn: </label>
              <textarea
                v-model="noteDescription"
                name="text-form"
                rows="8"
                cols="50"
                placeholder="Escriba aqui la descripciòn ...."
              ></textarea>
            </div>
        </form>
    </section>
    <section id="note-category">
          <label>Category: </label>
          <select  v-model="selectedCategory">
            <option value="null">Selecciona una categoria</option>
            <option
              v-for="index in this.listOfCategories"
              :value="index"
              :key="index.id_cat"
            >
              {{ index.name }}
            </option>
          </select>
    </section>
    <section id="buttons-area">
        <button @click="goBack">Atras</button>
        <button @click.prevent="addNewNote">Guardar</button>
    </section>
  </main>
</template>

<script>
import config from "@/config.js";
import Swal from "sweetalert2";
window.Swal = Swal;
import { v4 as uuidv4 } from "uuid";

export default {
  name: "AddNote",
  data() {
    return {
      pageTitle: "Añadir nota",
      noteTitle: "",
      noteDescription: "",
      listOfCategories: [],
      selectedCategory: null,
    };
  },
  created() {
    this.loadData();
  },

  methods: {
    enviarToque() {
      let localUser = localStorage.getItem("user");
      localUser = JSON.parse(localUser);
      let sender_name = localUser.name;
      let receiver_id = this.$router.params.id
      console.log(sender_name, "le ha enviado un toque a ", receiver_id)
    },
    async loadData() {
      //Categorias
      const responseCategories = await fetch(`${config.API_PATH}/categories`);
      this.listOfCategories = await responseCategories.json();
    },

    goBack() {
      if (this.isValidData()) {
        Swal.fire({
          title: "The note have changes. Do you want to save them?",
          showConfirmButton: true,
          showDenyButton: true,
        }).then((result) => {
          /* Read more about isConfirmed, isDenied below */
          if (result.isConfirmed) {
            this.addNewNote();
            this.$router.push("/notes");
            Swal.fire("Saved!", "", "success");
          } else if (result.isDenied) {
            Swal.fire("Changes are not saved", "", "info");
            this.$router.push("/notes");
          }
        });
      } else {
        this.$router.push("/notes");
      }
    },
    isValidData() {
      if (this.noteTitle != "" && this.noteDescription != "") {
        return true;
      } else {
        return false;
      }
    },
    addNewNote() {
      if (this.isValidData()) {
        let usuario = localStorage.getItem("user");
        let jsonUsuario = JSON.parse(usuario);
        let nextId = uuidv4();
        if (this.selectedCategory === null) {
          this.selectedCategory = { id_cat: "cat-0", name: "No category" };
        }
        let newNote = {
          id: nextId,
          title: this.noteTitle,
          text: this.noteDescription,
          user_id: jsonUsuario.id,
          id_cat: this.selectedCategory.id_cat,
        };
        const settings = {
          method: "POST",
          body: JSON.stringify(newNote),
          headers: {
            "Content-Type": "application/json",
            Authorization: jsonUsuario.id,
          },
        };
        fetch(`${config.API_PATH}/notes`, settings);

        Swal.fire({
          position: "center",
          icon: "success",
          title: "Your note has been saved",
          showConfirmButton: false,
          timer: 1500,
        });
        //Esto redirige a la página principal de todas las notas, justo despues de añadir una nueva
        // Si no queremos la redirección, sólo hay que borrar la línea de abajo
        this.$router.push("/notes");
        this.getTagsFromNoteDescription(newNote);
      } else {
        Swal.fire({
          position: "center",
          icon: "error",
          title: "Error! Fill all the fields out, please!",
          showConfirmButton: false,
          timer: 1500,
        });
      }

      this.noteTitle = "";
      this.noteDescription = "";
    },

    getTagsFromNoteDescription(note) {
      let tags = this.noteDescription.replace("\n", " ").split(" ");
      let filteredTags = [];
      for (let tag of tags) {
        if (tag.startsWith("#")) {
          filteredTags.push(tag);
        }
      }

      let objHashtag = { tag: filteredTags, note_id: note.id };

      const settings = {
        method: "POST",
        body: JSON.stringify(objHashtag),
        headers: {
          "Content-Type": "application/json",
          Authorization: note.user_id,
        },
      };
      fetch(`${config.API_PATH}/tags`, settings);
    },
  },
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Poppins:wght@500&display=swap");

* {
  font-family: Poppins;
  background-color: white;
}
main {
  margin-top: 20vh;
}
.title {
  color:rgb(50, 93, 234);
}

#note-detail {
  width: 80vw;
  display: flex;
  flex-direction: column;
  margin: auto;
  font-family: Poppins;
}

#note-category {
  width: 80vw;
  display: flex;
  flex-direction: column;
  margin: auto;
  font-family: Poppins;
}

#buttons-area {
  margin-top: 20px;
  display: flex;
  flex-direction: row;
  Justify-content: center;
}

textarea {
  text-align: left;
  width: 80vw;
}

section {
  width: 80vw;
  display: flex;
  flex-direction: column;
  margin: auto;
  font-family: Poppins;
}
.form {
  text-align: left;
  margin-top: 10px;
}
label {
  text-align: left;
  color:rgb(207, 105, 11);
}

input {
  width: 80vw;
}

button {
  color: rgb(207, 105, 11);
  width: 30vw;
  padding: 5px;
  margin: 10px;
  font-size: 1.5em;
  border-color: rgb(207, 105, 11);
  font-weight: bold;
}

</style>

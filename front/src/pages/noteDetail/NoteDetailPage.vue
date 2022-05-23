<template>
  <main>
    <div class="title">
    <h2>NOTA DETALLADA</h2>
    </div>
    <section id="note-detail">
        <label for="title">TITULO: </label>
        <input name="title" v-model="this.modifiedNote.title" />
        <label for="description">DESCRIPCION: </label>
        <textarea
          id="text"
          v-model="this.modifiedNote.text"
          rows="8"
          cols="49"
        ></textarea>
    </section>
    <section id="note-category">
      <label>Category: </label>
      <select v-model="clickedCategory">
        <option disabled value="">{{ this.noteCategoryName }}</option>
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
        <button @click="goBack" class="button">Back</button>
        <button @click.prevent="modifyNote(modifiedNote)" class="button">
          Save
        </button>
        <button @click="removeNote" class="button">Remove</button>
    </section>
  
  </main>
</template>

<script>
import config from "../../config.js";
import Swal from "sweetalert2";

export default {
  name: "NoteDetail",
  data() {
    return {
      note: {},
      modifiedNote: {},
      loggedUser: "",
      listOfCategories: [],
      clickedCategory: "",
      noteCategoryName: "",
    };
  },

  mounted() {
    this.loadData();
    this.getNoteTags();
  },

  methods: {
    async loadData() {
      let usuario = localStorage.getItem("user");
      let jsonUsuario = JSON.parse(usuario);
      const settings = {
        method: "GET",
        headers: {
          Authorization: jsonUsuario.id,
        },
      };
      //Carga los datos de la nota
      this.loggedUser = jsonUsuario.name;
      const response = await fetch(
        `${config.API_PATH}/notes` + "/" + this.$route.params.id,
        settings
      );
      this.note = await response.json();
      this.modifiedNote = JSON.parse(JSON.stringify(this.note));

      //Esto carga los datos de categorias
      const responseCategories = await fetch(`${config.API_PATH}/categories`);
      this.listOfCategories = await responseCategories.json();

      for (let category of this.listOfCategories) {
        if (category.id_cat == this.note.id_cat) {
          this.noteCategoryName = category.name;
        }
      }
    },
    async getNoteTags() {
      const response = await fetch(
        "http://localhost:5000/api/tags/" + this.$route.params.id
      );
      let data = await response.json();
      this.note.tags = data;
    },
    goBack() {
      if (this.isNoteEmpty()) {
        Swal.fire("Error!", "Fill all the fields out, please!", "error");
      } else {
        if (this.isNoteModified()) {
          Swal.fire({
            title: "The note have changes. Do you want to save them?",
            showConfirmButton: true,
            showDenyButton: true,
          }).then((result) => {
            /* Read more about isConfirmed, isDenied below */
            if (result.isConfirmed) {
              this.modifyNote();
              this.$router.push("/notes");
            } else if (result.isDenied) {
              Swal.fire("Changes are not saved", "", "info");
              this.$router.push("/notes");
            }
          });
        } else {
          this.$router.push("/notes");
        }
      }
    },
    removeNote() {
      Swal.fire({
        title: "ARE YOU SURE?",
        text: "You won't be able to revert this!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Yes, delete it!",
      }).then(async (result) => {
        if (result.isConfirmed) {
          await fetch(
            `${config.API_PATH}/notes` + "/" + this.$route.params.id,
            { method: "DELETE" }
          );
          this.$router.push("/notes");
          Swal.fire("Deleted!", "Your file has been deleted.", "success");
        }
      });
    },

    isNoteModified() {
      if (this.clickedCategory.id_cat != undefined) {
        this.modifiedNote.id_cat = this.clickedCategory.id_cat;
      }

      if (
        this.note.title != this.modifiedNote.title ||
        this.note.text != this.modifiedNote.text ||
        this.note.id_cat != this.modifiedNote.id_cat
      ) {
        return true;
      }
    },
    isNoteEmpty() {
      if (this.modifiedNote.title === "" || this.modifiedNote.text === "") {
        return true;
      } else {
        return false;
      }
    },

    async modifyNote() {
      if (this.isNoteEmpty() == true) {
        Swal.fire("Error!", "Fill all the fields out, please!", "error");
      } else {
        if (this.isNoteModified()) {
          const settings = {
            method: "PUT",
            body: JSON.stringify(this.modifiedNote),
            headers: {
              "Content-Type": "application/json",
            },
          };
          let id = this.note.id;
          await fetch(`${config.API_PATH}/notes` + "/" + id, settings);

          Swal.fire({
            position: "center",
            icon: "success",
            title: "Your work has been saved",
            showConfirmButton: false,
            timer: 1200,
          });
          this.$router.push("/notes");
        } else {
          Swal.fire({
            position: "center",
            icon: "info",
            title: "Note has not been modified",
            showConfirmButton: false,
            timer: 1500,
          });
        }
      }
    },
  },
};
</script>
<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Poppins:wght@500&display=swap");

main {
  margin-top: 10vh;
  font-family: Poppins;
  overflow: no-scroll;
  background-color: white;
}
.title {
  color:rgb(50, 93, 234);
}

section {
  width: 80vw;
  display: flex;
  flex-direction: column;
  font-family: Poppins;
}

label {
  text-align: left;
  color:rgb(207, 105, 11);
}

#note-category {
  font-family: Poppins;
}

#buttons-area {
  display: flex;
  flex-direction: row;
  Justify-content: center;
}

button {
  color: rgb(207, 105, 11);
  width: 20vw;
  padding: 5px;
  margin: 10px;
  font-size: 1.5em;
  border-color: rgb(207, 105, 11);
  font-weight: bold;
}
</style>

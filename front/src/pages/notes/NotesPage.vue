<template>
  <main>
    <section id="head">
      <h3>{{ notesTitle }}
      <i>{{ currentUser }}</i>    
      </h3>
    </section>
    <section id="filters">
      <p>Busqueda:</p>
      <article class="search-by-categories">
        <!-- <div>Categoria: {{ selectedCategories }}</div> -->
        <select v-model="selectedCategories">
          <option disabled value="">Seleccione una categoria</option>
          <option
            v-for="category in listOfCategories"
            :key="category"
            :value="category.id_cat"
          > {{ category.name }}
          </option>
        </select>
      </article>
        <article class="search-by-words">
          <input
            class="search"
            type="search"
            v-model="searchNote"
            placeholder="Palabra de busqueda..."
          />
          <span><i class="fa fa-search"></i></span>
        </article>
      </section>
      <section id="list-notes">
          <article class="panel" v-for="note in filterNote" :key="note.id">
            <p @click="goToNoteDetail(note)" class="text-button">
              {{ note.title }}
            </p>
            <p class="text-category"> Cat:
             ({{ getCategoryNameById(note.id_cat) }})
            </p>
            <button class="remove_button" @click="removeNote(note)">❌</button>
          </article>
          <router-link to="/notes/add"><button class="add_button">Añadir Nota</button></router-link>
      </section>
      
  </main>
</template>

<script>
import config from "../../config.js";
import Swal from "sweetalert2";

window.Swal = Swal;
export default {
  name: "Notes",
  data() {
    return {
      notesTitle: "Las notas de:",
      notesList: [],
      searchNote: "",
      currentUser: "",
      listOfCategories: [],
      selectedCategory: "",
      selectedCategories: [],
      checked: "",
    };
  },

  mounted() {
    this.loadData();
  },
  methods: {
    async loadData() {
      console.log;
      let usuario = localStorage.getItem("user");
      let jsonUsuario = JSON.parse(usuario);
      const settings = {
        method: "GET",
        headers: {
          Authorization: jsonUsuario.id,
        },
      };
      //Se cargan los datos de la nota
      const response = await fetch(`${config.API_PATH}/notes`, settings);
      this.notesList = await response.json();
      this.currentUser = jsonUsuario.name;

      //Se cargan los datos de la categoria
      const responseCategories = await fetch(`${config.API_PATH}/categories`);
      this.listOfCategories = await responseCategories.json();
    },
    getCategoryNameById(categoryId) {
      const result = this.listOfCategories
        .filter((c) => c.id_cat == categoryId)
        .map((c) => c.name)[0];
      return result;
    },
    goToNoteDetail(note) {
      this.$router.push("/notes/" + note.id);
    },
    async removeNote(note) {
      Swal.fire({
        title: "Estas seguro?",
        text: "You won't be able to revert this!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Yes, delete it!",
      }).then(async (result) => {
        if (result.isConfirmed) {
          await fetch(`${config.API_PATH}/notes` + "/" + note.id, {
            method: "DELETE",
          });
          Swal.fire("Deleted!", "Your file has been deleted.", "success").then(
            function () {
              location.reload();
            }
          );
        }
      });
    },
  },

  computed: {
    filterNote() {
      return this.notesList
        .filter(
          (note) =>
            note.title.toLowerCase().includes(this.searchNote.toLowerCase()) ||
            note.text.includes(this.searchNote)
        )
        .filter((note) => {
          if (Object.keys(this.selectedCategories).length == 0) {
            return this.notesList;
          }
          if (
            Object.values(this.selectedCategories).indexOf(note.id_cat) > -1
          ) {
            return true;
          } else {
            return false;
          }
        });
    },
  },
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Poppins:wght@500&display=swap");
main {
  background-color: white;
  width: 90vw;
  height: 90vh;
  margin: auto;
  font-family: poppins;
}
#head {
  height: 5vh;
  color: rgb(48, 84, 214);
  text-align: right;
  padding-right: 10vw;
}
#filters {
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  justify-content: space-around;
  width: 90vw;
  margin: auto;
  
  border: 0.5px;
}

.search-by-categories {
  margin: 15px;
  display: flex;
  flex-direction: row;
}
.search-by-words {
  margin: 15px;
  display: flex;
  flex-direction: row;
}
.fa {
  margin-left: 10px;
}
article {
  border: 0.5px double rgb(207, 105, 11);;
  margin: 5px;
  display: flex;
  justify-content: space-between;
  background-color: rgb(226, 231, 249);
}
.add_button {
  color: rgb(207, 105, 11);
  width: 30vw;
  padding: 5px;
  margin: 10px;
  font-size: 1.5em;
  border-color: rgb(207, 105, 11);
  font-weight: bold;
}
.text-button {
  width: 45vw;
  font-size: 1.0em;
  text-align: left;
  margin-left: 15px;
  text-transform: uppercase;
}

.text-button:hover {
  color: brown;
  font-size:1.01em;
  text-decoration: underline;
}
.text-category {
  font-size: 1.0em;
  color: gray;
}
.remove_button {
  width: 10vw;
  font-size: 1.2em;
  background-color: whitesmoke;
  border:  blue;
}
.remove_button:hover {
  background-color: rgb(172, 171, 171);
  
}
</style>
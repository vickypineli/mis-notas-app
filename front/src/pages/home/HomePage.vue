<template>
  <div class="home">
    <section class="container">
      <h2>Bienvenido</h2>
      <h1>TUS NOTAS PERSONALES</h1>
      <img src="@/assets/img/note-logo.png" alt="logo">
    </section>
    <section class="form-login">
        <h4>Inicia sesiòn</h4>
        <form>
          <input type="text" placeholder="Username" v-model="user" />
          <input type="password" placeholder="Password" v-model="password" /> 
          <button  @click.prevent="onButtonClicked">ENTER</button>
        </form>
    </section>
  </div>
</template>

<script>
import { useStorage } from "@vueuse/core";
import { login } from "@/services/auth.js";
import Swal from "sweetalert2";
window.Swal = Swal;
export default {
  name: "Home",
  data() {
    return {
      greeting: "Bienvenido",
      user: "",
      password: "",
      showPassword: true,
      localUser: useStorage("user", {}),
    };
  },

  methods: {
    async onButtonClicked() {
      const response = await login(this.user, this.password);
      const loginStatus = response.status;

      if (loginStatus === 401) {
        Swal.fire({
          icon: "Error",
          title: "Oops...",
          text: "el nombre de usuario o la contraseña es incorrecta!",
          footer: "Por favor intentelo de nuevo.",
        });
      } else {
        const auth = await response.json();
        localStorage.setItem("user", JSON.stringify(auth));
        this.$router.push("/notes");
      }
    },
    onSwitchVisibility() {
      this.showPassword = !this.showPassword;
    },
  },
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css?family=Montserrat:400,800");
@import url("https://fonts.googleapis.com/css2?family=Poppins:wght@500&display=swap");
.home {
  background-color: white;
  overflow: no-scroll;
}
.container {
  width: 80vw;
  margin: auto;
  font-family: poppins;
  color:  rgb(220, 143, 71);
}
.form-login{
  width: 50vw;
  margin: auto;
  padding: 5px;
  background-color: rgb(220, 225, 243);
  color:  rgb(50, 93, 234);
 
}
img{
  width: 30vw;
  margin: 10px;
  border: none;
}
button {
  color: rgb(207, 105, 11);
  width: 20vw;
  padding: 5px;
  margin: 10px;
  font-size: 1em;
  font-family:  'Arial Narrow Bold', sans-serif;
  border-color: rgb(207, 105, 11);
}
input {
  width: 40vw;
  height: 1vh;
  padding: 10px;
  margin: 2px;
}
</style>

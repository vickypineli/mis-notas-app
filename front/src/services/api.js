
// function getUserId() {
//     const userJson = localStorage.getItem("user");
//     const user = JSON.parse(userJson);
//     return user.id;
//   }
    
    export  function getUser() {
      const userJson = localStorage.getItem("user");
      const user = JSON.parse(userJson);
      return user;
    }
  
  
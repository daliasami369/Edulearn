
// function handleLogin(event) {
//     event.preventDefault(); 
//     const nameInput = document.getElementById("UserName");
//     const role = document.querySelector('input[name="Role"]:checked');
    
//     if (nameInput) {
//         let name = nameInput.value;
//         sessionStorage.setItem("UserName", name);
  

//    if(role){
//     if(role.value === "Teacher"){
//         window.location.href="/teacher/";
//     }
//     else{
//         window.location.href="/student/";
//     }
// }
//     }
// }

const photo = document.getElementById("photo");

if(photo){
    photo.addEventListener("change", function () {

        const file = this.files[0];

        const reader = new FileReader();

        reader.onload = function () {
            localStorage.setItem("userImage", reader.result);
        }

        reader.readAsDataURL(file);
    });
}
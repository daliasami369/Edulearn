
const photo = document.getElementById("photo");
const name = sessionStorage.getItem("UserName");
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


const photo = document.getElementById("photo");
const preview = document.getElementById("preview");

if (photo && preview) {

    // لو فيه صورة محفوظة قبل كده
    const savedImage = localStorage.getItem("userImage");
    if (savedImage) {
        preview.src = savedImage;
    }

    photo.addEventListener("change", function () {

        const file = this.files[0];

        if (!file) return;

        const reader = new FileReader();

        reader.onload = function (e) {

            preview.src = e.target.result;      // عرض الصورة داخل الدائرة

            localStorage.setItem(
                "userImage",
                e.target.result
            );

        };

        reader.readAsDataURL(file);

    });

}
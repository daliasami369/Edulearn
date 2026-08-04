window.onload = function(){

    const studentName = document.getElementById("studentName");

    const name = sessionStorage.getItem("UserName");

    if(name){
        studentName.innerHTML = `<b>Welcome Back, ${name}</b>`;
    }

    if(document.getElementById("teacherId")){
        showSection("chat");
    }

    // إشعار الاشتراك
    if(typeof notificationMessage !== "undefined" && notificationMessage !== ""){
        showNotification(notificationMessage,"success");
    }

}
  function showSection(section){

    const sections = [
        "homeSection",
        "subjectsSection",
        "lessonsSection",
        "myTeachersSection",
        "chatSection",
        "testsSection",
        "paymentSection"
    ];

    sections.forEach(id => {
        const el = document.getElementById(id);
        if(el){
            el.style.display = "none";
        }
    });

    if(section === "home")
        document.getElementById("homeSection").style.display = "block";

    else if(section === "subjects")
        document.getElementById("subjectsSection").style.display = "block";

    else if(section === "lessons")
        document.getElementById("lessonsSection").style.display = "block";

    else if(section === "teachers")
      document.getElementById("myTeachersSection").style.display = "block";

    else if(section === "chat")
        document.getElementById("chatSection").style.display = "block";

    else if(section === "test")
        document.getElementById("testsSection").style.display = "block";
    else if(section=="payment")
        document.getElementById("paymentSection").style.display ="block";
}

function showTeachers(subjectId)
{
    const teachersList =
        document.getElementById(
            "teachers-" + subjectId
        );

    if (teachersList.style.display === "none")
    {
        teachersList.style.display = "block";
    }
    else
    {
        teachersList.style.display = "none";
    }
}

function selectTeacher(
    teacherId,
    subjectId,
    firstName,
    secondName,
    subjectName,
     button
)
{
  
    fetch("/enroll/", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body:
            "teacher_id=" + teacherId +
            "&subject_id=" + subjectId
    })

    .then(response => response.text())

    .then(data => {

        const container =
        document.getElementById("myTeachersSection");

        container.innerHTML += `
        <div class="teacher-card">

        <h3>${firstName} ${secondName}</h3>

        <p>${subjectName}</p>

        <button onclick="openChat(${teacherId},'${firstName} ${secondName}')">
        Open Chat
        </button>

        </div>
        `;

       showNotification("✔ Teacher Selected");

button.disabled = true;
button.innerHTML = "Selected";

    });
}
function getCookie(name)
{
    let cookieValue = null;

    if (document.cookie)
    {
        const cookies = document.cookie.split(';');

        for (let cookie of cookies)
        {
            cookie = cookie.trim();

            if (cookie.startsWith(name + '='))
            {
                cookieValue =
                    decodeURIComponent(
                        cookie.substring(name.length + 1)
                    );
            }
        }
    }

    return cookieValue;
}

let currentTeacherId = null;

function openChat(teacherId, teacherName)
{
    currentTeacherId = teacherId;

    showSection("chat");

    document.getElementById("chatTeacher").innerText = teacherName;

    fetch("/load_student_messages/" + teacherId + "/")
.then(response => response.json())
.then(data => {

    const chatBox = document.getElementById("chatBox");

    chatBox.innerHTML = "";

    data.forEach(msg => {

        if(msg.mine){
            chatBox.innerHTML +=
            `<p><b>Me:</b> ${msg.content}</p>`;
        }
        else{
            chatBox.innerHTML +=
            `<p><b>${msg.sender}:</b> ${msg.content}</p>`;
        }

    });

});
}
function sendMessage()
{
    let message = document.getElementById("studentMessage").value;

    if(!currentTeacherId)
    {
        alert("Choose a teacher first");
        return;
    }
      console.log(currentTeacherId);
      console.log(message);
    fetch("/send_message/", {

        method: "POST",

        headers: {
            "Content-Type":
                "application/x-www-form-urlencoded",

            "X-CSRFToken":
                getCookie("csrftoken")
        },

        body:
            "receiver=" + currentTeacherId +
            "&content=" + encodeURIComponent(message)

    })

    .then(response => response.json())

  .then(data => {

    document.getElementById("studentMessage").value = "";
    showNotification("✔ Message Sent");

    openChat(
        currentTeacherId,
        document.getElementById("chatTeacher").innerText
    );

});
}

function payNow(){

    fetch("/pay/")

    .then(response => response.text())

    .then(data=>{

        alert(data);

        location.reload();

    });

}

function sendReceipt() {

   showNotification("✔ Payment Sent");

    let file = document.getElementById("receipt").files[0];

    if (!file){
        showNotification("Choose Receipt First");
        return;
    }

    let formData = new FormData();
    formData.append("receipt", file);

    fetch("/upload_payment/",{
        method:"POST",
        headers:{
            "X-CSRFToken":getCookie("csrftoken")
        },
        body:formData
    })
    .then(res=>res.json())
    .then(data=>{

    showNotification(data.message);

    document.getElementById("receipt").value = "";

});

}

function removeTeacher(id){
showNotification("Teacher ID = " + id);

    fetch("/remove_teacher/" + id + "/")
    .then(res => res.json())
    .then(data => {
        alert(data.message);
        location.reload();
    });

}
function showNotification(message,type="success"){

    const box = document.getElementById("notification");

    box.innerHTML = message;

    box.className = "show " + type;

    setTimeout(()=>{
        box.className="";
    },3000);

}
let currentTestId = null;

window.onload = function(){

   const TeacherName = document.getElementById("TeacherName");

const name = sessionStorage.getItem("UserName");

const teachername = document.getElementById("teacherName");

if(name){
    TeacherName.textContent = `Welcome Back, ${name}`;
    teachername.textContent = `Teacher : ${name}`;
}

  
}

  function showSection(section){
    document.getElementById("homeSection").style.display = "none";
    // document.getElementById("subjectsSection").style.display = "none";
    document.getElementById("lessonsSection").style.display = "none";
    document.getElementById("testsSection").style.display = "none";
    document.getElementById("announcementsSection").style.display = "none";
    document.getElementById("showlesson").style.display = "none";
    document.getElementById("chatSection").style.display = "none";
    document.getElementById("mystudentsSection").style.display = "none";
    document.getElementById("showresulttest").style.display = "none";

    if(section === "home")
        document.getElementById("homeSection").style.display = "block";

    // else if(section === "subjects")
    //     document.getElementById("subjectsSection").style.display = "block";

    else if(section === "lessons")
        document.getElementById("lessonsSection").style.display = "block";

    else if(section === "tests")
        document.getElementById("testsSection").style.display = "block";

    else if(section === "announcements")
        document.getElementById("announcementsSection").style.display = "block";

    else if(section === "chat")
        document.getElementById("chatSection").style.display = "block";

    else if(section === "students")
        document.getElementById("mystudentsSection").style.display = "block";

    else if (section === "showlesson")
        document.getElementById("showlesson").style.display = "block";
    else if (section === "showresulttest")
        document.getElementById("showresulttest").style.display = "block";
}

function showTeachers(subjectId)
{
    const teacherList =
        document.getElementById(
            "teachers-" + subjectId
        );

    if (teacherList.style.display === "none")
    {
        teacherList.style.display = "block";
    }
    else
    {
        teacherList.style.display = "none";
    }
}

let currentStudentId = null;
function openTeacherChat(studentId, studentName)
{
    currentStudentId = studentId;

    showSection("chat");

    document.getElementById("studentId").value =
        studentId;

    document.getElementById("chatStudent").innerHTML =
        studentName;

    fetch("/load_teacher_messages/" + studentId + "/")

    .then(response => response.json())

    .then(data => {

        const chatBox =
            document.getElementById("chatBox");

        chatBox.innerHTML = "";

        data.forEach(msg => {

            if(msg.mine){

                chatBox.innerHTML +=
                `<p><b>Me :</b> ${msg.content}</p>`;

            }

            else{

                chatBox.innerHTML +=
                `<p><b>${msg.sender} :</b> ${msg.content}</p>`;

            }

        });

    });

}

function sendTeacherMessage()
{

    let message =
        document.getElementById("teacherMessage").value;

    let studentId =
        document.getElementById("studentId").value;

    if(message.trim()=="")
        return;

    fetch("/send_message/",{

        method:"POST",

        headers:{

            "Content-Type":"application/x-www-form-urlencoded",

            "X-CSRFToken":getCookie("csrftoken")

        },

        body:

        "receiver="+studentId+

        "&content="+encodeURIComponent(message)

    })

    .then(response=>response.json())

    .then(data=>{
        showNotification("✔ Message Sent");
        const chatBox =
            document.getElementById("chatBox");

        chatBox.innerHTML +=
        `<p><b>Me :</b> ${message}</p>`;

        document.getElementById("teacherMessage").value="";

    });

}


function getCookie(name) {

    let cookieValue = null;

    if (document.cookie && document.cookie !== "") {

        const cookies = document.cookie.split(";");

        for (let i = 0; i < cookies.length; i++) {

            const cookie = cookies[i].trim();

            if (cookie.startsWith(name + "=")) {

                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );

                break;
            }

        }

    }

    return cookieValue;

}

function sendAnnouncement() {

    let title = document.getElementById("title").value;
    let message = document.getElementById("message").value;
    let level = document.getElementById("AnnouncementLevel").value;
    fetch("/add_announcement/", {

        method: "POST",

        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": getCookie("csrftoken")
        },

        body:
            "title=" + encodeURIComponent(title) +
            "&message=" + encodeURIComponent(message)+
            "&level="+encodeURIComponent(level)

    })

    .then(response => response.json())

    .then(data => {
        showNotification("Announcement sent successfully");
        document.getElementById("title").value = "";
        document.getElementById("message").value = "";

    });

}

function addLesson(){

let formData = new FormData();

formData.append(
"title",
document.getElementById("lessonTitle").value
);

formData.append(
"description",
document.getElementById("lessonDescription").value
);

formData.append(
"video_link",
document.getElementById("lessonLink").value
);

formData.append(
    "level",
    document.getElementById("lessonLevel").value
);

formData.append(
"pdf_file",
document.getElementById("lessonPdf").files[0]
);

fetch("/add_lesson/",{

method:"POST",

headers:{
"X-CSRFToken":getCookie("csrftoken")
},

body:formData

})

.then(res=>res.json())

.then(data=>{
showNotification(data.message);
document.getElementById("lessonTitle").value = "";
document.getElementById("lessonDescription").value = "";
document.getElementById("lessonLink").value = "";
document.getElementById("lessonPdf").value = "";

});

}

function createTest(){

    let title=document.getElementById("testTitle").value;
    let duration=document.getElementById("duration").value;
    let total=document.getElementById("totalMarks").value;
    let level = document.getElementById("testLevel").value;
    fetch("/add_test/",{

        method:"POST",

        headers:{
            "Content-Type":"application/x-www-form-urlencoded",
            "X-CSRFToken":getCookie("csrftoken")
        },

        body:
        "title="+encodeURIComponent(title)+
        "&duration="+encodeURIComponent(duration)+
        "&total_marks="+encodeURIComponent(total)+
        "&level=" + encodeURIComponent(level)

    })

    .then(res=>res.json())

    .then(data=>{
        showNotification("✔ Test Created");
        currentTest=data.test_id;

        document.getElementById("testsSection").style.display="none";

        document.getElementById("questionsSection").style.display="block";

    });

}


function addQuestion(){
    let question=document.getElementById("questionText").value;

    let a=document.getElementById("choiceA").value;

    let b=document.getElementById("choiceB").value;

    let c=document.getElementById("choiceC").value;

    let d=document.getElementById("choiceD").value;

    let mark=document.getElementById("mark").value;

    let selected = document.querySelector(
    'input[name="correct"]:checked'
);

if(!selected){
    alert("Choose the correct answer");
    return;
}

let correct = selected.value;
    console.log(currentTest);
    fetch("/add_question/",{

        method:"POST",

        headers:{
            "Content-Type":"application/x-www-form-urlencoded",
            "X-CSRFToken":getCookie("csrftoken")
        },

        body:

        "test="+currentTest+

        "&question="+encodeURIComponent(question)+

        "&a="+encodeURIComponent(a)+

        "&b="+encodeURIComponent(b)+

        "&c="+encodeURIComponent(c)+

        "&d="+encodeURIComponent(d)+

        "&correct="+correct+

        "&mark="+mark

    })

    .then(res=>res.json())

    .then(data=>{

       showNotification("✔ Question Added");

        document.getElementById("questionText").value="";
        document.getElementById("choiceA").value="";
        document.getElementById("choiceB").value="";
        document.getElementById("choiceC").value="";
        document.getElementById("choiceD").value="";
        document.getElementById("mark").value="";

    });

}

function finishTest() {
    showNotification("Test Saved Successfully");

    document.getElementById("questionsSection").style.display = "none";

    document.getElementById("testsSection").style.display = "block";

}

function showNotification(message){

    const box = document.getElementById("notification");

    box.innerHTML = message;

    box.style.display = "block";

    setTimeout(()=>{
        box.style.display="none";
    },3000);

}
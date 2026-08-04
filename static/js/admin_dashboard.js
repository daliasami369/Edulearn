function showSection(section){

    const sections = [
        "dashboardSection",
        "paymentsection",
        "teachersection",
        "studentsection",
        "statisticsection",
        "subscriptiosection"
    ];

    sections.forEach(id => {

        const el = document.getElementById(id);

        if(el){
            el.style.display = "none";
        }

    });

    if(section=="dashboard")
        document.getElementById("dashboardSection").style.display="block";

    else if(section=="payment")
        document.getElementById("paymentsection").style.display="block";

    else if(section=="teachers")
        document.getElementById("teachersection").style.display="block";

    else if(section=="students")
        document.getElementById("studentsection").style.display="block";

    else if(section=="statistics")
        document.getElementById("statisticsection").style.display="block";

    else if(section=="subscriptions")
        document.getElementById("subscriptiosection").style.display="block";

}

function approvePayment(id){

    fetch("/approve_payment/" + id + "/")

    .then(res => res.json())

    .then(data => {

        showNotification(data.message);

        location.reload();

    });

}

function rejectPayment(id){

    fetch("/reject_payment/" + id + "/")

    .then(res=>res.json())

    .then(data=>{

        showNotification("❌ Payment Rejected","error");

        location.reload();

    });

}

function unblockStudent(id){

    fetch("/unblock_student/" + id + "/")

    .then(res => res.json())

    .then(data => {
       showNotification("Student Activated");
        let row = document.getElementById("student" + id);

        row.querySelector(".status").innerHTML = "Active";

        row.querySelector(".action").innerHTML = `
            <button onclick="blockStudent(${id})">
                Block
            </button>
        `;
        location.reload();
    });
}

function blockStudent(id){

    fetch("/block_student/" + id + "/")

    .then(res => res.json())

    .then(data => {

         showNotification("Student Blocked","error");

        let row = document.getElementById("student" + id);

        row.querySelector(".status").innerHTML = "Blocked";

        row.querySelector(".action").innerHTML = `
            <button onclick="unblockStudent(${id})">
                Unblock
            </button>
        `;
        location.reload();
    });
}
function showNotification(message, type="success"){

    const box = document.getElementById("notification");

    box.innerHTML = message;

    box.className = "show " + type;

    setTimeout(function(){

        box.className = "";

    },3000);

}
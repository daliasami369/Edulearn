from django.shortcuts import render, redirect , get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Course, Announcement, Lesson, User, Message, Test, Enrollment, Subject, Payment, Test, Question, Choice, UserSession,StudentResult
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from user_agents import parse
def teacher(request):  
    print("SESSION =", dict(request.session))

    teacher_id = request.session.get("user_id")

    print("teacher_id =", teacher_id)

    if teacher_id is None:
        return HttpResponse("Session is Empty")

    print("SESSION USER ID =", teacher_id)

    teacher = User.objects.filter(id=teacher_id).first()

    print("Teacher Object =", teacher)

    if teacher is None:
        return HttpResponse(f"No user with id = {teacher_id}")

    print("Teacher =", teacher.id, teacher.role)
    courses = Course.objects.all()
    announcements = Announcement.objects.filter( teacher=teacher ).order_by("-created_at")
    lessons = Lesson.objects.filter(teacher=teacher).order_by("-created_at")
    msgs = Message.objects.filter(receiver=teacher)
    print("Messages =", msgs.count())
    for m in msgs:
        print(
            "Sender:",
            m.sender.id,
            m.sender.role,
            "Receiver:",
            m.receiver.id
        )
    print("TEACHER =", teacher.id, teacher.role)
    enrollments = Enrollment.objects.filter(teacher=teacher)
    courses_count = enrollments.count()
    messages = Message.objects.filter(    receiver=teacher    ).order_by("created_at")
    students = User.objects.filter(enrollments__teacher=teacher).distinct()
    print("Teacher ID =", teacher.id)
    students_with_messages = User.objects.filter( id__in=msgs.values_list("sender_id", flat=True), role="Student").distinct()

    print(students_with_messages)
    print("Count =", students_with_messages.count())

    for s in students_with_messages:
        print(s.id, s.username)
        print("Teacher =", teacher.id)
    print("===== LESSONS =====")

    for lesson in lessons:
      print(
        lesson.id,
        lesson.title,
        lesson.teacher.username
    )
    results = StudentResult.objects.filter(test__teacher=teacher).select_related("student", "test")
    tests = Test.objects.filter(teacher=teacher)
    context = {
        "courses": courses,
        "announcements": announcements,
        "lessons": lessons,

        "courses_count": courses.count(),
        "students_count": students.count(),
        "lessons_count": lessons.count(),

        "students": students,
        "teacher": teacher,
        "messages": messages,
        "students_with_messages":students_with_messages,
        "enrollments" :enrollments,
        "courses_count" :courses_count,
        "results":results,
        "tests":tests,
       
    }

    all_messages = Message.objects.all()

    print("MESSAGES COUNT =", all_messages.count())

    for msg in all_messages:
     print(
        msg.sender.username,
        "->",
        msg.receiver.username,
        ":",
        msg.content
    )
    print("RESULT =", students_with_messages)
    print("STUDENTS WITH MESSAGES =")
    for s in students_with_messages:
        print(s.username)
    print(
    request.session.get("user_id"),
    teacher.id,
    teacher.role
    )

    return render(request, 'pages/teacher.html', context)


def teacher_chat(request, student_id):

    teacher_id = request.session.get("user_id")

    teacher = User.objects.get(id=teacher_id)

    student = User.objects.get(id=student_id)

    messages = Message.objects.filter(
        sender=teacher,
        receiver=student
    ) | Message.objects.filter(
        sender=student,
        receiver=teacher
    )
    context={
         "selected_student": student,
        "messages": messages,
    }

    messages = messages.order_by("created_at")

    return render(
    request,
    "pages/teacher.html",
    {
        "student": student,
        "messages": messages
    }
)


def login_page(request):

    print("LOGIN VIEW CALLED")

    if request.method == "POST":

        username = request.POST.get("UserName")
        password = request.POST.get("Password")
        role = request.POST.get("Role")

        print(username, password, role)

        user = User.objects.filter(
            username=username,
            role=role
        ).first()

        if user and check_password(password, user.password):
            if not user.is_active:
                return HttpResponse("حسابك محظور. يرجى التواصل مع الإدارة.")
            request.session["user_id"] = user.id
           
            # إنشاء Session لو مش موجودة
            if not request.session.session_key:
                request.session.create()

            session_key = request.session.session_key

            # الحصول على IP
            forwarded = request.META.get("HTTP_X_FORWARDED_FOR")

            if forwarded:
                ip = forwarded.split(",")[0]
            else:
                ip = request.META.get("REMOTE_ADDR")

            # الحصول على معلومات الجهاز
            ua = request.META.get("HTTP_USER_AGENT")
            device = parse(ua)

            print("IP =", ip)
            print("Device =", device)

            # حفظ الجلسة في قاعدة البيانات
            UserSession.objects.create(
                user=user,
                session_key=session_key,
                ip_address=ip,
                device=str(device)
            )

            if user.role == "Admin":
                return redirect("admin_dashboard")

            elif user.role == "Teacher":
                return redirect("teacher")

            else:
                return redirect("student")

        return render(
            request,
            "pages/index.html",
            {
                "error": "Wrong username or password"
            }
        )

    return redirect("index")

def signup_student(request):

    if request.method == "POST":
        print("FILES =", request.FILES)
        image = request.FILES.get("image")
        print("IMAGE =", image)
        first_name = request.POST.get("FirstName")
        second_name = request.POST.get("SecondName")
        username = request.POST.get("UserName")
        password = request.POST.get("Password")
        level = request.POST.get("level")
        address = request.POST.get("Address")
        email = request.POST.get("Email")
        phone = request.POST.get("Phone")
        if User.objects.filter(  username=username,  role="Student").exists():
                    return render(
                           request,
                          "pages/signup_student.html",
                           {
                              "error": "Username already exists"
                           }
                )
        if User.objects.filter(email=email).exists():
                    return render(request, 'pages/signup_student.html', {
                        'error': 'Email already exists'
                    })
        
        user=User.objects.create(
                    first_name=first_name,
                    second_name=second_name,
                    username=username,
                    password=make_password(password),
                    level=level,
                    address=address,
                    email=email,
                    phone=phone,
                    role="Student",
                    image=image
                )
       
        print("Saved:", user.username)
        print("Total Users:", User.objects.count())
        request.session["user_id"] = user.id
        return redirect('student')

    return render(request, 'pages/signup_student.html')

def signup_teacher(request):

    if request.method == "POST":

        first_name = request.POST.get("FirstName")
        second_name = request.POST.get("SecondName")
        username = request.POST.get("UserName")
        password = request.POST.get("Password")
        subject_names = request.POST.getlist("subjects")
        if not subject_names:
          return render(
        request,
        "pages/signup_teacher.html",
        {"error": "Please select a subject"}
        )
        print(repr(subject_names))
        print(subject_names)
        address = request.POST.get("Address")
        email = request.POST.get("Email")
        phone = request.POST.get("Phone")
        image = request.FILES.get("image")
        if User.objects.filter(  username=username, role="Teacher" ).exists():
                        return render(
                        request,
                          "pages/signup_student.html",
                          {
                           "error": "Username already exists"
                          }
                       )
        if User.objects.filter(email=email).exists():
            return render(request, 'pages/signup_teacher.html', {
                'error': 'Email already exists'
            })
        user = User.objects.create(
                   first_name=first_name,
                   second_name=second_name,
                   username=username,
                   password=make_password(password),
                   address=address,
                   email=email,
                   phone=phone,
                   role="Teacher",
                   image=image,
            )
        print("Subjects selected from form:", subject_names)
        subjects = Subject.objects.filter(   name__in=subject_names)
        print("Subjects found in DB:", list(subjects))
        user.subjects.set(subjects)
        print("Saved subjects:", list(user.subjects.all()))
        subject_objs = Subject.objects.filter(name__in=subject_names)
        user.subjects.set(subject_objs)
        print("Saved:", user.username)
        print("Total Users:", User.objects.count())
        request.session["user_id"] = user.id
        return redirect('teacher')

    return render(request, 'pages/signup_teacher.html')


def index(request):
    return render (request,'pages/index.html')

def about(request):
    return render(request ,'pages/about.html')

def home(request):
    return render(request,'pages/index.html')

def student(request):

    student_id = request.session.get("user_id")

    if not student_id:
        return HttpResponse("No Session")

    student = User.objects.filter(
        id=student_id,
        role="Student"
    ).first()

    if not student:
        return HttpResponse("Current session is not a student")

    # الاشتراكات
    if student.subscription_end and student.subscription_end < timezone.now():
        student.is_paid = False
        student.save()

    enrollments = Enrollment.objects.filter(student=student)
    unpaid_enrollments = enrollments.filter(is_paid=False)
    paid_enrollments = enrollments.filter(is_paid=True)

    courses_count = unpaid_enrollments.count()
    amount = courses_count * 200
    # المدرسين الذين اختارهم الطالب
    my_teachers = [e.teacher for e in enrollments]


    teacher_ids = enrollments.values_list("teacher_id", flat=True)

    paid_teacher_ids = enrollments.filter(
        is_paid=True
    ).values_list("teacher_id", flat=True)

    if enrollments.filter(is_paid=True).exists():

        announcements = Announcement.objects.filter(
            teacher_id__in=paid_teacher_ids,
            level=student.level
        )

        lessons = Lesson.objects.filter(
            teacher_id__in=paid_teacher_ids,
            level=student.level
        )

    else:

        if student.subscription_end:

            announcements = Announcement.objects.filter(
                teacher_id__in=teacher_ids,
                created_at__lte=student.subscription_end,
                level=student.level
            )

            lessons = Lesson.objects.filter(
                teacher_id__in=teacher_ids,
                created_at__lte=student.subscription_end,
                level=student.level
            )

        else:

            announcements = Announcement.objects.none()
            lessons = Lesson.objects.none()
    print("All enrollments:")
    for e in enrollments:
      print(e.subject.name, e.is_paid)

    print("Unpaid enrollments:")
    print(unpaid_enrollments.count())

    for e in unpaid_enrollments:
       print(e.subject.name)
    notification = Payment.objects.filter(  student=student,  status="Approved",  is_seen=False).last()
    if notification:
       notification.is_seen = True
       notification.save()
    context = {
        "students": student,
        "subjects": Subject.objects.all(),
        "all_teachers": User.objects.filter(role="Teacher"),
        "my_teachers": my_teachers,
        "courses": Course.objects.all(),
        "announcements": announcements,
        "lessons": lessons,
        "tests": Test.objects.filter(  teacher__students_enrolled__student=student ).distinct(),
        "courses_count": courses_count,
        "lessons_count": lessons.count(),
        "amount": amount,
        "paid_enrollments":paid_enrollments,
        "unpaid_enrollments":unpaid_enrollments ,
         "notification": notification,
    }

    return render(request, "pages/student.html", context)

def enroll(request):
    if request.method == "POST":
        print("===== ENROLL =====")

        teacher_id = request.POST.get("teacher_id")
        subject_id = request.POST.get("subject_id")
        student_id = request.session.get("user_id")

        print("teacher_id =", teacher_id)
        print("subject_id =", subject_id)
        print("student_id =", student_id)

        teacher = User.objects.get(id=teacher_id)
        student = User.objects.get(id=student_id)
        subject = Subject.objects.get(id=subject_id)

        enrollment, created = Enrollment.objects.get_or_create(
            student=student,
            teacher=teacher,
            subject=subject
        )

        print("created =", created)
        print("Enrollment count =", Enrollment.objects.count())

        return HttpResponse("success")

def contact_us(request):
    return render (request,'pages/contact_us.html')

def fqa(request):
    return render(request,'pages/fqa.html')

def service(request):
    return render(request,'pages/service.html')

def chat(request, teacher_id):

    student_id = request.session.get("user_id")

    student = User.objects.get(id=student_id)

    teacher = User.objects.get(
        id=teacher_id,
        role="Teacher"
    )

    messages = Message.objects.filter(
        sender=student,
        receiver=teacher
    ) | Message.objects.filter(
        sender=teacher,
        receiver=student
    )

    messages = messages.order_by("created_at")

    courses = Course.objects.all()
    announcements = Announcement.objects.order_by('-created_at')[:5]
    lessons = Lesson.objects.all()
    tests = Test.objects.all()

    enrollments = Enrollment.objects.filter(student=student)

    my_teachers = []

    for enrollment in enrollments:
        my_teachers.append(enrollment.teacher)

    return render(
        request,
        "pages/student.html",
        {
            "courses": courses,
            "announcements": announcements,
            "lessons": lessons,
            "tests": tests,
            "courses_count": courses.count(),
            "lessons_count": lessons.count(),
            "students": student,
            "my_teachers": my_teachers,
            "subjects": Subject.objects.all(),

            "messages": messages,
            "selected_teacher": teacher,
            "open_chat": True
        }
    )
def send_message(request):
    print("======= SEND MESSAGE =======")

    if request.method == "POST":

        sender_id = request.session.get("user_id")

        receiver_id = request.POST.get("receiver")

        content = request.POST.get("content")

        sender = User.objects.get(id=sender_id)

        receiver = User.objects.get(id=receiver_id)
        print(sender.id, sender.role)
        print(receiver.id, receiver.role)
        print("SENDER =", sender.username)
        print("RECEIVER =", receiver.username)
        print("CONTENT =", content)
        msg = Message.objects.create(
        sender=sender,
        receiver=receiver,
        content=content
             )

        print("Saved Message =", msg.id)
        return JsonResponse({"status": "success"})



def load_teacher_messages(request, student_id):

    teacher_id = request.session.get("user_id")

    teacher = User.objects.get(id=teacher_id)

    student = User.objects.get(id=student_id)

    messages = Message.objects.filter(
        sender=teacher,
        receiver=student
    ) | Message.objects.filter(
        sender=student,
        receiver=teacher
    )

    messages = messages.order_by("created_at")

    data = []

    for msg in messages:

        data.append({

            "sender": msg.sender.username,

            "content": msg.content,

            "mine": msg.sender.id == teacher.id

        })

    return JsonResponse(data, safe=False)

def load_student_messages(request, teacher_id):

    student_id = request.session.get("user_id")

    student = User.objects.get(id=student_id)
    teacher = User.objects.get(id=teacher_id)

    messages = (
        Message.objects.filter(sender=student, receiver=teacher) |
        Message.objects.filter(sender=teacher, receiver=student)
    ).order_by("created_at")

    data = []

    for msg in messages:
        data.append({
            "sender": msg.sender.first_name,
            "content": msg.content,
            "mine": msg.sender.id == student.id
        })

    return JsonResponse(data, safe=False)

def add_announcement(request):

    if request.method == "POST":

        title = request.POST.get("title")
        message = request.POST.get("message")
        level = request.POST.get("level")
        teacher = User.objects.get(
            id=request.session["user_id"]
        )

        Announcement.objects.create(
            teacher=teacher,
            title=title,
            message=message,
            level=level
        )

        return JsonResponse({"message": "Announcement sent"})

def add_lesson(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        video_link = request.POST.get("video_link")
        pdf = request.FILES.get("pdf_file")
        level = request.POST.get("level")
        teacher = User.objects.get(id=request.session["user_id"])

        if "youtube.com" in video_link or "youtu.be" in video_link:
            link_type = "youtube"

            if "watch?v=" in video_link:
                vid = video_link.split("v=")[1].split("&")[0]
                video_link = f"https://www.youtube.com/embed/{vid}"
            elif "youtu.be/" in video_link:
                vid = video_link.split("youtu.be/")[1].split("?")[0]
                video_link = f"https://www.youtube.com/embed/{vid}"

        elif "drive.google.com" in video_link:
            link_type = "drive"

        elif "meet.google.com" in video_link:
            link_type = "meet"

        elif "zoom.us" in video_link:
            link_type = "zoom"

        else:
            link_type = "youtube"

        Lesson.objects.create(
            teacher=teacher,
            title=title,
            description=description,
            video_link=video_link,
            pdf_file=pdf,
            link_type=link_type,
            level=level
        )

        return JsonResponse({"message": "Lesson Added Successfully"})

def delete_lesson(request, lesson_id):
    teacher = User.objects.get(id=request.session["user_id"])
    lesson = get_object_or_404(Lesson, id=lesson_id, teacher=teacher)

    lesson.delete()
    return redirect("teacher")

def upload_payment(request):

    if request.method == "POST":

        student = User.objects.get(
            id=request.session["user_id"]
        )

        unpaid_enrollments = Enrollment.objects.filter(
            student=student,
            is_paid=False
        )
        
        amount = unpaid_enrollments.count() * 200

        Payment.objects.create(
            student=student,
            receipt=request.FILES["receipt"],
            amount=amount,
            status="Pending",
        )

        return JsonResponse({
            "message": "Payment Sent"
        })

    return JsonResponse({"message": "Invalid request"})

def approve_payment(request, payment_id):

    payment = Payment.objects.get(id=payment_id)

    # تحديث حالة الدفع
    payment.status = "Approved"
    payment.is_seen = False
    payment.save()

    student = payment.student

    # تفعيل كل الاشتراكات الخاصة بالطالب
    enrollments = Enrollment.objects.filter(student=student)

    for enrollment in enrollments:
        enrollment.is_paid = True
        enrollment.save()

    # تفعيل الاشتراك لمدة 30 يوم
    student.payment_date = timezone.now()
    student.subscription_end = timezone.now() + timedelta(days=30)
    student.is_paid = True
    student.save()

    return JsonResponse({
        "message": "✔ Subscription Approved"
    })


def admin_dashboard(request):
    print(request.session["user_id"])

    admin = User.objects.get(
      id=request.session["user_id"]
     )

    print(admin.username)
    print(admin.role)

    if admin.role != "Admin":
        return HttpResponse("Access Denied")

    payments = Payment.objects.filter(status="Pending").order_by("-id")
    
    students = User.objects.filter(role="Student").prefetch_related(
    "enrollments__teacher",
    "enrollments__subject"
     )

    teachers = User.objects.filter(role="Teacher")

    context = {

        "payments": payments,

        "students": students,

        "teachers": teachers,

        "students_count": students.count(),

        "teachers_count": teachers.count(),

    }

    return render(
        request,
        "pages/admin_dashboard.html",
        context
    )

def admin_login(request):

    print("===== ADMIN LOGIN =====")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        print("USERNAME =", username)

        admin = User.objects.filter(
            username=username,
            role="Admin"
        ).first()

        print("ADMIN =", admin)

        if admin and check_password(password, admin.password):

            request.session["user_id"] = admin.id

            print("NEW SESSION =", request.session["user_id"])

            return redirect("admin_dashboard")

        print("LOGIN FAILED")

    return render(request, "pages/admin_login.html")

def add_test(request):

    if request.method=="POST":

        teacher=User.objects.get(
            id=request.session["user_id"]
        )

        test=Test.objects.create(

            teacher=teacher,

            title=request.POST["title"],

            duration=request.POST["duration"],

            total_marks=request.POST["total_marks"],
            level=request.POST["level"],

        )

        return JsonResponse({

            "test_id":test.id

        })

def add_question(request):

    if request.method == "POST":

        test_id = request.POST.get("test")

        question_text = request.POST.get("question")

        choice_a = request.POST.get("a")

        choice_b = request.POST.get("b")

        choice_c = request.POST.get("c")

        choice_d = request.POST.get("d")

        correct = request.POST.get("correct")

        mark = request.POST.get("mark")

        test = Test.objects.get(id=test_id)

        question = Question.objects.create(
            test=test,
            question=question_text,
            mark=mark
        )

        Choice.objects.create(
            question=question,
            text=choice_a,
            is_correct=(correct == "A")
        )

        Choice.objects.create(
            question=question,
            text=choice_b,
            is_correct=(correct == "B")
        )

        Choice.objects.create(
            question=question,
            text=choice_c,
            is_correct=(correct == "C")
        )

        Choice.objects.create(
            question=question,
            text=choice_d,
            is_correct=(correct == "D")
        )

        return JsonResponse({
            "message": "Question Added Successfully"
        })

    return JsonResponse({
        "message": "Invalid Request"
    })

def take_test(request, test_id):

    test = Test.objects.get(id=test_id)

    student = User.objects.get(
        id=request.session["user_id"]
    )

    # التأكد أن الطالب مشترك ومدفوع لهذا المدرس
    enrolled = Enrollment.objects.filter(
        student=student,
        teacher=test.teacher,
        is_paid=True
    ).exists()

    if not enrolled:
        return HttpResponse("يجب الاشتراك في هذه المادة أولاً.")

    # منع إعادة الاختبار
    if StudentResult.objects.filter(
        student=student,
        test=test
    ).exists():
        return HttpResponse("لقد قمت بحل هذا الاختبار من قبل.")

    score = None

    if request.method == "POST":

        score = 0

        for question in test.questions.all():

            answer_id = request.POST.get(
                f"question_{question.id}"
            )

            if answer_id:

                choice = Choice.objects.get(id=answer_id)

                if choice.is_correct:
                    score += question.mark

        StudentResult.objects.create(
            student=student,
            test=test,
            score=score
        )

    return render(
        request,
        "pages/take_test.html",
        {
            "test": test,
            "score": score,
        }
    )

def test_results(request, test_id):
    test = Test.objects.get(id=test_id)
    results = StudentResult.objects.filter(test=test).select_related("student")

    return render(request, "pages/show_test.html", {
        "test": test,
        "results": results,
    })


def reject_payment(request, payment_id):

    payment = Payment.objects.get(id=payment_id)

    payment.status = "Rejected"

    payment.save()

    return JsonResponse({
        "message": "Rejected"
    })

def block_student(request, student_id):
    student = User.objects.get(id=student_id)
    student.is_active = False
    student.save()
    print(student.is_active )
    return JsonResponse({
        "message": "Student Blocked"
    })


def unblock_student(request, id):
    student = User.objects.get(id=id)
    student.is_active = True
    student.save()
    print(student.is_active )
    return JsonResponse({
        "message": "Student Unblocked"
    })

def delete_teacher(request,teacher_id):

    teacher=User.objects.get(id=teacher_id)

    teacher.delete()

    return redirect("admin_dashboard")

def watch_video(request, lesson_id):

    student = User.objects.get(id=request.session["user_id"])
    lesson = get_object_or_404(Lesson, id=lesson_id)

    enrolled = Enrollment.objects.filter(
        student=student,
        teacher=lesson.teacher
    ).exists()

    if not enrolled:
        return HttpResponse("You are not allowed to watch this video")

    return render(request, "pages/watch_video.html", {
        "lesson": lesson,
        "student": student
    })

def renew_subscription(request, student_id):

    student = get_object_or_404(User, id=student_id)

    # لو الاشتراك انتهى
    if not student.subscription_end or student.subscription_end < timezone.now():

        student.subscription_end = timezone.now() + timedelta(days=30)

    else:
        # لو لسه شغال نزود شهر
        student.subscription_end += timedelta(days=30)

    student.is_paid = True
    student.save()

    return redirect("admin_dashboard")

def show_lessons(request):
    teacher_id = request.session.get("user_id")
    lessons = Lesson.objects.filter(teacher_id=teacher_id)
    return redirect("pages/teacher.html")

def delete_lesson(request, lesson_id):
    teacher_id = request.session.get("user_id")
    lesson = get_object_or_404(
        Lesson,
        id=lesson_id,
        teacher_id=teacher_id
    )

    if request.method == "POST":
        lesson.delete()
        return redirect("teacher")

    return render(request, "pages/confirm_lesson.html", {"lesson": lesson})



def edit_lesson(request, lesson_id):
    teacher_id = request.session.get("user_id")
    lesson = get_object_or_404(
        Lesson,
        id=lesson_id,
        teacher_id=teacher_id
    )

    if request.method == "POST":
        lesson.title = request.POST.get("title")
        lesson.description = request.POST.get("description")
        lesson.video_link = request.POST.get("video_link")
        lesson.level = request.POST.get("level")

        new_pdf = request.FILES.get("pdf_file")
        if new_pdf:
           lesson.pdf = new_pdf  
        lesson.save()# استخدمي اسم حقل الملف في الموديل لديك
        return redirect("teacher")

    return render(request, "pages/edit_lesson.html", {"lesson": lesson})

def remove_teacher(request, teacher_id):

    print("REMOVE VIEW CALLED")

    student = User.objects.get(
        id=request.session["user_id"]
    )

    print(student.id)
    print(teacher_id)

    Enrollment.objects.filter(
        student=student,
        teacher_id=teacher_id
    ).delete()

    return JsonResponse({
        "message": "Removed Successfully"
    })

   
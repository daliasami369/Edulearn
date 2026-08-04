from django.db import models
from django.utils import timezone
from datetime import timedelta

# Create your models here.
class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class User(models.Model):
    ROLE_CHOICES=[
        ('Teacher','Teacher'),
        ('Student' , 'Student'),
        ('Admin', 'Admin'),
    ]
    first_name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    image = models.ImageField(upload_to='users/', blank=True, null=True)
    level = models.CharField(max_length=100 , blank=True,null=True)
    address = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    role = models.CharField(max_length=20,choices=ROLE_CHOICES)
    is_paid = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    payment_date = models.DateTimeField(
    null=True,
    blank=True
    )

    subscription_end = models.DateTimeField(
    null=True,
    blank=True
    )
    subjects = models.ManyToManyField(
    Subject,
    blank=True,
    related_name="teachers"
)
    def __str__(self):
        return self.username
    
class Course(models.Model):
    name = models.CharField(max_length=100)

class Announcement(models.Model):
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="announcements"
    )
    level = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
class Lesson(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)

    description = models.TextField()

    level = models.CharField(max_length=50)
    
    video_link = models.TextField()

    pdf_file = models.FileField(
        upload_to="lesson_pdfs/",
        blank=True,
        null=True
    )

    link_type = models.CharField(  max_length=20,
        choices=[
            ("youtube", "YouTube"),
            ("drive", "Google Drive"),
            ("meet", "Google Meet"),
            ("zoom", "Zoom"),
        ]
    )
    created_at = models.DateTimeField(  auto_now_add=True ) 
   

class Message(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_messages"
    )

    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_messages"
    )

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

class Enrollment(models.Model):

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="enrollments"
    )

    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="students_enrolled"
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE
    )
    is_paid = models.BooleanField(default=False)

class Payment(models.Model):

    STATUS = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    ]

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    amount = models.IntegerField()

    receipt = models.ImageField(
        upload_to="receipts/",
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="Pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    is_seen = models.BooleanField(default=False)

class Test(models.Model):

    teacher = models.ForeignKey(User,on_delete=models.CASCADE)

    title = models.CharField(max_length=100)

    duration = models.IntegerField()
    level = models.CharField(max_length=100 , blank=True,null=True)
    total_marks = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

class Question(models.Model):

    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        related_name="questions"
    )

    question = models.TextField()

    mark = models.IntegerField(default=1)

class Choice(models.Model):

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="choices"
    )

    text = models.CharField(max_length=200)

    is_correct = models.BooleanField(default=False)

class StudentResult(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.IntegerField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    
class UserSession(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sessions"
    )

    session_key = models.CharField(max_length=200)

    ip_address = models.GenericIPAddressField()

    device = models.CharField(max_length=300)

    last_login = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.device}"
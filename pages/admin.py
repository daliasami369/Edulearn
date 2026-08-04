
from django.contrib import admin
from .models import Course, Announcement, Lesson,User,Enrollment,Choice,Test,Question,StudentResult,Subject,Message,Payment,UserSession

admin.site.register(Course)
admin.site.register(Announcement)
admin.site.register(User)
admin.site.register(Lesson)
admin.site.register(Enrollment)
admin.site.register(Test)
admin.site.register(Choice)
admin.site.register(Question)
admin.site.register(StudentResult)
admin.site.register(Subject)
admin.site.register(Message)
admin.site.register(Payment)
admin.site.register(UserSession)


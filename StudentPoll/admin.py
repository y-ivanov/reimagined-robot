from django.contrib import admin

# Register your models here.
from StudentPoll.models import Faculty, Group, Subject, StudyPlan, Teacher, Vote, Category, VoteCounter, VoteResult, \
    DeaneryResult



admin.site.register(Faculty)
admin.site.register(Category)
admin.site.register(Group)
admin.site.register(Subject)
admin.site.register(StudyPlan)
admin.site.register(Teacher)
admin.site.register(Vote)
admin.site.register(VoteCounter)
admin.site.register(VoteResult)
admin.site.register(DeaneryResult)
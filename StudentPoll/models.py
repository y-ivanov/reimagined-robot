from django.db import models
import datetime

# Create your models here.


class Faculty(models.Model):
    facultyName = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.facultyName


class Category(models.Model):
    categoryName = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.categoryName


class Vote(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    startYear = models.SmallIntegerField(default=datetime.datetime.now().year)
    endYear = models.SmallIntegerField(default=datetime.datetime.now().year+1)
    half = models.SmallIntegerField(choices={(1, '1'), (2, '2')}, default=1)
    isActive = models.BooleanField('Активувати', default=False)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return "{} : {}/{} : {} половина".format(self.faculty, self.startYear, self.endYear, self.half)

    class Meta:
        unique_together = ['faculty','startYear','endYear','half', ]


class Group(models.Model):
    groupName = models.CharField(max_length=100)
    year = models.PositiveIntegerField(default=0)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    amount = models.SmallIntegerField(default=0)
    # course = models.SmallIntegerField(default=1)

    def __str__(self):
        return "{} : {}".format(self.groupName, self.year)

    class Meta:
        unique_together = ['groupName','year','faculty']


class Subject(models.Model):
    subjectName = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.subjectName


class Teacher(models.Model):
    lName = models.CharField(max_length=50)
    fName = models.CharField(max_length=50)
    mName = models.CharField(max_length=50)
    subject = models.ManyToManyField(Subject)

    def __str__(self):
        return "{} {} {}".format(self.lName, self.fName, self.mName)

    class Meta:
        unique_together = ['lName','fName','mName']


class StudyPlan(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject)
    semester = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return "{0} : {2} : {1}".format(self.group, self.subject, self.semester)

    class Meta:
        unique_together = ['group','subject','semester']


class VoteCounter(models.Model):
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    course = models.PositiveSmallIntegerField(default=1)
    counter = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return '{} : {} : {} : {}'.format(self.vote, self.group, self.course, self.counter)

    class Meta:
        unique_together = ['vote','group','course']


class VoteResult(models.Model):
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    value = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return '{} : {} : {} : {} : {}'.format(self.vote, self.subject, self.teacher, self.category, self.value)


class DeaneryResult(models.Model):
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE)
    value = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return '{} : {}'.format(self.vote, self.value)
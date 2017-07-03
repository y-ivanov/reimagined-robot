from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import datetime
from collections import defaultdict
import os.path
from django.views import View
from django.urls import reverse
from . import functions


# Create your views here.
from .forms import SelectVoteForm, LoginForm, PollAdd, EditState, SelectStatisticsVoteForm
from StudentPoll.models import Faculty, Subject, Group, StudyPlan, Teacher, Category, Vote, VoteCounter, VoteResult,\
    DeaneryResult


class Index(View):
    def get(self, request):
        print('Index_View')
        form = SelectVoteForm(initial={'f1': Faculty.objects.values('facultyName')[:1]})
        return render(request, 'StudentPoll/index.html', {'form': form, })


class Statistics(View):
    def get(self, request):
        print('statsPageGET')
        form = SelectStatisticsVoteForm(initial={'f1': Faculty.objects.values('facultyName')[:1]})
        if 'vote' in request.GET.keys():
            # form = SelectStatisticsVoteForm()
            # print(request.GET.get('vote'))
            # print(Vote.objects.get(id=request.GET['vote']), '////////////')
            v = Vote.objects.get(id=request.GET.get('vote'))
            print(v)
            file = 'StudentPoll/templates/StudentPoll/results/{}.xml'.format(str(v).replace(' : ', '_').replace('/', '!'))
            stats = None
            # if os.path.isfile(file):
            if False:
                print('exists')
                stats = file
            else:
                print('doesn\'t exists')
                functions.create_statistics_file(file, v)
                file = 'StudentPoll/templates/StudentPoll/results/{}.xml'.format(str(v).replace(' : ', '_').replace('/', '!'))
            stats = functions.read_statistics_file(file)
            # for key, value in stats.items():
            #     for k in value:
            #         print(key, k[0], k[1], sep=':: ::')
            # print(v)

            # print(stats.items())
            #
            # 'stats': stats.items()
            return render(request, 'StudentPoll/statistics.html', {'form': form,  'stats': stats})
        else:
            return render(request, 'StudentPoll/statistics.html', {'form': form, })

    def post(self, request):
        print('StatisticsViewPost')
        values_to_pop = ['csrfmiddlewaretoken','vote', 'group', 'course']
        data = request.POST.copy()
        for key, value in data.items():
            print(key, value)
        # vs = VoteCounter()
        group = Group.objects.get(id=request.POST.get('group'))
        # print(group.amount)
        vote = Vote.objects.get(id=data.get('vote'))
        vc, created = VoteCounter.objects.get_or_create(vote=vote,
                                                        group_id=data.get('group'),
                                                        course=int(data.get('course')))
        if created:
            vc.counter = group.amount

        print(vc.counter)
        if vc.counter > 0:
            for key in values_to_pop:
                if key in data:
                    data.pop(key)

            for key, value in data.items():
                if key != 'Якість роботи':

                    vr = VoteResult(vote=vote,
                                    subject=Subject.objects.get(subjectName=key.split(':')[0]),
                                    teacher=Teacher.objects.get(lName=key.split(':')[1].split(' ')[0],
                                                                fName=key.split(':')[1].split(' ')[1],
                                                                mName=key.split(':')[1].split(' ')[2]),
                                    category=Category.objects.get(categoryName=key.split(':')[2]),
                                    value=value)
                    vr.save()
                else:
                    dr = DeaneryResult(vote=vote, value=value)
                    dr.save()

            vc.counter -= 1
            vc.save()
            return HttpResponseRedirect(reverse('StudentPoll:Statistics'))
        else:
            return HttpResponseRedirect(reverse('StudentPoll:Statistics'))


class Login(View):
    print('Login_View')
    form_class = LoginForm
    template_name = 'StudentPoll/login.html'
    def get(self, request):
        print('LoginGET')
        return render(request, self.template_name, {'form': self.form_class()} )

    def post(self, request):
        print('LoginPOST')
        form = self.form_class(request.POST)
        print(form)
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('StudentPoll:PollAdmin')
        # return HttpResponseRedirect(reverse('StudentPoll:Login'))
        return render(request, self.template_name, {'error': 'An error occurred try once more', 'form': self.form_class})


class PollAdmin(LoginRequiredMixin, View):
    print('Admin_View')
    login_url = '/login/'

    def get(self, request):
        pollAdd = PollAdd
        voteActivate = EditState
        # print(form.choices)
        return render(request, 'StudentPoll/PollAdmin.html', {'pollAdd': pollAdd, 'voteActivate': voteActivate})

    def post(self, request):
        return redirect('StudentPoll:index')


class Vote_View(View):
    print('Vote_View')
    """ takes subjects and teachers and creates a vote for each subject/teacher pair"""
    def post(self, request):
        print('lalalalalalal')
        tempDict = request.POST.copy()
        fac = tempDict['faculty']
        tempDict.pop('csrfmiddlewaretoken')
        print(tempDict)
        # print(request.POST.get('faculty').split(' : ')[1].split('/')[1])
        startYear = int(request.POST.get('faculty').split(' : ')[1].split('/')[1]) - int(request.POST.get('course'))
        groupInfo = {}
        print(request.POST.items())

        # groupInfo['vote'] = Faculty.objects.get(facultyName=request.POST.get('faculty').split(' : ')[0]).id
        groupInfo['vote'] = Vote.objects.get(faculty__facultyName=request.POST.get('faculty').split(' : ')[0],
                                             startYear=request.POST.get('faculty').split(' : ')[1].split('/')[0],
                                             endYear=request.POST.get('faculty').split(' : ')[1].split('/')[1],
                                             half=request.POST.get('faculty').split(' : ')[2].split(' ')[0]
                                             ).id
        groupInfo['group'] = Group.objects.get(groupName=request.POST.get('group'), year=startYear).id
        groupInfo['course'] = request.POST.get('course')
        tempDict.pop('faculty')
        tempDict.pop('group')
        tempDict.pop('course')

        categories = Category.objects.filter(vote__faculty__facultyName=fac.split(' : ')[0],
                                             vote__startYear=fac.split(' : ')[1].split('/')[0],
                                             vote__endYear=fac.split(' : ')[1].split('/')[1],
                                             vote__half=fac.split(' : ')[2].split(' ')[0])
        print(categories)
        return render(request, 'StudentPoll/vote.html', {'subjects': tempDict.items(),
                                                         'categories': categories,
                                                         'groupInfo': groupInfo,})
    def get(self, request):
        return HttpResponse('wtf. get away')


def logout_view(request):
    logout(request)
    return redirect('StudentPoll:index')


def filterGroups_view(request):
    """ filters groups depending on "Vote" selection wich has "Faculty" in it
    @:return returns list of groups according to faculty"""
    if request.method == 'GET':
        groups = Group.objects.filter(faculty__facultyName=request.GET.get('faculty')).order_by('groupName')
        gDcit = []
        print(groups)
        for g in groups:
            if not gDcit.__contains__(g.groupName):
                gDcit.append(g.groupName)
        print(gDcit)
        if request.is_ajax():
            return JsonResponse(gDcit, safe=False)


def getSubjects_view(request):
    if request.method == 'GET':
        startYear = int(request.GET.get('year'))-int(request.GET.get('course'))
        group = Group.objects.values_list('groupName').filter(groupName=request.GET.get('group'),year=startYear)
        numberToSubstract = 0
        if request.GET.get('half') == '1':
            numberToSubstract = 1
        sem = ((int(request.GET.get('year')) - startYear) * 2) - numberToSubstract
        print(group, startYear, sem)
        print('sem {}'.format(sem))
        # DELETE THESE LINES
        # THE ARE FOR DEBUG PURPOSES
        # sem = 8 #DELETE LATER
        # UP TO HERE
        if sem != 0:
            print(4)
            subjects = StudyPlan.objects.values_list('subject__subjectName', flat=True).filter(semester=sem,
                                                                                group__groupName=request.GET.get('group'))
            try:
                if subjects[0] != '':
                    print(subjects[0])
            except IndexError:
                print('empty')
                return JsonResponse('error', safe=False)
            print(subjects)
            subjectTeacher = defaultdict(list)
            for subj in subjects:
                teachers = Teacher.objects.values_list('lName','fName','mName').filter(subject__subjectName=subj)
                for teacher in teachers:
                    subjectTeacher[subj].append(teacher)
            print(subjectTeacher)
            if request.is_ajax():
                return JsonResponse(subjectTeacher)


def pollAdd_view(request):
    print('pollAdd_View')
    if request.method == 'POST':
        print('faculty', request.POST.get('faculty'))
        print('startyear', request.POST.get('year').split('/')[0])
        print('endYear', int(request.POST.get('year').split('/')[1]))
        print('half', request.POST.get('half'))
        print('categories', request.POST.getlist('categories'))
        print(bool(request.POST.get('isActive')))

        v, created = Vote.objects.get_or_create(faculty_id=request.POST.get('faculty'),
                                                startYear=int(request.POST.get('year').split('/')[0]),
                                                endYear=int(request.POST.get('year').split('/')[1]),
                                                half=int(request.POST.get('half')))
        print(v)
        if created:
            print('created')
            v.isActive=bool(request.POST.get('isActive'))
            for i in request.POST.getlist('categories'):
                v.categories.add(int(i))
            v.save()
        else:
            print('exists')
        # print(v.categories)

        print(v.categories.all())
        return redirect('StudentPoll:PollAdmin')


def categoryAdd_view(request):
    print('categoryAdd_View')
    if request.method == 'POST':
        cat = Category(categoryName=request.POST.get('category'))
        cat.save()
        return redirect('StudentPoll:PollAdmin')


def editState_view(request):
    if request.method == 'POST':
        for key, value in request.POST.items():
            print(key, value)
        vote = Vote.objects.get(id=int(request.POST.get('vote')))
        print(vote)
        print(request.POST.get('activate'))
        if request.POST.get('activate') == 'True':
            vote.isActive = True
        else:
            vote.isActive = False
        vote.save()
        return redirect('StudentPoll:PollAdmin')
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from .models import Problem, Solution

import os, filecmp

# Create your views here.

def register(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('judge/login.html')
        
    context={'form': form}
    return render(request,'judge/register.html',context)

def loginPage(request):
    if request.method == 'POST':
        username= request.POST.get('username')
        password= request.POST.get('password') 
        
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('judge:problems')
    context={}
    return render(request, 'judge/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('judge:login')

@login_required(login_url='judge:login')
def problems(request):
    problems_list = Problem.objects.all()
    context = {'problems_list': problems_list}
    return render(request, 'judge/index.html',context)

@login_required(login_url='judge:login')
def problemDetail(request,problem_id):
    problem = get_object_or_404(Problem, pk = problem_id) 
    return render(request, 'judge/detail.html', {'problem': problem})

@login_required(login_url='judge:login')
def submitProblem(request, problem_id):
    f = request.FILES['solfile']
    pk=problem_id

    with open('C:/Users/ANSHIKA/files/solution.cpp', 'wb+') as dest:
        for chunk in f.chunks():
            dest.write(chunk)

    os.system('g++ C:/Users/ANSHIKA/files/solution.cpp')
    os.system('a.exe '+ f'< C:/Users/ANSHIKA/files/input{pk}.txt > '+ f'C:/Users/ANSHIKA/files/output{pk}.txt') 

    out1 = f'C:/Users/ANSHIKA/files/output{pk}.txt'
    out2 = f'C:/Users/ANSHIKA/files/act_output{pk}.txt'
    if(filecmp.cmp(out1,out2,shallow='False')):
        verdict = 'Accepted'
    else:
        verdict = 'Wrong Answer'
    print(verdict)

    solution = Solution()
    solution.problem = Problem.objects.get(pk = problem_id)
    solution.verdict = verdict
    solution.submitted_at = timezone.now()
    solution.submitted_code =  'C:/Users/ANSHIKA/files/solution.cpp'
    solution.save()

    return HttpResponseRedirect(reverse('judge:leaderboard'))

@login_required(login_url='judge:login')
def leaderboard(request):
    solutions = Solution.objects.order_by('-submitted_at')[:100]
    return render(request, 'judge/leaderboard.html',{'solutions': solutions})
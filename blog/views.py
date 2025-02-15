import random 

from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from .forms import signup_form, login_form, Add_post
from django.contrib.auth import authenticate, login , logout
from django.contrib import messages
from .models import Post
from django.contrib.auth.models import Group
from django.utils import timezone
from django.db.models import Q
from .utils import summarizer,text_to_speech
from django.contrib.auth.models import User


# Create your views here.
def home(request):
    query = ''
    # pid = request.GET.get('pid', None)
    # if pid is not None:
    #     pid = int(pid)
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET.get('query')
        print(query)
        # blog = Post.objects.filter(Q(title__icontains=query) | Q(desc__icontains=query))
        blog = Post.objects.filter(title__icontains=query)
    # elif request.method == 'GET' and 'pid' in request.GET:
    #     pid = request.GET.get('pid')
    #     print(pid)
    #     blog = Post.objects.all()
    #     return render(request,'blog/home.html',{'data':blog ,'pid':pid}) 
    else:
        blog = Post.objects.all()
    # print(pid)    
    return render(request,'blog/home.html',{'data':blog,'query':query})
    # return render(request,'blog/home.html',{'data':blog,'pid':pid,'query':query})

def summarize_page(request,pid):
    query = ''
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET.get('query')
        print(query)
        # blog = Post.objects.filter(Q(title__icontains=query) | Q(desc__icontains=query))
        blog = Post.objects.filter(title__icontains=query)
    else:
        blog = Post.objects.all()
    return render(request,'blog/home.html',{'data':blog,'pid':pid,'query':query})

def search(request):
    query = ''
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET.get('query')
        print(query)
        # blog = Post.objects.filter(Q(title__icontains=query) | Q(desc__icontains=query))
        blog = Post.objects.filter(title__icontains=query)
    else:
        blog = Post.objects.all()
    return render(request,'blog/home.html',{'data':blog,'query':query})


def about(request):
    return render(request,'blog/about.html')


def dashboard(request):
    if request.user.is_authenticated:
        user = request.user
        full_name = user.get_full_name()
        user = request.user

        if user.groups.filter(name='Author').exists():
            blog = Post.objects.filter(username = user.username)    
        else: 
            blog = Post.objects.all()
        gps = user.groups.all()
        all_user = User.objects.all()
        print(all_user.count())
        for g in gps:
            print(g)
        return render(request,'blog/dashboard.html',{'data':blog,'full_name':full_name,'groups':gps,'aluser':all_user})
    else:
        return HttpResponseRedirect('/login/')


def user_signup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            fm = signup_form(request.POST)
            if fm.is_valid():
                user = fm.save()
                group = Group.objects.get(name='Author')
                user.groups.add(group)
                return HttpResponseRedirect('/dashboard/')
        else:
            fm = signup_form()        
    else:
        return HttpResponseRedirect('/dashboard/')        
    return render(request,'blog/signup.html',{'form':fm})

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            fm = login_form(data = request.POST,request= request)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                key = authenticate(username=uname,password=upass)
                if key is not None:
                    login(request, key)
                    return HttpResponseRedirect('/dashboard/')
        else:
            fm = login_form(request)
        return render(request,'blog/login.html',{'form':fm})
    else:
        return HttpResponseRedirect('/dashboard/')

def user_logout(request):
    logout(request)
    return redirect('/')

def addpost(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = Add_post(request.POST)
            if fm.is_valid():
                tit = fm.cleaned_data['title']
                des = fm.cleaned_data['desc']
                sum = summarizer(des)
                user = request.user.username
                fname = request.user.get_full_name()
                data = Post(title=tit,desc=des,username=user,full_name=fname,summ=sum)
                data.save()
                fm = Add_post()   
                messages.success(request,'Succesfully Post')
        else:
            fm = Add_post()        
        return render(request,'blog/addpost.html',{'form':fm})
    else:
        return HttpResponseRedirect('/home/')

def updatepost(request, id):
    if request.user.is_authenticated:
        temp = Post.objects.get(pk=id)
        if request.method == 'POST':
            fm = Add_post(request.POST,instance=temp)
            if fm.is_valid():
                tit = fm.cleaned_data['title']
                des = fm.cleaned_data['desc']
                sum = summarizer(des)
                user = request.user.username
                fname = request.user.get_full_name()
                dat = timezone.now()
                data = Post(id=id,title=tit,desc=des,username=user,full_name=fname,date=dat,summ=sum)
                data.save()
                return HttpResponseRedirect('/dashboard/')
        else:
            fm = Add_post(instance=temp)
        return render(request,'blog/editpost.html',{'form':fm})     
    else:
        return HttpResponseRedirect('/home/')
        
    
def deletepost(request,id):
    if request.user.is_authenticated:
        temp = Post.objects.get(pk=id)
        temp.delete()
        return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/home/')

def expandpost(request,id):
    temp = Post.objects.get(pk=id)
    paras = temp.desc.split("\n")
    return render(request, 'blog/expand.html',{'data':temp,'para':paras})
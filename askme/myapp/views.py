from django.shortcuts import render , get_object_or_404 , Http404
from .models import Question , Profile , Comment , Replies
from .forms import *
from django.contrib.auth import authenticate ,logout ,login
from django.http import HttpResponse , HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

def ques_feed(request):

    ques = Question.objects.all().order_by('-id')
    context = {
        'ques' : ques
    }

    return render(request , 'ques_feed.html' , context = context)


def ques_detail(request,id):

    ques = get_object_or_404(Question,id=id)

    replies = Replies.objects.all().filter(ques = ques).order_by('-id')

    comments =  Comment.objects.all().filter(ques = ques).order_by('-id')

    if request.method == 'POST':

        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('askme:user_login'))

        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            cmnt = comment_form.save(commit=False)
            cmnt.user = request.user
            cmnt.ques = ques
            cmnt.save()
            return HttpResponseRedirect(reverse('askme:ques_detail',args = (id,)))
    else:
        comment_form  = CommentForm()

    context = {
        'q': ques,
        'comments' : comments,
        'comment_form' : comment_form ,
        'replies' : replies,
    }

    return render(request, 'ques_detail.html', context=context)

@login_required
def like_comment(request,id,comment_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('askme:user_login'))
    
    ques = get_object_or_404(Question,id=id)
    comment = get_object_or_404(Comment,id=comment_id)
    
    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)
    
    return HttpResponseRedirect(reverse('askme:ques_detail', args=[id,]))


def comment_reply(request,id):

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('askme:user_login'))

    text = request.POST.get('text')

    if len(text)==0:
        messages.success(request,'TextField is empty')
        return HttpResponseRedirect(reverse('askme:ques_detail', args=(id,)))

    ques = get_object_or_404(Question, id=id)

    comment_id = request.POST.get('comment_id')
    comment = Comment.objects.filter(id=comment_id).first()
    Replies.objects.create(ques = ques,comment=comment,user = request.user,content =text)

    return HttpResponseRedirect(reverse('askme:ques_detail',args=(id,)))



def user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('askme:ques_feed'))

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username,password=password)

            if user:

                if user.is_active:
                    login(request,user)
                    return HttpResponseRedirect(reverse('askme:ques_feed'))
                else:
                    return HttpResponse('User is not Active')
            else:
                return HttpResponse('User Not Available')
    else:
        form = LoginForm()

    context = {
        'form' : form
    }

    return render(request ,'login.html' ,context )



@login_required()
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('askme:ques_feed'))


def register(request):

    if request.user.is_authenticated:
        return HttpResponse('First logout')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Profile.objects.create(user = user)
            return HttpResponseRedirect(reverse('askme:user_login'))
    else:
        form = UserRegistrationForm()

    context = {
        'form' : form
    }

    return render(request , 'register.html',context)



def profilepage(request,username):
    user = User.objects.get(username=username)
    questions = Question.objects.filter(author=user)
    profile = Profile.objects.all()
    context = {
        'questions': questions,
        'profile' : profile,
        'user':user,
    }

    return render(request,'profile.html',context)



@login_required()
def ask_question(request):

    if request.method == 'POST':
        form = QuestionAskForm(request.POST)

        if form.is_valid():
            ques = form.save(commit=False)
            ques.author = request.user
            ques.save()

            return HttpResponseRedirect(reverse('askme:ques_feed'))
    else:
        form = QuestionAskForm()

    context = {
        'form' : form
    }

    return render(request , 'ask_a_ques.html',context)


def delete_comment(request,id):

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('askme:user_login'))

    cmnt_id = request.POST.get('comment_id')
    cmnt = get_object_or_404(Comment,id=cmnt_id)

    if cmnt.user != request.user:
        return Http404()
    cmnt.delete()
    return HttpResponseRedirect(reverse('askme:ques_detail', args=(id,)))



def delete_reply(request, id):

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('askme:user_login'))

    reply_id = request.POST.get('reply_id')
    reply = get_object_or_404(Replies, id=reply_id)

    if reply.user != request.user:
        return Http404()
    reply.delete()
    return HttpResponseRedirect(reverse('askme:ques_detail', args=(id,)))



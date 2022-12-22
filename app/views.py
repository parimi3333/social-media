from django.shortcuts import render,redirect
from .models import *
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
# Create your views here.
@login_required(login_url='signinpage')
def home(request):
    c_u = request.user
    messages.info(request,c_u)
    data = Post.objects.all()
    return render(request,'home.html',{'d':data})
@login_required(login_url='signinpage')
def userprofile(request):
    c_u = request.user
    data = Post.objects.filter(user=c_u)
    data2 = profile.objects.filter(user=c_u)
    return render(request,'profile.html',{'d':data,'d2':data2})
@login_required(login_url='signinpage')
def upload_data(request):
    return render(request,'upload_data.html')
@login_required(login_url='signinpage')
def upload(requset):
    if requset.method == 'POST':
        user = requset.user.username
        image = requset.FILES.get('image')
        caption = requset.POST['cap']
        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()
        data = Post.objects.all()
        return render(requset,'home.html',{'d':data})
    else:
        data = Post.objects.all()
        return render(requset,'home.html',{'d':data})

@login_required(login_url='signinpage')
def like_post(request):
        id = request.POST['img_id']
        user = request.user.username
        likes = Post.objects.get(id=id)
        like = LikePost.objects.filter(username=user)&LikePost.objects.filter(post_id=id)
        print(like)
        if like.exists():
            d=LikePost.objects.filter(username=user)&LikePost.objects.filter(post_id=id)
            d.delete()
            likes.no_of_likes=likes.no_of_likes-1
            likes.save()
            return redirect('/')

        else:
            d = LikePost.objects.create(username=user, post_id=id)
            d.save()
            likes.no_of_likes = likes.no_of_likes+1
            likes.save()
            return redirect('/')
@login_required(login_url='signinpage')
def user_profile(request):
    username = request.POST['user']
    followers = request.user.username
    profileuser = User.objects.get(username=username)
    pr = profile.objects.filter(user=profileuser)
    postuser =Post.objects.filter(user=username)
    f = len(FollowersCount.objects.filter(user=username))
    m = FollowersCount.objects.filter(user=username)&FollowersCount.objects.filter(follower=followers)
    if m.exists():
        messages.info(request,f)
        return render(request,'userprofile.html',{'d':pr,'d2':postuser,'d3':'unfollow'})
    else:
        messages.info(request,f)
        return render(request,'userprofile.html',{'d':pr,'d2':postuser,"d3":"follow"})


@login_required(login_url='signinpage')
def changepr(request):
    return render(request,'change.html')
def change(request):
    image = request.FILES.get('image')
    c_u = request.user
    pr = profile.objects.get(user=c_u)
    pr.profileimg = image
    pr.save()
    data = Post.objects.filter(user=c_u)
    data2 = profile.objects.filter(user=c_u)
    return render(request,'profile.html',{'d':data,'d2':data2})
@login_required(login_url='signinpage')
def follow(request):
    username = request.POST['user']
    c_u = request.user.username
    z = FollowersCount.objects.filter(follower=c_u)&FollowersCount.objects.filter(user=username)
    if z.exists():
        f = FollowersCount.objects.filter(follower=c_u)&FollowersCount.objects.filter(user=username)
        f.delete()
        profileuser = User.objects.get(username=username)
        pr = profile.objects.filter(user=profileuser)
        postuser = Post.objects.filter(user=username)
        f = len(FollowersCount.objects.filter(user=username))
        if f==0:
            f=0
            messages.info(request,f)
        else:
            f-=1
            messages.info(request,f)
        return render(request, 'userprofile.html', {'d': pr, 'd2': postuser,'d3':"follow"})
    else:
           f = FollowersCount.objects.create(follower=c_u,user=username)
           f.save()
           profileuser = User.objects.get(username=username)
           pr = profile.objects.filter(user=profileuser)
           postuser = Post.objects.filter(user=username)
           f = len(FollowersCount.objects.filter(user=username))
           messages.info(request,f)
           return render(request, 'userprofile.html', {'d': pr, 'd2': postuser,'d3':"unfollow"})
def signuppage(request):
    return render(request,'signup.html')
def signupdata(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(email=email).exists():
            messages.info(request,'email already taken')
            return render(request,'signup.html')
        elif User.objects.filter(username=username).exists():
            messages.info(request,'username already taken')
            return render(request,'signup.html')
        else:
            user = User.objects.create_user(username=username,email=email,password=password)
            user.save()
            new_model=auth.authenticate(username=username,password=password)
            if new_model is not None:
                login(request,new_model)
                get_user = User.objects.get(username=username)
                copy_data = profile.objects.create(user=get_user, id_user=get_user.id)
                copy_data.save()
                messages.info(request,username)
                data = Post.objects.all()
                return render(request,'home.html',{'d':data})
            else:
                return HttpResponse('profile not created')
def signindata(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            messages.info(request,username)
            data = Post.objects.all()
            return render(request,'home.html',{'d':data})
        else:
            messages.info(request,'invalid credintials')
            return render(request,'signin.html')
def signpage(request):
    return render(request,'signin.html')
def logoutdata(request):
    auth.logout(request)
    return render(request,'signin.html')
def dummy(request):
    user = request.user.username
    data = LikePost.objects.values('post_id')
    for i in data:
        data2 = LikePost.objects.filter(username=user)

    return render(request,'dummy.html',{'d':data2})
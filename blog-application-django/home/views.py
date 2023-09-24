from django.template import loader
import random
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth  import authenticate,  login, logout
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, BlogPostForm, LikeUnlikeForm
from django.views.generic import UpdateView
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

def adminlogin(request):
    msg=""
    if request.method=="POST":
        uname = request.POST.get('username')
        pwd =request.POST.get('password')
        if(uname=="admin" and pwd=="admin123"):
            return render(request, "adminmainpage.html")
        else:
            msg="Invalid UserName/Password"
    return render(request, "adminlogin.html", {'msg':msg})

def adminmainpage(request):
    return render(request, "adminmainpage.html")

def adminviewusers(request):
    posts = User.objects.all()
    return render(request, "adminviewusers.html",{'posts': posts})

def adminviewblogs(request):
    posts = BlogPost.objects.all()
    posts = BlogPost.objects.filter().order_by('-dateTime')
    return render(request, "adminviewblogs.html", {'posts': posts})

def adminviewlikes_unlikes(request):
    posts = LikeUnlike.objects.all()
    return render(request, "adminviewlikes_unlikes.html",{'posts': posts})

def adminaccept_rejectblogs(request):
    posts = BlogPost.objects.filter().order_by('-dateTime')
    return render(request, "adminaccept_rejectblogs.html", {'posts': posts})

def accept_rejectblogs(request, id, status):
    print("Blog Id       : ", id)
    print("Status Value  : ", status)
    BlogPost.objects.filter(id=id).update(status=status)
    print("Status Updated Success")
    posts = BlogPost.objects.filter().order_by('-dateTime')
    return render(request, "adminaccept_rejectblogs.html", {'posts': posts})

def blogs(request):
    posts = BlogPost.objects.all()
    posts = BlogPost.objects.filter(status='Accepted').order_by('-dateTime')
    return render(request, "blog.html", {'posts':posts})

def like_dislike(request, post_id, is_like):
    print("Like Dislike Post : ", post_id)
    print("True/False Value  : ", is_like)
    id = request.session['id']
    form = LikeUnlike.objects.create(user_id=id, post_id=post_id, is_like=is_like)
    print("Like Unlike Data Saved Success")
    form.save()
    return redirect("/")

def blogs_comments(request, slug, post_id):
    print("Post Id : ", post_id)
    request.session['post_id']=post_id
    like_unlike = LikeUnlike.objects.filter(post_id=post_id).values()
    #print("Like Unlike : ", like_unlike)

    like_count=0
    unlike_count=0
    for data in like_unlike:
        #print("Data : ", data)
        if(data['is_like']=="true"):
            like_count+=1
        else:
            unlike_count += 1

    post = BlogPost.objects.filter(slug=slug).first()
    comments = Comment.objects.filter(blog=post)
    if request.method=="POST":
        user = request.user
        content = request.POST.get('content','')
        blog_id =request.POST.get('blog_id','')
        comment = Comment(user = user, content = content, blog=post)
        comment.save()
    return render(request, "blog_comments.html", {'post':post, 'comments':comments,
                                                  'like_count':like_count,
                                                  'unlike_count':unlike_count})

def Delete_Blog_Post(request, slug):
    posts = BlogPost.objects.get(slug=slug)
    if request.method == "POST":
        posts.delete()
        return redirect('/')
    return render(request, 'delete_blog_post.html', {'posts':posts})

def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        blogs = BlogPost.objects.filter(title__contains=searched)
        return render(request, "search.html", {'searched':searched, 'blogs':blogs})
    else:
        return render(request, "search.html", {})

@login_required(login_url = '/login')
def add_blogs(request):
    if request.method=="POST":
        form = BlogPostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            blogpost = form.save(commit=False)
            blogpost.author = request.user
            blogpost.save()
            obj = form.instance
            alert = True
            return render(request, "add_blogs.html",{'obj':obj, 'alert':alert})
    else:
        form=BlogPostForm()
    return render(request, "add_blogs.html", {'form':form})

class UpdatePostView(UpdateView):
    model = BlogPost
    template_name = 'edit_blog_post.html'
    fields = ['title', 'slug', 'content', 'image']


def user_profile(request, myid):
    #id = request.session['id']
    print("User Id : ", myid)
    posts = User.objects.filter(id=myid)
    profile = Profile.objects.filter(user_id=myid)
    #post = BlogPost.objects.filter(id=myid)
    print("Posts : ", posts)
    print("Profile : ", profile)
    post=posts[0]
    profiledata={}
    if(profile):
        profiledata = profile[0]
    print("First Name : ", post.first_name, " Email : ", post.email)    
    return render(request, "user_profile.html", {'post':post, 'profiledata':profiledata})

def UserProfile(request):
    first_name = request.session['firstname']
    last_name = request.session['lastname']
    email=request.session['email']
    id=request.session['id']
    uname = request.session['username']
    print("User Id : ", id)
    posts = User.objects.filter(id=id)
    profile = Profile.objects.filter(user_id=id)
    # post = BlogPost.objects.filter(id=myid)
    post = posts[0]
    profiledata={}
    if(profile):
        profiledata = profile[0]
    return render(request, "profile.html",
                  {'id':id, 'first_name':first_name, 'last_name':last_name, 'email':email, 'id':id,
                   'user':uname, 'post':post, 'profiledata':profiledata})

def edit_profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)
    if request.method=="POST":
        form = ProfileForm(data=request.POST, files=request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            alert = True
            return render(request, "edit_profile.html", {'alert':alert})
    else:
        form=ProfileForm(instance=profile)
    return render(request, "edit_profile.html", {'form':form})


def Register(request):
    if request.method=="POST":   
        username = request.POST['username']
        email = request.POST['email']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('/register')
        
        user = User.objects.create_user(username, email, password1)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return render(request, 'login.html',{'info':'Registered Successfully'})   
    return render(request, "register.html")

def Login(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        #print("User : ", user.id, " First Name : ", user.first_name, " Last Name : ", user.last_name, " Email Id : ", user.email)
        if user is not None:
            request.session['firstname'] = user.first_name
            request.session['lastname'] = user.last_name
            request.session['email'] = user.email
            request.session['id'] = user.id
            request.session['username'] = username
            print("First Name : ",request.session['firstname'])
            login(request, user)
            messages.success(request, "Successfully logged in")
            return redirect("/")
        else:
            mydata = User.objects.all()
            flag=False
            for data in mydata:
                if (data.username == username and data.password == password):
                    flag = True
                    print("User Id : ", data.id)
                    request.session['userid'] = data.id
                    break
            if(flag):
                request.session['firstname'] = data.first_name
                request.session['lastname'] = data.last_name
                request.session['email'] = data.email
                request.session['id'] = data.id
                request.session['username'] = username
                print("First Name : ", request.session['firstname'])
                login(request, data)
                messages.success(request, "Successfully logged in")
                return redirect("/")
            messages.error(request, "Invalid Credentials")
        """
        mydata = NewUser.objects.all()
        for data in mydata:
            if (data.username == uname and data.password == pwd):
                userid = data.id
                firstname = data.firstname
                lastname = data.lastname
                phonenumber = data.phonenumber
                emailid = data.emailid
                request.session['userid'] = userid
                request.session['firstname'] = firstname
                request.session['lastname'] = lastname
                request.session['phonenumber'] = phonenumber
                request.session['emailid'] = emailid
                flag = True
                break
        if (flag == True):
            template = loader.get_template('newapp/usermainpage.html')
            context = {'data': mydata}
        else:
            template = loader.get_template('newapp/userlogin.html')
            context = {'data': mydata}
        """
    return render(request, "login.html")


def Logout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/login')



def passwordchangepage(request):
    print("Password Change Page")
    if request.method == 'POST':
        uname = request.POST.get('uname')
        pwd = request.POST.get('pwd')
        userid=request.session['userid']
        User.objects.filter(id=userid).update(password=pwd)
        print("Password Updated Success")
        return render(request, 'login.html', {'msg': 'Password Updated Success'})
    return render(request, 'login.html', {'msg': 'Password Not Updated'})

def userforgotpassword(request):
    flag = False
    if request.method == 'POST':
        uname = request.POST.get('username')
        toemail = request.POST.get('toemail')
        print("User Name : ", uname, " EmailId : ", toemail)
        mydata = User.objects.all()
        for data in mydata:
            if (data.username == uname and data.email == toemail):
                flag = True
                print("User Id : ", data.id)
                request.session['userid'] = data.id
                break
        if (flag == True):
            otp = random.randint(1000, 9999)
            print("OTP : ", otp)
            request.session['toemail'] = toemail
            request.session['uname'] = uname
            request.session['otp'] = otp
            print("User Id : ", request.session['userid'])
            return render(request, "generateotp.html", {'uname': uname, 'toemail': toemail, 'otp': otp,
                      'redirecturl': 'http://127.0.0.1:8000/enterotppage/'})
        else:
            context = {'msg': 'Invalid UserName/EmailId'}
            template = loader.get_template('userforgotpassword.html')
    else:
        template = loader.get_template('userforgotpassword.html')
        context = {'msg': ''}
    return HttpResponse(template.render(context, request))

def generateotppage(request):
    return render(request, "generateotp.html", {'uname': 'uname', 'toemail': 'toemail', 'otp': 'otp',
                                               'redirecturl': 'http://127.0.0.1:8000/userlogin/'})

def enterotppage(request):
    if request.method == 'POST':
        storedotp=request.session['otp']
        enteredotp = request.POST.get('otp')
        print("Entered OTP : ", enteredotp, " Stored OTP : ", storedotp)
        template = loader.get_template('passwordchangepage.html')
        if(int(storedotp)==int(enteredotp)):
            context = {'msg': ''}
            return HttpResponse(template.render(context, request))
        else:
            context = {'msg': ''}
            return render(request, "enterotppage.html",{'msg': 'Incorrect OTP'})
    return render(request, "enterotppage.html",{'msg': ''})
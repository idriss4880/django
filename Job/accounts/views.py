from django.shortcuts import redirect, render
from .forms import SignupForm , UserForm , ProfileForm
from django.contrib.auth import authenticate, login
from .models import Profile
from django.urls import reverse
from job.models import *
from .decorators import notLoggedU, allowedUser
from django.contrib.auth.models import Group

# Create your views here.


def signup(request):
    if request.method=="POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username,password=password)
            group = Group.objects.get(name="customers")
            user.groups.add(group)
            login(request,user)
            return redirect('/accounts/profile')
    else:
        form = SignupForm()
    return render(request,'registration/signup.html',{'form':form})




def profile(request):
    profile = Profile.objects.get(user=request.user)
    return render(request,'accounts/profile.html',{'profile': profile})



def profile_edit(request):
    profile = Profile.objects.get(user=request.user)

    if request.method=='POST':
        userform = UserForm(request.POST,instance=request.user)
        profileform = ProfileForm(request.POST,request.FILES,instance=profile )
        if userform.is_valid() and profileform.is_valid():
            userform.save()
            myprofile = profileform.save(commit=False)
            myprofile.user = request.user
            myprofile.save()
            return redirect(reverse('accounts:profile'))

    else :
        userform = UserForm(instance=request.user)
        profileform = ProfileForm(instance=profile)

    return render(request,'accounts/profile_edit.html',{'userform':userform , 'profileform':profileform})

@allowedUser(allowedGroups=['admins'])
def mypannel(request):
    mypannel = Profile.objects.all()
    myproduct = Job.objects.all()
    context = {'mypannel': mypannel,'myproduct':myproduct}
    return render(request,'accounts/mypannel.html',context)
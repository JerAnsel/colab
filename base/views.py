from urllib import request
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Message, Room, Project, Topic, UploadImage
from .forms import ProjectForm, UserImage, UserForm, ProfileForm

# Create your views here.

# rooms = [
#     {'id': 1, 'name': "Let's learn Python"},
#     {'id': 2, 'name': "Design with me"},
#     {'id': 3, 'name': "Frontend developers"},
# ]

def loginPage(request):

    page = 'login'
    user_form = UserForm()
    topics = Topic.objects.all()

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
    
        try:
            User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
    
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exist')

    context = {'page': page, 'topics': topics, 'user_form': user_form}
    return render(request, 'base/login_register.html', context)
    
def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):

    if request.user.is_authenticated:
        return redirect('home')

    user_form = UserForm()
    #profile_form = ProfileForm()
    topics = Topic.objects.all()

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        # profile_form = ProfileForm(request.POST)
        if user_form.is_valid(): #and profile_form.is_valid()
            user = user_form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')

            # Code to render home page after register.
            # q = request.GET.get('q') if request.GET.get('q') != None else ''

            # rooms = Room.objects.filter(
            # Q(topic__name__icontains=q) |
            # Q(name__icontains=q) |
            # Q(description__icontains=q) 
            # )
            # topics = Topic.objects.all()
            # room_count = rooms.count()

            # context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'registered': True}

            # return render(request, 'base/home.html', context)
        else:
            messages.error(request, 'An error occured during registration')

    return render(request, 'base/login_register.html', {'user_form': user_form, 'topics': topics})

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    projects = Project.objects.filter(
       Q(topic__name__icontains=q) |
       Q(name__icontains=q) |
       Q(description__icontains=q) 
    )
    topics = Topic.objects.all()
    project_count = projects.count()

    context = {'projects': projects, 'topics': topics, 'project_count': project_count}
    return render(request, 'base/home.html', context)

def project(request, pk):
    topics = Topic.objects.all()
    
    project = Project.objects.get(id=pk)

    if request.method == 'POST':
        project.members.add(request.user)

    members = project.members.all()
    is_member = request.user in members

    context = {'project': project,
               'topics': topics, 
               'members': project.members.all(),
               'is_member': is_member}
               
    return render(request, 'base/project.html', context)

def room(request, pk, public):
    topics = Topic.objects.all()
    
    project = Project.objects.get(id=pk)

    if public == 'private' and request.user not in project.members.all():
        return HttpResponse('Only project members can enter the Conference room.')


    project_rooms = Room.objects.filter(room_project=project)

    if project_rooms[0].private:
        private_room = project_rooms[0]
        public_room = project_rooms[1]
    else:
        private_room = project_rooms[1]
        public_room = project_rooms[0]

    room = private_room if not (public == 'public') else public_room

    room_messages = room.message_set.all().order_by('-created')

    participants = room.participants.all()

    if request.method == 'POST':

        if 'create_message_form' in request.POST:
            Message.objects.create(
                user=request.user,
                room=room,
                body=request.POST.get('body')
            )
            room.participants.add(request.user)
            return redirect('room', pk=project.id, public=public)

        elif 'edit_form' in request.POST:
            message = Message.objects.get(
                    id=request.POST.get('mid'),
                )
            message.body = request.POST.get('body')
            message.save()
            return redirect('room', pk=project.id, public=public)
        
        elif 'delete_message' in request.POST:
            message = Message.objects.get(
                    id=request.POST.get('mid'),
                )
            message.delete()
            return redirect('room', pk=project.id, public=public)

    context = {'project': project,
               'room': room,
               'room_messages': room_messages, 
               'participants': participants, 
               'topics': topics}

    return render(request, 'base/room.html', context)

@login_required(login_url='/login')
def createProject(request):
    topics = Topic.objects.all()
    form = ProjectForm()
    update = False

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            new_project = form.save(commit=False)
            new_project.host = request.user
            new_project.save()
            new_project.members.add(request.user)
            new_project.save()

            # Create public and private rooms
            public_room = Room(private=False, room_project=new_project)
            private_room = Room(private=True, room_project=new_project)
            public_room.save()
            private_room.save()
            return redirect('home')

    context = {'topics': topics, 'form': form, 'update': update}
    return render(request, 'base/project_form.html', context)

@login_required(login_url='/login')
def updateProject(request, pk):
    project = Project.objects.get(id=pk)
    form = ProjectForm(instance=project)
    topics = Topic.objects.all()

    update = True

    if request.user != project.host:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        if 'delete_project' in request.POST:
            project.delete()
            return redirect('home')


        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'topics': topics, 'form': form, 'update': update}
    return render(request, 'base/project_form.html', context)

# @login_required(login_url='/login')
# def deleteRoom(request, pk):
#     room = Room.objects.get(id=pk)
    
#     if request.user != room.host:
#         return HttpResponse('You are not allowed here!!')

#     if request.method == 'POST':
#         room.delete()
#         return redirect('home')
#     return render(request, 'base/delete.html', {'obj': room})

@login_required(login_url='/login')
def profile(request, pk):
    topics = Topic.objects.all()

    if not request.user.id == int(pk):
            return redirect('home')
    
    profile_form = ProfileForm()
    user_form = UserForm()
    update = False

    if request.method == 'POST':
        user = request.user
        data = dict(zip(request.POST.keys(), request.POST.values()))
        data['user'] = user
        first_name = request.POST.get('fullName').split()[0]
        last_name = request.POST.get('fullName').split()[1]
        user_data = {'username':user.username,
                     'first_name': first_name,
                     'last_name': last_name,
                     'email': user.email,
                     'password': user.password,
                     'password2': user.password}
        data.update(user_data)

        profile_form = ProfileForm(instance=user.profile, data=data)
        user_form = UserForm(instance=user, data=data)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            return redirect('home')

    context = {'topics': topics, 
               'user_form': user_form, 
               'profile_form': profile_form, 
               'update': update}

    prof = request.user.profile

    context = {'topics': topics, 'profile': prof}
    return render(request, 'base/profile_page.html', context)

def test(request):
    if request.method == 'POST':  
        form = UserImage(request.POST, request.FILES)  
        if form.is_valid():  
            form.save()  
  
            # Getting the current instance object to display in the template  
            img_object = form.instance  
              
            return render(request, 'base/test.html', {'form': form, 'img_obj': img_object})  
    else:  
        form = UserImage()
        form2 = UserForm()  
   
    return render(request, 'base/test.html', {'form': form, 'form2': form2})

def images(request):
    images = UploadImage.objects.all()
    return render(request, 'base/images.html', {'images': images})

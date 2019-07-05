from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from accounts.models import Note, Folder
from django.forms.models import model_to_dict
import json
from django.http import HttpResponse
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.middleware.csrf import get_token
import threading
from accounts.notelyTools import email_reminder


@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.method == "GET":
        response = HttpResponse(json.dumps({'csrf status': 'active', 'csrfchip': get_token(request)}), status=200)
    else:
        json_data = json.loads(request.body)
        if 'InPassword' not in json_data or 'InUsername' not in json_data:
            response = HttpResponse('Insufficient data for login')
        else:
            password_in = json_data['InPassword']
            username_in = json_data['InUsername']
            user = authenticate(request, username=username_in, password=password_in)
            if user is not None:
                login(request, user)
                response = HttpResponse('Login Successful. Welcome ' + user.first_name, status=200)
            else:
                response = HttpResponse('Login Failed. Invalid username or password.', status=401)
    return response


@require_POST
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        response = HttpResponse('Logout Successful', status=200)
    else:
        response = HttpResponse('You haven''t been logged in!!!', status=401)
    return response


@require_POST
def signup(request):
    json_data = json.loads(request.body)
    if 'NEWUsername' not in json_data or 'NEWPassword' not in json_data or 'NEWEmail' not in json_data or \
            'NEWFirst_name' not in json_data or 'NEWLast_name' not in json_data:
        response = HttpResponse('Insufficient data for signup', status=400)
    elif User.objects.filter(username=json_data['NEWUsername']).exists():
        response = HttpResponse('Duplicate Username', status=409)
    elif User.objects.filter(email=json_data['NEWEmail']).exists():
        response = HttpResponse('Duplicate Email', status=409)
    else:
        user = User.objects.create_user(username=json_data['NEWUsername'], password=json_data['NEWPassword'],
                                        email=json_data['NEWEmail'], first_name=json_data['NEWFirst_name'],
                                        last_name=json_data['NEWLast_name'])
        user.save()
        folder = Folder.objects.create(name='Uncategorized', list_notes='', user=user)
        folder.save()
        response = HttpResponse('User successfully signed up!!!', status=200)
    return response


@require_POST
def add_note(request):
    json_data = json.loads(request.body)
    if not request.user.is_authenticated:
        response = HttpResponse('Not signed in', status=403)
    elif not Folder.objects.filter(name=json_data['folder_name'], user=request.user).exists():
        response = HttpResponse('No folder with said name', status=400)
    elif Note.objects.filter(name=json_data['name'], folder_name=json_data['folder_name'],
                             user=request.user).exists():
        response = HttpResponse('Another note with the same name in the same folder exists already', status=409)
    else:
        note = Note.objects.create(name=json_data['name'], folder_name=json_data['folder_name'],
                                   data=json_data['data'], y_r=int(json_data['y_r']), m_r=int(json_data['m_r']),
                                   d_r=int(json_data['d_r']), h_r=int(json_data['h_r']),
                                   min_r=int(json_data['min_r']), s_r=int(json_data['s_r']),
                                   y_m=int(json_data['y_m']), m_m=int(json_data['m_m']), d_m=int(json_data['d_m']),
                                   h_m=int(json_data['h_m']), min_m=int(json_data['min_m']),
                                   s_m=int(json_data['s_m']), user=request.user)
        note.save()
        folder = Folder.objects.filter(name=note.folder_name, user=request.user).first()
        if folder.list_notes == '':
            folder.list_notes = note.name
        else:
            folder_list_updated = folder.list_notes.split(',')
            folder_list_updated.append(note.name)
            folder.list_notes = ','.join(folder_list_updated)
        folder.save()
        response = HttpResponse('Note saved successfully', status=200)
    return response


@require_GET
def get_note(request):
    json_data = json.loads(request.body)
    if not request.user.is_authenticated:
        response = HttpResponse('Not signed in', status=403)
    elif not Note.objects.filter(name=json_data['name'], folder_name=json_data['folder_name'],
                                 user=request.user).exists():
        response = HttpResponse('The requested note does not exist', status=404)
    else:
        note = Note.objects.filter(name=json_data['name'], folder_name=json_data['folder_name'],
                                   user=request.user).first()
        response = HttpResponse(json.dumps(model_to_dict(note)), status=200)
    return response


@require_POST
def update_note(request):
    json_data = json.loads(request.body)
    if not request.user.is_authenticated:
        response = HttpResponse('Not signed in', status=403)
    elif not Note.objects.filter(name=json_data['old_name'], folder_name=json_data['folder_name'],
                                 user=request.user).exists():
        response = HttpResponse('The note to be updated does not exist', status=409)
    else:
        note = Note.objects.filter(name=json_data['old_name'], folder_name=json_data['folder_name'],
                                   user=request.user).first()
        if 'name' in json_data:
            note.name = json_data['name']
            folder = Folder.objects.filter(name=note.folder_name, user=request.user).first()
            listed_note_names = folder.list_notes.split(',')
            listed_note_names = [json_data['name'] if note_name == json_data['old_name'] else note_name for
                                 note_name in listed_note_names]
            folder.list_notes = ','.join(map(str, listed_note_names))
            folder.save()
        if 'data' in json_data:
            note.data = json_data['data']
        if 'y_m' in json_data:
            note.y_m = int(json_data['y_m'])
            note.m_m = int(json_data['m_m'])
            note.d_m = int(json_data['d_m'])
            note.h_m = int(json_data['h_m'])
            note.min_m = int(json_data['min_m'])
            note.s_m = int(json_data['s_m'])
        if 'y_r' in json_data:
            note.y_r = int(json_data['y_r'])
            note.m_r = int(json_data['m_r'])
            note.d_r = int(json_data['d_r'])
            note.h_r = int(json_data['h_r'])
            note.min_r = int(json_data['min_r'])
            note.s_r = int(json_data['s_r'])
        note.save()
        response = HttpResponse('Note updated successfully', status=200)
    return response


@require_POST
def delete_note(request):
    json_data = json.loads(request.body)
    if not request.user.is_authenticated:
        response = HttpResponse('Not signed in', status=403)
    elif not Note.objects.filter(name=json_data['name'], folder_name=json_data['folder_name'],
                                 user=request.user).exists():
        response = HttpResponse('The note to be deleted does not exist', status=409)
    else:
        Note.objects.filter(name=json_data['name'], folder_name=json_data['folder_name'],
                            user=request.user).delete()
        folder = Folder.objects.filter(name=json_data['folder_name'], user=request.user).first()
        listed_note_names = folder.list_notes.split(',')
        listed_note_names.remove(json_data['name'])
        if len(listed_note_names) == 0:
            folder.list_notes = ''
        else:
            folder.list_notes = ','.join(map(str, listed_note_names))
        folder.save()
        response = HttpResponse('Note deleted successfully', status=200)
    return response


@require_POST
def add_folder(request):
    json_data = json.loads(request.body)
    if not request.user.is_authenticated:
        response = HttpResponse('Not signed in', status=403)
    elif Folder.objects.filter(name=json_data['name'], user=request.user).exists():
        response = HttpResponse('Duplicate folder name', status=400)
    else:
        folder = Folder.objects.create(name=json_data['name'], list_notes='', user=request.user)
        folder.save()
        response = HttpResponse('Folder created successfully', status=200)
    return response


@require_GET
def get_folder_list(request):
    if not request.user.is_authenticated:
        response = HttpResponse('Not signed in', status=403)
    else:
        folder_set = list(Folder.objects.filter(user=request.user).exclude(name='Uncategorized').values_list('name',
                                                                                                             flat=True))
        response = HttpResponse(json.dumps(folder_set), status=200)
    return response


@require_GET
def get_folder_content(request):
    json_data = json.loads(request.body)
    if not request.user.is_authenticated:
        response = HttpResponse('Not signed in', status=403)
    elif not Folder.objects.filter(name=json_data['name'], user=request.user).exists():
        response = HttpResponse('Requested folder does not exist')
    else:
        folder = Folder.objects.filter(name=json_data['name'], user=request.user).first()
        response = HttpResponse(json.dumps(model_to_dict(folder)), status=200)
    return response


@require_POST
def delete_folder(request):
    json_data = json.loads(request.body)
    if not request.user.is_authenticated:
        response = HttpResponse('Not signed in', status=403)
    elif not Folder.objects.filter(name=json_data['name'], user=request.user).exists():
        response = HttpResponse('Said folder does not exist')
    else:
        if json_data['name'] == 'Uncategorized':
            response = HttpResponse('The uncategorized folder cannot be deleted!!!', status=400)
        else:
            Folder.objects.filter(name=json_data['name'], user=request.user).delete()
            Note.objects.filter(folder_name=json_data['name'], user=request.user)
            response = HttpResponse('Successfully deleted the folder and its notes', status=200)
    return response


@require_POST
def start_timer(request):
    json_data = json.loads(request.body)
    if not request.user.is_authenticated:
        response = HttpResponse('Not signed in', status=403)
    else:
        threading.Thread(target=email_reminder, args=(request.user.email, request.user.first_name,
                                                        json_data['note_name'], int(json_data['time_left']))).start()
        response = HttpResponse('Timer Started Successfully', status=200)
    return response




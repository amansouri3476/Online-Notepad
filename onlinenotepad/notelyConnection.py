import requests
import json
from notelyClasses import NotelyNote, NotelyFolder, datatime_m_to_dict, datatime_r_to_dict


session_server = None
url_server = None
csrf_token = None


def initialize():
    global session_server, url_server
    session_server = requests.session()

    url_server = "http://127.0.0.1:8000/accounts/"
    refresh_csrf()


def refresh_csrf():
    global csrf_token
    server_res = session_server.get(url_server + "login/")
    if 'csrftoken' in server_res.cookies:
        csrf_token = server_res.cookies['csrftoken']
    else:
        csrf_token = 'null'


def send_request(url_page, dict_data, type_request):
    headers = {'Content-type': 'application/json', "X-CSRFToken": csrf_token, "Referer": (url_server + url_page)}
    dict_data['csrfmiddlewaretoken'] = csrf_token
    if type_request is "POST":
        return session_server.post(url_server + url_page, data=json.dumps(dict_data), headers=headers)
    elif type_request is "GET":
        return session_server.get(url_server + url_page, data=json.dumps(dict_data), headers=headers)
    else:
        print("No type other than GET or POST is supported yet")


def login_user(username, password):
    res = send_request("login/", {"InUsername": username, "InPassword": password}, "POST")
    refresh_csrf()
    print(res.text)
    return (res.status_code == 200), res.text, res.status_code


def logout_user():
    res = send_request("logout/", {}, "POST")
    print(res.text)
    return (res.status_code == 200), res.text, res.status_code


def signup_user(username, password, email, first_name, last_name):
    res = send_request("signup/", {'NEWUsername': username, 'NEWPassword': password, 'NEWEmail': email,
                                   'NEWFirst_name': first_name, 'NEWLast_name': last_name}, "POST")
    print(res.text)
    return (res.status_code == 200), res.text, res.status_code


def add_note_user(notely_note):
    res = send_request("note/add/", notely_note.to_dict(), "POST")
    print(res.text)
    return (res.status_code == 200), res.text, res.status_code


def get_note_user(name, folder_name):
    res = send_request("note/get/", {"name": name, "folder_name": folder_name}, "GET")
    if res.status_code == 200:
        return True, NotelyNote(dict_json=res.json()), res.status_code
    else:
        return False, res.text, res.status_code


def update_note_user(new_notely_note, old_notely_note):
    dict_update = {"old_name": old_notely_note.name, "folder_name": old_notely_note.folder_name}
    if new_notely_note.name != old_notely_note.name:
        dict_update['name'] = new_notely_note.name
    if new_notely_note.data != old_notely_note.data:
        dict_update['data'] = new_notely_note.data
    if new_notely_note.make_time != old_notely_note.make_time:
        dict_update.update(datatime_m_to_dict(new_notely_note.make_time))
    if new_notely_note.reminder != old_notely_note.reminder:
        dict_update.update(datatime_r_to_dict(new_notely_note.reminder))
    res = send_request("note/update/", dict_update, "POST")
    print(res.text)
    return (res.status_code == 200), res.text, res.status_code


def delete_note_user(name, folder_name):
    res = send_request("note/delete/", {"name": name, "folder_name": folder_name}, "POST")
    print(res.text)
    return (res.status_code == 200), res.text, res.status_code


def add_folder_user(notely_folder):
    res = send_request("folder/add/", {"name": notely_folder.name}, "POST")
    print(res.text)
    return (res.status_code == 200), res.text, res.status_code


def get_folder_list_user():
    res = send_request("folder/get_all/", {}, "GET")
    if res.status_code == 200:
        return True, res.json(), res.status_code
    else:
        return False, res.text, res.status_code


def get_folder_content_user(folder_name):
    res = send_request("folder/get_content/", {"name": folder_name}, "GET")
    if res.status_code == 200:
        return True, NotelyFolder(dict_json=res.json()), res.status_code
    else:
        return False, res.text, res.status_code


def delete_folder_user(folder_name):
    res = send_request("folder/delete/", {"name": folder_name}, "POST")
    print(res.text)
    return (res.status_code == 200), res.text, res.status_code

import datetime


class NotelyNote:
    def __init__(self, name=None, folder_name=None, data=None, reminder=datetime.datetime(1, 1, 1, 0, 0, 0),
                 dict_json=None):
        if dict_json is None:
            self.name = name
            self.folder_name = folder_name
            self.data = data
            self.reminder = reminder
            self.make_time = datetime.datetime.now()
        else:
            self.name = dict_json['name']
            self.data = dict_json['data']
            self.folder_name = dict_json['folder_name']
            self.make_time = dict_to_datetime_m(dict_json)
            self.reminder = dict_to_datetime_r(dict_json)

    def set_reminder(self, reminder):
        self.reminder = reminder

    def to_dict(self):
        dict_trans = {'name': self.name, 'data': self. data, 'folder_name': self.folder_name}
        dict_trans.update(datatime_m_to_dict(self.make_time))
        dict_trans.update(datatime_r_to_dict(self.reminder))
        return dict_trans


class NotelyFolder:
    def __init__(self, name=None, list_notes=None, dict_json=None):
        if dict_json is None:
            self.name = name
            self.list_notes = list_notes
        else:
            self.name = dict_json['name']
            list_temp = dict_json['list_notes'].split(',')
            if len(list_temp) == 1 and list_temp[0] == '':
                self.list_notes = []
            else:
                self.list_notes = list_temp

    def to_dict(self):
        dict_trans = {'name': self.name, 'list_notes': ','.join(map(str, self.list_notes))}
        return dict_trans


def datatime_m_to_dict(datetime_instance):
    dict_dt = {'y_m': datetime_instance.year, 'm_m': datetime_instance.month, 'd_m': datetime_instance.day,
               'h_m': datetime_instance.hour, 'min_m': datetime_instance.minute, 's_m': datetime_instance.second}
    return dict_dt


def datatime_r_to_dict(datetime_instance):
    dict_dt = {'y_r': datetime_instance.year, 'm_r': datetime_instance.month, 'd_r': datetime_instance.day,
               'h_r': datetime_instance.hour, 'min_r': datetime_instance.minute, 's_r': datetime_instance.second}
    return dict_dt


def dict_to_datetime_m(dict_dt):
    datatime_instance = datetime.datetime(int(dict_dt['y_m']), int(dict_dt['m_m']), int(dict_dt['d_m']),
                                          int(dict_dt['h_m']), int(dict_dt['min_m']), int(dict_dt['s_m']))
    return datatime_instance


def dict_to_datetime_r(dict_dt):
    datatime_instance = datetime.datetime(int(dict_dt['y_r']), int(dict_dt['m_r']), int(dict_dt['d_r']),
                                          int(dict_dt['h_r']), int(dict_dt['min_r']), int(dict_dt['s_r']))
    return datatime_instance


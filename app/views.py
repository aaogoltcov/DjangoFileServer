import datetime
import os
import platform
from datetime import datetime

from django.shortcuts import render

from app import settings


def get_slash():
    if platform.system() == 'Windows':
        return '\\'
    else:
        return '//'


def get_file_list(path):
    dict = list()
    for file in os.listdir(path):
        dict.append({'name': file,
                     'ctime': datetime.fromtimestamp(
                         os.stat(f'{path}{get_slash()}{file}').st_ctime),
                     'mtime': datetime.fromtimestamp(
                         os.stat(f'{path}{get_slash()}{file}').st_mtime)})
    return dict


def get_date(date):
    try:
        return datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        try:
            return datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f').date()
        except ValueError:
            return datetime.strptime(date, '%Y-%m-%d %H:%M:%S').date()
    except TypeError:
        return ''


def file_list(request, date=None):
    template_name = 'index.html'
    # Реализуйте алгоритм подготавливающий контекстные данные для шаблона по примеру:
    context = {
        'files': (list for list in get_file_list(settings.FILES_PATH)
                  if (get_date(date) == ''
                      or list['ctime'].date() == get_date(date)
                      or list['mtime'].date() == get_date(date))),
        'date': get_date(date)  # Этот параметр необязательный
    }

    return render(request, template_name, context)


def file_content(request, name):
    # Реализуйте алгоритм подготавливающий контекстные данные для шаблона по примеру:
    return render(
        request,
        'file_content.html',
        context={'file_name': name,
                 'file_content': open(f"{settings.FILES_PATH}{get_slash()}{name}", "r").read()}
    )

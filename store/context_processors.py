__author__ = 'Arlefreak'
# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse


def menu(request):
    menu = {"menu": [
        {'name': 'Home', 'url': reverse('home')},
        {'name': 'About', 'url': reverse('about')},
        {'name': 'Productos', 'url': reverse('categories')},
        {'name': 'Colaboraciones', 'url': reverse('colabs')},
        {'name': 'Prensa', 'url': reverse('press')},
        {'name': 'Contacto', 'url': reverse('contact')},
    ]}
    for item in menu['menu']:
        if request.path == item['url']:
            item['active'] = True
    return menu

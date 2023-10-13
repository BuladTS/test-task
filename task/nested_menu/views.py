from django.shortcuts import render, redirect
from .models import MenuLink
from .utils import wrapp_data

RAW_QUERY = ("select * from nested_menu_menulink where right_key > "
            "(select left_key from nested_menu_menulink where slug=%s) and left_key < "
            "(select right_key from nested_menu_menulink where slug=%s) order by left_key;")


def initial(request):
    return redirect(MenuLink.objects.get(left_key=1).url)


def menu(request, address=''):
    # data = MenuLink.objects.all().order_by('left_key')

    split_address = address.split('/')
    data = MenuLink.objects.raw(RAW_QUERY, [split_address[0], split_address[0]])
    data = wrapp_data(data, split_address)
    return render(request, 'nested_menu/index.html', {
        'data': data,
        'split_address': split_address,
    })

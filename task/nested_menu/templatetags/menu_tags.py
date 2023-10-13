from django import template
from ..models import MenuLink
from ..utils import wrapp_data
from django.conf import settings
from ..views import RAW_QUERY

register = template.Library()


@register.inclusion_tag('nested_menu/includes/menu_req.html')
def draw_menu(menu_slug=''):
    """
    Возвращает шаблон для вывода меню c параметрами
    :param menu_slug: slug меню
    :return: шаблон для вывода меню c параметрами
    """
    if menu_slug != '':
        menu_link = MenuLink.objects.get(slug=menu_slug)
    else:
        menu_link = MenuLink.objects.get(left_key=1)
    split_address = menu_link.url.replace(settings.DOMAIN, '').split('/')
    data = MenuLink.objects.raw(RAW_QUERY, [split_address[0], split_address[0]])
    data = wrapp_data(data, split_address)
    return {'data': data, 'split_address': split_address}


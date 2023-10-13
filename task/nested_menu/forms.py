from typing import Optional

from django import forms
from .models import MenuLink
from django.conf import settings
from django.db.models import F, QuerySet


class MenuLinkForm(forms.ModelForm):
    parent_right_key = forms.IntegerField()

    class Meta:
        model = MenuLink
        fields = ['title', 'slug', 'url', 'level', 'left_key', 'right_key']
        exclude = ['url', 'level', 'left_key', 'right_key']

    def clean_parent_right_key(self):
        """
        Проверяет правый ключ родителя, если нет записи с таким правым ключем, то
        присваивает ему максимальный правый ключ + 1
        :return: правый ключ родителя
        """
        cd = self.cleaned_data
        exist = MenuLink.objects.filter(right_key=cd['parent_right_key']).exists()
        if not exist and cd['parent_right_key'] != 0:
            # если не существует узла с таким же правым ключем, то создаеться новое меню
            cd['parent_right_key'] = MenuLink.objects.all().count() * 2 + 1
        return cd['parent_right_key']

    def save(self, commit=True):
        """
        Сохраняет новый узел в базе данных
        :param commit: параметр указывает, что сохранять новый узел в базе данных
        :return: новый узел
        """
        instance = super(MenuLinkForm, self).save(commit=False)
        cd = self.cleaned_data

        if cd['parent_right_key'] == MenuLink.objects.all().count() * 2 + 1:
            # если создаеться новое меню
            instance.url = self.create_url(None) + cd['slug']
            instance.level = 1
            instance.left_key = cd['parent_right_key']
            instance.right_key = instance.left_key + 1
        else:
            parent = MenuLink.objects.get(right_key=cd['parent_right_key'])
            instance.url = self.create_url(parent) + cd['slug']
            instance.level = parent.level + 1
            instance.left_key = parent.right_key
            instance.right_key = instance.left_key + 1

            self.update_tree(cd['parent_right_key'])
        if commit:
            instance.save()
        return instance

    def update_tree(self, parent_right_key: int) -> None:
        """
        Обновляет дерево после добавления нового узла в дереве
        :param parent_right_key: правый ключ родителя узла
        :return: None
        """
        MenuLink.objects.filter(left_key__gt=parent_right_key).update(right_key=F("right_key") + 2, left_key=F("left_key") + 2)
        MenuLink.objects.filter(right_key__gte=parent_right_key).filter(left_key__lt=parent_right_key).update(right_key=F("right_key") + 2)


    def create_url(self, node: Optional[MenuLink]) -> str:
        """
        Функция возвращает url для указанного узла
        :param node: увел у которого нужно узнать url
        :return: возвращает url для указанного узла
        """
        url = settings.DOMAIN
        if node is not None:
            parents = self.get_parent_branch(node)
            for parent in parents:
                url += parent.slug + '/'
        return url

    def get_parent_branch(self, node: MenuLink) -> QuerySet[MenuLink]:
        """
        Функция возвращает список всех предыдущих узлов в дереве
        :param node: увел родителей которого нужно узнать
        :return: возвращает список всех предыдущих узлов в дереве
        """
        data = MenuLink.objects.filter(left_key__lte=node.left_key).filter(right_key__gte=node.right_key).order_by('left_key')
        return data


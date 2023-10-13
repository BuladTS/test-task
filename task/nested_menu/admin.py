from django.contrib import admin
from django.db.models import F

from .models import MenuLink
from .forms import MenuLinkForm


# Register your models here.
@admin.register(MenuLink)
class MenuLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'url', 'level', 'left_key', 'right_key')
    list_filter = ('level',)
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    form = MenuLinkForm

    def delete_model(self, request, obj):
        """
        Функция удаляет узел из дерева
        :param request: запрос
        :param obj: обект для удаления
        :return: None
        """
        left_key, right_key = obj.left_key, obj.right_key
        super().delete_model(request, obj)
        delete_branch(left_key, right_key)
        update_tree(left_key, right_key)

    def delete_queryset(self, request, queryset):
        """
        Функция удаляет выбранные объекты из дерева
        :param request: запрос
        :param queryset: выбранные объекты для удаления
        :return: None
        """
        for obj in queryset:
            self.delete_model(request, obj)


def delete_branch(left_key: int, right_key: int) -> None:
    """
    Функция удаляет поддерево удаленного узла
    :param left_key: левый ключ удаленного узла
    :param right_key: правый ключ удаленного узла
    :return: None
    """
    MenuLink.objects.filter(left_key__gte=left_key, right_key__lte=right_key).delete()


def update_tree(left_key: int, right_key: int) -> None:
    """
    Обновляет дерево после удаления узла из дерева
    :param left_key: левый ключ удаленного узла
    :param right_key: правый ключ удаленного узла
    :return: None
    """
    deqr = (right_key - left_key + 1)
    MenuLink.objects.filter(right_key__gt=right_key, left_key__lt=left_key).update(
        right_key=F("right_key") - deqr
    )
    MenuLink.objects.filter(left_key__gt=right_key).update(
        left_key=F("left_key") - deqr, right_key=F("right_key") - deqr
    )

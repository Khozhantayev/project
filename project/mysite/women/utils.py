
from .models import Category
from django.db.models import Count
from django.core.cache import cache
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy


menu = [
    {'title': 'About us', 'url_name': 'about'},
    {'title': 'Add post', 'url_name': 'add_page'},
    {'title': 'Contact', 'url_name': 'contact'},
    {'title': 'Admin menu', 'url_name': 'contact_admin'},
]


class DataMixin():
    paginate_by = 3
    def get_user_context(self, **kwargs):
        context = kwargs
        cats = cache.get('cats')
        if not cats:
            cats = Category.objects.annotate(Count('postmodel'))
            cache.set('cats', cats, 60)
        user_menu = menu.copy()

        if self.request.user.is_superuser == False:
            user_menu.pop(3)

        if self.request.user.is_authenticated == False:
            user_menu.pop(1)


        context['menu'] = user_menu


        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context


class RedirectPermissionRequiredMixin(PermissionRequiredMixin):
    login_url = reverse_lazy('home')

    def handle_no_permission(self):
        return redirect(self.get_login_url())
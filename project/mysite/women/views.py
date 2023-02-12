
from multiprocessing import context
from turtle import title
from typing import List
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, FormView, TemplateView
from django.contrib.auth import logout, login
from .forms import *
from .models import *
from .utils import *


class BlogHome(DataMixin, ListView):
    model = PostModel
    template_name = 'women/index.html'
    context_object_name = 'posts'

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Main page')
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def get_queryset(self):
        return PostModel.objects.filter(is_published=True).select_related('cat')


class AdminHome(RedirectPermissionRequiredMixin, DataMixin, ListView):
    model = ContactAdmin
    template_name = 'women/contactadmin.html'
    context_object_name = 'txt'
    permission_required = 'women.contactadmin'

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Admin page')
        context = dict(list(context.items()) + list(c_def.items()))
        return context


class About(DataMixin, TemplateView):
    template_name = 'women/about.html'

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='About us')
        context = dict(list(context.items()) + list(c_def.items()))
        return context


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Add page')
        context = dict(list(context.items()) + list(c_def.items()))
        return context



class ContactFormView(DataMixin, CreateView):
    form_class = ContactForm
    template_name = 'women/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Contact with us')
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    # для формы не связанной с моделью
    # def form_valid(self, form):
    #     print(form.cleaned_data)
    #     return redirect('home')
    #     print(form.cleaned_data.values)

class ShowPost(DataMixin, DetailView):
    model = PostModel
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        context = dict(list(context.items()) + list(c_def.items()))
        return context


class Category(DataMixin, ListView):
    model = PostModel
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return PostModel.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Category - ' + str(c.name),
        cat_selected=c.pk)
        context = dict(list(context.items()) + list(c_def.items()))
        return context


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'women/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Registration')
        context = dict(list(context.items()) + list(c_def.items()))
        return context


    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')



class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'women/login.html'


    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Authentication')
        context = dict(list(context.items()) + list(c_def.items()))
        return context


    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


# View functions:


# def index(request):
#     posts = PostModel.objects.all()


#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Main page',
#         'cat_selected': 0
#     }
#     return render(request, 'women/index.html', context=context)

# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             #print(form.cleaned_data)
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#     return render(request, 'women/addpage.html', {'form': form, 'menu': menu, 'title': 'Add post'})


# def show_post(request, post_slug):
#     post = get_object_or_404(PostModel, slug=post_slug)

#     context = {
#         'post': post,
#         'menu': menu,
#         'title': title,
#         'cat_selected': post.cat_id
#     }

#     return render(request, 'women/post.html', context=context)


# def show_category(request, cat_slug):
#     posts = PostModel.objects.filter(cat__slug=cat_slug)

#     if len(posts) == 0:
#         raise Http404()

#     context = {
#             'posts': posts,
#             'menu': menu,
#             'title': 'Women categories',
#             'cat_selected': cat_slug
#     }
#     return render(request, 'women/index.html', context=context)

# def login(request):
#     return HttpResponse('login')


# def contact(request):
#     return HttpResponse('Contacts')
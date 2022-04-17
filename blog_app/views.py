from django.views.generic import DetailView, TemplateView, CreateView
from .models import *
from django.shortcuts import render
from django.http import Http404
from django.utils.translation import gettext as _
from django.urls import reverse_lazy,reverse
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms
from django.contrib.auth import get_user_model 

User = get_user_model()

class MyPageView(LoginRequiredMixin, DetailView):
    template_name = 'my_home.html'
    model = ArticleModel

    def get_context_data(self, **kwargs):
        ctxt = super().get_context_data()
        ctxt["object_list"] = ArticleModel.objects.all()
        ownerPk = self.kwargs['userid']
        ctxt['page_owner'] = User.objects.get(pk=ownerPk)
        return ctxt
    
    # オーバーライド
    # get_object()は何をしているのか? → 
    # urlに値する1つのデータを取得
    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        
        # request に 合致するデータを取得
        # return get_object_or_404(User, pk=self.request.session['user_id'])
        # pk = self.kwargs.get(self.request)
        # 原文
        pk = self.kwargs['userid']
        # pk = self.kwargs.get(self.pk_url_kwarg)
        # pk
        if pk is not None:
            # この時点で単数にする(?)
            queryset = queryset.filter(posted_by=pk)
        
        try:
            # Get the single item from the filtered queryset
            objs = queryset.filter()
        except queryset.model.DoesNotExist:
            raise Http404(
                _("No %(verbose_name)s found matching the query")
                % {"verbose_name": queryset.model._meta.verbose_name}
            )
        return objs

class HomePageView(LoginRequiredMixin, DetailView):
    template_name = '_main.html'
    model = ArticleModel

    def get_context_data(self, **kwargs):
        ctxt = super().get_context_data()
        ctxt["object_list"] = ArticleModel.objects.all()
        ownerPk = self.kwargs['userid']
        ctxt['page_owner'] = User.objects.get(pk=ownerPk)
        return ctxt
    
    # オーバーライド
    # get_object()は何をしているのか? → 
    # urlに値する1つのデータを取得
    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        
        # request に 合致するデータを取得
        # return get_object_or_404(User, pk=self.request.session['user_id'])
        # pk = self.kwargs.get(self.request)
        # 原文
        pk = self.kwargs['userid']
        # pk = self.kwargs.get(self.pk_url_kwarg)
        # pk
        if pk is not None:
            # この時点で単数にする(?)
            queryset = queryset.filter(posted_by=pk)
        
        try:
            # Get the single item from the filtered queryset
            objs = queryset.filter()
        except queryset.model.DoesNotExist:
            raise Http404(
                _("No %(verbose_name)s found matching the query")
                % {"verbose_name": queryset.model._meta.verbose_name}
            )
        return objs

class index_view(LoginRequiredMixin, TemplateView):
    template_name="index.html"

    def get_context_data(self, **kwargs):
        ctxt = super().get_context_data()
        ctxt["user_list"] = User.objects.all()
        return ctxt

class ArticleCreateView(LoginRequiredMixin, CreateView):
    template_name = 'create_article.html'
    model = ArticleModel
    fields = ('posted_text','posted_by')

    # オーバーライド
    # (https://torajirousan.hatenadiary.jp/entry/2018/08/31/023519)
    def get_success_url(self):
        return reverse_lazy("my_page",kwargs={"userid":self.kwargs["userid"]} )
    
    def get_form(self):
        form = super(ArticleCreateView, self).get_form()
        form.fields['posted_by'].label = '投稿者'
        form.initial['posted_by'] = self.kwargs['userid'] # フィールドの初期値の設定(https://k-mawa.hateblo.jp/entry/2017/10/31/235640)
        form.fields['posted_text'].required = True
        return form

class UserCreateView(CreateView):
    template_name = 'create_user.html'
    form_class = forms.SignUpForm

    # ! 本来ならばログイン画面に遷移
    success_url = reverse_lazy('index') # 投稿完了時の遷移先

class MyLoginView(LoginView):
    form_class = forms.LoginForm
    template_name = "login.html"

class MyLogoutView(LoginRequiredMixin, LogoutView):
    template_name = "logout.html"

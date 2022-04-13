from django.shortcuts import render
from django.views.generic import DetailView, TemplateView, CreateView
from .models import *
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.utils.translation import gettext as _
from django.urls import reverse_lazy,reverse

class MyPageView(DetailView):
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

# Create your views here.
class HomePageView(DetailView):
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

class index_view(TemplateView):
    template_name="index.html"

    def get_context_data(self, **kwargs):
        ctxt = super().get_context_data()
        ctxt["user_list"] = User.objects.all()
        return ctxt

class ArticleCreateView(CreateView):
    template_name = 'article_create.html'
    model = ArticleModel
    fields = ('posted_text','posted_by')

    # オーバーライド
    # (https://torajirousan.hatenadiary.jp/entry/2018/08/31/023519)
    def get_success_url(self):
        return reverse_lazy("my_page",kwargs={"userid":self.kwargs["userid"]} )

    # コメント投稿画面に投稿先を表示
    def get_context_data(self,**kwargs):
        ctxt = super().get_context_data()
        ctxt["user_list"] = User.objects.all()
        ## pkを元にオブジェクト取得(https://yaruki-strong-zero.hatenablog.jp/entry/django_model_lookup)
        # pkを元にオブジェクト取得2(https://k-mawa.hateblo.jp/entry/2017/10/31/235640)
        ctxt["post"] = User.objects.get(id=self.kwargs['userid'])
        return ctxt
    
    def get_form(self):
        form = super(ArticleCreateView, self).get_form()
        form.fields['posted_by'].label = '投稿者'
        form.initial['posted_by'] = self.kwargs['userid'] # フィールドの初期値の設定(https://k-mawa.hateblo.jp/entry/2017/10/31/235640)
        form.fields['posted_text'].required = True
        return form

class UserCreateView(CreateView):
    pass

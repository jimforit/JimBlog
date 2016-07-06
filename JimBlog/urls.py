"""JimBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from BlogDemo.views import IndexView,register,login,article_detail,article_publish,ArticleDetailView,likes_add,retrievepasswd,logout,CommentDetailView,comment_commit,comment_reply,article_search

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
	url(r'^home/',IndexView.as_view(template_name="index.html"),name='home_page') ,
	url(r'^login/',login,name='login_page') ,
	url(r'^logout/',logout,name='logout_page') ,
	url(r'^retrievepasswd/',retrievepasswd,name='retrievepasswd_page') ,
	url(r'^article/(?P<article_id>\d+)/likes',likes_add,name='likes_add_page') ,
	url(r'^register/',register,name='register_page') ,
	url(r'^comment_commit/(?P<article_id>\d+)',comment_commit,name='comment_commit_page'),
	url(r'^comment_reply/(?P<article_id>\d+)',comment_reply,name='comment_reply_page'),
	url(r'^article/(?P<article_id>\d+)',ArticleDetailView.as_view(),name='article_detail_page'),
	url(r'^comment/(?P<comment_id>\d+)',CommentDetailView.as_view(),name='comment_detail_page'),
	url(r'^category/(?P<cate_id>\d+)',IndexView.as_view(template_name="category_list.html"),name='category_article_page'),
	url(r'^article_create/',IndexView.as_view(template_name="article_create.html"),name='article_create_page'),
	url(r'^article_publish/',article_publish,name='article_publish_page'),
	url(r'^article_search/', article_search,name='article_search_page'),
]

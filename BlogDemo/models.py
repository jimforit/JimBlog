#encoding=utf-8
from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.
class Article(models.Model):
	status_choice=(
		('d','draft'),
		('p','Published')
	)
	
	title = models.CharField(u'标题',max_length=70)
	body = models.TextField(u'正文')
	create_time = models.DateTimeField(u'创建时间',auto_now_add=True)
	last_modified_time = models.DateTimeField(u'最后修改时间',auto_now = True)
	status = models.CharField(u'文章状态',max_length=1,choices = status_choice)
	abstract = models.CharField(u'文章摘要',max_length=54,blank=True,null=True,help_text=u'可选，如若为空将摘取正文的前54个字符')
	views = models.PositiveIntegerField(u'浏览量',default=0)
	likes = models.PositiveIntegerField(u'点赞数',default=0)
	likes_user = models.ManyToManyField('User',verbose_name=u'点赞人',null=True,related_name='user_hit_likes')
	topped = models.BooleanField(u'置顶',default=False)
	auther = models.ForeignKey('User',verbose_name = u'作者',null=True,on_delete = models.SET_NULL)
	category = models.ForeignKey('Category',verbose_name=u'分类',null=True,on_delete = models.SET_NULL)
	
	def __str__(self):
		return self.title
		
	def __unicode__(self):
		return self.title
	
	def get_absolute_url(self):
		return reverse('article_detail_page',kwargs={'article_id': self.pk})
		
	class Meta:
		ordering = ['-last_modified_time']

class Comment(models.Model):
	status_choice=(
		('R',u'已读'),
		('N',u'未读')
	)
	comment_user = models.ForeignKey('User',verbose_name = u'评论人',related_name="comment_user")
	comment_content = models.TextField(u'评论内容')
	comment_status = models.CharField(u'评论状态',max_length=10,choices = status_choice,default=u"未读")
	comment_time = models.DateTimeField(u'评论时间',auto_now = True)
	comment_reminder = models.ForeignKey('User',verbose_name=u"提醒人",null=True,related_name="comment_reminder")
	article = models.ForeignKey('Article',verbose_name = u'归属文章')
	
	def __str__(self):
		return self.comment_user.name
	
	def __unicode__(self):
		return self.comment_user.name
		
	class Meta():
		ordering = ['comment_time']
		
class Category(models.Model):
	name = models.CharField(u'类名',max_length=20)
	create_time = models.DateTimeField(u'创建时间',auto_now_add=True)
	last_modified_time = models.DateTimeField(u'最后修改时间',auto_now = True)
	
	def __str__(self):
		return self.name
		
	def __unicode__(self):
		return self.name
	
	class Meta():
		ordering = ['-last_modified_time']
		
class User(models.Model):
	user_status=(
		('invisible',u'隐身'),
		('online',u'在线'),
		('offline',u'离线')
	)
	name = models.CharField(u'用户名',max_length=20)
	passwd = models.CharField(u'密码',max_length=20,null = True)
	email = models.EmailField(u'邮箱地址',max_length=256,default='jimforit@163.com')
	status = models.CharField(u'状态',max_length=10,choices = user_status,default='online')
	last_login_time = models.DateTimeField(u'最后一次登录时间',auto_now = True)
	
	def __str__(self):
		return self.name
	
	def __unicode__(self):
		return self.name
		
	class Meta():
		ordering = ['last_login_time']
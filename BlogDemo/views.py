#encoding=utf-8
from django.shortcuts import render,HttpResponseRedirect,get_object_or_404
from BlogDemo.models import *
from django.views.generic import ListView,DetailView
from django.contrib import auth
from django.core.mail import send_mail,EmailMultiAlternatives
from django.conf import settings
import markdown2
import jieba

# Create your views here.
class IndexView(ListView):
	context_object_name = "article_list"
	template_name = "index.html"
	
	def get_queryset(self):
		self.request.session["current_url"] = self.request.path#获取当前页面url存入session中，如果文章只是刷新页面,而页面不跳转，则阅读数不增加。
		if self.template_name == "category_list.html":
			article_list=Article.objects.filter(category=self.kwargs['cate_id'],status='p')#如果传入category_id则获取对应分类文章作为article_list
		else:
			article_list = Article.objects.filter(status = 'p')#如果不传入category_id则获取所有文章作为article_list
		for articles in article_list:
			articles.body = markdown2.markdown(articles.body)#文章body部分进行markdown渲染
		return article_list
	
	def get_context_data(self,**kwargs):
		new_comment_list = []
		try:
			kwargs['category_name']=Category.objects.get(id=self.kwargs['cate_id']).name
		except:
			pass
		try:
			user_name = self.request.session['username']
			user = get_object_or_404(User,name=user_name)
			new_comment_list = Comment.objects.filter(comment_reminder=user,comment_status="N")
		except 	KeyError:
			pass
		comment_count = len(new_comment_list)
		kwargs['comment_list_user'] = new_comment_list
		kwargs['comment_count_user'] = comment_count
		kwargs['latest_login_user']=User.objects.all().order_by('-last_login_time')[:5]
		kwargs['category_list']=Category.objects.all().order_by('name')
		kwargs['popular_article']=Article.objects.all().order_by('likes')[:5]
		kwargs['views_article']=Article.objects.all().order_by('-views')[:5]
		kwargs['user_count']=User.objects.all().count()
		kwargs['article_count']=Article.objects.all().count()
		return super(IndexView,self).get_context_data(**kwargs)
		
def login(request):
	try:
		name,password,email = request.session['user_name_create'],request.session['password'],request.session['email']
		User.objects.create(name=name,passwd=password,email = email)
		del request.session['user_name_create'],request.session['password'],request.session['email']
		return render(request,"login.html",{'login_err':u'用户注册成功，请登录'})
	except:
		pass
	if request.method == "POST":
		username = request.POST.get("username")
		password = request.POST.get("password")
		new_comment_list = []
		try:
			user = User.objects.get(name=username,passwd=password)
			new_comment_list = Comment.objects.filter(comment_reminder=user,comment_status="N")
		except :
			return render(request,'404.html')
		article_list = Article.objects.filter(status = 'p')
		for articles in article_list:
			articles.body = markdown2.markdown(articles.body,)
		category_list = Category.objects.all().order_by('name')
		popular_article = Article.objects.all().order_by('-likes')[:5]
		views_article = Article.objects.all().order_by('views')[:5]
		user_count = User.objects.all().count()
		article_count = Article.objects.all().count()
		latest_login_user = User.objects.all().order_by('-last_login_time')[:5]
		
		comment_count_user = len(new_comment_list)
		if user:
			request.session["current_url"] = request.path
			request.session['username'],request.session['password'] = username,password
			return render(request,"index.html",{"comment_list_user":new_comment_list,"comment_count_user":comment_count_user,\
			"latest_login_user":latest_login_user,"user_count":user_count,"article_count":article_count,"article_list":article_list,\
			"category_list":category_list,"popular_article":popular_article,"views_article":views_article})
		else:
			return render(request,"login.html",{'login_err':u'用户名或密码错误'})
	else:
		return render(request,"login.html")
	
def register(request):
	error_info = ""
	user = ""
	user_email= ""
	if request.method == "POST":
		name = request.POST.get("username")
		email = request.POST.get("email")
		password = request.POST.get("password")
		repetpassword = request.POST.get("repeat_password")
		from_email = settings.DEFAULT_FROM_EMAIL
		try:
			user = User.objects.get(name=name)
		except:
			pass
		try:
			user_email = User.objects.get(email=email)
		except:
			pass
		if password != repetpassword:
			error_info = u'两次输入密码不一致，请检查后重新输入'
		elif user:
			error_info = u'当前用户已经存在，请更换账号重新注册'
		elif user_email:
			error_info = u'当前邮箱已经被占用，请更换邮箱重新注册'
		else:
			request.session['user_name_create'],request.session['password'],request.session['email'] = name,password,email
			url = 'http://127.0.0.1:8000/login/'
			subject = '欢迎加入JimBlog，请验证登录邮箱'
			text_content = u'欢迎加入JimBlog，您的登录邮箱是:'+email+'\n'+\
			u'请点击以下链接验证你的邮箱地址，以便以后找回账户信息'+'\n\n'+url+'\n'+\
			u'如果以上链接无法访问，请将该网址复制并粘贴到浏览器窗口进行访问'
			msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
			msg.send()
			error_info = u'邮箱验证邮件已经发送到您的邮箱,请按照提示完成相关验证'
		return render(request,"register.html",{'error_info':error_info})
	return render(request,"register.html",{'error_info':error_info})
	
def logout(request):
	if request.user:
		auth.logout(request)
		request.user = ""
	return render(request,'login.html',{'login_err':u'注销成功'})
	
def retrievepasswd(request):
	category_list = Category.objects.all().order_by('name')
	popular_article = Article.objects.all().order_by('-likes')[:5]
	views_article = Article.objects.all().order_by('views')[:5]
	user_count = User.objects.all().count()
	article_count = Article.objects.all().count()
	latest_login_user = User.objects.all().order_by('-last_login_time')[:5]
	
	if request.method == "POST":
		To_email = request.POST.get('email')
		username = request.POST.get('username')
		from_email = settings.DEFAULT_FROM_EMAIL
		try:
			user = User.objects.get(name=username,email = To_email)
			subject = '申请获取JimBlog账户信息邮件'
			text_content = u'#重新获取账号信息:'+'\n\n'+u'您的账号为:'+user.name+'\n\n'+u'账号密码为:'+user.passwd
			msg = EmailMultiAlternatives(subject, text_content, from_email, [To_email])
			msg.send()
			return render(request,"login.html",{'login_err':u'账户信息已经发送至您的邮箱，请查收'})
		except:
			return render(request,"reset_passwd.html",{'error_msg':u'您的邮箱信息与账号不匹配,请重新填写'})

	return render(request,"reset_passwd.html",{'category_list':category_list,'popular_article':popular_article,'views_article':views_article,'user_count':user_count,'article_count':article_count,'latest_login_user':latest_login_user})
	
def article_search(request):
	new_comment_list = []
	article_list = []
	keywords = request.GET.get('search_key')
	for article in Article.objects.all():
		title_data = ';'.join(jieba.cut(article.title,cut_all=True))
		title_data_list = title_data.split(';')
		content_data = ';'.join(jieba.cut(article.body,cut_all=True))
		content_data_list = content_data.split(';')
		if keywords in content_data_list or keywords in title_data_list:
			article_list.append(article)
	try:
		user_name = request.session["username"]
		user = User.objects.get(name = user_name)
		new_comment_list = Comment.objects.filter(comment_reminder=user,comment_status="N")
	except:
		pass
	comment_count_user = len(new_comment_list)
	category_list = Category.objects.all().order_by('name')
	popular_article = Article.objects.all().order_by('-likes')[:5]
	views_article = Article.objects.all().order_by('views')[:5]
	user_count = User.objects.all().count()
	article_count = Article.objects.all().count()
	latest_login_user = User.objects.all().order_by('-last_login_time')[:5]		
	return render(request,"search_list.html",{"comment_list_user":new_comment_list,"comment_count_user":comment_count_user,\
			"latest_login_user":latest_login_user,"user_count":user_count,"article_count":article_count,\
			"category_list":category_list,"popular_article":popular_article,"views_article":views_article,"article_list":article_list})	

def article_detail(request):
	return render(request,"article_detail.html")
	
def article_publish(request):
	if request.method == "POST":
		user_name = request.session['username']
		user = User.objects.get(name=user_name)
		article_title = request.POST.get("title")
		abstract = request.POST.get("abstract")
		article_body = request.POST.get("content")
		catogory_name = request.POST.get("category")
		category = Category.objects.get(name=catogory_name)
		article_status = request.POST.get("status")
		article_body = markdown2.markdown(article_body)
		Article.objects.create(title=article_title,body=article_body,status=article_status,abstract=abstract,auther=user,category=category)
	
	article_list = Article.objects.filter(status = 'p')
	for articles in article_list:
			articles.body = markdown2.markdown(articles.body,)
	user_count = User.objects.all().count()
	article_count = Article.objects.all().count()
	latest_login_user = User.objects.all().order_by('-last_login_time')[:5]
	category_list = Category.objects.all().order_by('name')
	popular_article = Article.objects.all().order_by('-likes')[:5]
	views_article = Article.objects.all().order_by('views')[:5]
	new_comment_list = []
	new_comment_list = Comment.objects.filter(comment_reminder=user,comment_status="N")
	comment_count_user = len(new_comment_list)
	return render(request,"index.html",{"comment_list_user":new_comment_list,"comment_count_user":comment_count_user,"latest_login_user":latest_login_user,"user_count":user_count,"article_count":article_count,"article_list":article_list,"category_list":category_list,"popular_article":popular_article,"views_article":views_article})
	
def comment_reply(request,article_id):
	user_name = request.session["username"]
	user_reply = User.objects.get(name=user_name)
	article = Article.objects.get(id = article_id)
	article_url = article.get_absolute_url()
	reply_content = request.POST.get('reply_content')
	replay_data_list = request.POST.get('reply_content').split(":")
	user_reminder_name = replay_data_list[0][1:]
	user_reminder = User.objects.get(name=user_reminder_name)
	comtent_without_user = replay_data_list[1]
	if comtent_without_user !="":
		from_email = settings.DEFAULT_FROM_EMAIL
		subject = '您有一条来自JimBlog的回复'
		text_content = '#Re:'+article.title+'\n\n'+'@'+user_reminder.name+'\n'+comtent_without_user+'\n'+\
		'---------------------------------------------------------------------------'+'\n'+\
		u'回复人:'+user_name+'\n'+'URL:'+'http://127.0.0.0.1:8000'+article_url
		msg = EmailMultiAlternatives(subject, text_content, from_email, [user_reminder.email])
		msg.send()
		comment_obj = Comment.objects.create(comment_user = user_reply,comment_content = reply_content,article=article,comment_status='N',comment_reminder=user_reminder)
	return HttpResponseRedirect(article_url)
	
def comment_commit(request,article_id):
	article = Article.objects.get(id=article_id)
	article_url = article.get_absolute_url()
	comment_error = ""
	
	if request.method == "POST":
		user_name = request.session["username"]
		user = User.objects.get(name=user_name)
		comment_content = request.POST.get("comment")
		
		if comment_content != "":
			subject = '您有一条来自JimBlog的评论'
			text_content = '#Comment:'+article.title+'\n\n'+user.name+":"+'\n'+comment_content+'\n'+\
			'---------------------------------------------------------------------------'+'\n'+\
			'URL:'+'http://127.0.0.0.1:8000'+article_url
			comment_content = markdown2.markdown(comment_content)
			comment_reminder = User.objects.get(name=article.auther.name)
			from_email = settings.DEFAULT_FROM_EMAIL
			msg = EmailMultiAlternatives(subject, text_content, from_email, [comment_reminder.email])
			msg.send()
			comment_obj = Comment.objects.create(comment_user = user,comment_content = comment_content,article=article,comment_status='N',comment_reminder=comment_reminder)
			
	comment_count = Comment.objects.all().count()
	article.body = markdown2.markdown(article.body)
	category_list = Category.objects.all().order_by('name')
	popular_article = Article.objects.all().order_by('-likes')[:5]
	views_article = Article.objects.all().order_by('views')[:5]
	
	return  HttpResponseRedirect(article_url)
	
class CommentDetailView(DetailView):
	model = Comment
	template_name = "comment_detail.html"
	context_object_name = "comment"
	pk_url_kwarg = "comment_id"
	
		
	def get_object(self):
		obj = super(CommentDetailView, self).get_object()
		obj.comment_content = markdown2.markdown(obj.comment_content)
		return obj
	
	def get_context_data(self,**kwargs):
		comment = Comment.objects.get(id=self.kwargs['comment_id'])
		comment.comment_status = "R"
		comment.save()
		try:
			user_name = self.request.session['username']
			user = get_object_or_404(User,name=user_name)
			user_comment_list = []
			user_comment_list = Comment.objects.filter(comment_reminder=user ,comment_status="N")
			comment_count_user = len(user_comment_list)
			likes_user = comment.article.likes_user.filter(name=self.request.session['username'])
			if user in likes_user:
				kwargs['in_likes_user']='Y'
		except KeyError:
			pass
		self.request.session['article_id'] = comment.article.pk
		users_likes = ""
		for users in comment.article.likes_user.all().order_by('-last_login_time')[:5]:
			users_likes = users_likes+users.name+','
		user_likes_count = comment.article.likes_user.all().count()
		users_likes = users_likes[:-1]
		comment.article.body = markdown2.markdown(comment.article.body)
		kwargs['comment_list_user'] = user_comment_list
		kwargs['comment_count_user'] = comment_count_user
		kwargs['article'] = comment.article
		kwargs['latest_login_user']=User.objects.all().order_by('-last_login_time')[:5]
		kwargs['user_likes_count'] = user_likes_count
		kwargs['users_likes'] = users_likes
		kwargs['user_count']=User.objects.all().count()
		kwargs['article_count']=Article.objects.all().count()
		kwargs['category_list']=Category.objects.all().order_by('name')
		kwargs['popular_article']=Article.objects.all().order_by('likes')[:5]
		kwargs['views_article']=Article.objects.all().order_by('-views')[:5]
		return super(DetailView,self).get_context_data(**kwargs)
	
def likes_add(request,article_id):
	article = Article.objects.get(id=article_id)
	article.likes = article.likes+1
	user = get_object_or_404(User,name=request.session['username'],passwd=request.session['password'])
	article.likes_user.add(user)
	article.save()
	article_url = article.get_absolute_url()	
	article.body = markdown2.markdown(article.body)
	category_list = Category.objects.all().order_by('name')
	popular_article = Article.objects.all().order_by('-likes')[:5]
	views_article = Article.objects.all().order_by('-views')[:5]
	return HttpResponseRedirect(article_url,{"article":article,"category_list":category_list,"popular_article":popular_article,"views_article":views_article})

	
class ArticleDetailView(DetailView):
	model = Article
	template_name = "article_detail.html"
	context_object_name = "article"
	pk_url_kwarg = 'article_id'
	
	
	def get_queryset(self):
		if self.request.session["current_url"] != self.request.path:
			a = Article.objects.get(id=self.kwargs['article_id'])
			article_url = a.get_absolute_url()
			a.views = a.views+1
			a.save()
			self.request.session["history_url"],self.request.session["current_url"] = self.request.session["current_url"],self.request.path
		article_list = Article.objects.filter(status = 'p')
		for articles in article_list:
			articles.body = markdown2.markdown(articles.body,)
		return article_list
	
    # 指定以上几个属性，已经能够返回一个DetailView视图了，为了让文章以markdown形式展现，我们重写get_object()方法。
	def get_object(self):
		obj = super(ArticleDetailView, self).get_object()
		obj.body = markdown2.markdown(obj.body)
		return obj
		
	def get_context_data(self,**kwargs):
		article = Article.objects.get(id=self.kwargs['article_id'])
		new_comment_list = []
		
		try:
			user = get_object_or_404(User,name=self.request.session['username'],passwd = self.request.session['password'])
			likes_user = article.likes_user.filter(name=self.request.session['username'])
			
			if user in likes_user:
				kwargs['in_likes_user']='Y'
			new_comment_list = Comment.objects.filter(comment_reminder=user,comment_status="N")
		except KeyError:
			pass
		
		users_likes = ""
		comment_list = Comment.objects.filter(article=article)
		comment_count = len(comment_list)
		
		for users in article.likes_user.all().order_by('-last_login_time')[:5]:
			users_likes = users_likes+users.name+','
		user_likes_count = article.likes_user.all().count()
		users_likes = users_likes[:-1]
		
		comment_count_user = len(new_comment_list)
		kwargs['comment_list_user'] = new_comment_list
		kwargs['comment_count_user'] = comment_count_user
		kwargs['comment_count'] = comment_count
		kwargs['comment_list'] = comment_list
		kwargs['latest_login_user']=User.objects.all().order_by('-last_login_time')[:5]
		kwargs['user_likes_count'] = user_likes_count
		kwargs['users_likes'] = users_likes
		kwargs['user_count']=User.objects.all().count()
		kwargs['article_count']=Article.objects.all().count()
		kwargs['category_list']=Category.objects.all().order_by('name')
		kwargs['popular_article']=Article.objects.all().order_by('likes')[:5]
		kwargs['views_article']=Article.objects.all().order_by('-views')[:5]
		return super(DetailView,self).get_context_data(**kwargs)
		
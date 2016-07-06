from django.contrib import admin

# Register your models here.
from models import Article,Category,User,Comment

class ArticleAdmin(admin.ModelAdmin):
	list_display = ('title','create_time','last_modified_time','abstract','status','views')
	
class CategoryAdmin(admin.ModelAdmin):
	list_display =('name','create_time','last_modified_time')
	
class UserAdmin(admin.ModelAdmin):
	list_display =('name','passwd','status','email')

class CommentAdmin(admin.ModelAdmin):
	list_display =('comment_user','comment_content','article','comment_reminder','comment_status')

admin.site.register(Article,ArticleAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(User,UserAdmin)
admin.site.register(Comment,CommentAdmin)
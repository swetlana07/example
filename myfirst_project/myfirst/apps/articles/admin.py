#from django.contrib import admin
from django.contrib.admin import AdminSite

from .models import Article, Comment

class BlogAdminSite(AdminSite):
    site_header='Администрирование блога' 
    
blog_admin=BlogAdminSite(name='blog_admin')

blog_admin.register(Article)
blog_admin.register(Comment)

"""myfirst URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#from django.contrib import admin
from django.urls import path, include
from articles.admin import blog_admin
from bboard.admin import bboard_admin
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.views import serve
from django.views.decorators.cache import never_cache
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('captcha/',include('captcha.urls')),
    path ('', include ( 'main.urls', namespace='')),
    path('articles/', include('articles.urls')),   # path('grappelli/', include('grappelli.urls')),
    path('bboard/', include('bboard.urls')),   
    path('bboard_admin/', bboard_admin.urls),
    path('blog_admin/', blog_admin.urls),
    #path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns.append(path('static/<path:path>', never_cache(serve)))
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
    print('urlpatterns')
    print(urlpatterns)
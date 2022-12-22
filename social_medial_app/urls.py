"""social_medial_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('signuppage',views.signuppage),
    path('signup',views.signupdata,name='signupdata'),
    path('signinpage',views.signpage,name='signinpage'),
    path('signin',views.signindata),
    path('',views.home),
    path('uploaddata',views.upload_data),
    path('logout',views.logoutdata),
    path('upload',views.upload),
    path('profile',views.userprofile),
    path('like',views.like_post),
    path('dummy',views.dummy),
    path('user',views.user_profile),
    path('follow',views.follow),
    path('change',views.changepr),
    path('changepr',views.change)
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
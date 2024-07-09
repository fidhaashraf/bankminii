"""
URL configuration for bankmini project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from app1 import views
# FOR MEDIA FILES!!
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('',views.all_login, name="admin"),
    path('login/', views.all_login, name="login"),
    path('user_register',views.user_register, name="user_register"),
    path('user_profile',views.user_profile),
    path('admin_register',views.admin_home),
    path('admin_profile',views.admin_profile),
    path('edit_profile',views.edit_profile),
    path('user_home',views.user_home),
    path('withraw',views.withraw),
    path('deposite',views.deposite),
    path('more',views.more),
    path('user_no',views.user_no),
    path('all_user',views.all_user),
    path('user_view/<int:id>',views.user_view, name="user_view"),
    path('user_history',views.user_history,name="user_history"),
    path('all_history/<int:id>',views.all_history,name="all_history"),
    path('userlogout',views.userlogout),
    path('search_user', views.search),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
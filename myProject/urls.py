from django.contrib import admin
from django.urls import path, include
from myApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('myApp.dashboard_urls')),
    path('api/chat/', views.chat_with_maria, name='chat_with_maria'),
    path('', views.home, name='home'),
]

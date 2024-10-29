from django.contrib import admin
from django.urls import path, include
from api import views

urlpatterns = [
    path('', views.home, name='home'),  # 기본 경로에 대한 뷰
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # api 앱의 urls.py 포함
]
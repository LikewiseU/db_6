"""
URL configuration for unicom project.

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
from unicomapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login_register/', views.login_register, name='login_register'),  # 로그인 및 회원가입 페이지 
    path('study_board/', views.study_board, name='study_board'),  # 스터디 게시판 페이지 
    path('study_create/', views.study_create, name='study_create'),  # 스터디 생성 
    path('study_detail/<int:study_board_post_id>/', views.study_detail, name='study_detail'),  # 스터디 게시글 상세 페이지 
    path('join_study/<int:study_id>/', views.join_study, name='join_study'), # 스터디 참여 창
    path('study_list/', views.study_list, name='study_list'), # 스터디 목록 
    path('study_home/<int:study_id>/', views.study_home, name='study_home'), # 스터디 상세 페이지
    path('study_cafe_reservation/', views.study_cafe_reservation, name='study_cafe_reservation'),
    path('settle_reservation/<int:reservation_id>/', views.settle_reservation, name='settle_reservation'),
    path('study_cafe_reservation/', views.study_cafe_reservation, name='study_cafe_reservation'),
    path('create_reservation/', views.create_reservation, name='create_reservation'),
    path('study/<int:study_id>/', views.my_view, name='my_view'),

]
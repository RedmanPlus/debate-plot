from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('one/', views.one, name='one'),
	path('all/', views.all, name='all'),
	path('home/', views.personal_page, name='personal_page'),
]
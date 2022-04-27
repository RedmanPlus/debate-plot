from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name='update'),
	path('add/', views.add, name='add'),
]
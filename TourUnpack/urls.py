from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name='update'),
	path('add/', views.add, name='add'),
	path('check/', views.update, name='update'),
	path('check/update/', views.load, name='load')
]
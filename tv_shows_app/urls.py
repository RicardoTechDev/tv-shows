from django.urls import path     
from . import views

urlpatterns = [
            path('shows', views.index, name='home'),	  
            path('shows/new', views.new_show, name='new_show'),	 
            path('shows/<int:id_show>', views.view_show, name='view_show'),	  
            path('shows/<int:id_show>/edit', views.edit_show, name='edit_show'), 
            path('shows/<int:id_show>/delete', views.delete_show, name='delete_show'), 
]


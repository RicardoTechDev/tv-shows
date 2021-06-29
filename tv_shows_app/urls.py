from django.urls import path     
from . import views

urlpatterns = [
            path('shows', views.index, name='home'),	  
            path('shows/new', views.new_show, name='new_show'),	 
            path('shows/<int:id_show>', views.view_show, name='view_show'),	  
            path('shows/<int:id_show>/edit', views.edit_show, name='edit_show'), 
            path('shows/<int:id_show>/delete', views.delete_show, name='delete_show'), 
            path('networks', views.networks, name='networks'),
            path('networks/new', views.new_network, name='new_network'),
            path('networks/<int:id_network>/edit', views.edit_network, name='edit_network'), 
            path('networks/<int:id_network>/delete', views.delete_network, name='delete_network'), 
]


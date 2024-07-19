from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.Login, name='login'),  
    
    path('dashboard/', views.dashboard, name='dashboard'),  
    
    path('add_lead/', views.add_lead, name='add_lead'), 
    
    path('view_lead/', views.view_lead, name='view_lead'),   
    
    path('lead_edit/<int:id>', views.lead_edit, name='lead_edit'), 
    
    path('add_followup/<int:id>', views.add_followup, name='add_followup'), 
    
    path('view_followup/<int:id>', views.view_followup, name='view_followup'),   
    
    path('logout/', views.Logout, name='logout'),

]
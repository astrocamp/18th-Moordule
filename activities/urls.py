from django.urls import path
from . import views

app_name = "activities"  

urlpatterns = [
    path('', views.activities, name="index"),
    path('create/', views.create, name='create'),
    path('update/<int:activity_id>/', views.update, name='update'),  
    path('delete/<int:activity_id>/', views.delete, name='delete'),  
    path('confirm_delete/<int:activity_id>/', views.confirm_delete, name='confirm_delete'),  
    path('create_category/', views.create_category, name='category'), 
]


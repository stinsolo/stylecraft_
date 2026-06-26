from django.urls import path
from .views import *

app_name="Staff"

urlpatterns= [
    path("",staff_home,name="staff_home"),
    path("user_login",user_login,name="user_login"),
    path("user_logout",user_logout,name="user_logout"),
    path('update_order_status/<int:order_id>/', update_order_status, name='update_order_status'),

]
from django.urls import path
from .views import *

app_name = "Admin"

urlpatterns = [
    path('', admin_home, name="home"),
    path('admin_home/', home, name='admin_home'),
    path('admin_log/', admin_login, name="admin_log"),
    path('admin_reg/', admin_reg, name='admin_reg'),
    path('staff_reg/', add_staff, name="staff_reg"),
    path('add_temp/', add_templates, name="add_temp"),
    path('admin_logout/', admin_logout, name="admin_logout"),
    path('view_staff/', view_staff, name="view_staff"),
    path('view_orders/', order_view, name="view_orders"),
    path('view_feedback/', view_feedback, name="view_feedback"),
    path('update_staff/<str:staff_id>/update/', update_staff, name="update_staff"),
    path('view_temp/', view_templates, name="view_temp"),
    path('update_temp/<str:temp_id>/update/', upadate_template, name='update_temp'),
    path('order_view/', order_details, name="order_view"),
    path('accept_order/<int:order_id>/', accept_order, name='accept_order'),
    path('orders/', order_view, name='order_view'),
    path('order/details/<int:order_id>/', order_details, name='order_details'),
    path('update_order_status/<int:order_id>/', update_order_status, name='update_order_status'),
    path('delete-item/<int:item_id>/', delete_item, name='delete_item'),
]

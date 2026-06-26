from django.urls import path
from django.conf import settings
from django.conf.urls.static import static 
from .views import *

app_name="User"

urlpatterns= [
    path("",user_home,name="userhome"),
    path("userReg",registration,name="userReg"),
    path("add_details",addDetails,name="add_details"),
    path("user_login",user_login,name='user_login'),
    path('user_logout',user_logout,name='user_logout'),
    path('view_profile/', view_profile, name='view_profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('place_order/<int:item_id>/', place_order, name='place_order'),
    path('enter_measurements/<int:item_id>/',enter_measurements, name='enter_measurements'), 
    path('custom_order/', custom_order, name='custom_order'),  # New URL for custom order
    path('order_history/', order_history, name='order_history'),  # Add order history page
    path('generate_dress/', generate_dress, name='generate_dress'), 
     path("shirt-color/", shirt_color, name="shirt_color"),
    path('payment/<int:order_id>/', payment_page, name='payment_page'),
    path('confirm_payment/<int:order_id>/', confirm_payment, name='confirm_payment'),

]
if settings.DEBUG:  # This ensures Django serves media files in development mode
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
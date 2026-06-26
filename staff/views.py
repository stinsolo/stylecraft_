from django.shortcuts import render,redirect
from  .models import *
from Admin.models import *
from django.views.decorators.csrf import *
from django.http import JsonResponse
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from staff.models import *
from Admin.models import *
from user.models import *
# Create your views here.


def userdetls(request):
    username = request.session.get('staff_email')
    username=Staff_reg.objects.get(email=username)
    return username


def user_login(request):
    if 'user_email' in request.session:
        username = request.session.get('staff_email') 
        return render(request, "User/userhome.html", {'username': username})

    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        
        user = Staff_reg.objects.filter(email=email, password=password).first()

        if user is not None:
            # Save session
            request.session['staff_email'] = email
            request.session['staff'] = user.username  
            return JsonResponse({'success': True})  # Return success response
        else:
            return JsonResponse({'success': False, 'message': 'Invalid credentials. Please try again.'})  # Return failure message

    return render(request, "Staff/userlogin.html")

def user_logout(request):
    if 'staff_email' in request.session:
        request.session.flush()
    return redirect("Admin:home")

def staff_home(request):
    staff = userdetls(request)
    assigned_orders = OrderStatus.objects.filter(staff=staff)
    context = {
        'assigned_orders': assigned_orders
    }
    return render(request, 'staff/staffhome.html', context)

def update_order_status(request, order_id):
    order = Order_table.objects.get(id=order_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        ob=OrderStatus.objects.filter(order=order).last()
        order.status=int(new_status)
        order.save()
        # Create a new record in the OrderStatus model
        ob.status=int(new_status)
        ob.save()
        
        return redirect('Staff:staff_home')
    
    context = {
        'order': order,
    }
    return render(request, 'staff/update_order_status.html', context)

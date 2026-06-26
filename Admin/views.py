from django.shortcuts import render,redirect
from .models import *
from staff.models import *
from user.models import *
from django.views.decorators.csrf import *
from django.http import JsonResponse


# Create your views here.
def admin_home(request):
    return render(request,"Admin/home.html")

def home(request):
    return render(request,"Admin/adminhome.html")

@csrf_exempt
def admin_login(request):
    if 'admin_email' in request.session:
        return render(request, "Admin/adminhome.html")

    if request.method =="POST":
        email=request.POST['email']
        password=request.POST['password']
        user= Admin_login.objects.filter(email=email,password=password).first()

        if user is not None:
            request.session['admin_email']=email
            return JsonResponse({'success':True},safe=False)
        else:
            return JsonResponse({'success':False},safe=False)
    return render(request,"Admin/adminlogin.html")


def admin_logout(request):
    if 'admin_email' in request.session:
        request.session.flush()
    return redirect('Admin:home')

@csrf_exempt
def admin_reg(request):
    if request.method =="POST":
        email=request.POST['email']
        password=request.POST['password']
        
        if Admin_login.objects.filter(email=email).exists():
            response={'success':0, 'message':'email already Exits'}
            return JsonResponse(response,safe=False)
        else:
            admin_obj=Admin_login(
                email=email,
                password=password
            )
            admin_obj.save()
            response={'success':1,'message':"admin registered successfully done"}
    return render(request,"Admin/adminreg.html")

@csrf_exempt
def add_staff(request):
    if request.method == "POST":
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        status=request.POST.get('gender')

        if Staff_reg.objects.filter(email=email).exists():
            response ={'success':0, 'message':'Staff already Exits'}
            return JsonResponse(response,safe=False)
        else:
            staff_obj=Staff_reg(
                username=username,
                email=email,
                password=password,
                status=status
            )
            staff_obj.save()
            return JsonResponse({'success':True,'message':'Staff registered successfully done '})
    return render(request,"Staff/staffReg.html")



def view_staff(request):
    staff= Staff_reg.objects.all()
    context={'staff':staff}
    return render(request,"Admin/viewstaff.html",context)

from django.http import JsonResponse
from django.shortcuts import render
from .models import upload_templates

def add_templates(request):
    if request.method == "POST":
        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')
        image3 = request.FILES.get('image3')
        price = request.POST.get('price')
        description = request.POST.get('description')
        item_name = request.POST.get('item_name')

        if not image1 or not image2 or not image3 or not price or not description or not item_name:
            return JsonResponse({'success': 0, 'message': 'All fields are required'}, status=400)

        if upload_templates.objects.filter(item_name=item_name).exists():
            return JsonResponse({'success': 0, 'message': 'Item already exists'}, status=400)

        try:
            addtemp_obj = upload_templates(
                image1=image1,
                image2=image2,
                image3=image3,
                price=price,
                description=description,
                item_name=item_name
            )
            addtemp_obj.save()
            return JsonResponse({'success': 1, 'message': 'Item added successfully'})
        except Exception as e:
            return JsonResponse({'success': 0, 'message': f'Error: {str(e)}'}, status=500)

    return render(request, "Admin/addtemplates.html")



def view_feedback(request):
    return render(request,"Admin/viewfeedback.html")


def view_orders(request):
    return render(request,"Admin/vieworders.html")


@csrf_exempt
def update_staff(request,staff_id):
    staff_item=Staff_reg.objects.get(pk=staff_id)
    if request.method == "POST":
        staff_item.username=request.POST.get("username")
        staff_item.email=request.POST.get('email')
        staff_item.password=request.POST.get('password')
        staff_item.status=request.POST.get('gender')

        staff_item.save()
        return redirect('Admin:view_staff')
    return render(request,"Admin/updatestaff.html",{'staff_item':staff_item})


def view_templates(request):
    temp=upload_templates.objects.all()
    context={'temp':temp}
    return render(request,"Admin/viewtemplates.html",context)

def view_users(request):
    users=User_Reg.objects.all()
    context={'user':user}
    return render(request,"Admin/viewusers.html",context)

def order_details(request):
    order=Order_table.objects.all()
    context={'order':order}
    return render(request,"Admin/order.html",context)
@csrf_exempt
def upadate_template(request,temp_id):
    tem_details=upload_templates.objects.get(pk=temp_id)
    if(request.method == "POST"):
        tem_details.image1=request.FILES.get("image1")
        tem_details.image2=request.FILES.get("image2")
        tem_details.image3=request.FILES.get("image3")
        tem_details.price=request.POST.get("price")
        tem_details.description=request.POST.get("description")

        tem_details.save()
        return redirect("Admin:view_templates")
    return render(request,"Admin/updatetem.html",{'tem_details':tem_details})







from django.shortcuts import render, get_object_or_404, redirect


def order_view(request):
    orders = Order_table.objects.all()
    return render(request, 'Admin/order_view.html', {'orders': orders})

def order_details(request, order_id):
    order = get_object_or_404(Order_table, id=order_id)
    o=OrderStatus.objects.filter(order=order).last()
    available_staff = Staff_reg.objects.all()
    return render(request, 'Admin/order_details.html', {'order': order, 'available_staff': available_staff,'o':o})

def update_order_status(request, order_id):
    order = get_object_or_404(Order_table, id=order_id)
    if request.method == 'POST':
        status = request.POST['status']
        o=OrderStatus.objects.filter(order=order).last()
        o.status=int(status)
        o.save()
        order.status = int(status)
        order.save()
        return redirect('Admin:order_view')

def accept_order(request, order_id):
    order = get_object_or_404(Order_table, id=order_id)
    if request.method == 'POST':
        staff_id = request.POST['staff']
        rate=request.POST['rate']
        staff = get_object_or_404(Staff_reg, id=staff_id)
        OrderStatus.objects.create(order=order, status=1, staff=staff,rate=rate)
        return redirect('Admin:order_view')



def delete_item(request, item_id):
    if request.method == "POST":
        item = get_object_or_404(upload_templates, id=item_id)
        item.delete()
    return redirect('Admin:view_temp')

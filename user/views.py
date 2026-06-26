from django.shortcuts import render,redirect
from  .models import *
from Admin.models import *
from django.views.decorators.csrf import *
from django.http import JsonResponse
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from .models import Upload_details, Order_table, OrderStatus, User_Reg

# Create your views here.

def user_home(request):
    temp=upload_templates.objects.all()
    context={'temp':temp}
    return render(request,"User/userhome.html",context)
@csrf_exempt
def registration(request):
    if request.method == "POST":
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        address=request.POST.get('address')
        gender=request.POST.get('gender')

        if User_Reg.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'message': 'User already exists'})

        else:
            user_obj=User_Reg(
                username=username,
                email=email,
                password=password,
                address=address,
                gender=gender
            )
            user_obj.save()
            return JsonResponse({'success': True, 'message': 'User registered successfully'})

            
    return render(request,"User/userregistartion.html")

@csrf_exempt
def addDetails(request):
    context = {}  
    if request.method == "POST":
        user = request.session.get('username')  # Get the logged-in username
        
        if not user:
            return JsonResponse({'success': 0, 'message': 'User is not logged in'})

        # Fetch the User_Reg instance based on the username
        user_instance = User_Reg.objects.filter(username=user).first()

        if not user_instance:
            return JsonResponse({'success': 0, 'message': 'User not found'})

        # Get other details from the form
        waist = request.POST.get('waist')
        hips = request.POST.get('hips')
        bust = request.POST.get('bust')
        chestgirth = request.POST.get('chestgirth')
        neck = request.POST.get('neck')
        shoulder = request.POST.get('shoulder')
        sleeve = request.POST.get('sleeve')
        bicep = request.POST.get('bicep')
        wrist = request.POST.get('wrist')
        back_waist_length = request.POST.get('back_waist_length')

        # Check if user details already exist
        if Upload_details.objects.filter(username=user_instance).exists():
            return JsonResponse({'success': 0, 'message': 'User details already exist'})

        # Create and save the details
        userdet_obj = Upload_details(
            username=user_instance,  # Use the User_Reg instance here
            waist=waist,
            hips=hips,
            bust=bust,
            chestgirth=chestgirth,
            neck=neck,
            shoulder=shoulder,
            sleeve=sleeve,
            bicep=bicep,
            wrist=wrist,
            back_waist_length=back_waist_length
        )

        userdet_obj.save()

        return JsonResponse({'success': 1, 'message': 'User details added successfully'})
    
    user = request.session.get('username')
    context = {'username': user}        
    return render(request, "User/adddetails.html", context)


def user_login(request):
    if 'user_email' in request.session:
        username = request.session.get('username') 
        return render(request, "User/userhome.html", {'username': username})

    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        
        user = User_Reg.objects.filter(email=email, password=password).first()

        if user is not None:
            # Save session
            request.session['user_email'] = email
            request.session['username'] = user.username  
            return JsonResponse({'success': True})  # Return success response
        else:
            return JsonResponse({'success': False, 'message': 'Invalid credentials. Please try again.'})  # Return failure message

    return render(request, "User/userlogin.html")

def user_logout(request):
    if 'user_email' in request.session:
        request.session.flush()
    return redirect("Admin:home")

@csrf_exempt
def place_order(request, item_id):
    # Fetch the product details (or template) from the database
    try:
        item = upload_templates.objects.get(id=item_id)  # This is fine; you're getting the item from upload_templates
    except upload_templates.DoesNotExist:
        return render(request,"User/confirmation.html",{"message_title":"The requested item does not exist."})
    
    username = request.session.get('username')  # Get the username from session
    
    # Ensure the user is logged in
    if not username:
        return render(request,"User/confirmation.html",{"message_title":"Please log in first."})

    try:
        user = User_Reg.objects.get(username=username)  # Get the user object based on session
    except User_Reg.DoesNotExist:
        return render(request,"User/confirmation.html",{"message_title":"User not found."})

    
    # Get the user's saved measurements from the Upload_details model
    user_details = Upload_details.objects.filter(username=user).first()  # Make sure this is the correct model

    if request.method == "POST":
        # Ask if the item is for the user or someone else
        is_for_others = request.POST.get('is_for_others')

        if is_for_others not in ['true', 'false']:
            return render(request,"User/confirmation.html",{"message_title":"Invalid value for 'is_for_others'. Please select a valid option."})        
        if is_for_others == 'true':  # If the item is for someone else, redirect to the measurement form
            return HttpResponseRedirect(reverse('User:enter_measurements', args=[item.id]))  # Redirect to measurements form

        elif is_for_others == 'false':  # If the item is for the user, use saved measurements
            if user_details:
                waist = user_details.waist
                hips = user_details.hips
                bust = user_details.bust
                chestgirth = user_details.chestgirth
                neck = user_details.neck
                shoulder = user_details.shoulder
                sleeve = user_details.sleeve
                bicep = user_details.bicep
                wrist = user_details.wrist
                back_waist_length = user_details.back_waist_length
            else:
                return render(request,"User/confirmation.html",{"message_title":"No measurements found for the user. Please add your details first."})


        # Create the order in the Order_table model
        order = Order_table(
            item_name=item,  # Corrected: item_name should be an instance of upload_templates
            status=0,  # Default status for the order
            make_sts=0,  # Default make status
            username=user,
            image1=item.image1,
            image2=item.image2,
            image3=item.image3,
            waist=waist,
            hips=hips,
            bust=bust,
            chestgirth=chestgirth,
            neck=neck,
            shoulder=shoulder,
            sleeve=sleeve,
            bicep=bicep,
            wrist=wrist,
            back_waist_length=back_waist_length
        )
        order.save()  # Save the order to the database
        OrderStatus.objects.create(order=order)
        return render(request,"User/confirmation.html",{"message_title":"Your order has been placed successfully!"})


    # If it's a GET request, show the page with options (is it for the user or someone else?)
    return render(request, 'User/order_confirmation.html', {'item': item})
@csrf_exempt
 # Ensure this is the correct model





def enter_measurements(request, item_id):
    item = get_object_or_404(upload_templates, id=item_id)  # Fetch item or return 404
    if request.method == "POST":
        # Get the entered measurements
        waist = request.POST.get('waist')
        hips = request.POST.get('hips')
        bust = request.POST.get('bust')
        chestgirth = request.POST.get('chestgirth')
        neck = request.POST.get('neck')
        shoulder = request.POST.get('shoulder')
        sleeve = request.POST.get('sleeve')
        bicep = request.POST.get('bicep')
        wrist = request.POST.get('wrist')
        back_waist_length = request.POST.get('back_waist_length')

        
        # Get the user session username
        username = request.session.get('username')
        if not username:
            return HttpResponse("Please log in first.")

        user = User_Reg.objects.get(username=username)

        # Fetch related order if it exists
        order = Order_table.objects.filter(item_name=item).first()
        image1 = order.image1 if order else None
        image2 = order.image2 if order else None
        image3 = order.image3 if order else None

        # Create a new order with measurements
        new_order = Order_table(
            item_name=item,
            status=0,  
            make_sts=0,  
            username=user,
            image1=image1,
            image2=image2,
            image3=image3,
            waist=waist,
            hips=hips,
            bust=bust,
            chestgirth=chestgirth,
            neck=neck,
            shoulder=shoulder,
            sleeve=sleeve,
            bicep=bicep,
            wrist=wrist,
            back_waist_length=back_waist_length
        )
        new_order.save()  
        OrderStatus.objects.create(order=new_order)

        return JsonResponse({'success': True,'message': 'Order confirmed successfully', 'status': 'success'})


    # If not a POST request, render the measurement form
    return render(request, 'user/enter_measurements.html', {'item': item})


def userdetls(request):
    username = request.session.get('username')
    ob=User_Reg.objects.filter(username=username).last()
    return ob


def order_history(request):
    # Get the current user
    user = userdetls(request)

    orders = Order_table.objects.filter(username=user)

    order_statuses = []
    for order in orders:
        latest_status = OrderStatus.objects.filter(order=order).last()  # Get the most recent status
        order_statuses.append({
            'order': order,
            'latest_status': latest_status
        })

    return render(request, 'User/order_history.html', {'order_statuses': order_statuses})



# def view_templates(request):
#     return render()



def view_profile(request):
    user = userdetls(request)
    return render(request, 'User/view_profile.html', {'user': user})

def edit_profile(request):
    user = userdetls(request)
    
    if request.method == 'POST':
        user.username = request.POST.get('username', user.username)
        user.address = request.POST.get('address', user.address)
        user.gender = int(request.POST.get('gender', user.gender))
        user.save()
        return redirect('User:view_profile')  # Redirect to profile view after saving changes

    return render(request, 'User/edit_profile.html', {'user': user})



from django.core.exceptions import ObjectDoesNotExist

# View to display the custom order form
def custom_order(request):
    if request.method == 'POST':
        try:
            # Retrieve the current user
            user = userdetls(request)

            # Create a new order with the form data
            waist = int(request.POST.get('waist'))
            hips = int(request.POST.get('hips'))
            bust = int(request.POST.get('bust'))
            chestgirth = int(request.POST.get('chestgirth'))
            neck = int(request.POST.get('neck'))
            shoulder = int(request.POST.get('shoulder'))
            sleeve = int(request.POST.get('sleeve'))
            bicep = int(request.POST.get('bicep'))
            wrist = int(request.POST.get('wrist'))
            back_waist_length = int(request.POST.get('back_waist_length'))

            # Get the images from the form submission
            image1 = request.FILES.get('image1')
            image2 = request.FILES.get('image2')
            image3 = request.FILES.get('image3')

            # Create the order in the database
            order = Order_table.objects.create(
                username=user,
                image1=image1,
                image2=image2,
                image3=image3,
                waist=waist,
                hips=hips,
                bust=bust,
                chestgirth=chestgirth,
                neck=neck,
                shoulder=shoulder,
                sleeve=sleeve,
                bicep=bicep,
                wrist=wrist,
                back_waist_length=back_waist_length
            )
            OrderStatus.objects.create(
                order=order
            )
            # Redirect to the user's profile or order confirmation page
            return redirect('User:userhome')

        except ObjectDoesNotExist:
            return render(request, 'User/custom_order.html', {'error': 'Item template does not exist.'})

    items = upload_templates.objects.all()  
    return render(request, 'User/custom_order.html', {'items': items})


import os
import requests
from django.shortcuts import render
from django.conf import settings

API_KEY = os.getenv("CLIPDROP_API_KEY", "0877b8710d7ba6a70d0896fc3a52aa9f3d35860120f3e877b71322ef0c79017e4a3b86f637eca78d6ecb655f18ffc470")
API_URL = "https://clipdrop-api.co/text-to-image/v1"

IMAGE_DIR = os.path.join(settings.BASE_DIR, "static/generated_images")
os.makedirs(IMAGE_DIR, exist_ok=True)

def generate_dress(request):
    image_url = None
    error = None  

    if request.method == "POST":
        # Get user input
        bodytype = request.POST.get("bodytype")
        skintone = request.POST.get("skintone")
        occasion = request.POST.get("occasion")
        dresscode = request.POST.get("dresscode")
        style = request.POST.get("style")
        fabric = request.POST.get("fabric")
        color = request.POST.get("color", "#000000")  
        pattern = request.POST.get("pattern")
        description = request.POST.get("description", "")

        # Construct AI Prompt
        prompt = (
            f"Generate 3 dresses design for a person with {bodytype} body type and {skintone} skin tone, "
            f"for a {occasion} occasion. The outfit should follow {dresscode} and {style}. "
            f"Fabric should be {fabric}, featuring {pattern} pattern. Use the color {color}. "
            f"Ensure variation in silhouette, neckline, sleeves, layering and collar design."
            f"Each outfit should be displayed on a headless mannequin with high-quality textures and realistic fabric details. "
            f"Use a neutral background to highlight the designs."
        )

        if description:
            prompt += f" Additional details: {description}."

        headers = {"x-api-key": API_KEY, "Content-Type": "application/json"}
        data = {"prompt": prompt}

        response = requests.post(API_URL, json=data, headers=headers)

        # ✅ Debugging: Print API response
        print("API Status Code:", response.status_code)
        print("API Response:", response.text)

        if response.status_code == 200 and "image" in response.headers.get("Content-Type", ""):
            image_path = os.path.join(IMAGE_DIR, "generated_dress.png")
            with open(image_path, "wb") as f:
                f.write(response.content)
            image_url = "/static/generated_images/generated_dress.png"
        else:
            error = f"Error: {response.status_code} - {response.text}"

    return render(request, "User/ai.html", {"image_url": image_url, "error": error})

# colour change
CLIPDROP_API_KEY = os.getenv("CLIPDROP_API_KEY", "0877b8710d7ba6a70d0896fc3a52aa9f3d35860120f3e877b71322ef0c79017e4a3b86f637eca78d6ecb655f18ffc470")

def shirt_color(request):
    return render(request, "User/shirt_color.html")

#payment

def payment_page(request, order_id):
    return render(request, 'User/payment_dummy.html', {'order_id': order_id})

def confirm_payment(request, order_id):
    if request.method == 'POST':
        order_status = OrderStatus.objects.filter(order_id=order_id).last()
        o=Order_table.objects.filter(id=order_id).last()
        o.status=2
        o.save()
        order_status.status = 2  # Payment Done
        order_status.save()
        return redirect('User:order_history')  # Redirect back to the order history page
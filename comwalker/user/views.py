from django.shortcuts import render,redirect
from.models import *
from service.models import *
from django.contrib import messages
import os 
from comwalker.settings import RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY
import razorpay
import pandas as pd
from collections import namedtuple


# Create your views here.
def user_reg(request):
    if request.method=="POST":
        fullname=request.POST.get("fullname")
        email=request.POST.get("email")
        location=request.POST.get("location")
        address=request.POST.get("address")
        pinaddress=request.POST.get("pinaddress")
        image=request.FILES.get("image")
        p1=request.POST.get("password")
        p2=request.POST.get("confirmpassword")
        if p1==p2:
            if com_TB.objects.filter(Email=email).exists():
                messages.info(request,'Email Already Exists')
            else:
                ucomdata=com_TB(FullName=fullname,Email=email,Location=location,Address=address,PinAddress=pinaddress,Image=image,Password=p1)
                ucomdata.save()
                return redirect("ulog")
        else:
            messages.info(request,'Password not match')
    return render(request,"user/userreg.html")


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import com_TB

def user_log(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            log = com_TB.objects.get(Email=email, Password=password)  # Direct password check
            request.session['F_name'] = log.FullName  # Store Full Name
            request.session['user_id'] = log.id  # Store User ID

            
            return redirect('uhome')
        except com_TB.DoesNotExist:
            messages.error(request, 'Invalid email or password. Please try again.')

    return render(request, "user/userlog.html")


def user_logout(request):
    request.session.flush()  # Clear all session data
    return redirect('ulog')  # Redirect to login page

def user_home(request):
    re = padd_DB.objects.all()
    if request.method=="POST":
        query = request.POST.get('query', '').lower()
        print("query",query)
        
        # Search in the database
        db_results = padd_DB.objects.filter(Name__icontains=query)
        # db_results = padd_DB.objects.filter(Name__icontains=query)
        
        # Load dataset
        dataset_path = r'C:\2024-2025\com\Intern\comwalker\mainapp_search.csv'  # Adjust path
        dataset = pd.read_csv(dataset_path)
        print("dataset",dataset)

        dataset_results = dataset[
            dataset['description'].str.contains(query, case=False, na=False)
        ]
        # Convert dataset rows to named tuples for template compatibility
        DatasetItem = namedtuple('DatasetItem', dataset.columns)
        dataset_results = [DatasetItem(**row) for row in dataset_results.to_dict(orient='records')]
        print("dataset_results",dataset_results)

        # Prepare results
        # db_results = db_results.values()  # Convert to dict for easy template usage
        # dataset_results = dataset_results.to_dict(orient='records')

        context = {
            'db_results': db_results,
            'dataset_results': dataset_results,
            'query': query,
        }
        return render(request,'user/search_results.html',{'re':re,'context':context,
                                                          'db_results':db_results,'dataset_results':dataset_results,'query':query})


    return render(request,'user/uhome.html',{'re':re})
# import pandas as pd
# from django.shortcuts import render
# from .models import padd_DB

def search_results(request):
    if request.method=="POST":
        query = request.POST.get('query', '').lower()
        
        # Search in the database
        db_results = padd_DB.objects.filter(Name__icontains=query)
        
        # Load dataset
        dataset_path = r'C:\2024-2025\com\Intern\comwalker\mainapp_search.csv'  # Adjust path
        dataset = pd.read_csv(dataset_path)
        dataset_results = dataset[
            dataset['description'].str.contains(query, case=False, na=False)
        ]
        
        # Prepare results
        db_results = db_results.values()  # Convert to dict for easy template usage
        dataset_results = dataset_results.to_dict(orient='records')

        context = {
            'db_results': db_results,
            'dataset_results': dataset_results,
            'query': query,
        }
    return render(request, 'search_results.html', context)

def user_inquire(request):
    return render(request,"user/uinquire.html")
import os
from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from user.models import com_TB  # Ensure the correct model is imported




def user_order(request):
    u=book_TB.objects.filter(uf=request.session['id'])
    return render(request,"user/uorder.html",{'u':u,})
def user_about(request):
    return render(request,"user/uabout.html")

def uproduct_detail_from_dataset(request,id):
    import pandas as pd

    dataset_path = r'C:\2024-2025\com\Intern\comwalker\mainapp_search.csv'  # Update this path
    dataset = pd.read_csv(dataset_path)
    
    # Find the item in the dataset
    product = dataset.loc[dataset['id'] == int(id)].to_dict(orient='records')
    
    if not product:
        return render(request, "error.html", {"message": "Item not found in dataset"})
    
    re = product[0]  # Extract the first result

    # re=padd_DB.objects.get(id=id)
    # trailb = re.Services.id
    if request.method=="POST":
        # ProductName = re['description']  # From dataset
        # Price = re['price']  # From dataset
        ProductName = re['description']  # Dataset's description field
        Price = re['price']  # Dataset's price field
        # ProductName = request.POST.get("ProductName")
        # Price = request.POST.get("Price")

        ServiceCentreName = "Admin Control"  # Dataset items are controlled by admin
        Quantity = request.POST.get("quantity")
        AddAddress = request.POST.get("addaddress")
        uf = request.session['id']  # User's session ID for linking
        # Determine the source (dataset in this case)
        source =  "dataset"

        ubook=book_TB(ProductName=ProductName,Price=Price, ServiceCentreName=ServiceCentreName,
                      Quantity=Quantity,AddAddress=AddAddress,sp_id=None,Services_id=None,uf_id=uf,source=source)
        ubook.save()
        return redirect('uhome')
    return render(request,"user/uproductdetaildataset.html",{'re':re})

# ***


# def uproduct_detail_from_dataset(request,id):
#     dataset_path = r'C:\2024-2025\com\Intern\comwalker\mainapp_search.csv'  # Update this path
#     dataset = pd.read_csv(dataset_path)
    
#     # Find the item in the dataset
#     product = dataset.loc[dataset['id'] == int(id)].to_dict(orient='records')
    
#     if not product:
#         return render(request, "error.html", {"message": "Item not found in dataset"})
    
#     product = product[0]  # Extract the first result

#     # re=padd_DB.objects.get(id=id)
#     # trailb = re.Services.id
#     if request.method=="POST":
#         ProductName = product['description']  # From dataset
#         Price = product['price']  # From dataset
#         ServiceCentreName = "Admin Control"  # Dataset items are controlled by admin
#         Quantity = request.POST.get("quantity")
#         AddAddress = request.POST.get("addaddress")
#         uf = request.session['id']  # User's session ID for linking
#         # Determine the source (dataset in this case)
#         source = 'dataset'

#         ubook=book_TB(ProductName=ProductName,Price=Price, ServiceCentreName=ServiceCentreName,Quantity=Quantity,AddAddress=AddAddress,sp_id=None,Services_id=None,uf_id=uf,source=source)
#         ubook.save()
#         return redirect('uhome')
#     return render(request,"user/uproductdetaildataset.html",{'product':product})
def uservice_details(request,id):
    trail = padd_DB.objects.get(id=id)
    trailb = trail.Services.id
    re=Service_DB.objects.get(id=trailb)
    return render(request,"user/usdetails.html",{'re':re,'trail': trail,'trailb': trailb})
client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))
def bookingpay(request,uid):

    global amount
    data = book_TB.objects.get(id=uid)
    # data.Price = True
    price=data.Price 
    quantiity=data.Quantity 
    amount = float(price)* int(quantiity)
    # amount = int(price)* int(quantiity)


    # data.save()
    # amount = 100
    print(amount)
    currency = "INR"
    api_key = RAZORPAY_API_KEY
    amt = int(amount) * 100
    payment_order = client.order.create(dict(amount=amt, currency="INR", payment_capture=1))
    book_TB.objects.filter(id=uid).update(Paymentstatus=True)
    payment_order_id = payment_order['id']
    # book_TB.objects.filter(uf=request.session['id']).update(Paymentstatus=True)

    # messages.info(request,'payment successfull ')

    return render(request, 'user/bookingpay.html', {'a': amount, 'api_key': api_key, 'order_id': payment_order_id})

from django.http import JsonResponse
from django.shortcuts import render

def add_product(request):
    if request.method == 'POST':
        # Process the form here (e.g., save data to database)
        # Example success response
        return JsonResponse({'success': True})

    return JsonResponse({'success': False})


def ufeedback(request):
    re = com_TB.objects.get(id=request.session['id'])
    f=User_Feedback.objects.all()
    if request.method=="POST":
       Name=request.POST.get("Name")
       Email=request.POST.get("Email")
       Feedback=request.POST.get("Feedback")
       user=request.session['id']
       sadd=User_Feedback(Name=Name,Email=Email,Feedback=Feedback,user_id=user)
       sadd.save()
    return render(request,"user/feedback.html",{'r':re,'f':f})

from datetime import date,datetime

   



# user/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.urls import path
from django.templatetags.static import static
from service.models import padd_DB

def live_search(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Check if AJAX request
        query = request.GET.get('q', '').strip()
        if query:
            results = padd_DB.objects.filter(ProductName__icontains=query).values('id', 'ProductName', 'Image')
            return JsonResponse(list(results), safe=False)
    return JsonResponse([], safe=False)

from django.shortcuts import render
from service.models import padd_DB  # Ensure padd_DB is correctly imported

def search_results(request):
    query = request.GET.get("q", "").strip()  # Get the search query
    db_results = []

    if query:
        db_results = padd_DB.objects.filter(Name__icontains=query)  # Filter by Name field

    # Debugging output
    print("Search Query:", query)
    print("Matching Products:", db_results)

    return render(request, "user/search_results.html", {"db_results": db_results, "query": query})
from django.http import JsonResponse
from django.shortcuts import render
from .models import padd_DB

from django.http import JsonResponse
from .models import padd_DB



from django.http import JsonResponse
from .models import padd_DB

def live_search(request):
    query = request.GET.get("q", "").strip()
    results = []
    if query:
        products = padd_DB.objects.filter(Name__icontains=query)[:5]  # Use correct field name
        results = [{
            "id": product.id,
            "name": product.Name,  # Ensure field exists
            "image": product.Productimage.url if product.Productimage else "/static/default.png"
        } for product in products]
    return JsonResponse({"products": results})


def uproduct_detail(request, id):
    try:
        re = padd_DB.objects.get(id=id)
    except padd_DB.DoesNotExist:
        return redirect('uhome')  # Redirect if product does not exist

    trailb = re.Services.id
    uf = request.session.get('id')
    
    if not uf:
        return redirect('ulog')  # Redirect to login if user session is missing
    
    # Get all reviews for this product
    reviews = Review.objects.filter(product_id=re.id).order_by('-created_at')

    if request.method == "POST":
        ProductName = request.POST.get("productname")
        Price = request.POST.get("price")
        ServiceCentreName = request.POST.get("centrename")
        Quantity = request.POST.get("quantity")
        AddAddress = request.POST.get("addaddress")
        sp = request.POST.get("sp")

        if not all([ProductName, Price, ServiceCentreName, Quantity, AddAddress, sp]):
            return render(request, "user/uproductdetail.html", {'re': re, 'reviews': reviews, 'error': "All fields are required."})

        ubook = book_TB(
            ProductName=ProductName, Price=Price, 
            ServiceCentreName=ServiceCentreName, Quantity=Quantity,
            AddAddress=AddAddress, sp_id=sp, Services_id=trailb,
            uf_id=uf, source='database'
        )
        ubook.save()
        return redirect('uhome')

    return render(request, "user/uproductdetail.html", {'re': re, 'reviews': reviews})






import os
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from .models import com_TB  # Adjust according to your model

def user_profile(request):
    try:
        re = com_TB.objects.get(id=request.session['id'])
    except ObjectDoesNotExist:
        return redirect('some_error_page')  # Redirect to an error page if no profile is found

    if request.method == "POST":
        # Handle file upload for the profile image
        if 'img' in request.FILES:
            # Delete old image if exists
            if re.Image and os.path.exists(re.Image.path):
                os.remove(re.Image.path)
            
            # Update the Image field with the new uploaded image
            re.Image = request.FILES['img']

        # Update other profile fields
        re.FullName = request.POST.get('fullname', re.FullName)
        re.Email = request.POST.get('Email', re.Email)
        re.Password = request.POST.get('password', re.Password)
        re.Location = request.POST.get('location', re.Location)
        re.Address = request.POST.get('address', re.Address)
        re.PinAddress = request.POST.get('pinaddress', re.PinAddress)

        # Save the updated profile data
        re.save()

        # Redirect to user home page after saving
        return redirect('uhome')  # Replace 'uhome' with the correct URL name if needed

    # Render the profile page with the current user profile data
    return render(request, "user/uprofile.html", {'update': re})




from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import Review
from .forms import ReviewForm
from service.models import padd_DB
from django.contrib.auth.decorators import login_required
 # Ensures only logged-in users can submit reviews
def add_review(request, product_id):
    product = get_object_or_404(padd_DB, id=product_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)

            # # Ensure request.user is authenticated before assigning
            # if not request.user.is_authenticated:
            #     messages.error(request, "You need to log in to submit a review.")
            #     return redirect("login")  # Redirect to login page

            review.product = product
            review.user = request.user  # Assign logged-in user
            review.uname = request.session.get("F_name")  # Fallback to username
            review.pname = product.Name
            review.save()

        #     messages.success(request, "Your review has been submitted successfully!")
        # else:
        #     messages.error(request, "There was an error submitting your review.")

    return redirect("uhome")




from django.shortcuts import render, get_object_or_404
from .models import Review, padd_DB  # Assuming Product is the model for your products

def all_reviews(request, product_id):
    product = get_object_or_404(padd_DB, id=product_id)
    reviews = Review.objects.filter(product_id=product_id).order_by('-id')
    return render(request, 'user/all_reviews.html', {'reviews': reviews, 'product': product})

from django.shortcuts import render, redirect
from .models import CommunityPost
from .forms import CommunityPostForm
from django.contrib.auth.decorators import login_required

def community_list(request):
    posts = CommunityPost.objects.all().order_by('-created_at')
    return render(request, 'user/community_list.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = CommunityPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('community_list')
    else:
        form = CommunityPostForm()
    return render(request, 'user/create_post.html', {'form': form})



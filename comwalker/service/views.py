from django.shortcuts import render,redirect
from.models import *
from django.contrib import messages
import os 
from user.models import*
# Create your views here.
def index(request):
    return render(request,'index.html')
def service_reg(request):
     if request.method=="POST":
        centrename=request.POST.get("centrename")
        email=request.POST.get("email")
        location=request.POST.get("location")
        address=request.POST.get("address")
        pinaddress=request.POST.get("pinaddress")
        centreimage=request.FILES.get("centreimage")
        p1=request.POST.get("password")
        p2=request.POST.get("confirmpassword")
        if p1==p2:
            if Service_DB.objects.filter(Email=email).exists():
                messages.info(request,'Email Already Exists')
            else:
                comdata=Service_DB(CentreName=centrename,Email=email,Location=location,Address=address,PinAddress=pinaddress,CentreImage=centreimage,Password=p1)
                comdata.save()
                return redirect("slog")
        else:
            messages.info(request,'Password not match')
     return render(request,"service/servicereg.html")
def service_log(request):
    if request.method == "POST":
        try:
            em = request.POST.get("email")
            pd = request.POST.get("password")
            log = Service_DB.objects.get(Email=em, Password=pd)

            if log.approve:
                request.session['id'] = log.id  # Store the service ID
                request.session['C_name'] = log.CentreName  # Store the Centre Name
                return redirect('shome')
            else:
                messages.info(request, 'Admin approval required')
        except Service_DB.DoesNotExist:
            messages.info(request, 'Invalid center')

    return render(request, "service/servicelog.html")




from django.shortcuts import render

def service_home(request):
    return render(request, 'service/shome.html')

def about(request):
    return render(request,"about.html")
def service_profile(request):
    s_profile=Service_DB.objects.get(id=request.session['id'])
    if request.method=="POST":
        if len(request.FILES)!=0:
            if len(s_profile.CentreImage)>0:
                os.remove(s_profile.CentreImage.path)
            s_profile.CentreImage=request.FILES['CentreImage']
        s_profile.CentreName=request.POST['centrename']
        s_profile.Email=request.POST['Email']
        s_profile.Location=request.POST['location']
        s_profile.Address=request.POST['address']
        s_profile.PinAddress=request.POST['pinaddress']
        s_profile.Password=request.POST['Password']
        s_profile.save()
        # return redirect('shome')

    return render(request,"service/sprofile.html",{'update':s_profile})
def service_sabout(request):
    return render(request,"service/sabout.html")
def service_sbooking(request):
    return render(request,"service/sbooking.html")
# def service_schat(request):
#     # today = date.today()
    
#     # Aid=request.session['id']
#     # data=Messages_Tb.objects.filter(Receiver_id=Aid)
#     # udata=[]
#     # Uid=[]
#     # for i in data:
#     #     uid=i.Send_id
#     #     Uid.append(i.Send_id)
#     # a=set(Uid)
#     # b=list(a)
#     # for i in b:
#     #     uid=i
#     #     udata.append(Service_DB.objects.get(id=uid))
        
#     return render(request,"service/schat.html")
def service_order_details(request):
    u=book_TB.objects.filter(Services=request.session['id'])
    return render(request,"service/sorderdetails.html",{'u':u,})
def product_view(request):
    mid=request.session['id']
    rme=padd_DB.objects.filter(Services=mid)
    return render(request,"service/productview.html",{'rme':rme})
def product_delete(request,id):
    product=padd_DB.objects.get(id=id)
    product.delete()
    return redirect('pview')
def product_update(request,uid):
    pup=padd_DB.objects.get(id=uid)
    if request.method=="POST":
        if len(request.FILES)!=0:
            if len(pup.Productimage)>0:
                os.remove(pup.Productimage.path)
            pup.Productimage=request.FILES["Productimage"]
        pup.Name=request.POST.get("Name")
        pup.Colour=request.POST.get("Colour")
        pup.Memorycapacity=request.POST.get("Memorycapacity")
        pup.Description=request.POST.get("Description")
        pup.Price=request.POST.get("Price")
        pup.Details=request.POST.get("Details")
        pup.save()
        return redirect('pview')
    return render(request,"service/productupdate.html",{'up':pup})
# service/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import padd_DB
from user.forms import ReviewForm  # Import the ReviewForm from the user app!
from user.models import Review # Import the Review model from the user app!
from django.contrib.auth.decorators import login_required

@login_required  # Require login to leave a review
def pdetail(request, id):
    rme = get_object_or_404(padd_DB, id=id)  # Get the product
    reviews = rme.reviews.all().order_by('-created_at') # Get all reviews for this product

    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES) # Create a form instance with the submitted data
        if form.is_valid():
            review = form.save(commit=False)  # Create a Review object but don't save it yet
            review.padd = rme  # Set the product for the review
            review.user = request.user  # Set the user for the review (the logged-in user)
            review.save()  # Save the review to the database
            return redirect('pdetails', id=id)  # Redirect back to the same product detail page (Note this is name=pdetails in url)
    else:
        form = ReviewForm()  # Create an empty form for displaying on the page

    context = {'re': rme, 'reviews': reviews, 'form': form}
    return render(request, "user/uproductdetail.html", context)
# def approve(request,id):
#     book_TB.objects.filter(id=id).update(approve=True)
#     return redirect('sorderdetails')
# def reject(request,id):
#     book_TB.objects.filter(id=id).update(reject=True)
#     return redirect('sorderdetails')
def userbookingapprove(request,pk):
    book_TB.objects.filter(id=pk).update(Bookingstatus=True)
    return redirect("service_order_details")




def product_add(request):
    if request.method == "POST":
        # Retrieve form data
        Productimage = request.FILES.get("Productimage")
        Name = request.POST.get("Name")
        Colour = request.POST.get("Colour")
        Memorycapacity = request.POST.get("Memorycapacity")
        Description = request.POST.get("Description")
        Price = request.POST.get("Price")
        Details = request.POST.get("Details")

        # Get the seller ID from session
        seller_id = request.session.get('id')

        # Debugging: Print session value
        print(f"Seller ID from session: {seller_id}")

        if not seller_id:
            messages.error(request, "No seller logged in.")
            return redirect('login')  # Redirect to login if no seller session

        try:
            # Check if the seller exists
            seller = Service_DB.objects.get(id=seller_id)
        except Service_DB.DoesNotExist:
            messages.error(request, "Invalid seller. Please log in again.")
            return redirect('login')  # Redirect if the seller does not exist

        # Create and save the product
        sadd = padd_DB(
            Productimage=Productimage,
            Name=Name,
            Colour=Colour,
            Memorycapacity=Memorycapacity,
            Description=Description,
            Price=Price,
            Details=Details,
            Services=seller  # Use the seller object, not just the ID
        )
        sadd.save()
        messages.success(request, "Successfully Submitted")

    return render(request, "service/productadd.html")

from django.shortcuts import render,redirect
from.models import *
from django.contrib import messages
import os 
from user.models import*
from service.models import*

# Create your views here.
def adm_log(request):
    if request.method=="POST":
        try:
            em=request.POST.get("email")
            pd=request.POST.get("password")
            log=prjctadm_DB.objects.get(Email=em,Password=pd)
            request.session['C_name']=log.Name
            request.session['id']=log.id
            return redirect('aindex')
        except prjctadm_DB.DoesNotExist as e:
            messages.info(request,'Invalid centre')
    return render(request,"prjctadm/adminlog.html")

def aindex(request):
    return render(request,"prjctadm/aindex.html")
def shopdetails(request):
    sd=Service_DB.objects.all()
    return render(request,"prjctadm/shopdetails.html",{'sd':sd})
def shopapprove(request,pk):
    Service_DB.objects.filter(id=pk).update(approve=True)
    return redirect("shopdetails")
def services(request):
    s=padd_DB.objects.all()
    return render(request,"prjctadm/services.html",{'s':s})
def userdetails(request):
    ud=com_TB.objects.all()
    return render(request,"prjctadm/userdetails.html",{'ud':ud})
def bookingdetails(request):
    bd=book_TB.objects.all()
    return render(request,"prjctadm/bookingdetails.html",{'bd':bd})
def feedbacks(request):
    f=User_Feedback.objects.all()
    return render(request,"prjctadm/feedbacks.html",{'f':f})
def stock(request):
    return render(request,"prjctadm/astock.html")
def adm_delete(request,id):
    duct=padd_DB.objects.get(id=id)
    duct.delete()
    return redirect('services')
def ad_delete(request,id):
    duc=Service_DB.objects.get(id=id)
    duc.delete()
    return redirect('shopdetails')

def datasetbookingdetails(request):
    bd=book_TB.objects.filter(ServiceCentreName="Admin Control")
    return render(request,"prjctadm/datasetbookingdetails.html",{'bd':bd})
def bookingapprove(request,pk):
    book_TB.objects.filter(id=pk).update(Bookingstatus=True)
    return redirect("datasetbookingdetails")


from user.models import CommunityPost
from user.forms import CommunityPostForm
def create_admin_post(request):
    if request.method == 'POST':
        form = CommunityPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user  # If admin login is via `request.user`
            post.save()
            return redirect('admin_post_list')  # You can create this view too
    else:
        form = CommunityPostForm()
    return render(request, 'prjctadm/create_admin_post.html', {'form': form})

def admin_post_list(request):
    posts = CommunityPost.objects.all().order_by('-created_at')
    return render(request, 'user/community_list.html', {'posts': posts})

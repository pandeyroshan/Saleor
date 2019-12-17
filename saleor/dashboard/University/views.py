#saleor >> dashboard>> University >> views.py
from django.shortcuts import render,redirect
from django.http import HttpResponse
from ...University.models import University,consignment
from .forms import CreateUniversity,consignmentForm,representativePushForm
from django.contrib.admin.views.decorators import (
    staff_member_required as _staff_member_required,
    user_passes_test,
)
from ...account.models import User
from django.urls import reverse
from ..views import superuser_required
# Create your views here.



def staff_member_required(f):
    return _staff_member_required(f, login_url="account:login")



@staff_member_required
def home(request):
    if request.user.is_superuser:
        university_data = University.objects.all()
        return render(request,'dashboard/university/home.html',{'university_data': university_data})
    return render(request,'dashboard/university/unauth.html')

@staff_member_required
def create_view(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = CreateUniversity(request.POST)
            if form.is_valid:
                form.save()
                university_data = University.objects.all()
                return redirect('/dashboard/university')
        else:
            form = CreateUniversity()
        return render(request,'dashboard/university/addUniversity.html',{'form': form})
    return render(request,'dashboard/university/unauth.html')


@staff_member_required
def delete_view(request,pk):
    if request.user.is_superuser:
        university_object = University.objects.get(id=pk)
        university_object.delete()
        return redirect("/dashboard/university")
    return render(request,'dashboard/university/unauth.html')


@staff_member_required
def edit_view(request,pk):
    if request.user.is_superuser:
        if request.method == 'POST':
            university_object = University.objects.get(id=pk)
            university_object.collegeName = request.POST.get('collegeName')
            university_object.collegeURL = request.POST.get('collegeURL')
            university_object.collegeLocation = request.POST.get('collegeLocation')
            university_object.collegeLocationURL = request.POST.get('collegeLocationURL')
            university_object.user = User.objects.get(id=request.POST.get('user'))
            university_object.userPhone = request.POST.get('userPhone')
            university_object.userEmail = request.POST.get('userEmail')
            university_object.save()
            university_data = University.objects.all()
            return redirect("/dashboard/university")
        university_object = University.objects.get(id=pk)
        form = CreateUniversity(initial={
            'collegeName': university_object.collegeName,
            'collegeURL': university_object.collegeURL,
            'collegeLocation': university_object.collegeLocation,
            'collegeLocationURL': university_object.collegeLocationURL,
            'user': university_object.user,
            'userPhone': university_object.userPhone,
            'userEmail': university_object.userEmail
            })
        return render(request,'dashboard/university/editUniversity.html',{'form': form,'pk':pk})
    return render(request,'dashboard/university/unauth.html')

@staff_member_required
def detail_view(request,pk,rk):
    if request.user.is_superuser:
        university_object = University.objects.get(id=pk)
        consignment_data = consignment.objects.filter(university=university_object,user=User.objects.get(id=rk)).values()
        return render(request,'dashboard/university/detailpage.html',{'college_data': university_object,'consignment_data':consignment_data})
    return render(request,'dashboard/university/unauth.html')

@staff_member_required
def add_consignment(request,pk,rk):
    if request.user.is_superuser:
        if request.method == 'POST':
            form_data = consignmentForm(request.POST)
            if form_data.is_valid:
                newForm = form_data.save(commit=False)
                newForm.user = User.objects.get(id=rk)
                newForm.save()
                redirectStr = '/dashboard/university/detail-page/'+request.POST.get('university')+"/"+str(rk)
                print(redirectStr)
                return redirect(redirectStr)
        university_object = University.objects.get(id=pk)
        form = consignmentForm(initial={'university' : university_object})
        return render(request,'dashboard/university/addconsignment.html',{'form':form})
    return render(request,'dashboard/university/unauth.html')

@staff_member_required
def delete_consignment(request,pk,qk):
    if request.user.is_superuser:
        consignment_object = consignment.objects.get(id=pk)
        consignment_object.delete()
        redirectStr = '/dashboard/university/detail-page/'+str(qk)
        return redirect(redirectStr)
    return render(request,'dashboard/university/unauth.html')

@staff_member_required
def edit_consignment(request,pk):
    if request.user.is_superuser:
        if request.method == 'POST':
            consignment_object = consignment.objects.get(id=pk)
            print(request.POST)
            consignment_object.university = University.objects.get(id=request.POST.get('university'))
            consignment_object.consignmentID = request.POST.get('consignmentID')
            consignment_object.totalPair = request.POST.get('totalPair')
            consignment_object.price = request.POST.get('price')
            consignment_object.status = request.POST.get('status')
            consignment_object.totalCommission = request.POST.get('totalCommission')
            consignment_object.save()
            key = consignment_object.university.id
            return redirect('/dashboard/university/detail-page/'+str(key)+'/')
        consignment_object = consignment.objects.get(id=pk)
        key = consignment_object.id
        form = consignmentForm(initial={
            'university': consignment_object.university,
            'consignmentID': consignment_object.consignmentID,
            'totalPair': consignment_object.totalPair,
            'price': consignment_object.price,
            'status': consignment_object.status,
            'totalCommission':  consignment_object.totalCommission,
        })
        return render(request,'dashboard/university/editconsignment.html',{'form':form})
    return render(request,'dashboard/university/unauth.html')

@staff_member_required
def my_consignment(request):
    consignment_data = consignment.objects.filter(user=request.user).values()
    return render(request,'dashboard/university/myconsignment.html',{'consignment_data': consignment_data})

@staff_member_required
def my_consignment_detail(request,pk):
    consignment_data = consignment.objects.get(id=pk)
    if request.user == consignment_data.user:
        data = consignment_data
        flag = True
    else:
        data = []
        flag = False
    return render(request,'dashboard/university/consignment_detail.html',{'data': data,'flag': flag})
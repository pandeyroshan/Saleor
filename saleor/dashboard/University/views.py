#saleor >> dashboard>> University >> views.py
from django.shortcuts import render
from django.http import HttpResponse
from ...University.models import University,CollegeRepr
from .forms import CreateUniversity
from django.contrib.admin.views.decorators import (
    staff_member_required as _staff_member_required,
    user_passes_test,
)
# Create your views here.



def staff_member_required(f):
    return _staff_member_required(f, login_url="account:login")

@staff_member_required
def create_view(request):
    if request.method == 'POST':
        form = CreateUniversity(request.POST)
        if form.is_valid:
            form.save()
            university_data = University.objects.all()
            return render(request,'dashboard/university/home.html',{'university_data': university_data})
    else:
        form = CreateUniversity()
    return render(request,'dashboard/university/addUniversity.html',{'form': form})


@staff_member_required
def delete_view(request,pk):
    university_object = University.objects.get(id=pk)
    university_object.delete()
    university_data = University.objects.all()
    return render(request,'dashboard/university/home.html',{'university_data': university_data})


@staff_member_required
def edit_view(request):
    pass


@staff_member_required
def home(request):
    university_data = University.objects.all()
    return render(request,'dashboard/university/home.html',{'university_data': university_data})
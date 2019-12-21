#saleor >> dashboard>> University >> views.py
from django.shortcuts import render,redirect
from django.http import HttpResponse
from ...University.models import University,consignment,representativePush, representative
from .forms import CreateUniversity,consignmentForm,representativePushForm,addMoneyForm,CreateRepr
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
def payment_approval(request):
    payment_data = representativePush.objects.all()
    print(payment_data)
    return render(request,'dashboard/university/payment_approval.html',{'payment_data': payment_data})




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
            university_object.save()
            university_data = University.objects.all()
            return redirect("/dashboard/university")
        university_object = University.objects.get(id=pk)
        form = CreateUniversity(initial={
            'collegeName': university_object.collegeName,
            'collegeURL': university_object.collegeURL,
            'collegeLocation': university_object.collegeLocation,
            'collegeLocationURL': university_object.collegeLocationURL,
            })
        return render(request,'dashboard/university/editUniversity.html',{'form': form,'pk':pk})
    return render(request,'dashboard/university/unauth.html')

@staff_member_required
def detail_view(request,pk):
    if request.user.is_superuser:
        university_object = University.objects.get(id=pk)
        repr_data = representative.objects.filter(College=university_object)
        return render(request,'dashboard/university/detailpage.html',{'college_data': university_object,'repr_data': repr_data})
    return render(request,'dashboard/university/unauth.html')

@staff_member_required
def add_consignment(request,uk,rk):
    if request.user.is_superuser:
        if request.method == 'POST':
            form_data = consignmentForm(request.POST)
            if form_data.is_valid:
                print(request.POST)
                newForm = form_data.save(commit=False)
                UniID = University.objects.get(id=request.POST.get('university'))
                newForm.consignmentID = str(UniID.collegeName).upper()[:3]+str(consignment.objects.all().count())
                newForm.representative = representative.objects.get(id=request.POST.get('representative'))
                newForm.totalCommission = (int(newForm.commissionPercentage)*int(newForm.price))/100
                newForm.save()
                redirectStr = '/dashboard/university/open-repr'+"/"+str(request.POST.get('representative'))
                print(redirectStr)
                return redirect(redirectStr)
        university_object = University.objects.get(id=uk)
        repr_object = representative.objects.get(id=rk)
        form = consignmentForm(initial={'university' : university_object,'representative': repr_object})
        return render(request,'dashboard/university/addconsignment.html',{'form':form})
    return render(request,'dashboard/university/unauth.html')

@staff_member_required
def delete_consignment(request,pk,rk):
    if request.user.is_superuser:
        consignment_object = consignment.objects.get(id=pk)
        consignment_object.delete()
        redirectStr = '/dashboard/university/open-repr/'+str(rk)
        return redirect(redirectStr)
    return render(request,'dashboard/university/unauth.html')

@staff_member_required
def edit_consignment(request,pk,uk,rk):
    if request.user.is_superuser:
        if request.method == 'POST':
            consignment_object = consignment.objects.get(id=pk)
            consignment_object.university = University.objects.get(id=request.POST.get('university'))
            consignment_object.totalPair = request.POST.get('totalPair')
            consignment_object.price = request.POST.get('price')
            consignment_object.status = request.POST.get('status')
            consignment_object.commissionPercentage = request.POST.get('commissionPercentage')
            consignment_object.save()
            key = consignment_object.university.id
            return redirect('/dashboard/university/open-repr/'+str(rk))
        consignment_object = consignment.objects.get(id=pk)
        key = consignment_object.id
        form = consignmentForm(initial={
            'university': consignment_object.university,
            'representative': consignment_object.representative,
            'consignmentID': consignment_object.consignmentID,
            'totalPair': consignment_object.totalPair,
            'price': consignment_object.price,
            'status': consignment_object.status,
            'commissionPercentage':  consignment_object.commissionPercentage,
        })
        return render(request,'dashboard/university/editconsignment.html',{'form':form})
    return render(request,'dashboard/university/unauth.html')

@staff_member_required
def my_consignment(request):
    if request.user.is_superuser:
        consignment_data = consignment.objects.filter().values()
        for data in consignment_data:
            if  data['totalPaid'] >= data['price']-data['totalCommission']:
                data.update( {'MoneyStatus' : True} )
            else:
                data.update( {'MoneyStatus': False})
            checkPushData = representativePush.objects.filter(consignment=consignment.objects.get(id=data['id']))
            flag= False
            approvedMoney = 0
            for subdata in checkPushData:
                if subdata.status == 'Initiated':
                    flag = True
                else:
                    approvedMoney += subdata.pushMoney
            if flag:
                data.update( {'popup': True})
            else:
                data.update( {'popup': False})
            data.update( {'repr': representative.objects.get(id=data['representative_id'])})
            data.update( {'approvedMoney': approvedMoney})
            print(data)
        return render(request,'dashboard/university/adminConsignment.html',{'consignment_data':consignment_data})
    else:
        consignment_data = consignment.objects.filter(representative=representative.objects.get(user=request.user)).values()
    return render(request,'dashboard/university/myconsignment.html',{'consignment_data': consignment_data})

@staff_member_required
def my_consignment_detail(request,pk):
    consignment_data = consignment.objects.get(id=pk)
    if request.user == consignment_data.representative.user:
        data = consignment_data
        money_data = representativePush.objects.filter(consignment=data)
        total_paid = 0
        for mindata in money_data:
            total_paid += mindata.pushMoney
        flag = True
    else:
        data = []
        money_data = []
        flag = False
        total_paid = 0
    return render(request,'dashboard/university/consignment_detail.html',{
        'data': data,
        'flag': flag,
        'money_data':money_data,
        'total_paid': total_paid
        })

@staff_member_required
def add_money(request,ck):
    if request.method == 'POST':
        formdata = addMoneyForm(request.POST)
        consignment_object = consignment.objects.get(id=ck)
        if request.user == consignment_object.representative.user:
            print('YES')
            fetchData = formdata.save(commit=False)
            consignment_object.totalPaid += int(request.POST.get('pushMoney'))
            consignment_object.save()
            fetchData.consignment = consignment_object
            fetchData.save()
            return redirect('/dashboard/university/my-consignment')
        else:
            return render(request,'dashboard/university/unauth.html')
    form = addMoneyForm()
    return render(request,'dashboard/university/addMoney.html', { 'form': form})

@staff_member_required
def toggle(request,pk):
    if request.user.is_superuser:
        payment_data = representativePush.objects.get(id=pk)
        payment_data.status = 'Approved'
        payment_data.save()
    return redirect('/dashboard/university/payment-approval')

@staff_member_required
def retoggle(request,pk):
    if request.user.is_superuser:
        payment_data = representativePush.objects.get(id=pk)
        payment_data.status = 'Initiated'
        payment_data.save()
    return redirect('/dashboard/university/payment-approval')




@staff_member_required
def add_repr(request,uk):
    if request.user.is_superuser:
        if request.method == 'POST':
            form_data = CreateRepr(request.POST)
            form_data.save()
            return redirect('/dashboard/university/detail-page/'+str(uk)+'/')
        form = CreateRepr(initial={'College': University.objects.get(id=uk)})
        return render(request,'dashboard/university/addRepr.html',{'form': form})
    return render(request,'dashboard/university/unauth.html')


@staff_member_required
def edit_repr(request,rk,uk):
    if request.user.is_superuser:
        if request.method == 'POST':
            repr_object = representative.objects.get(id=rk)
            repr_object.College = University.objects.get(id=request.POST.get('College'))
            repr_object.user = User.objects.get(id=request.POST.get('user'))
            repr_object.contactNo = request.POST.get('contactNo')
            repr_object.save()
            return redirect('/dashboard/university/detail-page/'+str(uk)+'/')
        repr_object = representative.objects.get(id=rk)
        form = CreateRepr(initial={
            'College': repr_object.College,
            'user': repr_object.user,
            'contactNo': repr_object.contactNo
        })
        return render(request,'dashboard/university/addRepr.html',{'form': form})
    return render(request,'dashboard/university/unauth.html')

@staff_member_required
def delete_repr(request,rk,uk):
    if request.user.is_superuser:
        repr_object = representative.objects.get(id=rk)
        repr_object.delete()
        return redirect('/dashboard/university/detail-page/'+str(uk)+'/')
    return render(request,'dashboard/university/unauth.html')


@staff_member_required
def open_repr(request,rk):
    if request.user.is_superuser:
        repr_object = representative.objects.get(id=rk)
        consignment_data = consignment.objects.filter(representative=representative.objects.get(id=rk))
        return render(request,'dashboard/university/openRepr.html',{'repr_data': repr_object,'consignment_data':consignment_data})
    return render(request,'dashboard/university/unauth.html')
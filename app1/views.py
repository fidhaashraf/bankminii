from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Customs, Transaction
from django.contrib.auth.models import User, auth


# Create your views here.

def user_register(request):
    if request.method == "POST":
        Acnt_no = request.POST['account_no']
        Name = request.POST['first_name']
        Address = request.POST['address']
        Adhar_no = request.POST['adhar_no']
        Image = request.FILES['image']
        # Account_no = request.POST['account_no']
        Dob = request.POST['dob']
        Pancard_no = request.POST['pancard_no']
        Amount = int(request.POST['amount'])
        if Amount < 1000:
            return render(request, 'register.html', {'message': "amount must be minimum 1000rs"})
        # if Bank.objects.filter(acnt_no=Acnt_no).exists():
        #     return render(request,'program.html',{'warning':"a/c already exist"})
        Phone_no = request.POST['phone_no']
        Email = request.POST['email']
        Username = request.POST['username']
        Password = request.POST['password']
        User = Customs.objects.create_user(first_name=Name, address=Address, adhar_no=Adhar_no, image=Image,
                                           acnt_no =Acnt_no, dob=Dob, pancard_no=Pancard_no, amount=Amount,
                                           phone_no=Phone_no, email=Email, username=Username, password=Password,
                                           user_type="user")
        User.save()
        return redirect(all_login)
    else:
        return render(request, 'user/user_register.html')


def all_login(request):
    if request.method == "POST":
        Username = request.POST['username']
        Password = request.POST['password']
        admin_user = auth.authenticate(request, username=Username, password=Password)
        if admin_user is not None and admin_user.is_staff:
            auth.login(request, admin_user)
            return redirect(admin_profile)
        data = auth.authenticate(username=Username, password=Password)
        if data is not None:
            auth.login(request, data)
            if data.user_type == "user":
                return redirect(user_profile)
            if data.user_type == "bank":
                return redirect(user_no)
        else:
            return HttpResponse("incorrect credentials")
    else:
        return render(request, 'user/login.html')


def user_profile(request):
    data = Customs.objects.get(id=request.user.id)
    return render(request, 'user/profile.html', {'data': data})


def edit_profile(request):
    data = Customs.objects.get(id=request.user.id)
    if request.method == "POST":
        data.first_name = request.POST['first_name']
        data.email = request.POST['email']
        data.address = request.POST['address']
        data.adhar_no = request.POST['adhar_no']
        data.username = request.POST['username']
        data.dob = request.POST['dob']
        data.phone_no = request.POST['phone_no']
        if 'image' in request.FILES:
            data.image = request.FILES['image']
        data.save()

        return redirect(user_profile)
    else:
        return render(request, 'user/edit_profile.html', {'data': data})


def user_home(request):
    data = Customs.objects.get(id=request.user.id)
    bank = Customs.objects.get(user_type="bank")
    return render(request, 'user/user_home.html', {'data': data, 'bank': bank})


def withraw(request):
    data = Customs.objects.get(id=request.user.id)
    if request.method == "POST":
        Account_no = int(request.POST["account_no"])
        withdraw = int(request.POST["withdraw"])
        try:
            data.acnt_no == Account_no
            if data.amount <= 1000:
                return render(request, 'user/withdraw.html',
                              {'withdraw': "can't withdraw money.minimum balance required 1000rs"})
            if withdraw < 200:
                return render(request, 'user/withdraw.html',
                              {'withdrawarning': "can't withdraw money.minimum amount required 200rs"})

            else:
                data.amount = data.amount - withdraw
                data.save()
                history = Transaction.objects.create(user_id=data.id, details="Debit", user_amount=withdraw)
                history.save()
                return render(request, 'user/withdraw.html', {'withdrawed': "amount withdrawed"})
        except:
            return render(request, 'user/withdraw.html', {'withdrawacntissue': "incorrect a/c number"})
    else:
        return render(request, 'user/withdraw.html')


def deposite(request):
    data = Customs.objects.get(id=request.user.id)
    if request.method == "POST":
        Account_no = int(request.POST["account_no"])
        deposite = int(request.POST["deposite"])
        try:
            data.acnt_no == Account_no
            if deposite < 200:
                return render(request, 'user/deposite.html',
                              {'depositewarning': "can't withdraw money.minimum amount required 200rs"})

            else:
                data.amount = data.amount + deposite
                data.save()
                history = Transaction.objects.create(user_id=data.id, details="Credit", user_amount=deposite)
                history.save()
                return render(request, 'user/deposite.html', {'deposited': "amount withdrawed"})
        except:
            return render(request, 'user/deposite.html', {'depositeacntissue': "incorrect a/c number"})
    else:
        return render(request, 'user/deposite.html')


def user_history(request):
    data = Transaction.objects.filter(user_id=request.user.id)
    print(data)
    return render(request, 'user/user_history.html', {'data': data})


def more(request):
    data = Customs.objects.get(id=request.user.id)
    bank = Customs.objects.get(user_type="bank")
    return render(request, 'user/more.html', {'data': data, 'bank': bank})


# ADMIN...

def admin_home(request):
    if request.method == "POST":
        Bank_name = request.POST['bank_name']
        Branch = request.POST['branch']
        Ifsc_code = request.POST['ifsc_code']
        Pincode = request.POST['pincode']
        Username = request.POST['username']
        Password = request.POST['password']
        if Customs.objects.filter(bank=Bank_name).exists():
            return render(request, 'admin/admin_register.html', {'caution': "bank already exist"})
        Bank = Customs.objects.create_user(bank=Bank_name, branch=Branch, ifsc_code=Ifsc_code,
                                           pincode=Pincode, username=Username, password=Password, user_type="bank")
        Bank.save()
        return redirect(admin_profile)
    else:
        return render(request, 'admin/admin_register.html')


def admin_profile(request):
    data = Customs.objects.filter(user_type="bank")
    return render(request, 'admin/admin_profile.html', {'data': data})


# Bank...

def user_no(request):
    user_number = Customs.objects.filter(user_type="user").count()
    return render(request, 'bank/user_no.html', {'user_number': user_number})


def all_user(request):
    all_user = Customs.objects.filter(user_type="user")
    return render(request, 'bank/all_user.html', {'users': all_user})


def user_view(request, id):
    data = Customs.objects.get(id=id)
    return render(request, 'bank/user_view.html', {'data': data})


def all_history(request, id):
    history = Transaction.objects.filter(user_id=id)
    return render(request, 'bank/all_history.html', {'history': history})


def userlogout(request):
    auth.logout(request)
    return redirect(all_login)

def search(request):
    if request.method == "POST":
        search = request.POST["search"]
        data = Customs.objects.filter(first_name__icontains=search)
        return render(request,'bank/all_user.html', {'data': data})
    else:
        return render(request, 'bank/all_user.html', )


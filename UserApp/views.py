from django.shortcuts import render,redirect
from django.http import HttpResponse
from AdminApp.models  import Toy,Category,Accounts,OrderMaster
from UserApp.models import UserInfo,MyCart
from django.contrib import messages

# Create your views here.
def homepage(request):
    cats = Category.objects.all()
    toys = Toy.objects.all()
    return render(request,"homepage.html",{"cats":cats,"toys":toys,})

def ShowToys(request,id):
    cat = Category.objects.get(id=id)
    toys = Toy.objects.filter(cat_fk = id)
    cats = Category.objects.all()
    return render(request,'homepage.html',{"toys":toys,"cats":cats,"cat":cat})

def ViewDetails(request,id):
    toy = Toy.objects.get(id=id)
    cats = Category.objects.all()
    return render(request,'ViewDetails.html',{"toy":toy,"cats":cats})

def login(request):
    if(request.method == "GET"):
        return render(request,"login.html",{})
    else:
        uname = request.POST["uname"]
        pwd = request.POST["pwd"]
        try: 
            user =  UserInfo.objects.get(username=uname,password=pwd)
        except:
            messages.error(request, 'Invalid username or password. Please try again.')
            return redirect(login)
        else:
            request.session["uname"] = uname
            return redirect(homepage)

def Signup(request):
    if(request.method == "GET"):
        return render(request,"Signup.html",{})
    else:
        uname = request.POST["uname"]
        pwd = request.POST["pwd"]
        rpwd = request.POST["rpwd"]
        email = request.POST["email"]
        try: 
            user =  UserInfo.objects.get(username=uname)
        except:
            if(rpwd == pwd):
                user = UserInfo(uname,pwd,email)
                user.save()
                return redirect(login)
            else:
                return redirect(Signup)
        else:
            return redirect(Signup)
        
def logout(request):
    request.session.clear()
    return redirect(homepage)

def AddToCart(request):
    if(request.method == "POST"):
        if("uname" in request.session):
            tid = request.POST["tid"]
            qty = request.POST["qty"]
            uname = request.session["uname"]
            try: 
                item = MyCart.objects.get(username = uname,id=tid)
            except:
                item = MyCart()
                item.user = UserInfo.objects.get(username = uname)
                item.Toy = Toy.objects.get(id = tid)
                item.qty = qty
                item.save()
                return redirect(ShowCart)
            else:
                return redirect(ShowCart)
        else:
            return redirect(login)
        
def ShowCart(request):
    items = MyCart.objects.filter(user = request.session["uname"])
    total = 0
    count = 0
    for item in items:
        total += item.qty * item.Toy.price
        count += 1
    request.session["count"] = count 
    request.session["total"] = total
    cats = Category.objects.all()
    return render(request,"ShowCart.html",{"items":items,"cats":cats})

def ModifyCart(request):
    action =request.POST["action"]
    tid = request.POST["tid"]
    item = MyCart.objects.get(user = request.session["uname"],Toy = tid)
    if(action == "Remove"):
        item.delete()
    else:
        item.qty = request.POST["qty"]
        item.save()
    return redirect(ShowCart)

def MakePayment(request):
    if(request.method == "GET"):
        return render(request,"MakePayment.html",{})
    else:
        cardno = request.POST["cardno"]
        cvv = request.POST["cvv"]
        expiry = request.POST["expiry"]
        try:
            buyer = Accounts.objects.get(cardno=cardno,cvv=cvv,expiry=expiry)
        except:
            return redirect(MakePayment)
        else:
            owner = Accounts.objects.get(cardno=222,cvv=222,expiry="12/2030")
            amount = request.session["total"]
            buyer.balance -= amount
            owner.balance += amount
            buyer.save()
            owner.save()
            order = OrderMaster()
            order.user = UserInfo.objects.get(username=request.session["uname"])
            order.amount = request.session["total"]
            details = []
            items = MyCart.objects.filter(user=request.session["uname"])
            for item in items:
                details.append(item.Toy.Toy_name)
                item.delete()
            order.details = ",".join(details)
            order.save()
            return redirect(homepage)

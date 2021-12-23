from django.http import HttpResponse
from django.shortcuts import render, redirect
from app.models import User, Product, Bid
from app.functions import gravatar_url
from django.core.files.storage import FileSystemStorage
import datetime
from django.db.models.aggregates import Max


#welcome page with email 
def landing(request):
    if request.session.has_key('email'):
        return redirect(dashboardView, user_id= User.objects.get(user_email = request.session['email']).id)
    else:
        return render(request, 'login.html')


# process login request
def loginRequest(request):
    #verify login request
    if request.method == 'POST':
        #search email in user database
        if User.objects.filter(user_email = request.POST.get('email')):
            #if true return dashboard
            request.session['email'] = request.POST.get('email')
            return redirect(dashboardView, user_id= User.objects.get(user_email = request.session['email']).id)
        else:
            #if not registered register user
            User.objects.create(user_email = request.POST.get('email'))
            request.session['email'] = request.POST.get('email')
            return redirect(dashboardView, user_id= User.objects.get(user_email = request.session['email']).id)
    else:
        return render(request, 'login.html')


#logout action
def logoutRequest(request):
    try:
        #delete user session
        if request.session.has_key('email'):
            del request.session["email"]
    except:
        pass
    return redirect("/app/login")


# dashboard page view
def dashboardView(request, user_id):
    #get dashboard page with user data
    if request.method == 'GET':
        if request.session.has_key('email'):
            if not user_id:
                user = User.objects.get(user_email=request.session['email'])
            else:
                user = User.objects.get(id=user_id)
                products = Product.objects.filter(bid_deadline__gt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S-06:00")).exclude(user_id=user_id)
        else:
            return redirect('/app/login')
    #load dashboard with user data
    return render(request, 'dashboard.html', {
        "avatar_url": gravatar_url(user.user_email, 64),
        "email": user.user_email,
        "products": products
    })


# dashboard redirect
def dashboardRedirect(request):
    if request.method == 'GET':
        if request.session.has_key('email'):
            user = User.objects.get(user_email=request.session['email'])
            return redirect(f"/app/dashboard/{user.id}")
        else:
            return redirect('/app/login')
            
    
# product upload
def addProduct(request):
    if request.session.has_key("email"):
        user = User.objects.get(user_email=request.session['email'])
        #handle get request
        if request.method == "GET":
            return render(request, "upload.html", {
                "user_id": user.id
            })
        #handle post request
        else:
            try:
                upload = request.FILES['photo']
                fss = FileSystemStorage()
                file = fss.save(upload.name, upload)
                file_url = fss.url(file)

                #create product
                Product.objects.create(
                    user_id = User.objects.get(user_email = request.session['email']),
                    name=request.POST.get('name'), 
                    description=request.POST.get('description'), 
                    photo=file_url,
                    minimum_bid=request.POST.get('min_bid'),
                    bid_deadline=datetime.datetime.strptime(request.POST.get('endtime'), "%Y-%m-%dT%H:%M").strftime("%Y-%m-%d %H:%M:%S-06:00")
                ).save()
            except:
                pass
            return redirect('/app/add/product')
    else:
        return redirect("/app/login") 


# get product details
def getProduct(request, product_id):
    if request.session.has_key("email"):
        user = User.objects.get(user_email=request.session['email'])
        product = Product.objects.filter(pk=product_id)
        bid = Bid.objects.filter(product_id=product_id).order_by("-ask_price")
        bid_available = False
        winner = None
        if product[0].bid_deadline > datetime.datetime.now(datetime.timezone.utc):
            bid_available = True
        else:
            winner = User.objects.get(pk=bid[0].user_id).first()
        return render(request, "product.html", {
            "user_id": user.id,
            "product": product[0],
            "bids": bid,
            "bid_available": bid_available,
            "winner": winner
        })
    else:
        return redirect("/app/login") 


# bid for product
def placeBid(request, product_id):
    if request.session.has_key("email"):
        user = User.objects.get(user_email=request.session['email'])
        product = Product.objects.get(pk=product_id)
        bid_count = Bid.objects.filter(product_id=product, bider=user).count()
        if bid_count > 0:
            Bid.objects.filter(product_id=product, bider=user).update(ask_price= request.POST.get("bid_price"))
        else:
            Bid.objects.create(
                product_id=product,
                bider= user,
                ask_price= request.POST.get("bid_price")
            ).save()
        return redirect(f"/app/get/product/{product_id}")
    else:
        return redirect("/app/login") 


# see all user products
def userProducts(request):
    if request.session.has_key("email"):
        user = User.objects.get(user_email=request.session['email'])
        products = Product.objects.filter(user_id = user.id)
        return render(request, "userproducts.html", {
            "avatar_url": gravatar_url(user.user_email, 64),
            "email": user.user_email,
            "user_id": user.id,
            "products": products
        })
    else:
        return redirect("/app/login")


# show winning bids
def bidWins(request):
    if request.session.has_key("email"):
        user = User.objects.get(user_email=request.session['email'])
        bids = Bid.objects.filter(bider=user.id)
        products = []
        for bid in bids:
            args = Bid.objects.filter(product_id=bid.product_id_id)
            maxVal = args.aggregate(Max('ask_price'))
            if bid.ask_price == maxVal["ask_price__max"] and bid.product_id.bid_deadline < datetime.datetime.now(datetime.timezone.utc):
                bid.product_id["winBy"] = bid.ask_price
                products.append(bid.product_id)
        return render(request, "winbids.html", {
            "avatar_url": gravatar_url(user.user_email, 64),
            "email": user.user_email,
            "user_id": user.id,
            "products": products
        })
    else:
        return redirect("/app/login")

    

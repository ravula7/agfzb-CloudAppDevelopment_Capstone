from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .models import CarModel, CarMake, CarDealer, DealerReview, ReviewPost
# from .restapis import related methods
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf,post_request, get_request
#get_dealer_by_id_from_cf,
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    return render(request,'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request,'djangoapp/contact.html')
# Create a `login_request` view to handle sign in request
def login_request(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            #messages.success(request, "Login successful!")
            return redirect('djangoapp:index')
        else:
            messages.warning(request, "Invalid username or password.")
            return redirect("djangoapp:index")


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    print("Log out the user `{}`".format(request.user.username))
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['pwd']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            user.is_superuser = True
            user.is_staff=True
            user.save()  
            login(request, user)
            return redirect("djangoapp:index")
        else:
            messages.warning(request, "The user already exists.")
            return redirect("djangoapp:registration")
# ...

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
     if request.method == "GET":
        context = {}
        url = "https://us-east.functions.appdomain.cloud/api/v1/web/eb5102a7-2e8e-4368-aa59-44294721901c/dealership-package/get-dealership"
        #"ravula7unc/dealerships/dealer-get"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        context["dealership_list"] = dealerships
        # Concat all dealer's short name
        # dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
    
        return render(request, 'djangoapp/index.html', context)

def get_dealer_by_id_from_cf(url, id):
    json_result = get_request(url, id=id)
    print('json_result from line 54',json_result)

    if json_result:
        dealers = json_result

        
        # print("line 70 restapis",json_result)
        dealer_doc = dealers
        print("0th address element line 73",dealers["address"])
        dealer_obj = CarDealer(address=dealers["address"], city=dealers["city"],
                                id=dealers["id"], lat=dealers["lat"], long=dealers["long"], full_name=dealers["full_name"],
                                
                                short_name=dealers["short_name"],st=dealers["st"], zip=dealers["zip"])
    return dealer_obj 


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, id):
    if request.method == "GET":
        context = {}
        dealer_url = "https://us-east.functions.appdomain.cloud/api/v1/web/eb5102a7-2e8e-4368-aa59-44294721901c/dealership-package/get-dealership"
        dealer = get_dealer_by_id_from_cf(dealer_url, id=id)
        context["dealer"] = dealer
    
        review_url = "https://us-east.functions.appdomain.cloud/api/v1/web/eb5102a7-2e8e-4368-aa59-44294721901c/dealership-package/get-review/"
        reviews = get_dealer_reviews_from_cf(review_url, id=id)
        #print(reviews)
        context["reviews"] = reviews
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
def add_review(request, id):
    context = {}
    dealer_url = "https://us-east.functions.appdomain.cloud/api/v1/web/eb5102a7-2e8e-4368-aa59-44294721901c/dealership-package/get-dealership"
    dealer = get_dealer_by_id_from_cf(dealer_url, id=id)
    context["dealer"] = dealer
    if request.method == 'GET':
        cars = CarModel.objects.all()
        print(cars)
        context["cars"] = cars
        
        return render(request, 'djangoapp/add_review.html', context)

    elif request.method == 'POST':
        if request.user.is_authenticated:
            username = request.user.username
            print(request.POST)
            json_payload = dict()
            car_id = request.POST["car"]
            car = CarModel.objects.get(pk=car_id)
            json_payload["time"] = datetime.utcnow().isoformat()
            json_payload["name"] = username
            json_payload["dealership"] = id
            json_payload["id"] = id
            json_payload["review"] = request.POST["content"]
            json_payload["purchase"] = False
            if "purchasecheck" in request.POST:
                if request.POST["purchasecheck"] == 'on':
                    json_payload["purchase"] = True
            json_payload["purchase_date"] = request.POST["purchasedate"]
            json_payload["car_make"] = car.make.name
            json_payload["car_model"] = car.name
            json_payload["car_year"] = int(car.year.strftime("%Y"))

            new_payload = {}
            new_payload["review"] = json_payload
            review_post_url = "https://us-east.functions.appdomain.cloud/api/v1/web/eb5102a7-2e8e-4368-aa59-44294721901c/dealership-package/post-review/"
            post_request(review_post_url, new_payload, id=id)
        return redirect("djangoapp:dealer_details", id=id)



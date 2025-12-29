import json
import logging

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import CarMake, CarModel
from .restapis import get_request, analyze_review_sentiments, post_review
from .populate import initiate

# Get an instance of a logger
logger = logging.getLogger(__name__)


def get_cars(request):
    """Return all car models; populate DB if empty."""
    if CarMake.objects.count() == 0:
        initiate()

    car_models = CarModel.objects.select_related("car_make")
    cars = [{"CarModel": cm.name,
             "CarMake": cm.car_make.name} for cm in car_models]

    return JsonResponse({"CarModels": cars})


@csrf_exempt
def login_user(request):
    """Handle user login request."""
    try:
        data = json.loads(request.body)
        username = data["userName"]
        password = data["password"]

        user = authenticate(username=username, password=password)
        result = {"userName": username}

        if user is not None:
            login(request, user)
            result["status"] = "Authenticated"

        return JsonResponse(result)

    except Exception as err:
        logger.error(f"Login error: {err}")
        return JsonResponse({"status": 400, "message": "Bad request"})


def logout_request(request):
    """Handle user logout request."""
    logout(request)
    return JsonResponse({"userName": ""})


@csrf_exempt
def registration(request):
    """Handle user registration request."""
    try:
        data = json.loads(request.body)
        username = data["userName"]
        password = data["password"]
        first_name = data["firstName"]
        last_name = data["lastName"]
        email = data["email"]

        if User.objects.filter(username=username).exists():
            return JsonResponse({"userName": username,
                                 "error": "Already Registered"})

        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email,
        )
        login(request, user)
        return JsonResponse({"userName": username, "status": "Authenticated"})

    except Exception as err:
        logger.error(f"Registration error: {err}")
        return JsonResponse({"status": 400, "message": "Bad request"})


def get_dealerships(request, state="All"):
    """Return list of dealerships; filter by state if provided."""
    endpoint = "/fetchDealers" if state == "All" else f"/fetchDealers/{state}"
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


def get_dealer_reviews(request, dealer_id):
    """Return all reviews for a given dealer with sentiment analysis."""
    if not dealer_id:
        return JsonResponse({"status": 400, "message": "Bad Request"})

    endpoint = f"/fetchReviews/dealer/{dealer_id}"
    reviews = get_request(endpoint)

    for review_detail in reviews:
        sentiment_response = analyze_review_sentiments(
            review_detail["review"]
        )
        review_detail["sentiment"] = sentiment_response.get(
            "sentiment",
            "neutral",
        )


    return JsonResponse({"status": 200, "reviews": reviews})


def get_dealer_details(request, dealer_id):
    """Return details of a given dealer."""
    if not dealer_id:
        return JsonResponse({"status": 400, "message": "Bad Request"})

    endpoint = f"/fetchDealer/{dealer_id}"
    dealership = get_request(endpoint)
    return JsonResponse({"status": 200, "dealer": dealership})


def add_review(request):
    """Submit a review; only allowed for logged-in users."""
    if request.user.is_anonymous:
        return JsonResponse({"status": 403,
                             "message": "Unauthorized"})

    try:
        data = json.loads(request.body)
        post_review(data)
        return JsonResponse({"status": 200})

    except Exception as err:
        logger.error(f"Add review error: {err}")
        return JsonResponse({"status": 401, 
                             "message": "Error in posting review"})

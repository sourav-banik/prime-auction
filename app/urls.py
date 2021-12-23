from django.urls import path
from app import views

urlpatterns = [

    # welcome page 
    path("", views.landing, name="landing"),
    path("login", views.loginRequest, name="login"),
    path("logout", views.logoutRequest, name="logout"),
    
    # user specific paths
    path("dashboard", views.dashboardRedirect, name="dashboardRedirect"),
    path("dashboard/<int:user_id>", views.dashboardView, name="dashboardView"),
    path("add/product", views.addProduct, name="addProduct"),
    path("get/product/<int:product_id>", views.getProduct, name="getProduct"),
    path("bid/product/<int:product_id>", views.placeBid, name="placeBid"),
    path("user/products", views.userProducts, name="userProducts"),
    path("user/bid/wins", views.bidWins, name="bidWins")

]
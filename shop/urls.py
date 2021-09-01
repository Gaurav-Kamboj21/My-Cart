from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.home, name="Home"),
    path("products/", views.index, name="products"),
    path("about/", views.about, name="AboutUs"),
    path("contact/", views.contact, name="ContactUs"),
    path("tracker/", views.tracker, name="TrackingStatus"),
    path("search/", views.search, name="Search"),
    path('products/<int:myid>', views.productView, name='ProductView'),
    path("checkout/", views.checkout, name="Checkout"),
    path("Signup/", views.signup, name="signup"),
    path("login/", views.logins, name="login"),
    path("logout/", views.logouts, name="logout"),
    path("handlerequest/", views.handlerequest, name="HandleRequest"),
    path('password_reset/',
         auth_views.PasswordResetView.as_view(),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
]

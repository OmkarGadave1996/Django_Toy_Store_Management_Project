from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage),
    path('ShowCakes/<id>',views.ShowToys),
    path('ViewDetails/<id>',views.ViewDetails),
    path('login',views.login),
    path('SignUp',views.Signup),
    path('Logout',views.logout),
    path('AddToCart',views.AddToCart),
    path('ShowCart',views.ShowCart),
    path('ModifyCart',views.ModifyCart),
    path('MakePayment',views.MakePayment)
]

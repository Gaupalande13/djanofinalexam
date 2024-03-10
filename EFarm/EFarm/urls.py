"""
URL configuration for EFarm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
 """
from django.contrib import admin
from django.urls import path, include
from django.urls import path
# from testapp3 import views
from django.conf.urls.static import static
from testapp4 import views
from .import settings 
from testapp4.views import Login,logout
from testapp4.views import Category
from testapp4.views import Cart
from testapp4.views import Checkout
from testapp4.views import OrderView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.signup, name='signup'),    
    path('login', Login.as_view(), name='login'),   
    path('in/', views.index, name='index'),    
    path('category/',Category.as_view(), name='category'),  
    path('logout/', logout, name='logout'), 
    path('cart/',Cart.as_view(), name='cart'),   
    path('checkout/',Checkout.as_view(), name='checkout'),   
    path('order/',OrderView.as_view(),name='order'),
    # path('search/',views.search,name='search'),
    path('contact/',views.contact, name='contact'),  

    path('payment/',views.payment, name='payment'),
    

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




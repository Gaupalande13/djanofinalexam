from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
#from .models import Product
# from .models import Product, ContactMessage
# # from .models import Product, CartItem
from django.core.exceptions import ValidationError
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from .models import Category as CategoryModel  # Assuming CategoryModel is your Django model for categories
from django.contrib.auth.hashers import check_password
from django.views import View
from . models import Product
from . models import Category
# from . models import SignupPage
# from . models import Cart
from . models import Customer
from . models import Orders
# from . models import Checkout
from django.db import IntegrityError
from datetime import datetime








def index(request):
    products = Product.get_all_products();
    print(products)
    return render(request, 'testapp/index.html')



class Category(View):
    @staticmethod
    def get_all_categories():
        # Retrieve all categories from the database using Django models
        return CategoryModel.objects.all()

    def post(self, request):
        product_id = request.POST.get('product')
        remove = request.POST.get('remove')

        # Initialize cart if it doesn't exist in the session
        cart = request.session.get('cart', {})

        if remove:
            if product_id in cart:
                if cart[product_id] > 1:
                    cart[product_id] -= 1
                else:
                    del cart[product_id]
        else:
            cart[product_id] = cart.get(product_id, 0) + 1

        # Update the cart in the session
        request.session['cart'] = cart

        return redirect('category')

    def get(self, request):
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        categories = Category.get_all_categories()
        category_id = request.GET.get('category')
        products = Product.get_products_by_category_id(category_id) if category_id else Product.get_all_products()

        # Pass 'cart' to the template context
        data = {'products': products, 'categories': categories, 'cart': request.session.get('cart', {})}
        print('you are : ', request.session.get('email'))
        return render(request, 'testapp/category.html', data)








# class Category(View):
#     @staticmethod
#     def get_all_categories():
#         # Retrieve all categories from the database using Django models
#         return CategoryModel.objects.all()

#     def post(self, request):
#         product = request.POST.get('product')
#         remove = request.POST.get('remove')
#         cart = request.session.get('cart',{})
#         quantity = cart.get(product)
#         cart[product] = quantity + 1 if quantity else 1
#         request.session['cart'] = cart
#         print('cart', request.session['cart'])
#         return redirect('index')

#     def get(self, request):
#        categories = Category.get_all_categories()
#        category_id = request.GET.get('category')
#        products = Product.get_products_by_category_id(category_id) if category_id else Product.get_all_products()

#        # Clear the 'cart' session key
#        request.session.pop('cart', None)

#        # Pass 'cart' to the template context
#        data = {'products': products, 'categories': categories, 'cart': request.session.get('cart', {})}
#        print('you are : ', request.session.get('username'))
#        return render(request, 'testapp/category.html', data)







# class Category(View):
#     def post(self,request):
#         product = request.POST.get('product')
#         remove = request.POST.get('remove')
#         cart = request.session.get('cart')
#         if cart:
#             quantity = cart.get(product)
#             if quantity:
#                 if remove:
#                     cart[product] = quantity-1
#                 else:
#                     cart[product] = quantity+1
#             else:
#                 cart[product] = 1
#         else:
#             cart = {}
#             cart[product] = 1





# def category(request):
#     products = None
#     categories = Category.get_all_categories()
#     categoryid = request.GET.get('category')
#     if categoryid:
#         products = Product.get_products_by_categoryid(categoryid)
#     else:
#         products = Product.get_all_products()

#     data = {}
#     data['products'] = products
#     data['categories'] = categories
#     print('you are : ',request.session.get('username'))
#     return render(request,'testapp/category.html',data)





def signup(request):
    if request.method == 'GET':
        return render(request, 'testapp/signup.html') 
    elif request.method == 'POST':
        postData = request.POST
        first_name = postData.get('fname')
        middle_name = postData.get('mname')
        last_name = postData.get('lname')
        age = postData.get('age')
        mob_no = postData.get('mob_no')
        dob = postData.get('dob')
        # username = postData.get('username')
        email = postData.get('email')
        password1 = postData.get('password1')

        # Form validation
        value = {'first_name' : first_name,'middle_name' :middle_name,'last_name':last_name,'age':age,'mobile_no':mob_no,'dob':dob,'email':email}
        error_message = None
        if not first_name:
            error_message = 'First Name Required!!'
        elif len(first_name) < 4:
            error_message = 'First Name must be 4 characters'
        elif not middle_name:
            error_message = 'Middle Name Required'
        elif len(middle_name) < 4:
            error_message = 'Middle Name must be 4 characters'
        elif not last_name:
            error_message = 'Last Name Required'
        elif len(last_name) < 4:
            error_message = 'Last Name must be 10 characters'
        elif not mob_no :
            error_message = 'Mobile no. Required'
        elif len(mob_no) < 10:
            error_message = 'Mobile no. must be 10 numbers'
        # elif not username :
        #     error_message = 'Username Required'
        # elif len(username) <= 10:
        #     error_message = 'Username must be 10 characters'
        elif len(password1) < 8:
            error_message = "password must be 8 character"
        elif len(email) < 5:
            error_message = "email must be 5 character "
        elif Customer.objects.filter(email=email).exists():  # Check if customer with email already exists
            error_message = 'Email already exists'
        

        if not dob:
            error_message = 'Date of birth is required.'
        else:
            try:
                # Validate the format of the date
                datetime.strptime(dob, '%Y-%m-%d')
            except ValueError:
                error_message = 'Date of birth must be in YYYY-MM-DD format.'

        if age and not age.isdigit():
            error_message = 'Age must be a valid number.'

        if error_message:
            return render(request, 'testapp/signup.html', {'error_message': error_message})

        try:
            # Data processing - create Customer instance and save
            customer = Customer(
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                age=int(age),
                mobile_no=mob_no,
                dob=dob,
                # username=username,
                email=email,
                password=password1
            )
            customer.password = make_password(customer.password)
            customer.register()
            data = {
                'values' : value
            }
        except ValidationError as e:
            return render(request, 'testapp/signup.html', {'error_message': e.message},data)
        except IntegrityError:
            return render(request, 'testapp/signup.html', {'error_message': 'Failed to save customer. Please try again.'},data)
        
        # If everything goes well, redirect to success page
        return redirect('index')  # Corrected redirect usage




class Login(View):
    def get(self, request):
        return render(request, 'testapp/login.html')

    def post(self, request):
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        customer = Customer.objects.filter(email=email).first()

        error_message = None
        if customer:
            flag = check_password(password1, customer.password)
            if flag:
                request.session['customer_id'] = customer.id
                request.session['email'] = customer.email

                return redirect('index')
            else:
                error_message = 'Email or password invalid'
        else:
            error_message = 'Email or password invalid'

        return render(request, 'testapp/login.html', {'error': error_message})




def logout(request):
    request.session.clear()
    return redirect('index')


class Cart(View):
    def get(self,request):
        ids = (list(request.session.get('cart')))
        products = Product.get_products_by_id(ids)
        print(products)
        return render(request,'testapp/cart.html',{'products' : products})


class Checkout(View):
    def post(self, request):
        address = request.POST.get('address')
        phoneno = request.POST.get('phone')
        customer = request.session.get('customer_id')
        cart = request.session.get('cart')
        products = Product.get_products_by_id(list(cart.keys()))
        print(address,phoneno,customer,cart,products)
        
        for product in products:
            order = Orders(customer = Customer(id = customer),
                         product = product,
                         quantity = cart.get(str(product.id)),
                         price = product.discounted_price,
                         address = address,
                         phone = phoneno)
            print(order.placeOrder());
            order.save()
        request.session['cart'] = {}
        return redirect('cart')


class OrderView(View):
    def get(self,request):
        customer = request.session.get('customer_id')
        orders = Orders.get_orders_by_customer(customer)
        print(orders)
        orders = orders.reverse()
        return render(request,'testapp/orders.html',{'orders':orders})

    
class PaymentView(View):
    def post(self, request):
        # Retrieve the customer's email, name, and amount from the form
        customer_email = request.POST.get('email')
        customer_name = request.POST.get('name')
        amount = int(request.POST.get('amount')) * 100  # Convert amount to paise (Razorpay accepts amount in smallest currency unit)

        # Initialize Razorpay client with your key ID and secret
        client = razorpay.Client(auth=(rzp_test_UpgBpE3lgKjfX6, ysfJXH48EZjz017WrZiQc2L6))

        # Create a Razorpay order
        order = client.order.create({
            'amount': amount,
            'currency': 'INR',  # Change currency as per your requirements
            'payment_capture': 1  # Automatically capture the payment after successful verification
        })
        print(customer_email,customer_name,amount)
        # Pass the order ID and other details to the template for redirection to Razorpay payment page
        return render(request, 'testapp/payment.html', {'order_id': order['id'], 'order_amount':order[amount], 'customer_email': customer_email, 'customer_name': customer_name})

    def get(self, request):
        # If the user tries to access the payment page directly via GET, redirect them to the homepage
        return redirect('index')





        
# def login(request):
#     if request.method == 'GET':
#         return render(request,'testapp/login.html')
#     else:
#         uname = request.POST.get('username')
#         pass1 = request.POST.get('password1')
#         customer = Customer.get_customer_by_username(uname)
#         error_message = None
#         if customer:
#             flag = check_username(uname)
#             if flag:
#                 return redirect('index')
#             else:
#                 error_message = 'Username or Password Invalid!!'

#         else:
#             error_message = 'Username or Password Invalid!!'

#         print(username,password)
#         return render(request,'testapp/login.html',{'error':error_message})


















# from django.core.exceptions import ObjectDoesNotExist

# def login(request):
#     error_message = None  # Initialize error_message variable
    
#     if request.method == 'GET':
#         return render(request, 'testapp/login.html', {'error_message': error_message})
#     elif request.method == 'POST':
#         username = request.POST.get('uname')
#         password = request.POST.get('pass1')
        
#         try:
#             customer = Customer.get_customer_by_username(username)
        
#         except ObjectDoesNotExist:
#             error_message = 'Invalid username or password.'  # Set error message
#             return render(request, 'testapp/login.html', {'error_message': error_message})

#         print(customer)
#         print(username, password)
        
#         # Assuming you want to render index.html after successful login
#         return redirect('index')





def contact(request):
    return render(request,'testapp/contact.html')

def payment(request):
    return render(request,'testapp/payment.html')



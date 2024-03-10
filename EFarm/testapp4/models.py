from django.db import models
from django.utils import timezone
# from django.db import Orders
import datetime

# Create your models here.




class Category(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name

    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    @staticmethod
    def get_all_categories_by_categoryid(category_id):
        if category_id:
            return Category.objects.filter(category = category_id)
        else:
            return Product.get_all_products();





class Product(models.Model):
    #pro_id = models.AutoField
    pro_name=models.CharField(max_length=25)
    selling_price = models.IntegerField()
    discounted_price = models.CharField(max_length=10)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,default=1)
    desc = models.CharField(max_length=200)
    product_image = models.ImageField(upload_to='uploads/to')

    # class Meta:
    #     app_label = 'testapp'  # Add this line with your app name

    def __str__(self):
        return self.pro_name

    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in = ids)




    @staticmethod
    def get_all_products():
        return Product.objects.all()

    
    @classmethod
    def get_products_by_categoryid(cls, category_id):
        # Implement logic to retrieve products by category ID
        return cls.objects.filter(category_id=category_id)



class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField()
    mobile_no = models.CharField(max_length=15)
    dob = models.DateField(max_length=8)
    # username = models.CharField(max_length=10)
    email = models.EmailField()
    password = models.CharField(max_length=500)

    def register(self):
        self.save()

    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email = email)
        except:
            return False
            

            

    def isExists(self):
        if Customer.objects.filter(email = self.email):
            return True

        return False


class Orders(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField(max_length=500,default='',blank=True)
    phone = models.CharField(max_length=10,default='',blank=True)
    date = models.DateTimeField(default=timezone.now)
    status = models.BooleanField(default='False')



    def placeOrder(self):
        self.save()

    @staticmethod 
    def get_orders_by_customer(customer_id):
        return Orders.objects.filter(customer = customer_id).order_by('date')


# class Checkout(models.Model):
#     # Define your fields here
#     pass
 
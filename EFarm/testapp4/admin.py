from django.contrib import admin
from testapp4.models import Product
from testapp4.models import Category
from testapp4.models import Customer
from testapp4.models import Orders



# # # Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display=['pro_name','selling_price','discounted_price','category','desc','product_image']
admin.site.register(Product,ProductAdmin)



class CategoryAdmin(admin.ModelAdmin):
    list_display=['name']
admin.site.register(Category,CategoryAdmin)


admin.site.register(Customer)

admin.site.register(Orders)








from django.contrib import admin
from .models import *

class ProductImageAdmin(admin.StackedInline):
    list_display = ['product_name','product_price']
    model =ProductImage

class ProductAdmin(admin.ModelAdmin):
    inlines =[ProductImageAdmin]
    readonly_fields = ['created_by','created_at']

    def save_model(self, request, obj, form, change):
        if not obj.created_by:  # Only set created_by if it's not already set
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)

class OrderedAdmin(admin.StackedInline):
    model = Ordered
    extra = 0
    readonly_fields = ['product', 'quantity', 'orderedby']

class OrderedByAdmin(admin.ModelAdmin):
    list_display = ['customer', 'order_date', 'process_status']
    inlines = [OrderedAdmin]
    readonly_fields = ['userprofile', 'address', 'date','total']

    def customer(self, obj):
        return obj.userprofile.user.username  # Assuming you have a user field in OrderedBy model

    def order_date(self, obj):
        return obj.date
    
    def process_status(self, obj):
        return "✅" if obj.process else "❌"

admin.site.register(OrderedBy, OrderedByAdmin)

admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(Favorite)
admin.site.register(Feedback)

class UserProfileAdmin(admin.ModelAdmin):
    readonly_fields = ['user','phone','address','rating','no_of_sales','total_sales','products_uploaded']

admin.site.register(UserProfile,UserProfileAdmin)




from django.forms import ModelForm
from .models import Product, Supplier, Brand, Category


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['description', 'price', 'stock', 'brand', 'categories',
                  'line', 'supplier', 'expiration_date', 'image', 'state','user']


class SupplierForm(ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'ruc', 'address', 'phone','user','image', 'state']
    


class BrandForm(ModelForm):
    class Meta:
        model = Brand
        fields = ['description', 'user', 'state']
        
class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['description', 'user', 'state']
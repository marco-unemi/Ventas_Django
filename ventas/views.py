from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Product, Company, Supplier, Brand, Category
from .forms import ProductForm, SupplierForm, BrandForm, CategoryForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import IntegrityError
from django.contrib import messages

# Create your views here.
def home(request):
    company = Company.objects.first()
    data = {
        'company': company,
    }
    return render(request, 'ventas/home.html', data)


def signup(request):
    if request.method == 'GET':
        return render(request, 'ventas/signup.html', {
            'form': UserCreationForm()
        })
    else:
        if request.method == 'POST':
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            if password1 and password2 and password1 == password2:
                try:
                    user = User.objects.create_user(username=request.POST['username'], password=password1)
                    user.save()
                    login(request, user)
                    return redirect('ventas:products')
                except IntegrityError:
                    return render(request, 'ventas/signup.html', {
                        'form': UserCreationForm(),
                        'error_message': 'Username already exists'
                    })
            else:
                return render(request, 'ventas/signup.html', {
                    'form': UserCreationForm(),
                    'error_message': 'Passwords do not match'
                })

def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'ventas/signin.html', {
            'form': AuthenticationForm()
        })
    else:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('ventas:products')
        else:
            return render(request, 'ventas/signin.html', {
                'form': AuthenticationForm,
                'error_message': 'Username or password is incorrect.'
            })
    

def products(request):
    company = Company.objects.first()
    products = Product.objects.all().order_by('id')
    brands = Brand.objects.all()
    categories = Category.objects.all()
    suppliers = Supplier.objects.all()
    users = User.objects.all()
    status_choices = Product.Status.choices
    
    if request.method == 'GET':
        query = request.GET.get('q')
        if query:
            products = products.filter(description__icontains=query)
            
        data = {
            "title1": "Productos",
            "title2": "Consulta De Productos",
            'form': ProductForm(),
            'products': products,
            'company': company,
            'brands': brands,
            'categories': categories,
            'suppliers': suppliers,
            'users': users,
            'status_choices': status_choices,
        }
        return render(request, 'ventas/products/products.html', data)
    
    elif request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ventas:products')
        else:
            products = Product.objects.all().order_by('id')  # Asegúrate de que los productos se vuelvan a cargar
            data = {
                'form': form,  # Enviar el formulario con errores
                'error_message': form.errors,
                'title1': "Productos",
                'title2': "Consulta De Productos",
                'products': products,
                'company': company,
                'brands': brands,
                'categories': categories,
                'suppliers': suppliers,
                'users': users,
                'status_choices': status_choices,
            }
            return render(request, 'ventas/products/products.html', data)
        
def view_product(request, product_id):
    company = Company.objects.first()
    product = get_object_or_404(Product, id=product_id)  # Fetch the specific product or return 404
    brands = Brand.objects.all()
    categories = Category.objects.all()
    suppliers = Supplier.objects.all()
    users = User.objects.all()
    status_choices = Product.Status.choices
     
    if request.method == 'GET':
        query = request.GET.get('q')
        if query:
            # Optionally filter related products based on the query
            related_products = Product.objects.filter(description__icontains=query).exclude(id=product_id)
        else:
            related_products = None

        return render(request, 'ventas/products/view_product.html', {
            'title1': "Producto",
            'title2': "Visualizar De Producto",
            'form': ProductForm(),
            'product': product,  # Pass the single product to the template
            'related_products': related_products,  # Pass related products if any
            'company': company,
            'brands': brands,
            'categories': categories,
            'suppliers': suppliers,
            'users': users,
            'status_choices': status_choices,
        })
        
def update_product(request, product_id):
    company = Company.objects.first()
    product = get_object_or_404(Product, pk=product_id)
    brands = Brand.objects.all()
    categories = Category.objects.all()
    suppliers = Supplier.objects.all()
    users = User.objects.all()
    status_choices = Product.Status.choices
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('ventas:products')
        else:
            return render(request, 'ventas/products/update_product.html', {
                'form': ProductForm(),
                'error_message': form.errors,
                'title1': "Productos",
                'title2': "Update Productos",
                'product': product,
                'company': company,
                'brands': brands,
                'categories': categories,
                'suppliers': suppliers,
                'users': users,
                'status_choices': status_choices,
            })
    else:
        form = ProductForm(instance=product)
        data = {
            'form': form,
            "title1": "Productos",
            "title2": "Update Productos",
            'product': product,
            'company': company,
            'brands': brands,
            'categories': categories,
            'suppliers': suppliers,
            'users': users,
            'status_choices': status_choices,
        }
        return render(request, 'ventas/products/update_product.html', data)
        
def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    company = Company.objects.first()
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('ventas:products')
    
    return render(request, 'ventas/products/delete_product.html', {
        'title1': "Products",
        'title2': "Delete Productos",
        'product': product,
        'company': company,
    })
    
    
def suppliers(request):
    company = Company.objects.first()
    suppliers = Supplier.objects.all().order_by('id')
    
    if request.method == 'GET':
        query = request.GET.get('q')
        if query:
            suppliers = suppliers.filter(ruc__icontains=query)
        data = {
            "title1": "Suppliers",
            "title2": "Consulta De Suppliers",
            "form": SupplierForm(),
            'suppliers': suppliers,
            'company': company,
        }
        return render(request, 'ventas/suppliers/suppliers.html', data)
    
    elif request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ventas:suppliers')
        else:
            print(form.errors)  # Añadir esto para ver errores en la consola
            data = {
                'form': form,  # Enviar el formulario con errores
                'error_message': form.errors,
                "title1": "Suppliers",
                "title2": "Consulta De Suppliers",
                'suppliers': suppliers,
                'company': company,
            }
            return render(request, 'ventas/suppliers/suppliers.html', data)  # Added return statement                                                                                                                                                                                                                              
    
def update_supplier(request, supplier_id):
    company = Company.objects.first()
    supplier = get_object_or_404(Supplier, pk=supplier_id)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('ventas:suppliers')
        else:
            return render(request, 'ventas/suppliers/update_supplier.html', {
                'form': SupplierForm(),
                'error_message': form.errors,
                'title1': "Suppliers",
                'title2': "Update Suppliers",
               'supplier': supplier,
                'company': company,
            })
    else:
        form = SupplierForm(instance=supplier)
        data = {
            'form': form,
            "title1": "Suppliers",
            "title2": "Update Suppliers",
           'supplier': supplier,
            'company': company,
        }
        return render(request, 'ventas/suppliers/update_supplier.html', data)
    
def delete_supplier(request, supplier_id):
    company = Company.objects.first()
    supplier = get_object_or_404(Supplier, pk=supplier_id)
    if request.method == 'POST':
        supplier.delete()
        messages.success(request, 'Supplier deleted successfully!')
        return redirect('ventas:suppliers')
    
    return render(request, 'ventas/suppliers/delete_supplier.html', {
        'title1': "Suppliers",
        'title2': "Eliminacion De Suppliers",
        'supplier': supplier,
        'company': company,
    })
    
    
def brands(request):
    company = Company.objects.first()
    brands = Brand.objects.all().order_by('id')
    users = User.objects.all()
    
    if request.method == 'GET':
        query = request.GET.get('q')
        if query:
            brands = brands.filter(name__icontains=query)
        data = {
            "title1": "Brands",
            "title2": "Brands Query",
            "form": BrandForm(),
            'brands': brands,
            'company': company,
            'users': users,
        }
        return render(request, 'ventas/brands/brands.html', data)
    elif request.method == 'POST':
        form = BrandForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ventas:brands')
        else:
            data={
                'form': form,  # Enviar el formulario con errores
                'error_message': form.errors,
                "title1": "Brands",
                "title2": "Brands Query",
                'brands': brands,
                'company': company,
                'users': users,
            }
            render(request, 'ventas/brands/brands.html', data)

def update_brand(request, brand_id):
    company = Company.objects.first()
    brand = get_object_or_404(Brand, pk=brand_id)
    users = User.objects.all()
    
    if request.method == 'POST':
        form = BrandForm(request.POST, instance=brand)
        if form.is_valid():
            form.save()
            return redirect('ventas:brands')
        else:
            return render(request, 'ventas/brands/update_brand.html', {
                'form': BrandForm(),
                'error_message': form.errors,
                'title1': "Brands",
                'title2': "Update Brands",
                'brand': brand,
                'company': company,
                'users': users,
            })
    else:
        form = BrandForm(instance=brand)
        data = {
            'form': form,
            "title1": "Brands",
            "title2": "Update Brands",
            'brand': brand,
            'company': company,
            'users': users,
        }
        return render(request, 'ventas/brands/update_brand.html', data)

def delete_brand(request, brand_id):
    company = Company.objects.first()
    brand = get_object_or_404(Brand, pk=brand_id)
    
    if request.method == 'POST':
        brand.delete()
        messages.success(request, 'Brand deleted successfully!')
        return redirect('ventas:brands')
    
    return render(request, 'ventas/brands/delete_brand.html', {
        'title1': "Brands",
        'title2': "Delete Brands",
        'brand': brand,
        'company': company,
    })


def categories(request):
    company = Company.objects.first()
    categories = Category.objects.all().order_by('id')
    users = User.objects.all()
    
    if request.method == 'GET':
        query = request.GET.get('q')
        if query:
            categories = categories.filter(name__icontains=query)
        data = {
            "title1": "Categories",
            "title2": "Categories Query",
            "form": CategoryForm(),
            'categories': categories,
            'company': company,
            'users': users,
        }
        return render(request, 'ventas/categories/categories.html', data)
    elif request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ventas:categories')
        else:
            data={
                'form': form,  # Enviar el formulario con errores
                'error_message': form.errors,
                "title1": "Categories",
                "title2": "Categories Query",
                'categories': categories,
                'company': company,
                'users': users,
            }
            render(request, 'ventas/categories/categories.html', data)

def update_category(request, category_id):
    company = Company.objects.first()
    category = get_object_or_404(Category, pk=category_id)
    users = User.objects.all()
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('ventas:categories')
        else:
            return render(request, 'ventas/categories/update_category.html', {
                'form': CategoryForm(),
                'error_message': form.errors,
                'title1': "Categories",
                'title2': "Update Categories",
                'category': category,
                'company': company,
                'users': users,
            })
    else:
        form = CategoryForm(instance=category)
        data = {
            'form': form,
            "title1": "Categories",
            "title2": "Update Categories",
            'category': category,
            'company': company,
            'users': users,
        }
        return render(request, 'ventas/categories/update_category.html', data)

def delete_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    company = Company.objects.first()
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('ventas:categories')
    
    return render(request, 'ventas/categories/delete_category.html', {
        'title1': "Categories",
        'title2': "Delete Categories",
        'category': category,
        'company': company,
    })

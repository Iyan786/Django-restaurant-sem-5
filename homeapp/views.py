from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate,login,logout,get_user_model
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from homeapp.forms import CategoryForm
from homeapp.forms import ProductForm
from homeapp.models import UserProfile,Book_Table,ItemList,Item,Tables,p_orders
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import JsonResponse
from django.contrib import messages
# Create your views here.

def index(request):
    return render(request,'dashboard.html')
def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            return HttpResponse("Your password and confirm password are not the same.")
        else:
            try:
                # Use the custom create_user method in UserProfileManager
                my_user = UserProfile.objects.create_user(username=uname, email=email, phone=phone, password=pass1)
                my_user.save()
                return redirect('home')  # Redirect to the home page after successful signup
            except Exception as e:
                return HttpResponse(f"Error: {str(e)}")

    return render(request, 'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)

        if user and user.is_superuser:
            login(request,user)
            return redirect('/dashboard/')
        
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse("Username or password is incorrect!!!")
        
    return render(request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')


def home(request):
    return render(request,'home.html')


def menu(request):
    category_name = request.GET.get('category')  # Get selected category from the query string
    if category_name:
        items = Item.objects.filter(Category__Category_name=category_name)  # Filter items by category
    else:
        items = Item.objects.all()  # Show all items if no category is selected

    paginator = Paginator(items, 6)  # Paginate the items (6 items per page)
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.get_page(page_number)  # Fetch the requested page
    except PageNotAnInteger:
        page_obj = paginator.page(1)  # If page is not an integer, show the first page
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)  # If page is out of range, show the last page

    categories = ItemList.objects.all()  # Fetch all categories for the filter menu
    return render(request, 'menu.html', {
        'categories': categories,
        'page_obj': page_obj,
    })
    
def productdetail(request, id):
    items = get_object_or_404(Item, id=id)
    category = ItemList.objects.all()
    
    if request.method == 'POST':
        counter_value = int(request.POST.get('counter_value', 1))  # Default to 1 if not provided
        item = get_object_or_404(Item, pk=id)
        
        # Calculate total price
        total_price = item.Price * counter_value
        
        # Hidden input for order status (default to "Pending")
        order_status = request.POST.get('order_status', 'Pending')  # Default order status

        # Store the order in the Orders model
        order = p_orders.objects.create(
            user=request.user,
            item=item,
            quantity=counter_value,
            total_price=total_price,
            order_status=order_status  # Save the order status
        )
        order.save()

        # Optional: Redirect to an order confirmation page or return a success message
        #return redirect('order_confirmation')  # Adjust this to your actual confirmation page

    # Render the product detail page if not POST
    return render(request, 'productdetail.html', {'items': items, 'category': category})

def about(request):
    return render(request,'about.html')

def orders(request):
    order = p_orders.objects.filter(user=request.user)  # Filter by the logged-in user
    paginator = Paginator(order, 5)  # Show 10 orders per page (change `orders` to `order`)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    
    return render(request, 'orders.html', context)

def aorder(request):
    order = p_orders.objects.all()
    Users = UserProfile.objects.all()
    paginator = Paginator(order, 5)  # Show 5 objects per page

    page_number = request.GET.get('page')  # Get the page number from the query parameters
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)  # Deliver first page if page is not an integer
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)  # Deliver last page if out of range

    return render(request, 'dashboard/aorder.html', {'page_obj': page_obj})


def update_order_status(request, id):
    if request.method == 'POST':
        order = get_object_or_404(p_orders, id=id)
        new_status = request.POST.get('order_status')

        # Update the order status
        order.order_status = new_status
        order.save()

        # Redirect to the order list or details page
        return redirect('aorder')  # Replace 'order_list' with the actual name of your order list view

    # If not a POST request, redirect to the order list (or handle this as needed)
    return redirect('aorder') 

def cancel_order(request, id):
    if request.method == 'POST':
        order = get_object_or_404(p_orders, id=id)
        order.order_status = "Canceled"
        order.save()
        return JsonResponse({'status': 'success', 'new_status': order.order_status})
    return JsonResponse({'status': 'fail'})

def contact(request):
    return render(request,'contact.html')


def order(request):
    return render(request,'order.html')

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Tables  # Replace with your actual table model

@login_required
def book_table(request):
    user = request.user

    # Check if all tables are reserved
    all_tables_reserved = not Tables.objects.filter(status='Booked').exists()

    if request.method == 'POST':
        # Fetch details from the form
        time = request.POST.get('time')
        special_requests = request.POST.get('special_requests')
        preference = request.POST.get('preference')
        occasion = request.POST.get('occasion')
        person = request.POST.get('person')
        date = request.POST.get('date')

        # Find the first available "Booked" table to update
        table_to_update = Tables.objects.filter(status='Booked').first()

        if table_to_update:
            # Update only the specific row
            table_to_update.name = user.username
            table_to_update.email = user.email
            table_to_update.person = person
            table_to_update.date = date
            table_to_update.time = time
            table_to_update.special_requests = special_requests
            table_to_update.preference = preference
            table_to_update.occasion = occasion
            table_to_update.status = 'reserved'  # Change status to Reserved
            table_to_update.save()

            messages.success(request, 'Your table has been reserved successfully!')
            return redirect('book_table')

        else:
            # If no tables are available, show the popup
            messages.error(request, 'No available tables to reserve. Please try again later.')
            return render(request, 'book_table.html', {'all_tables_reserved': True})

    return render(request, 'book_table.html', {'all_tables_reserved': False})



def display_user(request):
    Users = UserProfile.objects.all()
    paginator = Paginator(Users, 5)  # Show 5 objects per page

    page_number = request.GET.get('page')  # Get the page number from the query parameters
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)  # Deliver first page if page is not an integer
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)  # Deliver last page if out of range

    return render(request, 'dashboard/user.html', {'page_obj': page_obj,'Users':Users})

def tables(request):
    tables = Tables.objects.all()
    Users = UserProfile.objects.all()
    paginator = Paginator(tables, 5)  # Show 5 objects per page

    page_number = request.GET.get('page')  # Get the page number from the query parameters
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)  # Deliver first page if page is not an integer
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)  # Deliver last page if out of range

    return render(request, 'dashboard/tables.html', {'page_obj': page_obj,'Users':Users})

def table_manage(request):
    tables = Tables.objects.all()
    paginator = Paginator(tables, 5)  # Show 5 objects per page

    page_number = request.GET.get('page')  # Get the page number from the query parameters
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)  # Deliver first page if page is not an integer
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)  # Deliver last page if out of range

    return render(request, 'dashboard/table_manage.html', {'page_obj': page_obj})

@login_required
def add_empty_table(request):
    # Create a new table instance with all fields set to None
    table = Tables.objects.create(
        name=None,
        email=None,
        person=None,
        date=None,
        time=None,
        special_requests=None,
        preference=None,
        occasion=None,
        status="Booked"
    )

    # Save the new table instance
    table.save()

    # Redirect to a page (replace 'table_list' with your desired URL name)
    return redirect('table_manage')

def update_table_status(request, id):
    if request.method == 'POST':
        # Fetch the table object by ID
        table = get_object_or_404(Tables, id=id)

        # Get the new status from the form
        new_status = request.POST.get('order_status')

        # Check and update only if the new status is valid
        valid_statuses = ['Booked', 'reserved']  # Add any additional statuses here
        if new_status in valid_statuses:
            table.status = new_status
            
            # Set all other fields (except specific ones) to None if the status is 'Booked'
            if new_status == 'Booked':
                for field in table._meta.fields:
                    if field.name not in ['status', 'id']:  # Skip 'status' and 'id'
                        # Check if the field is editable and nullable before updating
                        if field.editable and field.null:
                            setattr(table, field.name, None)
            
            table.save()

        # Redirect to the 'tables' view after updating
        return redirect('tables')

def display_category(request):
    category = ItemList.objects.all()
    paginator = Paginator(category, 5)  # Show 5 objects per page

    page_number = request.GET.get('page')  # Get the page number from the query parameters
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)  # Deliver first page if page is not an integer
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)  # Deliver last page if out of range

    return render(request, 'dashboard/category.html', {'page_obj': page_obj})

def display_product(request):
    product = Item.objects.all()
    paginator = Paginator(product, 5)  # Show 5 objects per page

    page_number = request.GET.get('page')  # Get the page number from the query parameters
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)  # Deliver first page if page is not an integer
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)  # Deliver last page if out of range

    return render(request, 'dashboard/product.html', {'page_obj': page_obj})

@login_required(login_url="/login")
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/display_category/')  # Replace 'category_list' with the name of your category list view
    else:
        form = CategoryForm()
    return render(request, 'dashboard/add_category.html', {'form': form})

@login_required(login_url="/login")
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/display_product/')  # Replace 'category_list' with the name of your category list view
    else:
       form = ProductForm()
    return render(request, 'dashboard/add_product.html', {'form': form})

@login_required(login_url="/login")
def pro_delete(request, id):
    product = get_object_or_404(Item, id=id)
    if request.method == 'POST':
        product.delete()
        return redirect('/display_product/')
    return render(request, 'dashboard/product_confirm_delete.html', {'product': product})
    
@login_required(login_url="/login")
def table_delete(request, id):
    Table = get_object_or_404(Tables, id=id)
    if request.method == 'POST':
        Table.delete()
        return redirect('/table_manage/')
    return render(request, 'dashboard/table_delete.html', {'Table': Table})

@login_required(login_url="/login")
def edit_product(request, id):
    product = get_object_or_404(Item, id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('/display_product')
    else:
        form = ProductForm(instance=product)
    return render(request, 'dashboard/add_product.html', {'form': form})
 
@login_required(login_url="/login")
def cat_delete(request, id):
    category = get_object_or_404(ItemList, id=id)
    if request.method == 'POST':
        category.delete()
        return redirect('/display_category')
    return render(request, 'dashboard/category_confirm_delete.html', {'category': category})
                                                                  
@login_required(login_url="/login")
def edit_category(request, id):
    category = get_object_or_404(ItemList, id=id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect('/display_category')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'dashboard/category_edit.html', {'form': form})

def download_bill(request, order_id):
    # Get the order object
    order = p_orders.objects.get(id=order_id)

    # Load the template
    template = get_template('bill_template.html')
    context = {'order': order}

    # Render the template with order data
    html = template.render(context)

    # Create a response object
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="order_bill.pdf"'

    # Generate the PDF using xhtml2pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response
    )

    # If there was an error in PDF generation, return error
    if pisa_status.err:
        return HttpResponse('We had some errors with the PDF generation <pre>' + html + '</pre>')

    return response
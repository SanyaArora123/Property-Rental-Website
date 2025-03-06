# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, SellerRegistrationForm, PropertyForm
from .models import Property, Seller
from django.contrib.auth import authenticate, login, logout

def home(request):
    properties = Property.objects.all()
    
    # If fewer than 3 properties with image1, fill with all properties
    if len(properties) < 3:
        properties = list(properties) + list(
            Property.objects.exclude(
                id__in=[p.Pid for p in properties]
            )[:3 - len(properties)]
        )
    
    # Get unique states and cities for dropdowns
    states = Property.objects.values_list('state', flat=True).distinct()
    cities = Property.objects.values_list('city', flat=True).distinct()
    
    return render(request, 'myapp/home.html', {
        'properties': properties,
        'states': states,
        'cities': cities
    })

def search(request):
    # Start with all properties
    properties = Property.objects.all()
    
    # Price Range Filter
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price and max_price:
        properties = properties.filter(
            rental_amount__gte=min_price, 
            rental_amount__lte=max_price
        )
    elif min_price:
        properties = properties.filter(rental_amount__gte=min_price)
    elif max_price:
        properties = properties.filter(rental_amount__lte=max_price)

    # Property Type Filter
    property_type = request.GET.get('property_type')
    if property_type:
        properties = properties.filter(property_type=property_type)

    # Area Range Filter
    min_area = request.GET.get('min_area')
    max_area = request.GET.get('max_area')
    if min_area and max_area:
        properties = properties.filter(
            area_sqft__gte=min_area, 
            area_sqft__lte=max_area
        )
    elif min_area:
        properties = properties.filter(area_sqft__gte=min_area)
    elif max_area:
        properties = properties.filter(area_sqft__lte=max_area)

    # State Filter
    state = request.GET.get('state')
    if state:
        properties = properties.filter(state=state)

    # City Filter
    city = request.GET.get('city')
    if city:
        properties = properties.filter(city=city)

    # Pincode Filter
    pincode = request.GET.get('pincode')
    if pincode:
        properties = properties.filter(pincode=pincode)

    # Get unique states and cities for dropdowns
    states = Property.objects.values_list('state', flat=True).distinct()
    cities = Property.objects.values_list('city', flat=True).distinct()

    context = {
        'properties': properties,
        'states': states,
        'cities': cities,
    }

    return render(request, 'myapp/home.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}. You can now log in.')
            return redirect('loginUser')
    else:
        form = UserRegistrationForm()
    return render(request, 'myapp/register.html', {'form': form})

def property_detail(request,Pid):
    rent = get_object_or_404(Property,id=Pid)
    return render(request, 'myapp/property_detail.html', {'rent': rent})

def logOut(request):
    logout(request)
    return redirect('home')

def loginUser(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
    return render(request, "myapp/loginUser.html")
@login_required
def become_seller(request):
    # Check if user is already a seller
    if hasattr(request.user, 'seller'):
        messages.info(request, 'You are already registered as a seller.')
        return redirect('home')
    
    if request.method == 'POST':
        form = SellerRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            seller = form.save(commit=False)
            seller.user = request.user
            seller.save()
            messages.success(request, 'You are now registered as a seller!')
            return redirect('home')
    else:
        form = SellerRegistrationForm()
    
    return render(request, 'myapp/become_seller.html', {'form': form})

@login_required
def properties_list(request):
    # Get all properties sorted by creation date
    properties = Property.objects.all().order_by('-created_at')
    
    # Set up pagination - 3 properties per page
    paginator = Paginator(properties, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'properties': properties,  # Keep original queryset for backward compatibility
        'page_obj': page_obj,      # Add paginated object for the template
    }
    
    return render(request, 'myapp/properties_list.html', context)




@login_required
def add_property(request):
    # Check if user is a seller
    try:
        seller = request.user.seller
    except Seller.DoesNotExist:
        messages.warning(request, 'You need to register as a seller first.')
        return redirect('become_seller')
    
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property = form.save(commit=False)
            property.seller = seller
            property.save()
            messages.success(request, 'Property added successfully!')
            return redirect('home')
    else:
        form = PropertyForm()
    
    return render(request, 'myapp/add_property.html', {'form': form})
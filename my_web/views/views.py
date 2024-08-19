from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from my_web.models import Customer
from my_web.forms import CustomerModelForm
from django.core.paginator import Paginator


# Create your views here.


def project_management(request):
    return render(request, 'my_web/project-management.html')


def customers(request):
    search = request.GET.get('search')
    filter_date = request.GET.get('filter', '')
    customers = Customer.objects.all()
    paginator = Paginator(customers, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if search:
        page_obj = page_obj.filter(Q(full_name__icontains=search) | Q(email__icontains=search))
    if filter_date == 'filter_date':
        page_obj = customers.order_by('-created_at')
    context = {'customers': page_obj}
    return render(request, 'my_web/customers.html', context)


def customer_details(request, customer_slug):
    customer = Customer.objects.get(slug=customer_slug)
    context = {'customer': customer}
    return render(request, 'my_web/customer-details.html', context)


def profile(request):
    return render(request, 'my_web/profile.html')


def profile_settings(request):
    return render(request, 'my_web/settings.html')


def add_customer(request):
    form = CustomerModelForm()
    if request.method == 'POST':
        form = CustomerModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('customers')

    context = {'form': form}

    return render(request, 'my_web/add-customer.html', context)


def edit_customer(request, customer_slug):
    customer = get_object_or_404(Customer, slug=customer_slug)
    form = CustomerModelForm(instance=customer)
    if request.method == 'POST':
        form = CustomerModelForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customers', )
    return render(request, 'my_web/settings.html', {'form': form, 'customer': customer})


def delete_customer(request, customer_slug):
    customer = get_object_or_404(Customer, slug=customer_slug)
    if customer:
        customer.delete()
        return redirect('customers')

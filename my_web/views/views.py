from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.views import View
from django.core.paginator import Paginator
from tablib import Dataset

from my_web.resources import CustomerResource
from my_web.models import Customer
from my_web.forms import CustomerModelForm


# Create your views here.


def project_management(request):
    return render(request, 'my_web/project-management.html')


# def customers(request):
#     search = request.GET.get('search')
#     filter_date = request.GET.get('filter', '')
#     customers = Customer.objects.all()
#     paginator = Paginator(customers, 2)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     if search:
#         page_obj = page_obj.filter(Q(full_name__icontains=search) | Q(email__icontains=search))
#     if filter_date == 'filter_date':
#         page_obj = customers.order_by('-created_at')
#     context = {'customers': page_obj}
#     return render(request, 'my_web/customers.html', context)


class CustomerListView(View):
    def get(self, request):
        search = request.GET.get('search')
        filter_date = request.GET.get('filter', '')
        customers = Customer.objects.all()
        paginator = Paginator(customers, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        if search:
            customers = customers.filter(Q(full_name__icontains=search) | Q(email__icontains=search))
        if filter_date == 'filter_date':
            page_obj = customers.order_by('-created_at')
        context = {'customers': page_obj}
        return render(request, 'my_web/customers.html', context)


# def customer_details(request, customer_slug):
#     customer = Customer.objects.get(slug=customer_slug)
#     context = {'customer': customer}
#     return render(request, 'my_web/customer-details.html', context)


class CustomerDetailsView(View):
    def get(self, request, *args, **kwargs):
        customer_slug = kwargs['customer_slug']
        customer = Customer.objects.get(slug=customer_slug)
        context = {'customer': customer}
        return render(request, 'my_web/customer-details.html', context)


def profile(request):
    return render(request, 'my_web/profile.html')


def profile_settings(request):
    return render(request, 'my_web/settings.html')


# def add_customer(request):
#     form = CustomerModelForm()
#     if request.method == 'POST':
#         form = CustomerModelForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('customers')
#
#     context = {'form': form}
#
#     return render(request, 'my_web/add-customer.html', context)


class CustomerCreateView(View):
    def get(self, request):
        form = CustomerModelForm()
        context = {'form': form}
        return render(request, 'my_web/add-customer.html', context)

    def post(self, request):
        form = CustomerModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('customers')


# def edit_customer(request, customer_slug):
#     customer = get_object_or_404(Customer, slug=customer_slug)
#     form = CustomerModelForm(instance=customer)
#     if request.method == 'POST':
#         form = CustomerModelForm(request.POST, request.FILES, instance=customer)
#         if form.is_valid():
#             form.save()
#             return redirect('customers', )
#     return render(request, 'my_web/settings.html', {'form': form, 'customer': customer})


class CustomerUpdateView(View):
    def get(self, request, customer_slug):
        customer = get_object_or_404(Customer, slug=customer_slug)
        form = CustomerModelForm(instance=customer)
        context = {'customer': customer, 'form': form}
        return render(request, 'my_web/settings.html', context)

    def post(self, request, customer_slug):
        customer = get_object_or_404(Customer, slug=customer_slug)
        form = CustomerModelForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

            return redirect('customer_details', customer.slug)


# def delete_customer(request, customer_slug):
#     customer = get_object_or_404(Customer, slug=customer_slug)
#     if customer:
#         customer.delete()
#         return redirect('customers')


class CustomerDeleteView(View):
    def get(self, request, customer_slug):
        customer = get_object_or_404(Customer, slug=customer_slug)
        if customer:
            customer.delete()
            return redirect('customers')


# def export_data(request):
#     export_format = request.GET.get('format')
#     customer_resource = CustomerResource()
#     dataset = customer_resource.export()
#     response = HttpResponse(dataset, content_type=format)
#     date = datetime.now().strftime("%Y-%m-%d")
#     if export_format == 'csv':
#         response = HttpResponse(dataset.csv, content_type='text/csv')
#         response['Content-Disposition'] = f'attachment; filename="{Customer._meta.object_name}-{date}.csv"'
#
#     elif export_format == 'json':
#         response = HttpResponse(dataset.json, content_type='application/json')
#         response['Content-Disposition'] = f'attachment; filename="{Customer._meta.object_name}-{date}.json"'
#
#     elif export_format == 'xls':
#         response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
#         response['Content-Disposition'] = f'attachment; filename="{Customer._meta.object_name}-{date}.xls"'
#
#     elif export_format == 'yaml':
#         response = HttpResponse(dataset.yaml, content_type='application/yaml')
#         response['Content-Disposition'] = f'attachment; filename="{Customer._meta.object_name}-{date}.yaml"'
#
#     return response


class ExportDataView(View):
    def get(self, request, *args, **kwargs):
        export_format = request.GET.get('format')
        customer_resource = CustomerResource()
        dataset = customer_resource.export()
        response = HttpResponse(dataset, content_type=format)
        date = datetime.now().strftime("%Y-%m-%d")
        if export_format == 'csv':
            response = HttpResponse(customer_resource.export(), content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{Customer._meta.object_name}-{date}.csv"'
        elif export_format == 'json':
            response = HttpResponse(dataset.json, content_type='application/json')
            response['Content-Disposition'] = f'attachment; filename="{Customer._meta.object_name}-{date}.json"'

        elif export_format == 'xls':
            response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = f'attachment; filename="{Customer._meta.object_name}-{date}.xls"'

        elif export_format == 'yaml':
            response = HttpResponse(dataset.yaml, content_type='application/yaml')
            response['Content-Disposition'] = f'attachment; filename="{Customer._meta.object_name}-{date}.yaml"'

        return response

# def import_data(request):
#     if request.method == 'POST':
#         format = request.GET.get('format')
#         customer_resource = CustomerResource()
#         dataset = Dataset()
#         new_employees = request.FILES['importData']
#
#         if format == 'CSV':
#             imported_data = dataset.load(new_employees.read().decode('utf-8'), format='csv')
#             result = customer_resource.import_data(dataset, dry_run=True)
#         elif format == 'JSON':
#             imported_data = dataset.load(new_employees.read().decode('utf-8'), format='json')
#             result = customer_resource.import_data(dataset, dry_run=True)
#
#         if not result.has_errors():
#             # Import now
#             customer_resource.import_data(dataset, dry_run=False)
#
#     return render(request, 'import.html')

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import View
from django.views.generic import CreateView, UpdateView, DetailView, ListView, TemplateView, DeleteView
from product.forms import ProductModelForm
from product.models import Product, ProductAttribute
from django.urls import reverse_lazy


# Create your views here.


# def product_list(request):      ->->-> vell done!
#     products = Product.objects.all()
#     product_attributes = ProductAttribute.objects.all()
#     paginator = Paginator(products, 3)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     context = {'products': page_obj,
#                'attributes': product_attributes}
#     return render(request, 'product/product-list.html', context)


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    paginate_by = 2
    context_object_name = 'product'
    template_name = 'product/product-list.html'

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        products = self.get_queryset()
        page = self.request.GET.get('page')
        paginator = Paginator(products, self.paginate_by)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        context['products'] = products
        return context


# def add_product(request):     ->->-> vell done!
#     form = ProductModelForm()
#     if request.method == 'POST':
#         form = ProductModelForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('product_list')
#
#     context = {'form': form}
#     return render(request, 'product/add-product.html', context)


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = 'product/add-product.html'
    fields = ['name', 'price', 'category', 'description', 'discount', 'quantity', 'image']
    success_url = reverse_lazy('product_list')

    # def form_valid(self, form):
    #     form.instance.author = self.request.user
    #     return super().form_valid(form)


# def edit_product(request, product_slug):   ->->-> vell done!
#     product = get_object_or_404(Product, slug=product_slug)
#     form = ProductModelForm(instance=product)
#     if request.method == 'POST':
#         form = ProductModelForm(request.POST, request.FILES, instance=product)
#         if form.is_valid():
#             form.save()
#             return redirect('product_list')
#     return render(request, 'product/edit-product.html', {'form': form})


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'product/edit-product.html'
    slug_field = 'slug'
    slug_url_kwarg = 'product_slug'
    context_object_name = 'product'
    fields = ['name', 'price', 'category', 'description', 'discount', 'quantity', 'image']
    success_url = reverse_lazy('product_list')


# def delete_product(request, product_slug):   ->->-> vell done!
#     product = get_object_or_404(Product, slug=product_slug)
#     if product:
#         product.delete()
#         return redirect('product_list')


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'product/delete-product.html'
    slug_field = 'slug'
    slug_url_kwarg = 'product_slug'
    context_object_name = 'product'
    success_url = reverse_lazy('product_list')


# def product_detail(request, product_slug):    ->->-> vell done!
#     product = Product.objects.get(slug=product_slug)
#     context = {'product': product}
#     return render(request, 'product/product-details.html', context)


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'product/product-details.html'
    slug_field = 'slug'
    slug_url_kwarg = 'product_slug'
    context_object_name = 'product'

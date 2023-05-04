from django.db.models import Q
from django.shortcuts import render, redirect

from products.forms import ProductCreateForm, ReviewCreateForm
from products.models import Product, Review
from products.constants import PAGINATION_LIMIT


def main_page_view(request):
    if request.method == 'GET':
        context = {
            'user': request.user
        }
        return render(request, 'layouts/index.html', context=context)


def products_view(request):
    if request.method == 'GET':
        products = Product.objects.all()
        search = request.GET.get('search')
        page = int(request.GET.get('page', 1))

        max_page = products.__len__() / PAGINATION_LIMIT
        if round(max_page) < max_page:
            max_page = round(max_page) + 1
        else:
            max_page = round(max_page)

        products = products[PAGINATION_LIMIT * (page-1):PAGINATION_LIMIT * page]

        if search:
            products = products.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search))

        context = {
            'products': products,
            'user': request.user,
            'pages': range(1, max_page+1)
        }

        return render(request, 'products/products.html', context=context)


def products_detail_view(request, id):
    if request.method == 'GET':
        product = Product.objects.get(id=id)
        context = {
            'product': product,
            'review': product.review_set.all(),
            'user': request.user
        }
        return render(request, 'products/detail.html', context=context)

    if request.method == 'POST':
        form = ReviewCreateForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            text = form.cleaned_data['text']
            review = Review(name=name, text=text)
            review.save()
    else:
        form = ReviewCreateForm()
    reviews = Review.objects.all()
    return render(request, 'products/detail.html', context={
        'form': form,
        'reviews': reviews
    })


def product_create_view(request):
    if request.method == 'GET':
        context = {
            'form': ProductCreateForm
        }
        return render(request, 'products/create.html', context=context)

    if request == 'PRODUCT':
        data, files = request.PRODUCT, request.FILES
        form = ProductCreateForm(data, files)

        if form.is_valid():
            Product.objects.create(
                image=form.cleaned_data.get('image'),
                title=form.cleaned_data.get('title'),
                description=form.cleaned_data.get('description'),
                best_before_date=form.cleaned_data.get('best_before_date')
            )

            return redirect('/products/')

        return render(request, 'products/detail.html', context={
            'form': form
        })


def product_detail_view(request):
    return None
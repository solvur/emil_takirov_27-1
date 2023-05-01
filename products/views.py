from django.shortcuts import render, redirect

from products.forms import ProductCreateForm, ReviewCreateForm
from products.models import Product, Review


def main_page_view(request):
    if request.method == 'GET':
        context = {
            'user': request.user
        }
        return render(request, 'layouts/index.html', context=context)


def products_view(request):
    if request.method == 'GET':
        products = Product.objects.all()

        context = {
            'products': products,
            'user': request.user
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
    return render(request, 'products/detail.html', {'form': form, 'reviews': reviews})


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


# def review_create_view(request):
#     if request.method == 'GET':
#         context = {
#             'form': ReviewCreateForm
#         }
#         return render(request, 'products/create.html', context=context)
#
#     if request.method == 'PRODUCT':
#         form = ReviewCreateForm(data=request)
#
#         if form.is_valid():
#             Review.objects.create(
#                 text=form.cleaned_data.get('text')
#             )
#
#             return redirect('/products/')
#
#         return render(request, '/products/', context={
#             'form': form
#         })
def product_detail_view(request):
    return None
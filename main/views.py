from django.shortcuts import render, get_object_or_404
from django.db import models
from django.core.paginator import Paginator
from .models import Category, Product


def product_list(request, category_slug=None):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    category = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # Обработка поиска
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(
            models.Q(name__icontains=search_query) | 
            models.Q(description__icontains=search_query)
        )
    
    # Обработка сортировки
    sort_by = request.GET.get('sort', 'name')
    if sort_by == 'name':
        products = products.order_by('name')
    elif sort_by == '-name':
        products = products.order_by('-name')
    elif sort_by == 'price':
        products = products.order_by('price')
    elif sort_by == '-price':
        products = products.order_by('-price')
    elif sort_by == 'created':
        products = products.order_by('created')
    elif sort_by == '-created':
        products = products.order_by('-created')
    else:
        products = products.order_by('name')
    
    # Пагинация
    paginator = Paginator(products, 9)  # 9 товаров на страницу
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    
    return render(request, 'main/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products,
                   'current_sort': sort_by,
                   'search_query': search_query})


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    related_products = Product.objects.filter(category=product.category,
                                              available=True).exclude(id=product.id)[:4]
    return render(request, 'main/product/detail.html', {'product': product,
                                                        'related_products': related_products})

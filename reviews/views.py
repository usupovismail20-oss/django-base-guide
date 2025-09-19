from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Avg, Count
from main.models import Product
from .models import Review
from .forms import ReviewForm


def review_list(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product, is_approved=True).select_related('user')
    
    # Пагинация
    paginator = Paginator(reviews, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Статистика отзывов
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    rating_counts = reviews.values('rating').annotate(count=Count('rating')).order_by('rating')
    
    # Создаем словарь для удобного отображения
    rating_stats = {i: 0 for i in range(1, 6)}
    for item in rating_counts:
        rating_stats[item['rating']] = item['count']
    
    # Получаем общее количество отзывов
    total_reviews = reviews.count()
    
    # Создаем список для отображения в шаблоне
    rating_display = []
    for rating in range(5, 0, -1):  # От 5 до 1 звезд
        count = rating_stats[rating]
        percentage = (count / total_reviews * 100) if total_reviews > 0 else 0
        rating_display.append({
            'rating': rating,
            'count': count,
            'percentage': percentage
        })
    
    context = {
        'product': product,
        'page_obj': page_obj,
        'avg_rating': round(avg_rating, 1),
        'rating_stats': rating_stats,
        'rating_display': rating_display,
        'total_reviews': total_reviews,
    }
    
    return render(request, 'reviews/review_list.html', context)


@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Проверяем, не оставлял ли пользователь уже отзыв
    existing_review = Review.objects.filter(product=product, user=request.user).first()
    if existing_review:
        messages.warning(request, 'Вы уже оставляли отзыв на этот товар.')
        return redirect('reviews:review_list', product_id=product.id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, 'Ваш отзыв добавлен и будет опубликован после модерации.')
            return redirect('reviews:review_list', product_id=product.id)
    else:
        form = ReviewForm()
    
    return render(request, 'reviews/add_review.html', {'form': form, 'product': product})
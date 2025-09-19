from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product_link', 'rating_stars', 'title', 'is_approved', 'created']
    list_filter = ['rating', 'is_approved', 'created']
    search_fields = ['user__username', 'product__name', 'title', 'comment']
    list_editable = ['is_approved']
    readonly_fields = ['created', 'updated']
    list_per_page = 20
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'product', 'rating', 'title', 'comment')
        }),
        ('Статус', {
            'fields': ('is_approved',)
        }),
        ('Даты', {
            'fields': ('created', 'updated'),
            'classes': ('collapse',)
        }),
    )
    
    def product_link(self, obj):
        url = reverse('admin:main_product_change', args=[obj.product.id])
        return format_html('<a href="{}">{}</a>', url, obj.product.name)
    product_link.short_description = 'Товар'
    product_link.admin_order_field = 'product__name'
    
    def rating_stars(self, obj):
        return format_html(
            '<span style="color: #ffc107;">{}</span>',
            obj.get_stars()
        )
    rating_stars.short_description = 'Рейтинг'
    rating_stars.admin_order_field = 'rating'
    
    
    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f"Одобрено отзывов: {queryset.count()}")
    
    def reject_reviews(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, f"Отклонено отзывов: {queryset.count()}")
    
    approve_reviews.short_description = "Одобрить выбранные отзывы"
    reject_reviews.short_description = "Отклонить выбранные отзывы"
    
    actions = [approve_reviews, reject_reviews]
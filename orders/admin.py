from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    readonly_fields = ['product', 'price', 'quantity']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'email', 'status_badge', 'paid_badge', 'total_cost', 'created', 'tracking_number']
    list_filter = ['status', 'paid', 'created', 'updated']
    inlines = [OrderItemInline]
    search_fields = ['first_name', 'last_name', 'email', 'tracking_number']
    readonly_fields = ['created', 'updated']
    fieldsets = (
        ('Информация о заказе', {
            'fields': ('id', 'created', 'updated', 'status', 'paid')
        }),
        ('Данные покупателя', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Адрес доставки', {
            'fields': ('address', 'city', 'postal_code')
        }),
        ('Отслеживание', {
            'fields': ('tracking_number', 'notes')
        }),
    )
    
    def customer_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    customer_name.short_description = 'Покупатель'
    
    def status_badge(self, obj):
        colors = {
            'pending': 'warning',
            'processing': 'info',
            'shipped': 'primary',
            'delivered': 'success',
            'cancelled': 'danger'
        }
        color = colors.get(obj.status, 'secondary')
        return format_html(
            '<span class="badge bg-{}">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Статус'
    
    def paid_badge(self, obj):
        if obj.paid:
            return format_html('<span class="badge bg-success">Оплачен</span>')
        else:
            return format_html('<span class="badge bg-warning">Не оплачен</span>')
    paid_badge.short_description = 'Оплата'
    
    def total_cost(self, obj):
        return f"{obj.get_total_cost()} руб."
    total_cost.short_description = 'Сумма'
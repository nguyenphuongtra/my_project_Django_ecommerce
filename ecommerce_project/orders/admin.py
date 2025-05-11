from django.contrib import admin
from .models import Order, OrderItem, Province, District, Ward, PAYMENT_METHODS, ORDER_STATUS
from decimal import Decimal, InvalidOperation

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('formatted_price', 'formatted_subtotal')
    fields = ('product', 'quantity', 'price', 'formatted_subtotal')

    def formatted_subtotal(self, obj):
        try:
            return f"{int(obj.price * obj.quantity):,}".replace(',', '.') + ' đ'
        except (TypeError, ValueError, InvalidOperation):
            return "0 đ"
    formatted_subtotal.short_description = 'Thành tiền'

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ('id', 'user', 'status', 'created_at', 'formatted_total', 'get_payment_method_display')
    list_filter = ('status', 'created_at', 'payment_method')
    search_fields = ('id', 'user__username', 'user__email')
    readonly_fields = ('formatted_total', 'formatted_shipping_fee', 'get_payment_method_display')
    fieldsets = (
        ('Thông tin đơn hàng', {
            'fields': ('user', 'status', 'created_at', 'payment_method', 'get_payment_method_display')
        }),
        ('Địa chỉ giao hàng', {
            'fields': ('province', 'district', 'ward', 'shipping_address')
        }),
        ('Chi phí', {
            'fields': ('shipping_fee', 'formatted_shipping_fee', 'total', 'formatted_total')
        }),
    )

    def formatted_total(self, obj):
        try:
            return f"{int(obj.total):,}".replace(',', '.') + ' đ'
        except (TypeError, ValueError, InvalidOperation):
            return "0 đ"
    formatted_total.short_description = 'Tổng tiền'

    def formatted_shipping_fee(self, obj):
        try:
            return f"{int(obj.shipping_fee):,}".replace(',', '.') + ' đ'
        except (TypeError, ValueError, InvalidOperation):
            return "0 đ"
    formatted_shipping_fee.short_description = 'Phí vận chuyển'
    
    def get_payment_method_display(self, obj):
        payment_methods_dict = dict(PAYMENT_METHODS)
        return payment_methods_dict.get(obj.payment_method, obj.payment_method)
    get_payment_method_display.short_description = 'Phương thức thanh toán'
    
    def save_model(self, request, obj, form, change):
        if obj.shipping_fee is None or obj.shipping_fee == '':
            obj.shipping_fee = Decimal('0')
        if obj.total is None or obj.total == '':
            obj.total = Decimal('0')
            
        try:
            Decimal(obj.shipping_fee)
            Decimal(obj.total)
        except InvalidOperation:
            obj.shipping_fee = Decimal('0')
            obj.total = Decimal('0')
            
        super().save_model(request, obj, form, change)

admin.site.register(Province)
admin.site.register(District)
admin.site.register(Ward)
admin.site.register(Order, OrderAdmin)

from django.db import models
from django.conf import settings
from shop.models import Product
from decimal import Decimal

# === Phân cấp hành chính ===
class Province(models.Model):
    code           = models.CharField(max_length=20, primary_key=True)
    name           = models.CharField(max_length=100)
    name_with_type = models.CharField(max_length=100)

    class Meta:
        verbose_name        = "Tỉnh/Thành phố"
        verbose_name_plural = "Tỉnh/Thành phố"
        ordering            = ['name']

    def __str__(self):
        return self.name_with_type


class District(models.Model):
    code           = models.CharField(max_length=20, primary_key=True)
    province       = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='districts')
    name           = models.CharField(max_length=100)
    name_with_type = models.CharField(max_length=100)

    class Meta:
        verbose_name        = "Quận/Huyện"
        verbose_name_plural = "Quận/Huyện"
        ordering            = ['province__name', 'name']

    def __str__(self):
        return self.name_with_type


class Ward(models.Model):
    code           = models.CharField(max_length=20, primary_key=True)
    district       = models.ForeignKey(District, on_delete=models.CASCADE, related_name='wards')
    name           = models.CharField(max_length=100)
    name_with_type = models.CharField(max_length=100)

    class Meta:
        verbose_name        = "Xã/Phường"
        verbose_name_plural = "Xã/Phường"
        ordering            = ['district__name', 'name']

    def __str__(self):
        return self.name_with_type


ORDER_STATUS = (
    ('pending', 'Đang xử lý'),
    ('shipping', 'Đang giao hàng'),
    ('delivered', 'Đã giao hàng'),
    ('cancelled', 'Đã hủy')
)

PAYMENT_METHODS = (
    ('cod', 'Thanh toán khi nhận hàng'),
    ('bank', 'Chuyển khoản ngân hàng')
)

class Order(models.Model):
    user            = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    created_at      = models.DateTimeField(auto_now_add=True)
    status          = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    payment_method  = models.CharField(max_length=10, choices=PAYMENT_METHODS)

    province        = models.ForeignKey(Province, on_delete=models.SET_NULL, null=True, blank=True)
    district        = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)
    ward            = models.ForeignKey(Ward,     on_delete=models.SET_NULL, null=True, blank=True)

    shipping_address = models.CharField(max_length=255, blank=True)
    shipping_fee     = models.DecimalField(max_digits=10, decimal_places=0, default=Decimal('0'))
    total            = models.DecimalField(max_digits=10, decimal_places=0, default=Decimal('0'))

    class Meta:
        verbose_name        = "Đơn hàng"
        verbose_name_plural = "Đơn hàng"
        ordering            = ['-created_at']

    def save(self, *args, **kwargs):
        if self.shipping_fee is None:
            self.shipping_fee = Decimal('0')
        
        if self.total is None:
            self.total = Decimal('0')
            
        if isinstance(self.shipping_fee, str) and self.shipping_fee.strip() == '':
            self.shipping_fee = Decimal('0')
            
        if isinstance(self.total, str) and self.total.strip() == '':
            self.total = Decimal('0')
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Order #{self.id}'

    @property
    def formatted_shipping_fee(self):
        """Return shipping fee formatted for display"""
        try:
            return f"{int(self.shipping_fee):,}".replace(',', '.')
        except (TypeError, ValueError):
            return "0"

    @property
    def formatted_total(self):
        """Return total formatted for display"""
        try:
            return f"{int(self.total):,}".replace(',', '.')
        except (TypeError, ValueError):
            return "0"


class OrderItem(models.Model):
    order    = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price    = models.DecimalField(max_digits=10, decimal_places=0)

    class Meta:
        verbose_name        = "Mặt hàng đơn hàng"
        verbose_name_plural = "Mặt hàng đơn hàng"

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'

    @property
    def formatted_price(self):
        """Return price formatted for display"""
        try:
            return f"{int(self.price):,}".replace(',', '.')
        except (TypeError, ValueError):
            return "0"

    @property
    def subtotal(self):
        """Calculate subtotal for this item"""
        try:
            return self.price * self.quantity
        except (TypeError, ValueError):
            return Decimal('0')

    @property
    def formatted_subtotal(self):
        """Return subtotal formatted for display"""
        try:
            subtotal = self.price * self.quantity
            return f"{int(subtotal):,}".replace(',', '.')
        except (TypeError, ValueError):
            return "0"

from django.db import models

from users.models import User
from products.models import Product
from django.utils.functional import cached_property


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт {self.product.name}'

    @cached_property
    def get_items_cached(self):
        return self.user.basket.select_related()

    def sum(self):
        return self.product.price * self.quantity

    def total_quantity(self):
        baskets = self.get_items_cached
        return sum(basket.quantity for basket in baskets)

    def total_sum(self):
        baskets = self.get_items_cached
        return sum(basket.sum() for basket in baskets)

    @staticmethod
    def get_item(pk):
        return Basket.objects.filter(pk=pk).first()

    @staticmethod
    def get_items(user):
        return Basket.objects.filter(user=user)

    # def delete(self):
    #     self.product.quantity += self.quantity
    #     self.product.save()
    #     super(Basket, self).delete()

    # def save(self, *args, **kwargs):
    #     if self.pk:
    #         self.product.quantity -= self.quantity - self.__class__.get_item(self.pk).quantity
    #     else:
    #         self.product.quantity -= self.quantity
    #     self.product.save()
    #     super(self.__class__, self).save(*args, **kwargs)

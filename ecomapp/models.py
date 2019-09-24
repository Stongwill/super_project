# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from decimal import Decimal
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify
from django.core.urlresolvers import reverse
from transliterate import translit
from notifications.signals import notify
from django.contrib.auth.models import User
from PIL import Image
import os
import glob
# Create your models here.


class Category(models.Model):

	name = models.CharField(verbose_name='Имя', max_length=100)
	slug = models.SlugField(blank=True)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('category_detail', kwargs={'category_slug': self.slug})
#автозаполнение поля слаг
def pre_save_category_slug(sender, instance, *args, **kwargs):
	if not instance.slug:
		slug = slugify(translit(str(instance.name), reversed=True))
		instance.slug = slug

pre_save.connect(pre_save_category_slug, sender=Category)

class Author(models.Model):

    name = models.CharField(verbose_name='ФИО', max_length=100)

    def __str__(self):
    	return self.name


def image_folder(instance, filename):
	filename = instance.slug + '.' + filename.split('.')[1]
	return "{0}/{1}".format(instance.slug, filename)


class Book(models.Model):

	category = models.ForeignKey(Category, verbose_name='Категория')
	author = models.ForeignKey(Author, verbose_name='Автор')
	title = models.CharField(verbose_name='Название книги', max_length=120)
	slug = models.SlugField(verbose_name='Слег')
	description = models.TextField(verbose_name='Описание')
	image = models.ImageField(verbose_name='Картинка', upload_to=image_folder)
	price = models.DecimalField(verbose_name='Цена', max_digits=9, decimal_places=2)
	available = models.BooleanField(default=True, verbose_name="Доступен")

	class Meta:
		verbose_name = "Book"
		verbose_name_plural = "Books"
		ordering = ["title", "price", "-price"]


	def __str__(self):
		return self.title


	def get_absolute_url(self):
		return reverse('product_detail', kwargs={'product_slug': self.slug})






def product_available_notification(sender, instance, *args, **kwargs):
	if instance.available:
		await_for_notify = [notification for notification in MiddlwareNotification.objects.filter(
			product=instance)]
		for notification in await_for_notify:
			notify.send(
				instance,
				recipient=[notification.user_name],
				verb='Уважаемый {0}! {1}, который Вы ждете, поступил'.format(
					notification.user_name.username,
					instance.title),
				description=instance.slug
				)
			notification.delete()


post_save.connect(product_available_notification, sender=Book)



class CartItem(models.Model):

	product = models.ForeignKey(Book, verbose_name='Книга')
	qty = models.PositiveIntegerField(verbose_name='Количество', default=1)
	item_total = models.DecimalField(verbose_name='Изменить цену', max_digits=9, decimal_places=2, default=0.00)

	def __str__(self):
		return "В корзине находится книга: {0}".format(self.product.title)


class Cart(models.Model):

	items = models.ManyToManyField(CartItem, blank=True)
	cart_total = models.DecimalField(verbose_name='Итоговая сумма', max_digits=9, decimal_places=2, default=0.00)

	def __str__(self):
		return str(self.id)



	def add_to_cart(self, product_slug):
		cart = self
		product = Book.objects.get(slug=product_slug)
		new_item, _ = CartItem.objects.get_or_create(product=product, item_total=product.price)
		cart_items = [item.product for item in cart.items.all()]
		if new_item.product not in cart_items:
			cart.items.add(new_item)
			cart.save()


	def remove_from_cart(self, product_slug):
		cart = self
		product = Book.objects.get(slug=product_slug)
		for cart_item in cart.items.all():
			if cart_item.product == product:
				cart.items.remove(cart_item)
				cart.save()


	def change_qty(self, qty, item_id):
		cart = self
		cart_item = CartItem.objects.get(id=int(item_id))
		cart_item.qty = int(qty)
		cart_item.item_total = int(qty) * Decimal(cart_item.product.price)
		cart_item.save()
		new_cart_total = 0.00
		for item in cart.items.all():
			new_cart_total += float(item.item_total)
		cart.cart_total = new_cart_total
		cart.save()


ORDER_STATUS_CHOICES = (
	('Принят в обработку', 'Принят в обработку'),
	('Выполняется', 'Выполняется'),
	('Оплачен', 'Оплачен')
)

class Order(models.Model):

	user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Заказчик')
	items = models.ForeignKey(Cart, verbose_name='Товары')
	total = models.DecimalField(verbose_name='Общая сумма', max_digits=9, decimal_places=2, default=0.00)
	first_name = models.CharField(verbose_name='Имя', max_length=200)
	last_name = models.CharField(verbose_name='Фамилия', max_length=200)
	phone = models.CharField(verbose_name='Номер телефона', max_length=20)
	address = models.CharField(verbose_name='Адрес', max_length=255)
	buying_type = models.CharField(verbose_name='Тип заказа', max_length=40,  choices=(('Самовывоз', 'Самовывоз'), ('Доставка', 'Доставка')), default='Самовывоз')
	date = models.DateTimeField(verbose_name='Дата', auto_now_add=True)
	comments = models.TextField(verbose_name='Комментарии')
	status = models.CharField(verbose_name='Статус', max_length=100, choices=ORDER_STATUS_CHOICES, default=ORDER_STATUS_CHOICES[0][0])


	def __str__(self):
		return "Заказ №{0}".format(str(self.id))

class MiddlwareNotification(models.Model):

	user_name = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Имя пользователя')
	product = models.ForeignKey(Book, verbose_name='Книга')
	is_notified = models.BooleanField(default=False)

	def __str__(self):
		return "Нотификация для пользователя {0} о поступлении товара {1}".format(
	   	self.user_name.username,
	   	self.product.title
	   	)



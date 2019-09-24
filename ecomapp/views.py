# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from decimal import Decimal
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import login, authenticate
from ecomapp.forms import OrderForm, RegistrationForm, LoginForm, BookFilterForm
from ecomapp.models import Category, Book, CartItem, Cart, Order
from django.views.generic import View
from django.contrib.auth.models import User


# Create your views here.
def base_view(request):
	products = Book.objects.all()
	categories = Category.objects.all()
	product = BookFilterForm(request.GET)
	if product.is_valid():
		if product.cleaned_data["min_price"]:
			products = products.filter(price__gte=product.cleaned_data["min_price"])
		if product.cleaned_data["max_price"]:
			products = products.filter(price__lte=product.cleaned_data["max_price"])

		if product.cleaned_data["ordering"]:
			products = products.order_by(product.cleaned_data["ordering"])

	page = request.GET.get('page', 1)
	paginator = Paginator(products, 12)
	try:

		products = paginator.page(page)
	except PageNotAnInteger:
		products = paginator.page(1)
	except EmptyPage:
		products = paginator.page(paginator.num_pages)
	context = {
		'categories': categories,
		'products': products,
		'product': product,
	}
	return render(request, 'base.html', context)



#def base_view(request):
# 	try:
# 		cart_id = request.session['cart_id']
# 		cart = Cart.objects.get(id=cart_id)
# 		request.session['total'] = cart.items.count()
# 	except:
# 		cart = Cart()
# 		cart.save()
# 		cart_id = cart.id
# 		request.session['cart_id'] = cart_id
# 		cart = Cart.objects.get(id=cart_id)
# 	categories = Category.objects.all()
# 	products = Book.objects.all()
# 	context = {
# 	    'categories': categories,
# 	    'products': products,
# 	    'cart': cart
# 	}
# 	return render(request, 'base.html', context)




def product_view(request, product_slug):
	try:
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id)
		request.session['total'] = cart.items.count()
	except:
		cart = Cart()
		cart.save()
		cart_id = cart.id
		request.session['cart_id'] = cart_id
		cart = Cart.objects.get(id=cart_id)
	product = Book.objects.get(slug=product_slug)
	categories = Category.objects.all()
	context = {
	   'product': product,
	   'categories': categories,
	   'cart': cart
	}
	return render(request, 'product.html', context)


def category_view(request, category_slug):
	try:
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id)
		request.session['total'] = cart.items.count()
	except:
		cart = Cart()
		cart.save()
		cart_id = cart.id
		request.session['cart_id'] = cart_id
		cart = Cart.objects.get(id=cart_id)
	category = Category.objects.get(slug=category_slug)
	price_filter_type = request.GET.get('price_filter_type')
	print(price_filter_type)
	products_of_category = Book.objects.filter(category=category)
	categories = Category.objects.all()
	context = {
	    'category': category,
	    'products_of_category': products_of_category,
		'cart': cart,
		'categories': categories
	}
	return render(request, 'category.html', context)

def	cart_view(request):
	try:
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id)
		request.session['total'] = cart.items.count()
	except:
		cart = Cart()
		cart.save()
		cart_id = cart.id
		request.session['cart_id'] = cart_id
		cart = Cart.objects.get(id=cart_id)
	categories = Category.objects.all()
	context = {
	    'cart': cart,
	    'categories': categories
	}
	return render(request, 'cart.html', context)



def add_to_cart_view(request):
	try:
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id)
		request.session['total'] = cart.items.count()
	except:
		cart = Cart()
		cart.save()
		cart_id = cart.id
		request.session['cart_id'] = cart_id
		cart = Cart.objects.get(id=cart_id)
	product_slug = request.GET.get('product_slug')
	product = Book.objects.get(slug=product_slug)
	cart.add_to_cart(product.slug)
	new_cart_total = 0.00
	for item in cart.items.all():
		new_cart_total += float(item.item_total)
	cart.cart_total = new_cart_total
	cart.save()
	return JsonResponse({'cart_total': cart.items.count(), 'cart_total_price': cart.cart_total})


def remove_from_cart_view(request):
	try:
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id)
		request.session['total'] = cart.items.count()
	except:
		cart = Cart()
		cart.save()
		cart_id = cart.id
		request.session['cart_id'] = cart_id
		cart = Cart.objects.get(id=cart_id)
	product_slug = request.GET.get('product_slug')
	product = Book.objects.get(slug=product_slug)
	cart.remove_from_cart(product.slug)
	new_cart_total = 0.00
	for item in cart.items.all():
		new_cart_total += float(item.item_total)
	cart.cart_total = new_cart_total
	cart.save()
	return JsonResponse(
		{'cart_total': cart.items.count(),
		'cart_total_price': cart.cart_total})


def change_item_qty(request):
	try:
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id)
		request.session['total'] = cart.items.count()
	except:
		cart = Cart()
		cart.save()
		cart_id = cart.id
		request.session['cart_id'] = cart_id
		cart = Cart.objects.get(id=cart_id)
	qty = request.GET.get('qty')
	item_id = request.GET.get('item_id')
	cart.change_qty(qty, item_id)
	cart_item = CartItem.objects.get(id=int(item_id))
	return JsonResponse(
		{'cart_total': cart.items.count(),
		'item_total': cart_item.item_total,
		'cart_total_price': cart.cart_total})



def checkout_view(request):
	try:
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id)
		request.session['total'] = cart.items.count()
	except:
		cart = Cart()
		cart.save()
		cart_id = cart.id
		request.session['cart_id'] = cart_id
		cart = Cart.objects.get(id=cart_id)
	categories = Category.objects.all()
	context = {
        'cart': cart,
        'categories': categories
	}
	return render(request, 'checkout.html', context)


def order_create_view(request):
	try:
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id)
		request.session['total'] = cart.items.count()
	except:
		cart = Cart()
		cart.save()
		cart_id = cart.id
		request.session['cart_id'] = cart_id
		cart = Cart.objects.get(id=cart_id)
	form = OrderForm(request.POST or None)
	categories = Category.objects.all()
	context = {
	   'form': form,
	   'cart': cart,
	   'categories': categories
	}
	return render(request, 'order.html', context)



def make_order_view(request):
	try:
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id)
		request.session['total'] = cart.items.count()
	except:
		cart = Cart()
		cart.save()
		cart_id = cart.id
		request.session['cart_id'] = cart_id
		cart = Cart.objects.get(id=cart_id)
	form = OrderForm(request.POST or None)
	categories = Category.objects.all()
	if form.is_valid():
		name = form.cleaned_data['name']
		last_name = form.cleaned_data['last_name']
		phone = form.cleaned_data['phone']
		buying_type = form.cleaned_data['buying_type']
		address = form.cleaned_data['address']
		comments = form.cleaned_data['comments']
		new_order = Order.objects.create(
			user=request.user,
			items=cart,
			total=cart.cart_total,
			first_name=name,
			last_name=last_name,
			phone=phone,
			address=address,
			buying_type=buying_type,
			comments=comments
			)
		del request.session['cart_id']
		del request.session['total']
		return HttpResponseRedirect(reverse('thank_you'))
	return render(request, 'order.html', {'categories': categories})



def account_view(request):
	order = Order.objects.filter(user=request.user).order_by('-id')
	categories = Category.objects.all()
	for item in order:
		for new_item in item.items.items.all():
			print(new_item.item_total)
	context = {
		'order': order,
		'categories': categories
	}
	return render(request, 'account.html', context)

def registration_view(request):
	form = RegistrationForm(request.POST or None)
	categories = Category.objects.all()
	if form.is_valid():
		new_user = form.save(commit=False)
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		email = form.cleaned_data['email']
		first_name = form.cleaned_data['first_name']
		last_name = form.cleaned_data['last_name']
		new_user.username = username
		new_user.set_password(password)
		new_user.first_name = first_name
		new_user.last_name = last_name
		new_user.email = email
		new_user.save()
		login_user = authenticate(username=username, password=password)
		if login_user:
			login(request, login_user)
			return HttpResponseRedirect(reverse('base'))
	context = {
		'form': form,
		'categories': categories
	}
	return render(request, 'registration.html', context)


def login_view(request):
	form = LoginForm(request.POST or None)
	categories = Category.objects.all()
	if form.is_valid():
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		login_user = authenticate(username=username, password=password)
		if login_user:
			login(request, login_user)
			return HttpResponseRedirect(reverse('base'))
	context = {
		'form': form,
		'categories': categories
	}
	return render(request, 'login.html', context)


class search_view(View):

	template_name = 'search.html'
	def get(self, request, *args, **kwargs):
		query = self.request.GET.get('q')
		categories = Category.objects.all()
		founded_articles = Book.objects.filter(
			Q(title__icontains=query)|
			Q(description__icontains=query))
		context = {
			'founded_articles': founded_articles,
			'categories': categories
		}
		return render(self.request, self.template_name, context)


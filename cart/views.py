from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from store.models import Item
from .models import Cart, CartItem


@login_required
def cart(request):
    """
    Представление для вывода всех объектов
    товаров корзины и самой корзины.
    """
    cart = Cart.objects.filter(user=request.user).first()

    if not cart:
        cart = Cart.objects.create(user=request.user)

    context = {
        'cart_items': CartItem.objects.filter(cart=cart),
        'cart': cart
    }

    return render(request, 'cart/cart.html', context)


@login_required
def add_to_cart(request, item_slug):
    """
    Представление для добавления товара в корзину
    либо увеличения его количества на 1.
    """
    item = get_object_or_404(Item, slug=item_slug)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        item=item
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart:cart')


@login_required
def delete_cart_item(request, item_slug):
    """
    Представление для удаления объекта товара в корзине.
    """
    cart_item = CartItem.objects.get(
        cart=Cart.objects.get(user=request.user),
        item=get_object_or_404(Item, slug=item_slug)
    )
    cart_item.delete()
    return redirect('cart:cart')


@login_required
def update_cart_item(request):
    if request.method == 'POST':
        cart_id = request.POST.get('cart_id')
        cart_item_id = request.POST.get('cart_item_id')
        new_quantity = int(request.POST.get('new_quantity'))

        # Получаем корзину и товар из корзины
        cart = get_object_or_404(Cart, id=cart_id, user=request.user)
        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart=cart)

        # Обновляем количество товара в корзине
        cart_item.quantity = new_quantity
        cart_item.save()

        # Пересчитываем цену товара и общую стоимость корзины
        cart_item_total_price = cart_item.item.price * cart_item.quantity
        cart_total_price = cart.total_price # Получаем обновленную общую цену корзины

        # Возвращаем обновленные данные
        return JsonResponse({
            'cart_item_total_price': cart_item_total_price,
            'cart_total_price': cart_total_price,
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)


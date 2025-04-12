$(document).ready(function () {
  // Обработчик клика на кнопку "минус"
  $('.minus').click(function () {
    var $input = $(this).parent().find('input');
    var count = parseInt($input.val()) - 1;  // Уменьшаем количество на 1

    // Если количество меньше 1, то присваиваем 1
    count = count < 1 ? 1 : count;
    $input.val(count);  // Обновляем поле ввода с новым количеством

    updateCartItem($input, count);  // Отправляем запрос на сервер
  });

  // Обработчик клика на кнопку "плюс"
  $('.plus').click(function () {
    var $input = $(this).parent().find('input');
    var count = parseInt($input.val()) + 1;  // Увеличиваем количество на 1
    $input.val(count);  // Обновляем поле ввода с новым количеством

    updateCartItem($input, count);  // Отправляем запрос на сервер
  });

  // Функция для отправки данных на сервер через AJAX
  function updateCartItem($input, count) {
    var cartItemId = $input.attr('data-cart-item-id');  // Получаем ID товара в корзине
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();  // Получаем CSRF-токен
    var cartId = $('#cart-total-price').data('cart-id');  // Получаем ID корзины

    // Здесь мы сразу обновляем цену на клиенте, используя цену товара
    var pricePerItem = parseFloat($input.closest('tr').find('.cart-item-total-price').data('price-per-item'));
    var newItemTotalPrice = (pricePerItem * count).toFixed(2);  // Новая цена для данного товара

    // Обновляем отображение общей стоимости товара сразу
    $('.cart-item-total-price[data-cart-item-id="' + cartItemId + '"]').text(newItemTotalPrice);

    // Также обновляем общую стоимость корзины на клиенте, пока не получили ответ с сервера
    updateCartTotalPrice();

    // Отправляем AJAX-запрос на сервер
    $.ajax({
      url: '/cart/update_cart_item/',  // Путь для обновления элемента корзины
      method: 'POST',
      data: {
        cart_id: cartId,
        new_quantity: count,
        cart_item_id: cartItemId,
        csrfmiddlewaretoken: csrfToken
      },
      success: function (data) {
        // После успешного запроса обновляем общую сумму корзины
        $('.cart-item-total-price[data-cart-item-id="' + cartItemId + '"]').text(data.cart_item_total_price);
        $('#cart-total-price').text(data.cart_total_price);
      },
      error: function () {
        console.log('Ошибка при обновлении корзины');
      }
    });
  }

  // Функция для обновления общей стоимости корзины
  function updateCartTotalPrice() {
    var total = 0;
    $('.cart-item-total-price').each(function() {
      total += parseFloat($(this).text());
    });
    $('#cart-total-price').text(total.toFixed(2));  // Обновляем общую стоимость корзины
  }
});

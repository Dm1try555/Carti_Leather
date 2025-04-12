$('.minus').click(function () {
  var $input = $(this).parent().find('input');
  var count = parseInt($input.val()) - 1;  // Уменьшаем количество на 1

  // Если количество меньше 1, то присваиваем 1
  count = count < 1 ? 1 : count;
  $input.val(count);  // Обновляем поле ввода с новым количеством
});

$('.plus').click(function () {
  var $input = $(this).parent().find('input');
  var count = parseInt($input.val()) + 1;  // Увеличиваем количество на 1
  $input.val(count);  // Обновляем поле ввода с новым количеством
});

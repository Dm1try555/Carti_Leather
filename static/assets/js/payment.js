var stripe = Stripe('pk_test_51RBK4gH0u1LI0zsJzVl7VRo6Ib9uIzS44a6gg99msGVZKf9Pduj7uUtk93NrfprDNm7rDo3IGwKjLd6tM2LSotyS004sCNZIGM');
var elements = stripe.elements();
var card = elements.create('card');
card.mount('#card-element');

var form = document.getElementById('payment-form');
form.addEventListener('submit', function(event) {
    event.preventDefault();

    stripe.createToken(card).then(function(result) {
        if (result.error) {
            // Покажіть помилку користувачеві
            var errorElement = document.getElementById('card-errors');
            errorElement.textContent = result.error.message;
        } else {
            // Надсилайте токен на сервер
            var form = document.getElementById('payment-form');
            var hiddenInput = document.createElement('input');
            hiddenInput.setAttribute('type', 'hidden');
            hiddenInput.setAttribute('name', 'stripeToken');
            hiddenInput.setAttribute('value', result.token.id);
            form.appendChild(hiddenInput);

            // Тепер ви можете надіслати форму
            form.submit();
        }
    });
});

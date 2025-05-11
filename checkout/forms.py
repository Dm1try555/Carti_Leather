from django import forms

from .models import Order, ShippingAddress


class PlaceholderForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PlaceholderForm, self).__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs['placeholder'] = field.help_text




class OrderCreateForm(PlaceholderForm):
    first_name = forms.CharField(max_length=100, help_text='Введіть своє ім\'я', label='Ім\'я', required=True)
    last_name = forms.CharField(max_length=100, help_text='Введіть своє прізвище', label="Прізвище", required=True)
    email = forms.EmailField(help_text='Введіть свою електронну пошту', label='Електронна пошта')
    phone = forms.CharField(max_length=13, help_text='Введіть свій номер телефону', label='Телефон', required=True)
    city = forms.CharField(max_length=100, help_text='Введіть своє місто для доставки НП', label='Місто', required=True)
    office = forms.CharField(max_length=100, help_text='Введіть номер відділення НП', label='№ Відділення Нової Пошти', required=True)
    payment_method = forms.ChoiceField(choices=Order.PAYMENT_METHOD_CHOICES, label="Спосіб оплати", required=True)



    class Meta:
        model = ShippingAddress
        fields = ['first_name', 'last_name', 'email', 'phone', 'city', 'office', 'feedback_messengers', 'payment_method']

    

    


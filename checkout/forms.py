from django import forms

from .models import Order, ShippingAddress


class PlaceholderForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PlaceholderForm, self).__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs['placeholder'] = field.help_text




class OrderCreateForm(PlaceholderForm):
    first_name = forms.CharField(max_length=100, help_text='Ім\'я')
    last_name = forms.CharField(max_length=100, help_text='Прізвище')
    email = forms.EmailField(help_text='Email')
    phone = forms.CharField(max_length=13, help_text='Телефон')
    payment_method = forms.ChoiceField(choices=Order.PAYMENT_METHOD_CHOICES)
    feedback_messengers = forms.MultipleChoiceField(
        choices=[
            ('viber', ''),
            ('telegram', ''),
            ('whatsapp', ''),
        ],
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Доступні месенджери',
    )


    class Meta:
        model = ShippingAddress
        fields = ['first_name', 'last_name', 'email', 'phone', 'city_ref', 'warehouse_ref', 'feedback_messengers']
       

    

    


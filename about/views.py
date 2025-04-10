from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):
    template_name = 'about/author.html'


class AboutDeliveryView(TemplateView):
    template_name = 'about/delivery.html'


class AboutPaymentView(TemplateView):
    template_name = 'about/payment.html'

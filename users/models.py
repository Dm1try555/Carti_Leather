from django.db import models






class Feedback(models.Model):
    feedback_name = models.CharField(max_length=50, verbose_name='Ім\'я',)
    feedback_email = models.EmailField(verbose_name='Пошта покупця',)
    feedback_message = models.TextField(verbose_name='Текст',)
    feedback_phone = models.CharField(max_length=13, verbose_name='Телефон покупця', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення',)

    class Meta:
        verbose_name = 'Зворотній зв\'язок покупця'
        verbose_name_plural = 'Зворотній зв\'язок покупців'

    def __str__(self):
        return self.feedback_message

from django.contrib import admin

from .models import Feedback


class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        'feedback_name',
        'feedback_email',
        'short_message',
        'feedback_phone',
        'created_at',
    )
    ordering = ('-created_at',)

    def short_message(self, obj):
        """
        Ограничивает длину сообщения до 100 символов.
        """
        if len(obj.feedback_message) > 100:
            return obj.feedback_message[:100] + '...'
        return obj.feedback_message

    short_message.short_description = 'Повідомлення'


admin.site.register(Feedback, FeedbackAdmin)

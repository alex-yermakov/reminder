from django.contrib import admin
from django.contrib.admin.decorators import register
from django.utils.translation import ugettext_lazy as _

from .models import *


@register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_name', 'note', 'date', 'time', 'periodicity')

    def user_name(self, instance):
        return instance.user.get_full_name()
    user_name.short_description = _('User name')

    def date(self, instance):
        return instance.get_date_display()
    date.short_description = _('Date (day)')

    def periodicity(self, instance):
        return instance.get_date_display()
    periodicity.short_description = _('Periodicity')

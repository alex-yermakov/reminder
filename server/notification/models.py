from datetime import datetime

from django.db import models
from django.core.validators import MaxValueValidator
from django.utils.translation import ugettext_lazy as _

__all__ = ('Notification',
           # Periodicity choices
           'NON_PERIODIC', 'DAILY', 'WEEKLY', 'MONTHLY', 'ANNUALLY',
           # Months choices
           'JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY',
           'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER',
           # Days of week choices
           'MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY')

NON_PERIODIC, DAILY, WEEKLY, MONTHLY, ANNUALLY = range(1, 6)
PERIODICITY_CHOICES = (
    (NON_PERIODIC, _('Not periodic')),
    (DAILY, _('Daily')),
    (WEEKLY, _('Weekly')),
    (MONTHLY, _('Monthly')),
    (ANNUALLY, _('Annually')),
)

JANUARY, FEBRUARY, MARCH, APRIL, MAY, JUNE, JULY, AUGUST, SEPTEMBER, OCTOBER, NOVEMBER, DECEMBER = range(1, 13)
MONTHS_CHOICES = (
    (JANUARY, _('January')),
    (FEBRUARY, _('February')),
    (MARCH, _('March')),
    (APRIL, _('April')),
    (MAY, _('May')),
    (JUNE, _('June')),
    (JULY, _('July')),
    (AUGUST, _('August')),
    (SEPTEMBER, _('September')),
    (OCTOBER, _('October')),
    (NOVEMBER, _('November')),
    (DECEMBER, _('December')),
)

MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY = range(1, 8)
DAYS_OF_WEEK_CHOICES = (
    (MONDAY, _('Monday')),
    (TUESDAY, _('Tuesday')),
    (WEDNESDAY, _('Wednesday')),
    (THURSDAY, _('Thursday')),
    (FRIDAY, _('Friday')),
    (SATURDAY, _('Saturday')),
    (SUNDAY, _('Sunday')),
)


class Notification(models.Model):
    user = models.ForeignKey('user.User', related_name='notifications', on_delete=models.CASCADE)
    note = models.TextField(_('Note'), default='')

    periodicity = models.PositiveSmallIntegerField(_('Periodicity'), choices=PERIODICITY_CHOICES,
                                                   default=NON_PERIODIC, db_index=True)

    year = models.PositiveSmallIntegerField(_('Year'), null=True, blank=True, db_index=True)
    month = models.PositiveSmallIntegerField(_('Month'), choices=MONTHS_CHOICES, null=True,
                                             blank=True, db_index=True)
    day = models.PositiveSmallIntegerField(_('Day'), null=True, blank=True, db_index=True,
                                           validators=[MaxValueValidator(31, _('Day cannot be more than 31'))])
    day_of_week = models.PositiveSmallIntegerField(_('Day of week'), choices=DAYS_OF_WEEK_CHOICES,
                                                   null=True, blank=True, db_index=True)

    time = models.TimeField(_('Time'), db_index=True)

    class Meta:
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')

    def get_date_display(self):
        if self.periodicity == NON_PERIODIC:
            date = datetime(self.year, self.month, self.day).date()
            return date.strftime('%d.%m.%Y')
        elif self.periodicity == ANNUALLY:
            return _('%(day)sth of %(month)s') % {
                'day': self.day,
                'month': self.get_month_display()
            }
        elif self.periodicity == MONTHLY:
            return '%sth' % self.day
        elif self.periodicity == WEEKLY:
            return self.get_day_of_week_display()
        return '-'

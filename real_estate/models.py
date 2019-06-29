from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now as datetime_now

# Create your models here.


class SearchWord(models.Model):
    word = models.CharField(_('Word'), max_length=200,)
    status = models.PositiveIntegerField(choices=((1, _('In process')), (2, _('Failed')), (3, _('Done'))), default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Search word')
        verbose_name_plural = _('Search words')
        ordering = ['-created_at']

    def __str__(self):
        return self.word


class RealEstateDetail(models.Model):
    name = models.CharField(_('Name'), max_length=150)
    search_word = models.ForeignKey(SearchWord, related_name='real_estate_detail', on_delete=models.CASCADE)
    url = models.URLField(_('Url'))
    work_phone = models.CharField(_('Work phone'), max_length=150, null=True, blank=True)
    mobile_phone = models.CharField(_('Mobile phone'), max_length=150, null=True, blank=True)
    agency_name = models.CharField(_('Agency name'), max_length=150, null=True, blank=True)
    realtor_name = models.CharField(_('Realtor name'), max_length=150, null=True, blank=True)
    city = models.CharField(_('City'), max_length=150, null=True, blank=True)
    district = models.CharField(_('District'), max_length=150, null=True, blank=True)
    street = models.CharField(_('Street'), max_length=150, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Real estate detail')
        verbose_name_plural = _('Real estate details')
        ordering = ['-created_at']

    def __str__(self):
        return self.name

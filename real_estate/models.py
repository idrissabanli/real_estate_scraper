from django.db import models
from django.utils.translation import ugettext_lazy as _

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


class PhoneNumber(models.Model):
    real_estate = models.ForeignKey(RealEstateDetail, on_delete=models.CASCADE, related_name='phone_numbers')
    title = models.CharField(_('Title'), max_length=10)
    phone = models.CharField(_('Number'), max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Phone number')
        verbose_name_plural = _('Phone numbers')
        ordering = ['-created_at']

    def __str__(self):
        return self.real_estate.name

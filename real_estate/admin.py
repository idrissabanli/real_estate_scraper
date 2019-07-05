from django.contrib import admin

# Register your models here.
from real_estate.models import SearchWord, RealEstateDetail, PhoneNumber


@admin.register(SearchWord)
class SearchWordAdmin(admin.ModelAdmin):
    list_display = ('word', 'status', 'created_at',)
    list_filter = ('status',)
    search_fields = ('word',)


@admin.register(PhoneNumber)
class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ('real_estate', 'title', 'phone', 'created_at',)
    search_fields = ('real_estate', 'title', 'phone', )


class PhoneNumberInline(admin.TabularInline):
    model = PhoneNumber


@admin.register(RealEstateDetail)
class RealEstateDetailAdmin(admin.ModelAdmin):
    inlines = [PhoneNumberInline]
    list_display = ('agency_name', 'realtor_name', 'city', 'district', 'street',  'phone_number', 'created_at',)
    search_fields = ('name',)
    list_filter = ('street', 'district', 'city', )

    def phone_number(self, obj):
        return [(number.title+ ' ' + number.phone) for number in obj.phone_numbers.all()]

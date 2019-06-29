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
    list_display = ('name', 'search_word', 'url', 'created_at',)
    search_fields = ('name', 'search_word',)



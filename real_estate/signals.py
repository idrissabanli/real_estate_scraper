from datetime import timedelta

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from real_estate.tasks import get_page_datas
from real_estate.models import SearchWord


@receiver(post_save, sender=SearchWord, dispatch_uid='run_scraper_by_search_word')
def run_scraper_by_search_word(sender, created, **kwargs):
    if created:
        instance = kwargs.get('instance') # get Model object
        get_page_datas(instance.id, instance.created_at)
        instance.save()

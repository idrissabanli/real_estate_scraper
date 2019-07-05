from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class BaseUserConfig(AppConfig):
    name = 'base_user'
    verbose_name = _('Kullanıcı')

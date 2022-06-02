from django import template
from auth_APIs.models import ProviderUserAdditionalData
register = template.Library()

@register.simple_tag
def licenseTypeDetails(userId):
    providerAdditionalData = ProviderUserAdditionalData.objects.filter(userId=userId).first()
    return providerAdditionalData

from django.contrib import admin
from .models import InvestorRegistration, StartUpsForm, PartnerMembership, ContactUs

# Register your models here.
admin.site.register(InvestorRegistration)
admin.site.register(StartUpsForm)
admin.site.register(PartnerMembership)
admin.site.register(ContactUs)
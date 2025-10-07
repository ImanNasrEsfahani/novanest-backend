from django.contrib import admin
from .models import InvestorRegistration, StartUpsForm, AffiliateRegistration, ContactUs

# Register your models here.
admin.site.register(InvestorRegistration)
admin.site.register(StartUpsForm)
admin.site.register(AffiliateRegistration)
admin.site.register(ContactUs)
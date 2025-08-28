from .models import StartUpsForm,ContactUs,PartnerMembership,InvestorRegistration, Entrepreneur
from rest_framework import serializers
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import logging

logger = logging.getLogger(__name__)

class StartupFormSerializer(serializers.ModelSerializer):
    financialModelFile = serializers.FileField(required=False)
    financialFile = serializers.FileField(required=False)
    pitchDeckFile = serializers.FileField(required=False)
    businessPlanFile = serializers.FileField(required=False)

    class Meta:
        model = StartUpsForm
        fields = '__all__'
        read_only_fields = ['id', 'createdAt']

    def create(self, validated_data):
        instance = super().create(validated_data)

        subject = 'Thank you for registering your startup'
        from_email = 'amir.esfahanizadeh@landaholding.com'  # Use the same email as in EMAIL_HOST_USER
        to_email = instance.email
        context = {'first_name': instance.firstName}
        text_content = f"Hi {instance.firstName},\n\nThanks for registering your startup with us."
        html_content = render_to_string('startup_registration_email.html', context)

        email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        email.attach_alternative(html_content, "text/html")

        try:
            email.send()
        except Exception as e:
            logger.error(f"Failed to send registration email: {e}")

        return instance
    
class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = '__all__'
        read_only_fields = ['id', 'createdAt']

    def create(self, validated_data):
        instance = super().create(validated_data)

        subject = 'Thanks for contacting us!'
        from_email = 'amir.esfahanizadeh@landaholding.com'
        to_email = instance.email
        context = {'name': instance.name}
        text_content = f"Hi {instance.name},\n\nThanks for reaching out. We'll respond to your message shortly."
        html_content = render_to_string('contact_us_email.html', context)

        email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        email.attach_alternative(html_content, "text/html")
        email.send()

        return instance

class PartnerMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartnerMembership
        fields = '__all__'
        read_only_fields = ['id', 'createdAt']

    def create(self, validated_data):
        instance = super().create(validated_data)

        subject = 'Thanks for joining our partner network'
        from_email = 'amir.esfahanizadeh@landaholding.com'
        to_email = instance.email
        context = {'name': instance.firstName}
        text_content = f"Hi {instance.firstName},\n\nWe're excited to have you as a partner!"
        html_content = render_to_string('partner_membership_email.html', context)

        email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        email.attach_alternative(html_content, "text/html")
        email.send()

        return instance
    
class InvestorRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestorRegistration
        fields = '__all__'
        read_only_fields = ['id','createdAt']

    def create(self, validated_data):
        instance = super().create(validated_data)

        # Prepare email content
        subject = 'Thank you for registering as an investor'
        from_email = 'amir.esfahanizadeh@landaholding.com'
        to_email = instance.email
        context = {'first_name': instance.firstName}
        text_content = f"Hi {instance.firstName},\n\nThank you for registering as an investor. We appreciate your interest and will get back to you shortly.\n\nBest regards,\nThe Investment Platform Team"
        html_content = render_to_string('investor_registration_email.html', context)

        # Create and send email
        email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        email.attach_alternative(html_content, "text/html")
        email.send()

        return instance
    

class EntrepreneurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entrepreneur
        fields = '__all__'
        read_only_fields = ['id','createdAt']

    def create(self, validated_data):
        instance = super().create(validated_data)

        # Prepare email content
        subject = 'Thank you for registering as an investor'
        from_email = 'amir.esfahanizadeh@landaholding.com'
        to_email = instance.email
        context = {'first_name': instance.firstName}
        text_content = f"Hi {instance.firstName},\n\nThank you for registering as an investor. We appreciate your interest and will get back to you shortly.\n\nBest regards,\nThe Investment Platform Team"
        html_content = render_to_string('Entrepreneur_registration_email.html', context)

        # Create and send email
        email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        email.attach_alternative(html_content, "text/html")
        email.send()

        return instance
    
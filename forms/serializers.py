from .models import StartUpsForm,ContactUs,AffiliateRegistration,InvestorRegistration,MentorRegistration,TeamRegistration
from rest_framework import serializers
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .graph_mail import send_graph_mail
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .utils import save_request_file
import logging
import os
import mimetypes
import secrets, string

logger = logging.getLogger(__name__)

class StartupFormSerializer(serializers.ModelSerializer):
    pitchDeckFile = serializers.FileField(required=False)
    businessPlanFile = serializers.FileField(required=False)
    financialModelFile = serializers.FileField(required=False)
    financialFile = serializers.FileField(required=False)

    class Meta:
        model = StartUpsForm
        fields = '__all__'
        read_only_fields = ['id', 'createdAt']

    def create(self, validated_data):
        instance = super().create(validated_data)

        subject = 'Your Startup Information Has Been Received by NovaNest'
        from_email = settings.MS_GRAPH_SENDER  # Use configured default sender
        to_email = instance.email
        context = {
            'first_name': instance.firstName,
            'last_name': instance.lastName,
            'email': instance.email,
            'phone_number': instance.phoneNumber,
            'country_of_residence': instance.countryOfResidence,
            'city_of_residence': instance.cityOfResidence,
            
            'startup_type': instance.startupType,
            
            'pitch_deck_file': instance.pitchDeckFile.url if instance.pitchDeckFile else None,
            
            'product_name': instance.productName,
            'site_address': instance.siteAddress,
            
            'customer_problem': instance.customerProblem,
            
            'unique_value_proposition': instance.uniqueValueProposition,
            'technology_readiness_level': instance.technologyReadinessLevel,
            
            'monetization_of_your_plan': instance.monetizationOfYourPlan,
            'structure_of_your_sales': instance.structureOfYourSales,
            
            'customer_characteristic': instance.customerCharacteristic,
            'current_customers': instance.currentCustomers,
            'estimated_market_size': instance.estimatedMarketSize,
            
            'startup_revenue': instance.startupRevenue,
            'monthly_income': instance.monthlyIncome,
            'current_interest_rate': instance.currentInterestRate,
            'current_raised_funding': instance.currentRaisedFunding,
            'needed_capital': instance.neededCapital,
            
            'business_plan_file': instance.businessPlanFile.url if instance.businessPlanFile else None,
            
            'financial_file': instance.financialFile.url if instance.financialFile else None,
            
            'cooperated_with_investors': instance.cooperatedWithInvestors,
            'how_did_you_know_us': instance.howDidYouKnowUs,
            
            'created_at': instance.createdAt,
            'updated_at': instance.updatedAt,
        }
        text_content = f"Hi {instance.firstName},\n\nThanks for registering your startup with us."
        html_content = render_to_string('startup_registration_email.html', context)

        # Try Graph first
        if not send_graph_mail(subject, 'startup_registration_email.html', context, [to_email], text_content):
            email = EmailMultiAlternatives(subject=subject, body=text_content, from_email=from_email, to=[to_email], cc=getattr(settings, "ALTERNATIVE_CC_EMAILS", []), bcc=getattr(settings, "ALTERNATIVE_BCC_EMAILS", []))
            email.attach_alternative(html_content, "text/html")
            try:
                email.send()
            except Exception as e:
                logger.error(f"Failed to send startup registration email (SMTP fallback): {e}")

        return instance
    
class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = '__all__'
        read_only_fields = ['id', 'createdAt']

    def create(self, validated_data):
        instance = super().create(validated_data)
        subject = 'Thanks for contacting us!'
        from_email = settings.MS_GRAPH_SENDER
        to_email = instance.email
        context = {'name': instance.name}
        text_content = f"Hi {instance.name},\n\nThanks for reaching out. We'll respond to your message shortly."
        html_content = render_to_string('contact_us_email.html', context)

        if not send_graph_mail(subject, 'contact_us_email.html', context, [to_email], text_content):
            email = EmailMultiAlternatives(subject=subject, body=text_content, from_email=from_email, to=[to_email], cc=getattr(settings, "ALTERNATIVE_CC_EMAILS", []), bcc=getattr(settings, "ALTERNATIVE_BCC_EMAILS", []))
            email.attach_alternative(html_content, "text/html")
            email.send()

        return instance

class AffiliateRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AffiliateRegistration
        fields = '__all__'
        read_only_fields = ['id', 'createdAt']

    def create(self, validated_data):
        instance = super().create(validated_data)
        subject = 'Your Affiliation Request Has Been Received by NovaNest'
        from_email = settings.MS_GRAPH_SENDER
        to_email = instance.email
        context = {
                'first_name': instance.firstName,
                'last_name': instance.lastName,
                'email': instance.email,
                'phone_number': instance.phoneNumber,
                'country': instance.countryOfResidence,
                'city': instance.cityOfResidence,
                'company_name': instance.companyName,
                'website': instance.website,
                'linkedin': instance.linkedin,
                'brief_introduction': instance.briefIntroduction,
                'how_did_you_know_us': instance.howDidYouKnowUs,
                'created_at': instance.createdAt,
            }
        text_content = f"Hi {instance.firstName},\n\nWe're excited to have you as an affiliate!"
        html_content = render_to_string('affiliate_registration_email.html', context)

        if not send_graph_mail(subject, 'affiliate_registration_email.html', context, [to_email], text_content):
            email = EmailMultiAlternatives(subject=subject, body=text_content, from_email=from_email, to=[to_email], cc=getattr(settings, "ALTERNATIVE_CC_EMAILS", []), bcc=getattr(settings, "ALTERNATIVE_BCC_EMAILS", []))
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
        subject = 'Thank You For Registering as an Investor'
        from_email = settings.MS_GRAPH_SENDER
        to_email = instance.email
        context = {
            'first_name': instance.firstName,
            'last_name': instance.lastName,
            'email': instance.email,
            'phone_number': instance.phoneNumber,
            'country_of_residence': instance.countryOfResidence,
            'investment_ceiling': instance.investmentCeiling,
            'preferred_areas': instance.preferredAreas,
            'how_did_you_know_us': instance.howDidYouKnowUs,
            'created_at': instance.createdAt,
            'updated_at': instance.updatedAt,
        }
        text_content = f"Hi {instance.firstName},\n\nThank you for registering as an investor. We appreciate your interest and will get back to you shortly.\n\nBest regards,\nThe Investment Platform Team"
        html_content = render_to_string('investor_registration_email.html', context)

        # Create and send email
        if not send_graph_mail(subject, 'investor_registration_email.html', context, [to_email], text_content):
            email = EmailMultiAlternatives(subject=subject, body=text_content, from_email=from_email, to=[to_email], cc=getattr(settings, "ALTERNATIVE_CC_EMAILS", []), bcc=getattr(settings, "ALTERNATIVE_BCC_EMAILS", []))
            email.attach_alternative(html_content, "text/html")
            email.send()

        return instance


class MentorRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MentorRegistration
        fields = '__all__'
        read_only_fields = ['id','createdAt']

    def create(self, validated_data):
        instance = super().create(validated_data)

        # Prepare email content
        subject = 'Thank You for Your Interest in Joining NovaNest as a Mentor'
        from_email = settings.MS_GRAPH_SENDER
        to_email = instance.email
        context = {
            'first_name': instance.firstName,
            'last_name': instance.lastName,
            'email': instance.email,
            'phone_number': instance.phoneNumber,
            'country_of_residence': instance.countryOfResidence,
            'city_of_residence': instance.cityOfResidence,
            'birth_date': instance.birthDate,
            'website': instance.website,
            'linkedin': instance.linkedin,
            'instagram': instance.instagram,
            'experties_areas': instance.ExpertiesAreas,
            'how_did_you_know_us': instance.howDidYouKnowUs,
            'created_at': instance.createdAt,
        }
        text_content = f"Hi {instance.firstName},\n\nThank you for registering as a mentor. We appreciate your interest and will get back to you shortly.\n\nBest regards,\nThe Mentorship Platform Team"
        html_content = render_to_string('mentor_registration_email.html', context)

        # Create and send email
        if not send_graph_mail(subject, 'mentor_registration_email.html', context, [to_email], text_content):
            email = EmailMultiAlternatives(subject=subject, body=text_content, from_email=from_email, to=[to_email], cc=getattr(settings, "ALTERNATIVE_CC_EMAILS", []), bcc=getattr(settings, "ALTERNATIVE_BCC_EMAILS", []))
            email.attach_alternative(html_content, "text/html")
            email.send()

        return instance
    
class TeamRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamRegistration
        fields = '__all__'
        read_only_fields = ['id','createdAt']

    def validate(self, data):
        """
        Conditional validation depending on presence of cvFile in request.FILES or initial_data.
        - If cvFile is present: require cvFile, firstName, lastName, email, phoneNumber,
          TypeOfCollaboration, FieldOfExpert
        - If cvFile not present: require firstName, lastName, email, phoneNumber,
          TypeOfCollaboration, FieldOfExpert, birthDate, educationField, educationLevel, workHistorySummary
        """
        request = self.context.get('request')
        initial = getattr(self, 'initial_data', {}) or {}
        files = getattr(request, 'FILES', {}) if request is not None else {}
        has_cv = bool(files.get('cvFile') or initial.get('cvFile'))

        required_base = ['firstName', 'lastName', 'email', 'phoneNumber', 'countryOfResidence', 'cityOfResidence', 'TypeOfCollaboration', 'FieldOfExpert']
        required_extra = ['birthDate', 'educationField', 'educationLevel', 'workHistorySummary']

        missing = {}
        # check file separately
        if has_cv:
            if not (files.get('cvFile') or initial.get('cvFile')):
                missing['cvFile'] = 'cvFile is required when uploading a CV.'

        # choose required set
        required = required_base + ( [] if has_cv else required_extra )

        for key in required:
            # look in validated data first then raw initial_data
            val = data.get(key) if isinstance(data, dict) else None
            if val in [None, '']:
                val = initial.get(key, None)
            if val in [None, '']:
                missing[key] = 'This field is required.'

        if missing:
            raise serializers.ValidationError(missing)

        return data

    def create(self, validated_data):
        request = self.context.get('request')
        
        # check file is available in the request
        files = getattr(request, 'FILES', {}) or {}
        saved_path = None
        saved_filename = None
        uploaded_content = None
        if 'cvFile' in files and files['cvFile']:
            saved_path, saved_filename, uploaded_content = save_request_file(
                request=request,
                field_name='cvFile',
                storage_dir='team_cv',
                random_length=15
            )
            
        instance = super().create(validated_data)

        cv_present = bool(uploaded_content)

        context = {
            'first_name': instance.firstName,
            'last_name': instance.lastName,
            'email': instance.email,
            'phone_number': instance.phoneNumber,
            'country_of_residence': instance.countryOfResidence,
            'city_of_residence': instance.cityOfResidence,
            'type_of_collaboration': instance.TypeOfCollaboration,
            'field_of_expert': instance.FieldOfExpert,
            'birth_date': instance.birthDate,
            'education_level': instance.educationLevel,
            'education_field': instance.educationField,
            'work_history_summary': instance.workHistorySummary,
            'created_at': instance.createdAt,
            
            'cv_present': cv_present,
        }

        subject = 'Thank You for Registering to Join Our Team'
        from_email = settings.MS_GRAPH_SENDER
        to_email = instance.email
        text_content = f"Hi {instance.firstName},\n\nThank you for registering to join our team. We appreciate your interest and will get back to you shortly.\n\nBest regards,\nThe Team Platform Team"

        # Prepare attachments for Graph
        attachments = []
        if cv_present:
            ctype = mimetypes.guess_type(saved_filename)[0] or 'application/octet-stream'
            logger.debug("Attached CV for %s: filename=%s type=%s", to_email, saved_filename, ctype)
            attachments.append((saved_filename, uploaded_content, ctype))
        
        # Try Graph with attachments
        use_smtp_fallback = not send_graph_mail(
            subject, 
            'team_registration_email.html', 
            context, 
            [to_email], 
            text_content,
            attachments=attachments or None
        )
    
        if use_smtp_fallback:
            from django.template.loader import render_to_string
            
            html_content = render_to_string('team_registration_email.html', context)
            email = EmailMultiAlternatives(subject=subject, body=text_content, from_email=from_email, to=[to_email], cc=getattr(settings, "ALTERNATIVE_CC_EMAILS", []), bcc=getattr(settings, "ALTERNATIVE_BCC_EMAILS", []))
            email.attach_alternative(html_content, "text/html")

            # attach CV file if present
            if cv_present:
                ctype = mimetypes.guess_type(saved_filename)[0] or 'application/octet-stream'
                email.attach(saved_filename, uploaded_content, ctype)
                logger.debug("Attached CV for %s: filename=%s type=%s", to_email, saved_filename, ctype)
                
            email.send()
 
        return instance
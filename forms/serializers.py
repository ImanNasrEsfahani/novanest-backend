from .models import StartUpsForm,ContactUs,PartnerMembership,InvestorRegistration,MentorRegistration,TeamRegistration,Entrepreneur
from rest_framework import serializers
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .graph_mail import send_graph_mail
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import logging
import os
import mimetypes

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
        from_email = settings.MS_GRAPH_SENDER  # Use configured default sender
        to_email = instance.email
        context = {'first_name': instance.firstName}
        text_content = f"Hi {instance.firstName},\n\nThanks for registering your startup with us."
        html_content = render_to_string('startup_registration_email.html', context)

        # Try Graph first
        if not send_graph_mail(subject, 'startup_registration_email.html', context, [to_email], text_content):
            email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
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
                'website': instance.websiteAddress,
                'linkedin': instance.linkedinAddress,
                'brief_intro': instance.briefIntroduction,
                'how_did_you_know': instance.howDidYouKnowUs,
                'created_at': instance.createdAt,
            }
        text_content = f"Hi {instance.firstName},\n\nWe're excited to have you as a partner!"
        html_content = render_to_string('partner_membership_email.html', context)

        if not send_graph_mail(subject, 'partner_membership_email.html', context, [to_email], text_content):
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
        from_email = settings.MS_GRAPH_SENDER
        to_email = instance.email
        context = {'first_name': instance.firstName}
        text_content = f"Hi {instance.firstName},\n\nThank you for registering as an investor. We appreciate your interest and will get back to you shortly.\n\nBest regards,\nThe Investment Platform Team"
        html_content = render_to_string('investor_registration_email.html', context)

        # Create and send email
        if not send_graph_mail(subject, 'investor_registration_email.html', context, [to_email], text_content):
            email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
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
        subject = 'Thank you for registering as a mentor'
        from_email = settings.MS_GRAPH_SENDER
        to_email = instance.email
        context = {'first_name': instance.firstName}
        text_content = f"Hi {instance.firstName},\n\nThank you for registering as a mentor. We appreciate your interest and will get back to you shortly.\n\nBest regards,\nThe Mentorship Platform Team"
        html_content = render_to_string('mentor_registration_email.html', context)

        # Create and send email
        if not send_graph_mail(subject, 'mentor_registration_email.html', context, [to_email], text_content):
            email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
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

        required_base = ['firstName', 'lastName', 'email', 'phoneNumber', 'TypeOfCollaboration', 'FieldOfExpert']
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
        uploaded = getattr(request, 'FILES', {}).get('cvFile')
        saved_path = None
        if uploaded:
            # unique path example
            name = f"team_cv/{uploaded.name}"
            saved_path = default_storage.save(name, ContentFile(uploaded.read()))

        # remove cvFile from validated_data if present to avoid unexpected keys
        if uploaded and 'cvFile' not in validated_data:
            # save instance first
            instance = super().create(validated_data)
            # set FileField on instance (assumes TeamRegistration.cvFile exists)
            instance.cvFile = uploaded
            instance.save(update_fields=['cvFile'])
        else:
            instance = super().create(validated_data)

        # get request.FILES safely and log
        try:
            req_files = getattr(request, 'FILES', {}) or {}
        except Exception:
            req_files = {}
        logger.debug("TeamRegistration.create: request.FILES keys=%s validated_data_keys=%s",
                     list(req_files.keys()), list(validated_data.keys()))

        cv_file = getattr(instance, 'cvFile', None)
        cv_present = bool(cv_file)
        
        logger.debug("TeamRegistration.create: cv_file %s", cv_file)
        logger.debug("TeamRegistration.create: cv_present %s", cv_present)

        context = {
            'first_name': instance.firstName,
            'last_name': instance.lastName,
            'email': instance.email,
            'phone_number': instance.phoneNumber,
            'type_of_collaboration': instance.TypeOfCollaboration,
            'field_of_expert': instance.FieldOfExpert,
            'birth_date': instance.birthDate,
            'education_level': instance.educationLevel,
            'education_field': instance.educationField,
            'work_history_summary': instance.workHistorySummary,
            'created_at': instance.createdAt,
            
            'cv_present': cv_present,
            'cv_filename': os.path.basename(cv_file.name) if cv_present else None,
        }

        subject = 'Thank you for registering to join our team'
        from_email = settings.MS_GRAPH_SENDER
        to_email = instance.email
        text_content = f"Hi {instance.firstName},\n\nThank you for registering to join our team. We appreciate your interest and will get back to you shortly.\n\nBest regards,\nThe Team Platform Team"
        html_content = render_to_string('team_registration_email.html', context)

        # Try Graph first (existing helper). If it doesn't handle attachments, fallback SMTP will attach.
        if not send_graph_mail(subject, 'team_registration_email.html', context, [to_email], text_content):
            email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
            email.attach_alternative(html_content, "text/html")

            # attach CV file if present on the instance (SMTP fallback)
            if cv_present:
                try:
                    # ensure file is open
                    try:
                        cv_file.open(mode='rb')
                    except Exception:
                        pass
                    filename = os.path.basename(cv_file.name)
                    content = cv_file.read()
                    ctype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
                    email.attach(filename, content, ctype)
                except Exception as e:
                    logger.exception("Failed to attach CV file to email: %s", e)
                finally:
                    try:
                        cv_file.close()
                    except Exception:
                        pass

            try:
                email.send()
            except Exception as e:
                logger.error(f"Failed to send team registration email (SMTP fallback): {e}")

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
        from_email = settings.MS_GRAPH_SENDER
        to_email = instance.email
        context = {'first_name': instance.firstName}
        text_content = f"Hi {instance.firstName},\n\nThank you for registering as an investor. We appreciate your interest and will get back to you shortly.\n\nBest regards,\nThe Investment Platform Team"
        html_content = render_to_string('Entrepreneur_registration_email.html', context)

        # Create and send email
        if not send_graph_mail(subject, 'Entrepreneur_registration_email.html', context, [to_email], text_content):
            email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
            email.attach_alternative(html_content, "text/html")
            email.send()

        return instance

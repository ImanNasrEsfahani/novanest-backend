from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from django.middleware.csrf import get_token
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from .models import StartUpsForm,ContactUs,AffiliateRegistration,InvestorRegistration,MentorRegistration,TeamRegistration,TraineeRegistration
from .serializers import StartupFormSerializer,ContactUsSerializer,AffiliateRegistrationSerializer,InvestorRegistrationSerializer, MentorRegistrationSerializer, TeamRegistrationSerializer, TraineeRegistrationSerializer
# Create your views here.

class StartUpsFormView(CreateAPIView):
    queryset = StartUpsForm.objects.all()
    serializer_class = StartupFormSerializer
    parser_classes = [FormParser,MultiPartParser]
    http_method_names = ['post']

class ContactUsView(CreateAPIView):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer
    http_method_names = ['post']

class AffiliateRegistrationView(CreateAPIView):
    queryset = AffiliateRegistration.objects.all()
    serializer_class = AffiliateRegistrationSerializer
    http_method_names = ['post']

class InvestorRegistrationView(CreateAPIView):
    queryset = InvestorRegistration.objects.all()
    serializer_class = InvestorRegistrationSerializer
    http_method_names = ['post']

class JoinAsMentorView(CreateAPIView):
    queryset = MentorRegistration.objects.all()
    serializer_class = MentorRegistrationSerializer
    http_method_names = ['post']

class JoinOurTeamView(CreateAPIView):
    queryset = TeamRegistration.objects.all()
    serializer_class = TeamRegistrationSerializer
    parser_classes = [JSONParser, FormParser, MultiPartParser]  # accept JSON and file uploads
    http_method_names = ['post']

class JoinOurTraineeView(CreateAPIView):
    queryset = TraineeRegistration.objects.all()
    serializer_class = TraineeRegistrationSerializer
    parser_classes = [JSONParser, FormParser, MultiPartParser]  # accept JSON and file uploads
    http_method_names = ['post']

# csrf token 
class CSRFTokenView(APIView):
    def get(self, request, format=None):
        token = get_token(request)
        return Response({'csrfToken': token})
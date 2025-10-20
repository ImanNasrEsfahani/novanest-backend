from django.urls import path
from .views import StartUpsFormView,ContactUsView,AffiliateRegistrationView,InvestorRegistrationView,JoinAsMentorView,JoinOurTeamView,JoinOurTraineeView,CSRFTokenView


app_name = "forms"
urlpatterns = [
    path('startups-form',StartUpsFormView.as_view(),name='startups-form'),
    path('contactUs-form',ContactUsView.as_view(),name='contactus-form'),
    path('affiliate-registration-form',AffiliateRegistrationView.as_view(),name='affiliate-registration'),
    path('investor-registration',InvestorRegistrationView.as_view(),name='investor-registration'),
    path('join-as-mentor',JoinAsMentorView.as_view(),name='join-as-mentor'),
    path('join-our-team',JoinOurTeamView.as_view(),name='join-our-team'),
    path('join-as-a-trainee',JoinOurTraineeView.as_view(),name='join-as-a-trainee'),
    path('get-csrf-token', CSRFTokenView.as_view(), name='get_csrf_token'),
]
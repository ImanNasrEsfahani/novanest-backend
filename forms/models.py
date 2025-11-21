from django.db import models

# Create your models here.

class StartUpsForm(models.Model):
  firstName=models.CharField(max_length=300,blank=True)
  lastName=models.CharField(max_length=300,blank=True)
  email=models.EmailField(max_length=75, blank=True)
  phoneNumber=models.CharField(max_length=250,blank=True)
  countryOfResidence=models.CharField(max_length=300,blank=True)
  cityOfResidence=models.CharField(max_length=300,blank=True)
  
  # MVP or Early Traction or Scale-Up
  startupType=models.CharField(max_length=300,blank=True)
  
  # with Pitchdeck file
  pitchDeckFile=models.FileField(upload_to='pitchdeckfile',null=True,blank=True,editable=True)      
  
  # General Information without pitchdeck file
  productName=models.CharField(max_length=500,blank=True)
  siteAddress=models.CharField(max_length=500,blank=True)
  
  # Problem accordion
  customerProblem=models.TextField(max_length=1500, blank=True)
  
  # Solution accordion
  uniqueValueProposition=models.TextField(max_length=1500, blank=True)
  technologyReadinessLevel=models.TextField(max_length=1500, blank=True)
  
  # business model accordion
  monetizationOfYourPlan=models.TextField(max_length=1500, blank=True)
  structureOfYourSales=models.TextField(max_length=1500, blank=True)
  
  # Target Market accordion
  customerCharacteristic = models.TextField(max_length=1500, blank=True)
  currentCustomers = models.TextField(max_length=1500, blank=True)
  estimatedMarketSize= models.TextField(max_length=1500, blank=True)
  
  # Property accordion
  startupRevenue=models.TextField(max_length=1500, blank=True)
  monthlyIncome=models.TextField(max_length=1500, blank=True)
  currentInterestRate=models.TextField(max_length=1500, blank=True)
  currentRaisedFunding=models.TextField(max_length=1500, blank=True)
  neededCapital=models.TextField(max_length=1500, blank=True)
  
  # other files
  businessPlanFile=models.FileField(upload_to='businessPlan',null=True,blank=True,editable=True)
  financialFile= models.FileField(upload_to='financialFile',null=True,blank=True,editable=True)
  
  # last questions
  cooperatedWithInvestors=models.TextField(max_length=1500, blank=True)
  howDidYouKnowUs=models.TextField(max_length=1500, blank=True)
  
  createdAt= models.DateTimeField(auto_now_add=True,blank=True)
  updatedAt= models.DateTimeField(auto_now=True,blank=True)


class ContactUs(models.Model):
  firstName=models.CharField(max_length=250,blank=True)
  lastName=models.CharField(max_length=250,blank=True)
  email=models.EmailField(max_length=75, blank=True)
  phoneNumber=models.CharField(max_length=250,blank=True)
  subject=models.CharField(max_length=500,blank=True)
  message=models.TextField(max_length=1500, blank=True)
  createdAt=models.DateTimeField(auto_now_add=True,blank=True)


class AffiliateRegistration(models.Model):
  firstName=models.CharField(max_length=500, blank=True)
  lastName=models.CharField(max_length=500, blank=True)
  email=models.EmailField(max_length=75, blank=True)
  phoneNumber=models.CharField(max_length=15, blank=True)
  countryOfResidence=models.CharField(max_length=300, blank=True)
  cityOfResidence=models.CharField(max_length=300, blank=True)
  companyName=models.CharField(max_length=500, blank=True)
  website=models.CharField(max_length=500, blank=True)
  linkedin=models.CharField(max_length=500, blank=True)
  briefIntroduction=models.TextField(max_length=1500, blank=True)
  howDidYouKnowUs=models.TextField(max_length=1500, blank=True)
  createdAt=models.DateTimeField(auto_now_add=True, blank=True)     
  updatedAt=models.DateTimeField(auto_now=True, blank=True)

class InvestorRegistration(models.Model):
  firstName=models.CharField(max_length=500, blank=True)
  lastName=models.CharField(max_length=500, blank=True)
  email=models.EmailField(max_length=75, blank=True)
  phoneNumber=models.CharField(max_length=25, blank=True)
  countryOfResidence=models.CharField(max_length=300, blank=True)
  investmentCeiling=models.CharField(max_length=500, blank=True)
  preferredAreas=models.CharField(max_length=500, blank=True)
  howDidYouKnowUs=models.CharField(max_length=1500, blank=True)
  createdAt=models.DateTimeField(auto_now_add=True)
  updatedAt=models.DateTimeField(auto_now=True)

class MentorRegistration(models.Model):
  firstName=models.CharField(max_length=500, blank=True)
  lastName=models.CharField(max_length=500, blank=True)
  email=models.EmailField(max_length=75, blank=True)
  phoneNumber=models.CharField(max_length=25, blank=True)
  countryOfResidence=models.CharField(max_length=300, blank=True)
  cityOfResidence=models.CharField(max_length=300, blank=True)
  birthDate=models.DateField(blank=True)
  website=models.CharField(max_length=500, blank=True)
  linkedin=models.CharField(max_length=500, blank=True)
  instagram=models.CharField(max_length=500, blank=True)
  ExpertiesAreas=models.CharField(max_length=1500, blank=True)
  howDidYouKnowUs=models.CharField(max_length=1500, blank=True)
  createdAt=models.DateTimeField(auto_now_add=True)
  updatedAt=models.DateTimeField(auto_now=True)

class TeamRegistration(models.Model):
  firstName=models.CharField(max_length=500, blank=True)
  lastName=models.CharField(max_length=500, blank=True)
  email=models.EmailField(max_length=75, blank=True)
  phoneNumber=models.CharField(max_length=25, blank=True)
  countryOfResidence=models.CharField(max_length=300, blank=True)
  cityOfResidence=models.CharField(max_length=300, blank=True)
  TypeOfCollaboration=models.CharField(max_length=100, blank=True)
  FieldOfExpert=models.CharField(max_length=100, blank=True)
  FieldOfExpertOther=models.CharField(max_length=100, blank=True)
  birthDate=models.DateField(null=True, blank=True)
  educationLevel=models.CharField(max_length=100, null=True, blank=True)
  educationField=models.CharField(max_length=300, null=True, blank=True)
  workHistorySummary=models.CharField(max_length=1500, null=True, blank=True)
  createdAt=models.DateTimeField(auto_now_add=True)
  updatedAt=models.DateTimeField(auto_now=True)

class TraineeRegistration(models.Model):
  firstName=models.CharField(max_length=500, blank=True)
  lastName=models.CharField(max_length=500, blank=True)
  email=models.EmailField(max_length=75, blank=True)
  phoneNumber=models.CharField(max_length=25, blank=True)
  countryOfResidence=models.CharField(max_length=300, blank=True)
  cityOfResidence=models.CharField(max_length=300, blank=True)
  birthDate=models.DateField(null=True, blank=True)
  fieldOfExpert=models.CharField(max_length=100, blank=True)
  fieldOfExpertOther=models.CharField(null=True, max_length=100, blank=True)
  tellUsAboutYourself=models.CharField(max_length=1500, null=True, blank=True)
  createdAt=models.DateTimeField(auto_now_add=True)
  updatedAt=models.DateTimeField(auto_now=True)

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.
class Adult(models.Model):
    sfu_id = models.IntegerField()
    given_name = models.CharField(max_length = 100)
    surname = models.CharField(max_length = 100)
    birth_date = models.DateField()
    address = models.CharField(max_length=200)
    yearsOfEducation = models.SmallIntegerField(
        validators=[
            MinValueValidator(0), 
            MaxValueValidator(50),
        ]
    )
    phone = models.CharField(max_length=50)
    email = models.EmailField()

    GENDER_CHOICES = (
        ('F', 'Female'),
        ('M', 'Male'),
        ('O', 'Other'),
    )
    gender = models.CharField(
        max_length = 1, 
        choices = GENDER_CHOICES
    )

    CONTACT_CHOICES = (
        ('P', 'Phone'),
        ('E', 'Email'),
    )
    contact_pref = models.CharField(
        max_length = 1,
        choices = CONTACT_CHOICES,
    )    

    PHONETIME_CHOICES = (
        ('WDM', 'Weekday Mornings'),
        ('WDA', 'Weekday Afternoons'),
        ('WDE', 'Weekday Evenings'),
        ('WEM', 'Weekend Mornings'),
        ('WEA', 'Weekend Afternoons'),
        ('WEE', 'Weekend Evenings'),
        ('DNC', 'Do Not Call'),
        ('ANY', 'Anytime'),
    )
    pref_phone_time = models.CharField(
        max_length = 3,
        choices = PHONETIME_CHOICES
    )
    def __str__(self):
        return self.given_name

# class Child(models.Model):
#     givenName = models.CharField(max_length=100)
#     surName = models.CharField(max_length=100)
#     birthDate = models.DateField('Birth Date')
#     gestationLengthWeeks = models.SmallIntegerField()
#     fullTerm = models.BooleanField()
#     birthWeight = models.SmallIntegerField()
#     birthHeight = models.SmallIntegerField()
#     personalNotes = models.TextField(max_length=1000)
#     # hxRepeatedEarInfection
#     # lastEarInfection
#     # hereditaryAuditoryProblems
#     # hereditaryLanguagePathologies
#     # healthNotes

#     FEMALE = 'FEMALE'
#     MALE = 'MALE'
#     OTHER = 'OTHER'
#     GENDER_CHOICES = (
#         (FEMALE, 'Female'),
#         (MALE, 'Male'),
#         (OTHER, 'Other'),
#     )
#     gender = models.CharField(
#         max_length = 6, 
#         choices = GENDER_CHOICES,
#         default = OTHER,
#     )
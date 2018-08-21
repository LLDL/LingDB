from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class Language(models.Model):
    language_name = models.CharField(max_length = 100, primary_key=True)
    
class Family(models.Model):
    class Meta:
        verbose_name_plural = "Families"

class Musical_Experience(models.Model):
    class Meta:
        verbose_name = "Musical Experience"
        verbose_name_plural = "Musical Experiences"
    skill = models.CharField(max_length = 100)

class Adult(models.Model):
    sfu_id = models.IntegerField(blank = True, null = True)
    given_name = models.CharField(max_length = 100)
    preferred_name = models.CharField(max_length = 100, blank = True, null = True)
    surname = models.CharField(max_length = 100)
    birth_date = models.DateField()
    address = models.CharField(max_length=200)
    years_of_education = models.SmallIntegerField(
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
        choices = PHONETIME_CHOICES,
        blank = True, 
        null = True
    )
    def __str__(self):
        return self.given_name

    languages = models.ManyToManyField(Language, through='Speaks')
    musical_experiences = models.ManyToManyField(Musical_Experience, through='IsExperiencedIn')
    parent_in = models.ManyToManyField(Family, through='IsParentIn', blank = True)


class Child(models.Model):
    class Meta:
        verbose_name_plural = "Children"
    given_name = models.CharField(max_length = 100)
    preferred_name = models.CharField(max_length = 100, blank = True, null = True)
    birth_date = models.DateField()
    gestation_length_weeks = models.SmallIntegerField(blank = True, null = True)
    was_full_term = models.BooleanField(blank = True, null = True)
    birth_weight = models.SmallIntegerField()
    birth_height = models.SmallIntegerField()
    personal_notes = models.TextField(max_length=1000)
    hx_repeated_ear_infection = models.TextField(max_length=1000, blank = True, null = True)
    last_ear_infection = models.DateField(blank = True, null = True)
    hereditary_audio_problems = models.BooleanField()
    hereditary_language_pathologies = models.BooleanField()
    health_notes = models.TextField(max_length=1000, blank = True, null = True)
    family = models.ManyToManyField(Family)
    exposed_to = models.ManyToManyField(Language, through='IsExposedTo')

    GENDER_CHOICES = (
        ('F', 'Female'),
        ('M', 'Male'),
        ('O', 'Other'),
    )
    gender = models.CharField(
        max_length = 1, 
        choices = GENDER_CHOICES
    )

class IsExposedTo(models.Model):
    class Meta:
        verbose_name_plural = "Is Exposed To"
    child = models.ForeignKey(Child, on_delete = models.PROTECT)
    language = models.ForeignKey(Language, on_delete = models.PROTECT)
    percentage_exposure = models.SmallIntegerField(
        validators=[
            MinValueValidator(0), 
            MaxValueValidator(100),
        ]
    )

class Speaks(models.Model):
    class Meta:
        verbose_name_plural = "Speaks"
    person = models.ForeignKey(Adult, on_delete = models.PROTECT)
    language = models.ForeignKey(Language, on_delete = models.PROTECT)
    is_native = models.BooleanField()
    nth_most_dominant = models.SmallIntegerField(
        validators=[
            MinValueValidator(1), 
            MaxValueValidator(20),
        ]
    )
    age_learning_started = models.SmallIntegerField(
        validators=[
            MinValueValidator(0), 
            MaxValueValidator(120),
        ]
    )

    age_learning_ended = models.SmallIntegerField(
        validators=[
            MinValueValidator(0), 
            MaxValueValidator(120),
        ]
    )

class IsExperiencedIn(models.Model):
    class Meta:
        verbose_name_plural = "Musical Experience Relations"
    person = models.ForeignKey(Adult, on_delete = models.PROTECT)
    experience = models.ForeignKey(Musical_Experience, on_delete = models.PROTECT)
    nth_most_dominant = models.SmallIntegerField(
        validators=[
            MinValueValidator(1), 
            MaxValueValidator(20),
        ]
    )
    age_learning_started = models.SmallIntegerField(
        validators=[
            MinValueValidator(0), 
            MaxValueValidator(120),
        ]
    )

    age_learning_ended = models.SmallIntegerField(
        validators=[
            MinValueValidator(0), 
            MaxValueValidator(120),
        ]
    )

class IsParentIn(models.Model):
    class Meta:
        verbose_name_plural = "Parents"
    person = models.ForeignKey(Adult, on_delete = models.PROTECT)
    family = models.ForeignKey(Family, on_delete = models.PROTECT)
    is_primary_contact = models.BooleanField()




class Experiment(models.Model):
    class Meta:
        verbose_name = "Experiment"
        verbose_name_plural = "Experiments"
    experiment_name = models.CharField(max_length = 100)
    LAB_CHOICES = (
        ('ld', 'LangDev'),
        ('ph', 'Phono'),
    )
    lab = models.CharField(
        max_length = 2,
        choices = LAB_CHOICES
    )
    STATUS_CHOICES = (
        ('prep', 'In Prep'),
        ('recruiting', 'Actively Recruiting'),
        ('inactive', 'Inactive'),
    )
    status = models.CharField(
        max_length = 10, 
        choices = STATUS_CHOICES
    )


class Experiment_Section(models.Model):
    class Meta:
        verbose_name = "Experiment Section"
        verbose_name_plural = "Experiment Sections"
    experiment_section_name = models.CharField(max_length = 100)
    STATUS_CHOICES = (
        ('prep', 'In Prep'),
        ('recruiting', 'Actively Recruiting'),
        ('inactive', 'Inactive'),
    )
    status = models.CharField(
        max_length = 10, 
        choices = STATUS_CHOICES
    )
    section_of = models.ForeignKey(Language, on_delete=models.CASCADE)

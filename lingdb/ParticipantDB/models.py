from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.contrib.auth.models import Group, User



class Language(models.Model):
    class Meta:
        verbose_name = "Language"
        verbose_name_plural = "Languages"
        ordering = ['language_name']
    language_name = models.CharField("Language Name", max_length = 100, primary_key = True)
    def __str__(self):
        return '%s' % (self.language_name) 

class MusicalSkill(models.Model):
    class Meta:
        verbose_name = "Musical Skill"
        verbose_name_plural = "Musical Skills"
        ordering = ['skill']
    skill = models.CharField('Skill', max_length = 100, primary_key = True)
    def __str__(self):
        return '%s' % (self.skill) 

class Lab(models.Model):
    class Meta:
        verbose_name = "Lab"
        verbose_name_plural = "Labs"
        ordering = ['lab_name']
    lab_name = models.CharField(max_length = 100, primary_key = True)
    group = models.ForeignKey(Group, null= True, blank= True, on_delete = models.SET_NULL)
    def __str__(self):
        return '%s' % (self.lab_name) 

class Person(models.Model):
    id = models.IntegerField(primary_key = True, verbose_name = "ID")
    given_name = models.CharField(max_length = 100, verbose_name = "Given Name")
    preferred_name = models.CharField(max_length = 100, blank = True, null = True, verbose_name = "Preferred Name")
    surname = models.CharField(max_length = 100, default='', verbose_name = "Surname")
    birth_date = models.DateField(verbose_name = "Birth Date")
    gender = models.CharField(max_length = 100, default='')
    health_notes = models.TextField(max_length=1000, blank = True, null = True, verbose_name = "Health Notes")
    personal_notes = models.TextField(max_length=1000, blank = True, null = True, verbose_name="Personal Notes")
    def __str__(self):
        return '%s: %s %s' % (self.id, self.given_name, self.surname) 

    class Meta:
        abstract = True
    
class Adult(Person):
    class Meta:
        verbose_name = "Adult"
        verbose_name_plural = "Adults"
        ordering = ['id']
    sfu_id = models.IntegerField(blank = True, null = True, verbose_name = "SFU ID")
    address = models.CharField(max_length=200, blank = True, null = True)
    years_of_education = models.IntegerField(
        blank = True,
        null = True,
        validators=[
            MinValueValidator(0), 
            MaxValueValidator(20),
        ],
        verbose_name = "Years of Education"
    )
    phone = models.CharField(max_length=50, blank = True, null = True)
    email = models.EmailField(blank = True, null = True)

    CONTACT_CHOICES = (
        ('P', 'Phone'),
        ('E', 'Email'),
    )
    contact_pref = models.CharField(max_length=1, choices = CONTACT_CHOICES, verbose_name = "Contact Preference", blank = True, null = True)    

    PHONETIME_CHOICES = (
        ('WDM', 'Weekday Mornings'),
        ('WDA', 'Weekday Afternoons'),
        ('WDE', 'Weekday Evenings'),
        ('WEM', 'Weekend Mornings'),
        ('WEA', 'Weekend Afternoons'),
        ('WEE', 'Weekend Evenings'),
        ('ANY', 'Anytime'),
        ('DNC', 'Do Not Call'),
    )
    pref_phone_time = models.CharField(max_length = 3, choices = PHONETIME_CHOICES, verbose_name = "Preferred Phone Time", blank = True, null = True)
    
    languages = models.ManyToManyField('Language', blank = True, through='Speaks', related_name = 'speaks')
    musical_background = models.ManyToManyField('MusicalSkill', blank = True, through='MusicalExperience')


class Child(Person):
    class Meta:
        verbose_name = "Child"
        verbose_name_plural = "Children"
        ordering = ['id']
    gestation_length_weeks = models.SmallIntegerField(blank = True, null = True, verbose_name = "Gestation Length (Weeks)")
    was_full_term = models.BooleanField(blank = True, null = True, verbose_name = "Was Full Term?")
    birth_weight = models.SmallIntegerField(blank = True, null = True, verbose_name = "Birth Weight (Grams)")
    birth_height = models.SmallIntegerField(blank = True, null = True, verbose_name = "Birth Height (CM)")
    hx_repeated_ear_infection = models.TextField(max_length=1000, blank = True, null = True, verbose_name = "HX of Repeated Ear Infection")
    hereditary_audio_problems = models.BooleanField(verbose_name = "Hereditary Audio Problems?")
    hereditary_language_pathologies = models.BooleanField(verbose_name = "Hereditary Language Pathologies?")
    exposed_to = models.ManyToManyField('Language', through='IsExposedTo', default = None, verbose_name = "Languages Exposed To")

class Family(models.Model):
    class Meta:
        verbose_name = "Family"
        verbose_name_plural = "Families"
        ordering = ['id']
    id = models.IntegerField(primary_key = True, verbose_name = "ID")
    parents = models.ManyToManyField('Adult', through='IsParentIn')
    children = models.ManyToManyField('Child', through='IsChildIn')
    notes = models.TextField(max_length=1000, blank = True, null = True, verbose_name = "Notes")
    def __str__(self):
        return 'Family # %s' % (self.id) 

class Experiment(models.Model):
    class Meta:
        ordering = ['experiment_name']
    experiment_name = models.CharField('Experiment Name', max_length = 100, primary_key = True)
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)
    STATUS_CHOICES = (
        ('prep', 'In Prep'),
        ('recruiting', 'Actively Recruiting'),
        ('inactive', 'Inactive'),
    )
    status = models.CharField(max_length = 10, choices = STATUS_CHOICES)
    def __str__(self):
        return '%s' % (self.experiment_name) 

class Experiment_Section(models.Model):
    class Meta:
        verbose_name = "Experiment Section"
        verbose_name_plural = "Experiment Sections"
        ordering = ['experiment_section_name']
    experiment_section_name = models.CharField(max_length = 100)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    STATUS_CHOICES = (
        ('prep', 'In Prep'),
        ('recruiting', 'Actively Recruiting'),
        ('inactive', 'Inactive'),
    )
    section_status = models.CharField(max_length = 10, choices = STATUS_CHOICES)

    def __str__(self):
        return '%s: %s' % (self.experiment, self.experiment_section_name) 

class Experiment_Section_Run(models.Model):
    class Meta:
        verbose_name = "Experiment Section Run"
        verbose_name_plural = "Experiment Section Runs"
        ordering = ['experiment_section', 'participantAdult', 'participantChild']
    participantAdult = models.ForeignKey(Adult, verbose_name='Adult Participant', on_delete = models.CASCADE, null=True, blank=True)
    participantChild = models.ForeignKey(Child, verbose_name='Child Participant', on_delete = models.CASCADE, null=True, blank=True)
    experiment_section = models.ForeignKey(Experiment_Section, on_delete = models.CASCADE)
    date = models.DateField()
    notes = models.TextField(max_length=1000, null=True, blank=True)
    assessor = models.ForeignKey(User, null= True, blank= True, on_delete = models.SET_NULL)

class Experiment_Section_Field(models.Model):
    class Meta:
        verbose_name = "Experiment Section Field"
        verbose_name_plural = "Experiment Section Fields"
        ordering = ['field_name']
    field_name = models.CharField(max_length = 100, verbose_name = "Field Name")
    field_of = models.ForeignKey(Experiment_Section, on_delete = models.CASCADE)
    TYPE_OPTIONS = (
        ('Numeric', 'Numeric'),
        ('Pass/Fail', 'Pass/Fail'),
        ('Text', 'Text'),
    )
    type = models.CharField(max_length = 9, choices = TYPE_OPTIONS)
    def __str__(self):
        return '%s field %s for %s' % (self.type, self.field_name, self.field_of)

class Experiment_Section_Run_Field_Score(models.Model):
    experiment_section_run = models.ForeignKey(Experiment_Section_Run, on_delete = models.CASCADE)
    experiment_section_field = models.ForeignKey(Experiment_Section_Field, on_delete = models.CASCADE)
    score = models.CharField(max_length=100) 
    def __str__(self):
        return 'Score of [%s] for field [%s] of run [%s]' % (self.score, self.experiment_section_field, self.experiment_section_run)

class Assessment(models.Model):
    class Meta:
        ordering = ['assessment_name']
    assessment_name = models.CharField('Assessment Name', max_length = 100, primary_key = True)
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % (self.assessment_name) 


class Assessment_Run(models.Model):
    class Meta:
        verbose_name = "Assessment Run"
        verbose_name_plural = "Assessment Runs"
        ordering = ['participantAdult', 'participantChild']
    participantAdult = models.ForeignKey(Adult, verbose_name='Adult Participant', on_delete = models.CASCADE, null=True, blank=True)
    participantChild = models.ForeignKey(Child, verbose_name='Child Participant', on_delete = models.CASCADE, null=True, blank=True)
    assessment = models.ForeignKey(Assessment, on_delete = models.CASCADE, related_name="assessment_ran")

    date = models.DateField()
    notes = models.TextField(max_length=1000, null= True, blank= True)
    assessor = models.ForeignKey(User, null= True, blank= True, on_delete = models.SET_NULL)
    
    def __str__(self):
        return '%s took %s' % (self.participantAdult or self.participantChild, self.assessment)

class Assessment_Field(models.Model):
    class Meta:
        verbose_name = "Assessment Field"
        verbose_name_plural = "Assessment Fields"
    field_name = models.CharField(max_length = 100, verbose_name = "Field Name")
    field_of = models.ForeignKey(Assessment, on_delete = models.CASCADE)
    TYPE_OPTIONS = (
        ('Numeric', 'Numeric'),
        ('Pass/Fail', 'Pass/Fail'),
        ('Text', 'Text'),
    )
    type = models.CharField(max_length = 9, choices = TYPE_OPTIONS)
    def __str__(self):
        return '%s field %s for %s' % (self.type, self.field_name, self.field_of)

class Assessment_Run_Field_Score(models.Model):
    class Meta:
        verbose_name = "Assessment Run Field Score"
        verbose_name_plural = "Assessment Run Field Scores"
    assessment_run = models.ForeignKey(Assessment_Run, on_delete = models.CASCADE)
    assessment_field = models.ForeignKey(Assessment_Field, on_delete = models.CASCADE)
    score = models.CharField(max_length=100) 

    def __str__(self):
        return 'Score of [%s] for field [%s] of run [%s]' % (self.score, self.assessment_field, self.assessment_run)


class IsExposedTo(models.Model):
    class Meta:
        verbose_name = "Is Exposed To"
        verbose_name_plural = "Are Exposed To"
    child = models.ForeignKey(Child, on_delete = models.CASCADE, default = None)
    lang = models.ForeignKey(Language, on_delete = models.CASCADE, default = None)
    percentage_exposure = models.SmallIntegerField(
        validators=[
            MinValueValidator(0), 
            MaxValueValidator(100),
        ]
    )
    def __str__(self):
        return '%s is exposed %s to %s' % (self.child, self.percentage_exposure, self.lang) 

class Speaks(models.Model):
    class Meta:
        verbose_name_plural = "Speaks"
    person = models.ForeignKey(Adult, related_name = 'speaker', on_delete = models.CASCADE, default = None)
    lang = models.ForeignKey(Language, related_name = 'languagespoken', on_delete = models.CASCADE, default = None)
    is_native = models.BooleanField('', default = False)

    PROFICIENCY_OPTIONS = (
        ('Native', 'Native Like'),
        ('Advanced', 'Advanced'),
        ('Intermediate', 'Intermediate'),
        ('Basic','Basic'),
    )
    proficiency = models.CharField(max_length = 12, choices = PROFICIENCY_OPTIONS, default = 'Basic')

    age_learning_started = models.SmallIntegerField(
        validators=[
            MinValueValidator(0), 
            MaxValueValidator(120),
        ],
    )

    age_learning_ended = models.SmallIntegerField(
        blank=True,
        null=True,
        validators=[
            MinValueValidator(0), 
            MaxValueValidator(120),
        ],
    )
    def __str__(self):
        return '%s speaks %s at a %s level' % (self.person, self.lang, self.proficiency) 
        
class MusicalExperience(models.Model):
    class Meta:
        verbose_name_plural = "Musical Experiences"
    person = models.ForeignKey(Adult, related_name = 'musician', on_delete = models.CASCADE, default = None)
    experience = models.ForeignKey(MusicalSkill, related_name = 'instrument', on_delete = models.CASCADE, default = None)

    PROFICIENCY_OPTIONS = (
        ('Professional', 'Professional'),
        ('Advanced', 'Advanced'),
        ('Intermediate', 'Intermediate'),
        ('Basic','Basic'),
    )
    proficiency = models.CharField(max_length = 12, choices = PROFICIENCY_OPTIONS, default = 'Basic')


    age_learning_started = models.SmallIntegerField(
        validators=[
            MinValueValidator(0), 
            MaxValueValidator(120),
        ],
    )

    age_learning_ended = models.SmallIntegerField(
        blank=True,
        null=True,
        validators=[
            MinValueValidator(0), 
            MaxValueValidator(120),
        ],
    )
    def __str__(self):
        return '%s performs %s at a %s level' % (self.person, self.experience, self.proficiency) 
        
class IsParentIn(models.Model):
    class Meta:
        verbose_name = "Is Parent In"
        verbose_name_plural = "Are Parents In"
    parent = models.ForeignKey(Adult, related_name='parent', on_delete = models.CASCADE)
    family = models.ForeignKey(Family, related_name='a_family', on_delete = models.CASCADE, blank=True, null=True)
    isPrimary = models.BooleanField(default = False, verbose_name = "Primary Contact")

class IsChildIn(models.Model):
    class Meta:
        verbose_name = "Is Child In"
        verbose_name_plural = "Are Children In"
    child = models.ForeignKey(Child, related_name='childin', on_delete = models.CASCADE)
    family = models.ForeignKey(Family, related_name='c_family', on_delete = models.CASCADE, blank=True, null=True)
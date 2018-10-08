from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse

class Language(models.Model):
    language_name = models.CharField(max_length = 100, primary_key = True)
    def __str__(self):
        return '%s' % (self.language_name) 

class MusicalSkill(models.Model):
    class Meta:
        verbose_name = "Musical Skill"
        verbose_name_plural = "Musical Skills"

    skill = models.CharField(max_length = 100, primary_key = True)
    def __str__(self):
        return '%s' % (self.skill) 

class Lab(models.Model):
    lab_name = models.CharField(max_length = 100, primary_key = True)

class Person(models.Model):
    id = models.IntegerField(primary_key = True, verbose_name = "ID")
    given_name = models.CharField(max_length = 100, verbose_name = "Given Name")
    preferred_name = models.CharField(max_length = 100, blank = True, null = True, verbose_name = "Preferred Name")
    surname = models.CharField(max_length = 100, default='', verbose_name = "Surname")
    birth_date = models.DateField(verbose_name = "Birth Date")
    gender = models.CharField(max_length = 100, default='')
    def __str__(self):
        return '%s %s' % (self.given_name, self.surname) 

    class Meta:
        abstract = True
    
class Adult(Person):
    sfu_id = models.IntegerField(blank = True, null = True, verbose_name = "SFU ID")
    address = models.CharField(max_length=200)
    years_of_education = models.SmallIntegerField(
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
    contact_pref = models.CharField(max_length=1, choices = CONTACT_CHOICES, verbose_name = "Contact Preference")    

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
    pref_phone_time = models.CharField(max_length = 3, choices = PHONETIME_CHOICES, default = 'DNC', verbose_name = "Preferred Phone Time")
    
    health_notes = models.TextField(max_length=1000, blank = True, null = True, verbose_name = "Health Notes")
    languages = models.ManyToManyField('Language', blank = True, through='Speaks')
    musical_background = models.ManyToManyField('MusicalSkill', blank = True, through='MusicalExperience')


class Child(Person):
    class Meta:
        verbose_name_plural = "Children"
    gestation_length_weeks = models.SmallIntegerField(blank = True, null = True, verbose_name = "Gestation Length (Weeks)")
    was_full_term = models.BooleanField(blank = True, null = True, verbose_name = "Was Full Term?")
    birth_weight = models.SmallIntegerField(blank = True, null = True, verbose_name = "Birth Weight (Grams)")
    birth_height = models.SmallIntegerField(blank = True, null = True, verbose_name = "Birth Height (CM)")
    personal_notes = models.TextField(max_length=1000, blank = True, null = True, verbose_name="Personal Notes")
    hx_repeated_ear_infection = models.TextField(max_length=1000, blank = True, null = True, verbose_name = "HX of Repeated Ear Infection")
    last_ear_infection = models.DateField(blank = True, null = True, verbose_name = "Last Ear Infection")
    hereditary_audio_problems = models.BooleanField(verbose_name = "Hereditary Audio Problems?")
    hereditary_language_pathologies = models.BooleanField(verbose_name = "Hereditary Language Pathologies?")
    health_notes = models.TextField(max_length=1000, blank = True, null = True, verbose_name = "Health Notes")
    exposed_to = models.ManyToManyField('Language', through='IsExposedTo', default = None, verbose_name = "Languages Exposed To")

class Family(models.Model):
    class Meta:
        verbose_name = "Family"
        verbose_name_plural = "Families"
    id = models.IntegerField(primary_key = True, verbose_name = "ID")
    parents = models.ManyToManyField('Adult', through='IsParentIn')
    children = models.ManyToManyField('Child', through='IsChildIn')
    def __str__(self):
        return 'Parents: %s, Children: %s' % (self.parents, self.children) 

class Experiment(models.Model):
    experiment_name = models.CharField(max_length = 100, primary_key = True, verbose_name = "Experiment Name")
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)
    STATUS_CHOICES = (
        ('prep', 'In Prep'),
        ('recruiting', 'Actively Recruiting'),
        ('inactive', 'Inactive'),
    )
    status = models.CharField(max_length = 10, choices = STATUS_CHOICES)
    def __str__(self):
        return '%s: %s (%s)' % (self.status, self.experiment_name, self.lab) 

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
    status = models.CharField(max_length = 10, choices = STATUS_CHOICES)
    section_of = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    
    flex_1_name = models.CharField(max_length = 100, blank = True, null = True)
    flex_1_min_value = models.SmallIntegerField(blank = True, null = True)
    flex_1_max_value = models.SmallIntegerField(blank = True, null = True)
    
    flex_2_name = models.CharField(max_length = 100, blank = True, null = True)
    flex_2_min_value = models.SmallIntegerField(blank = True, null = True)
    flex_2_max_value = models.SmallIntegerField(blank = True, null = True)

    flex_3_name = models.CharField(max_length = 100, blank = True, null = True)
    flex_3_min_value = models.SmallIntegerField(blank = True, null = True)
    flex_3_max_value = models.SmallIntegerField(blank = True, null = True)

    flex_4_name = models.CharField(max_length = 100, blank = True, null = True)
    flex_4_min_value = models.SmallIntegerField(blank = True, null = True)
    flex_4_max_value = models.SmallIntegerField(blank = True, null = True)

    flex_5_name = models.CharField(max_length = 100, blank = True, null = True)
    flex_5_min_value = models.SmallIntegerField(blank = True, null = True)
    flex_5_max_value = models.SmallIntegerField(blank = True, null = True)

    flex_6_name = models.CharField(max_length = 100, blank = True, null = True)
    flex_6_min_value = models.SmallIntegerField(blank = True, null = True)
    flex_6_max_value = models.SmallIntegerField(blank = True, null = True)

    def __str__(self):
        return '%s: %s of %s' % (self.status, self.experiment_section_name, self.section_of) 

class Experiment_Section_Run(models.Model):
    class Meta:
        verbose_name = "Experiment Section Run"
        verbose_name_plural = "Experiment Section Runs"
    adult_participant = models.ForeignKey(Adult, on_delete = models.CASCADE)
    child_participant = models.ForeignKey(Child, on_delete = models.CASCADE)
    experiment_section = models.ForeignKey(Experiment_Section, on_delete = models.CASCADE)
    date = models.DateField()
    notes = models.TextField(max_length=1000)
    assessor = models.TextField(max_length=100)
    flex_1_score = models.SmallIntegerField(blank = True, null = True)
    flex_2_score = models.SmallIntegerField(blank = True, null = True)
    flex_3_score = models.SmallIntegerField(blank = True, null = True)
    flex_4_score = models.SmallIntegerField(blank = True, null = True)
    flex_5_score = models.SmallIntegerField(blank = True, null = True)
    flex_6_score = models.SmallIntegerField(blank = True, null = True)


class Assessment(models.Model):
    assessment_name = models.CharField(max_length = 100, primary_key = True)
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)

    flex_1_name = models.CharField(max_length = 100, blank = True, null = True)
    flex_1_min_value = models.SmallIntegerField(blank = True, null = True)
    flex_1_max_value = models.SmallIntegerField(blank = True, null = True)
    
    flex_2_name = models.CharField(max_length = 100, blank = True, null = True)
    flex_2_min_value = models.SmallIntegerField(blank = True, null = True)
    flex_2_max_value = models.SmallIntegerField(blank = True, null = True)

    flex_3_name = models.CharField(max_length = 100, blank = True, null = True)
    flex_3_min_value = models.SmallIntegerField(blank = True, null = True)
    flex_3_max_value = models.SmallIntegerField(blank = True, null = True)

    flex_4_name = models.CharField(max_length = 100, blank = True, null = True)
    flex_4_min_value = models.SmallIntegerField(blank = True, null = True)
    flex_4_max_value = models.SmallIntegerField(blank = True, null = True)

    flex_5_name = models.CharField(max_length = 100, blank = True, null = True)
    flex_5_min_value = models.SmallIntegerField(blank = True, null = True)
    flex_5_max_value = models.SmallIntegerField(blank = True, null = True)

    flex_6_name = models.CharField(max_length = 100, blank = True, null = True)
    flex_6_min_value = models.SmallIntegerField(blank = True, null = True)
    flex_6_max_value = models.SmallIntegerField(blank = True, null = True)

    def __str__(self):
        return '%s (%s)' % (self.assessment_name, self.lab) 


class Assessment_Run(models.Model):
    class Meta:
        verbose_name = "Assessment Run"
        verbose_name_plural = "Assessment Runs"
    adult_participant = models.ForeignKey(Adult, on_delete = models.CASCADE)
    child_participant = models.ForeignKey(Child, on_delete = models.CASCADE)
    assessment = models.ForeignKey(Assessment, on_delete = models.CASCADE)
    date = models.DateField()
    notes = models.TextField(max_length=1000)
    assessor = models.TextField(max_length=100)
    flex_1_score = models.SmallIntegerField(blank = True, null = True)
    flex_2_score = models.SmallIntegerField(blank = True, null = True)
    flex_3_score = models.SmallIntegerField(blank = True, null = True)
    flex_4_score = models.SmallIntegerField(blank = True, null = True)
    flex_5_score = models.SmallIntegerField(blank = True, null = True)
    flex_6_score = models.SmallIntegerField(blank = True, null = True)

class IsExposedTo(models.Model):
    class Meta:
        verbose_name_plural = "Is Exposed To"
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
    is_native = models.BooleanField(default = False)
    nth_most_dominant = models.SmallIntegerField(
        validators=[
            MinValueValidator(1), 
            MaxValueValidator(20),
        ],
    )
    age_learning_started = models.SmallIntegerField(
        validators=[
            MinValueValidator(0), 
            MaxValueValidator(120),
        ],
    )

    age_learning_ended = models.SmallIntegerField(
        validators=[
            MinValueValidator(0), 
            MaxValueValidator(120),
        ],
    )
    def __str__(self):
        return '%s\'s n=%s is %s' % (self.person, self.nth_most_dominant, self.lang) 

class MusicalExperience(models.Model):
    class Meta:
        verbose_name_plural = "Musical Experiences"
    person = models.ForeignKey(Adult, related_name = 'musician', on_delete = models.CASCADE, default = None)
    experience = models.ForeignKey(MusicalSkill, related_name = 'instrument', on_delete = models.CASCADE, default = None,)
    nth_most_dominant = models.SmallIntegerField(
        validators=[
            MinValueValidator(1), 
            MaxValueValidator(20),
        ],
    )
    age_learning_started = models.SmallIntegerField(
        validators=[
            MinValueValidator(0), 
            MaxValueValidator(120),
        ],
    )

    age_learning_ended = models.SmallIntegerField(
        validators=[
            MinValueValidator(0), 
            MaxValueValidator(120),
        ],
    )
    def __str__(self):
        return '%s\'s n=%s is %s' % (self.person, self.nth_most_dominant, self.experience) 

class IsParentIn(models.Model):
    class Meta:
        verbose_name = "Is Parent In"
        verbose_name_plural = "Are Parents In"
    parent = models.ForeignKey(Adult, related_name='parent', on_delete = models.CASCADE)
    family = models.ForeignKey(Family, related_name='family', on_delete = models.CASCADE)

class IsChildIn(models.Model):
    class Meta:
        verbose_name = "Is Child In"
        verbose_name_plural = "Are Children In"
    child = models.ForeignKey(Child, on_delete = models.CASCADE)
    family = models.ForeignKey(Family, on_delete = models.CASCADE)
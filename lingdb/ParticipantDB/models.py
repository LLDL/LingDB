from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Language(models.Model):
    language_name = models.CharField(
        max_length = 100, 
        primary_key = True
    )
    def __str__(self):
        return '%s' % (self.language_name) 
    


class Musical_Skill(models.Model):
    class Meta:
        verbose_name = "Musical Skill"
        verbose_name_plural = "Musical Skills"
    skill = models.CharField(
        max_length = 100, 
        primary_key = True
    )
    def __str__(self):
        return '%s' % (self.skill) 

class Experiment(models.Model):
    experiment_name = models.CharField(
        max_length = 100, 
        primary_key = True
    )
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
    def __str__(self):
        return '%s: %s (%s)' % (self.status, self.experiment_name, self.lab) 

class Experiment_Section(models.Model):
    class Meta:
        verbose_name = "Experiment Section"
        verbose_name_plural = "Experiment Sections"
    experiment_section_name = models.CharField(
        max_length = 100
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
    section_of = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    def __str__(self):
        return '%s: %s of %s' % (self.status, self.experiment_section_name, self.section_of) 

class Person(models.Model):
    given_name = models.CharField(max_length = 100)
    preferred_name = models.CharField(max_length = 100, blank = True, null = True)
    surname = models.CharField(max_length = 100, default='')
    birth_date = models.DateField()
    GENDER_CHOICES = (
        ('F', 'Female'),
        ('M', 'Male'),
        ('O', 'Other (Specify Below)'),
    )
    gender = models.CharField(
        max_length = 1, 
        choices = GENDER_CHOICES
    )
    other_gender = models.CharField(
        verbose_name = "Other Gender", 
        max_length = 100, 
        blank = True, 
        null = True, 
    )
    def __str__(self):
        return '%s %s' % (self.given_name, self.surname) 

    class Meta:
        abstract = True
    
class Adult(Person):
    sfu_id = models.IntegerField(
        blank = True, 
        null = True
    )
    birth_date = models.DateField()
    address = models.CharField(
        max_length=200
    )
    years_of_education = models.SmallIntegerField(
        validators=[
            MinValueValidator(0), 
            MaxValueValidator(20),
        ]
    )
    phone = models.CharField(
        max_length=50
    )
    email = models.EmailField()

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
        ('ANY', 'Anytime'),
    )
    pref_phone_time = models.CharField(
        max_length = 3,
        choices = PHONETIME_CHOICES,
        blank = True, 
        null = True
    )

    languages = models.ManyToManyField(Language, through='Speaks')
    musical_background = models.ManyToManyField(Musical_Skill, through='Musical_Experience', blank = True)
    participation = models.ManyToManyField(Experiment_Section, through='Participated', blank = True)

class Child(Person):
    class Meta:
        verbose_name_plural = "Children"
    gestation_length_weeks = models.SmallIntegerField(
        blank = True, 
        null = True
    )
    was_full_term = models.BooleanField(
        blank = True, 
        null = True
    )
    birth_weight = models.SmallIntegerField("Birth Weight (Grams)", blank = True, null = True)
    birth_height = models.SmallIntegerField("Birth Height (CM)", blank = True, null = True)
    personal_notes = models.TextField(
        max_length=1000,
        blank = True, 
        null = True

    )
    hx_repeated_ear_infection = models.TextField(
        max_length=1000, 
        blank = True, 
        null = True
    )
    last_ear_infection = models.DateField(
        blank = True, 
        null = True
    )
    hereditary_audio_problems = models.BooleanField()
    hereditary_language_pathologies = models.BooleanField()
    health_notes = models.TextField(
        max_length=1000, 
        blank = True,
        null = True
    )
    exposed_to = models.ManyToManyField(Language, through='IsExposedTo', default = None)
    participations = models.ManyToManyField(Experiment_Section, through='Participated', default = None)

class Family(models.Model):
    class Meta:
        verbose_name = "Family"
        verbose_name_plural = "Families"
    parents = models.ManyToManyField(Adult, through='IsParentIn')
    children = models.ManyToManyField(Child, through='IsChildIn')
    def __str__(self):
        return 'Parents: %s, Children: %s' % (self.parents, self.children) 

class IsExposedTo(models.Model):
    class Meta:
        verbose_name_plural = "Is Exposed To"
    child = models.ForeignKey(Child, on_delete = models.CASCADE, default = None)
    language = models.ForeignKey(Language, on_delete = models.CASCADE, default = None)
    percentage_exposure = models.SmallIntegerField(
        validators=[
            MinValueValidator(0), 
            MaxValueValidator(100),
        ]
    )
    def __str__(self):
        return '%s is exposed %s to %s' % (self.child, self.percentage_exposure, self.language) 

class Speaks(models.Model):
    class Meta:
        verbose_name_plural = "Speaks"
    person = models.ForeignKey(Adult, on_delete = models.CASCADE, default = None)
    language = models.ForeignKey(Language, on_delete = models.CASCADE, default = None)
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
    def __str__(self):
        return '%s\'s n=%s is %s' % (self.person, self.nth_most_dominant, self.language) 

class Musical_Experience(models.Model):
    class Meta:
        verbose_name = "Musical Experience"
        verbose_name_plural = "Musical Experiences"
    person = models.ForeignKey(Adult, on_delete = models.CASCADE, default = None)
    experience = models.ForeignKey(Musical_Skill, on_delete = models.CASCADE, default = None)
    nth_most_dominant = models.SmallIntegerField(
        validators=[
            MinValueValidator(1), 
            MaxValueValidator(20),
        ], 
        blank = True,
        null = True,
    )
    age_learning_started = models.SmallIntegerField(
        blank = True,
        null = True,
        validators=[
            MinValueValidator(0), 
            MaxValueValidator(120),
        ], 
    )

    age_learning_ended = models.SmallIntegerField(
        blank = True,
        null = True,
        validators=[
            MinValueValidator(0), 
            MaxValueValidator(120),
        ], 
    )

class IsParentIn(models.Model):
    class Meta:
        verbose_name = "Is Parent In"
        verbose_name_plural = "Are Parents In"
    parent = models.ForeignKey(Adult, on_delete = models.CASCADE)
    family = models.ForeignKey(Family, on_delete = models.CASCADE)
    is_primary_contact = models.BooleanField(default=False)

class IsChildIn(models.Model):
    class Meta:
        verbose_name = "Is Child In"
        verbose_name_plural = "Are Children In"
    child = models.ForeignKey(Child, on_delete = models.CASCADE)
    family = models.ForeignKey(Family, on_delete = models.CASCADE)
    is_primary_contact = models.BooleanField(default=False)

class Participated(models.Model):
    class Meta:
        verbose_name = "Participation"
        verbose_name_plural = "Participations"
    adult_participant = models.ForeignKey(Adult, on_delete = models.CASCADE)
    child_participant = models.ForeignKey(Child, on_delete = models.CASCADE)
    section = models.ForeignKey(Experiment_Section, on_delete = models.CASCADE)
    date = models.DateField()
    notes = models.TextField(
        max_length=1000
    )
    assessor = models.TextField(
        max_length=100
    )
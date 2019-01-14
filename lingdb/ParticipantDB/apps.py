from django.apps import AppConfig
from watson import search as watson

class ParticipantDBConfig(AppConfig):
    name = 'ParticipantDB'
    def ready(self):
        Adult = self.get_model("Adult")
        watson.register(Adult)
        Child = self.get_model("Child")
        watson.register(Child)
        Family = self.get_model("Family")
        watson.register(Family)
        Experiment = self.get_model("Experiment")
        watson.register(Experiment)
        Experiment_Section = self.get_model("Experiment_Section")
        watson.register(Experiment_Section)
        Assessment = self.get_model("Assessment")
        watson.register(Assessment)
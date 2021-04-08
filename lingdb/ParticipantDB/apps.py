from django.apps import AppConfig

class ParticipantDBConfig(AppConfig):
    name = 'ParticipantDB'
    def ready(self):
        Adult = self.get_model("Adult")
        Child = self.get_model("Child")
        Family = self.get_model("Family")
        Experiment = self.get_model("Experiment")
        Experiment_Section = self.get_model("Experiment_Section")
        Assessment = self.get_model("Assessment")

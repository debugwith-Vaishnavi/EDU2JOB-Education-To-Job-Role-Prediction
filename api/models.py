# api/models.py
from django.db import models
from django.contrib.auth.models import User

class PredictionHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    input_data = models.TextField()  # store JSON string of input
    predicted = models.CharField(max_length=200)
    meta = models.JSONField(null=True, blank=True)  # store alternatives, probabilities, etc.
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.predicted} - {self.created_at}"

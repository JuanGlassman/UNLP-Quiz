from django.db import models

class UserResponse(models.Model):
    question = models.CharField(max_length=255)
    selected_answer = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=255)
    is_correct = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.question} - {'Correcta' if self.is_correct else 'Incorrecta'}"

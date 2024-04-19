from django.db import models

class ArduinoData(models.Model):
    tag_uid = models.CharField(max_length=255, blank=True, null=True)
    servo_state = models.CharField(max_length=10, blank=True, null=True)
    food_level = models.FloatField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ArduinoData - ID: {self.id}, Timestamp: {self.timestamp}"

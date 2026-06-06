from django.db import models

class AuditLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    actor = models.CharField(max_length=255)
    action = models.CharField(max_length=100)
    resource = models.CharField(max_length=100)
    resource_id = models.CharField(max_length=255, null=True)
    payload = models.JSONField(null=True)
    changes = models.JSONField(null=True)

    class Meta:
        ordering = ['-timestamp']

from django.conf import settings
from django.db import models


class Todo(models.Model):
    class Priority(models.TextChoices):
        LOW = 'LOW', 'Low'
        MEDIUM = 'MED', 'Medium'
        HIGH = 'HIGH', 'High'

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='todos',
    )
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    due_date = models.DateField(blank=True, null=True)
    priority = models.CharField(
        max_length=4,
        choices=Priority.choices,
        default=Priority.MEDIUM,
    )
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('is_completed', 'due_date', '-created_at')

    def __str__(self):
        return self.title

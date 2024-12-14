from django.db import models
from django.utils import timezone

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    ordem = models.IntegerField(unique=True)
    created_at = models.DateTimeField(default=timezone.now)  # Valor padrão temporário

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ['-created_at']

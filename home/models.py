from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    ordem = models.IntegerField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Adicionado campo de data de criação

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ['-created_at']  # Ordenação padrão por data de criação (mais recente primeiro)

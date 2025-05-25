from django.db import models

# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True



class Vertical(BaseModel):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Vertical'
        verbose_name_plural = 'Verticais'

    def __str__(self):
        return self.name


class Plan(BaseModel):
    name = models.CharField(max_length=255)
    is_basic = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    vertical = models.ManyToManyField(Vertical)

    class Meta:
        verbose_name = 'Plano'
        verbose_name_plural = 'Planos'

    def __str__(self):
        return self.name
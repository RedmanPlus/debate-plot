from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Tournament(models.Model):
	name = models.CharField(max_length=30)
	date_conducted = models.DateField(auto_now=False, auto_now_add=False)

class PlayerTournamentRelation(models.Model):
	toutnament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
	player = models.ForeignKey(User, on_delete=models.CASCADE)
	r1 = models.IntegerField()
	r2 = models.IntegerField()
	r3 = models.IntegerField()
	r4 = models.IntegerField()
	r5 = models.IntegerField()
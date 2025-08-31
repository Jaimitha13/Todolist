from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    srno=models.AutoField(primary_key=True,auto_created=True)
    title=models.CharField(max_length=200)
    date=models.DateField(auto_now=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    

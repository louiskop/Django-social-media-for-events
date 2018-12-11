from django.db import models
from django.urls import reverse
from django.conf import settings
import misaka
from django.contrib.auth import get_user_model
import datetime
from django.utils import timezone
User = get_user_model()
COUNTRY_CHOICES = (
    ('southafrica','South Africa'),
    ('america', 'America'),
    ('england','England'),
    ('russia','Russia'),
    ('china','China'),
)



class Post(models.Model):
    user = models.ForeignKey(User,related_name='party',on_delete=models.CASCADE,default='1')
    title = models.CharField(max_length=30)
    # author = models.ForeignKey('auth.User')
    date = models.DateField()
    time = models.TimeField()
    timeend = models.TimeField()
    age = models.CharField(max_length=30)
    color = models.CharField(max_length=30,choices=COUNTRY_CHOICES, default='america')
    drinks = models.BooleanField(default=False)
    image = models.ImageField(upload_to = 'imgs',default='none/none.png')
    location = models.CharField(max_length=30,default='no location specified')
    keyword = models.CharField(max_length=30,default='no keywords')

    def publish(self):
        self.save()
    

    def get_absolute_url(self):
        return reverse('party:party',kwargs={'username':self.user.username,'pk':self.pk})

    def str():
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('party.Post',on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse("party:party")

    def __str__(self):
        return self.text
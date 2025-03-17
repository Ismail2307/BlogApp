from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now


# 1. Auth and Profile
# 2. Publishing Text
# 3. Liking, commenting and reading

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    followers = models.ManyToManyField(User, related_name='following', blank=True)
    prof_pic = models.ImageField(upload_to='prof_pics/',null=True, blank=True)

    def follow(self, user):
        self.followers.add(user)

    def unfollow(self,user):
        self.followers.remove(user)

    def __str__(self):
       return self.user.username

class Blog(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogger' )
    created_at = models.DateTimeField(default=now)


    def __str__(self):
        return f"{self.title} by {self.created_by.username}"

class Post(models.Model):
    title = models.CharField(max_length=225)
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
      return f'{self.title} is in {self.blog.title} blog'

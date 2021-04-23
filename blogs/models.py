from authentication.models import User, BaseModel
from django.db import models

# Create your models here.

class Tags(BaseModel):
    name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

class Blogs(BaseModel):

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="blogs_user")

    title = models.CharField(max_length=255, null=True, blank=True)
    media = models.FileField(blank=True, null=True, upload_to='doc/')
    tags = models.ManyToManyField(Tags, related_name="blogs_tags")
    content = models.TextField()
                         


class Comments(BaseModel):
    
    blog = models.ForeignKey(Blogs,
                             on_delete=models.CASCADE,
                             related_name="comment_blogs")    
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="comment_user")

    comment = models.TextField()                        

class Likes(BaseModel):
    
    blog = models.ForeignKey(Blogs,
                             on_delete=models.CASCADE,
                             related_name="like_blogs")    
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="like_user")


class Activity(BaseModel):
    user = models.ForeignKey(User,
                            on_delete=models.CASCADE,
                            related_name="activity_user")

    blog = models.ForeignKey(Blogs,
                             on_delete=models.CASCADE,
                             related_name="activity_blogs")
    
    msg = models.TextField()


                         

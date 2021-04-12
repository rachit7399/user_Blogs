from authentication.models import User, BaseModel
from django.db import models

# Create your models here.
class Blogs(BaseModel):

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="blogs_user")

    title = models.CharField(max_length=255, null=True, blank=True)

    content = models.TextField()
                         


class Comments(BaseModel):
    
    blog = models.ForeignKey(Blogs,
                             on_delete=models.CASCADE,
                             related_name="Comment_blogs")    
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
                         

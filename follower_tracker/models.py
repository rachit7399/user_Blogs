from authentication.models import User, BaseModel
from django.db import models
    
class follower(BaseModel):

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="follower_user")
    my_followers = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="myfollowers", null=True, blank=True)  

    my_requests = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="requestsuser",null=True, blank=True)                                                        

    def __str__(self) -> str:
        return str(self.user.uid)

    class Meta:
        db_table = "follower_table"
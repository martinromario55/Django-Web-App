from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'
    
    # Override the save method
    def save(self):
        super().save()

        # Open image
        img = Image.open(self.image.path)

        # Check if current image height or width is more than 300px
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            # Resize image
            img.thumbnail(output_size)
            img.save(self.image.path)

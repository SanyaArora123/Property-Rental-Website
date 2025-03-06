from django.db import models
from django.contrib.auth.models import User

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to Django User
    phone = models.CharField(max_length=15, unique=True)
    photo = models.ImageField(upload_to="seller_photos/", blank=True, null=True)

    def __str__(self):
        return f"Seller: {self.user.username}"

class Property(models.Model):
    Pid = models.CharField(max_length=255)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)  # Property belongs to a Seller
    title = models.CharField(max_length=255)
    description = models.TextField()
    rental_amount = models.DecimalField(max_digits=10, decimal_places=2)
    house_address = models.CharField(max_length=255)
    area_sqft = models.PositiveIntegerField()
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    pincode = models.PositiveIntegerField(null = True)
    property_type = models.CharField(max_length=100, choices=[
        ('1 BHK', '1 BHK'), ('2 BHK', '2 BHK'), ('3 BHK', '3 BHK'),
        ('Villa', 'Villa'), ('Independent House', 'Independent House'),
        ('High Rise', 'High Rise'), ('Low Rise', 'Low Rise')
    ])
    image1 = models.ImageField(upload_to="property_images/", blank=True, null=True)
    image2 = models.ImageField(upload_to="property_images/", blank=True, null=True)
    image3 = models.ImageField(upload_to="property_images/", blank=True, null=True)
    image4 = models.ImageField(upload_to="property_images/", blank=True, null=True)
    image5 = models.ImageField(upload_to="property_images/", blank=True, null=True)
    image6 = models.ImageField(upload_to="property_images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.city}, {self.state}"
    def get_images(self):
        """
        Dynamically retrieve all uploaded images for the property.
        
        Returns:
        - List of image URLs for all non-empty image fields
        """
        images = []
        for i in range(1, 7):  # image1 through image6
            image_field = getattr(self, f'image{i}')
            if image_field and image_field.url:
                images.append(image_field)
        return images

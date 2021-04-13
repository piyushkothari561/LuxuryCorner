from django.db import models # importing the model library from the django database
from django.contrib.auth.models import User

class ProductProperty(models.Model):
    title = models.CharField(max_length=30, null= False)
    slug = models.CharField(max_length= 30, null= False, unique= True)

    def __str__(self):
        return self.title

    class Meta: 
        abstract = True 

# creating Gender Model
class Gender(ProductProperty):
    pass

# creating Brand Model
class Brand(ProductProperty):
    pass

# creating Colour Model
class Colour(ProductProperty):
    pass   

# creating Category Model
class Categorie(ProductProperty):
    pass   

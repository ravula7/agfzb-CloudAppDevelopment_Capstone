from django.db import models
from django.utils.timezone import now


# Create your models here.
CHOICES = [
    ('SEDAN', 'Sedan'),
    ('SUV', 'SUV'),
    ('WAGON', 'Wagon')
]

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    Name = models.CharField(null=False,max_length=200, default="car make")
    Description = models.CharField(null=False, max_length=500, default="description")
    def __str__(self):
            return "Name: " + self.Name + "," + \
                "Description: " + self.Description

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):

    make = models.ForeignKey(CarMake, on_delete=models.CASCADE,default='django.db.models.AutoField')
    Name = models.CharField(null=False, max_length=200,default="name")
    Dealerid = models.IntegerField(default=1,primary_key=True)
    Type = models.CharField(null=False,max_length=2000, choices=CHOICES)
    Year = models.DateField(default=now)

    def __str__(self):
                return "Name: " + self.Name + "," + \
                    "Description: " + str(self.Dealerid) + \
                    "Type: " + self.Type

                    
# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip
    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, dealership, name, purchase, review, sentiment):
        # Required attributes
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.sentiment = sentiment
    def __str__(self):
        return "Review: " + self.review

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

class ReviewPost:

    def __init__(self, dealership, name, purchase, review):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = ""
        self.car_make = ""
        self.car_model = ""
        self.car_year = ""

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

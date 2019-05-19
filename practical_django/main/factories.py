import factory 
import factory.fuzzy 
from . import models 
from django.contrib.auth.hashers import make_password

user_password = 'userpasswords1111'    

class UserFactory(factory.django.DjangoModelFactory):

    email = "user@site.com"
    password =  make_password(user_password)

    class Meta:
        model = models.User 
        django_get_or_create = ('email',)


class ProductFactory(factory.django.DjangoModelFactory):
    price = factory.fuzzy.FuzzyDecimal(1.0,1000.0,2)

    class Meta: 
        model = models.Product 


class AddressFactory(factory.django.DjangoModelFactory):
    address1 = factory.fuzzy.FuzzyText()
    address2 = factory.fuzzy.FuzzyText()
    city = factory.fuzzy.FuzzyText()
    country = factory.fuzzy.FuzzyText(length=3)
    zip_code = factory.fuzzy.FuzzyText()
    user = factory.SubFactory(UserFactory)

    class Meta: 
        model = models.Address

        
class OrderLineFactory(factory.django.DjangoModelFactory):
    class Meta: 
        model = models.OrderLine


class OrderFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = models.Order

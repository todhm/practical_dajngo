from django.test import TestCase 
from main import models ,forms,factories 
from django.core.files.images import ImageFile
from decimal import Decimal


class TestSignal(TestCase):
    def test_thumbnails_are_generated_on_save(self):
        product= models.Product(
            name="The cathedral and the bazaar",
            price=Decimal("10.00"),
        )
        product.save() 
        with open("main/fixtures/the-cathedral-the-bazaar.jpg","rb") as f:
            image = models.ProductImage(
                product=product,
                image=ImageFile(f,name='tctb.jpg')
            )
            with self.assertLogs("main",level="INFO") as cm:
                image.save() 
        self.assertGreaterEqual(len(cm.output),1)
        image.refresh_from_db()
        self.assertTrue(len(image.thumbnail.read())>0)
        
        image.thumbnail.delete(save=False)
        image.image.delete(save=False)


    def test_orderlines_are_saved(self):
        p1 = factories.ProductFactory()
        a1 = factories.AddressFactory()
        user1 = factories.UserFactory()
        order_data = {
                "status":10,
                "billing_name":"test1",
                "billing_address1":a1.address1,
                "billing_address2":a1.address2,
                "billing_zip_code":a1.zip_code, 
                "billing_city":a1.city,
                "billing_country":a1.country, 
                "shipping_name":"hello",
                "shipping_address1": a1.address1,
                "shipping_address2": a1.address2,
                "shipping_zip_code": a1.zip_code, 
                "shipping_city": a1.city,
                "shipping_country": a1.country,
        }
        order = models.Order.objects.create(
            user=user1,
            **order_data
        )

        orderline = models.OrderLine.objects.create(
            product=p1,
            order=order,
            status=10
        )
        orderline.status=30
        orderline.save()
        orderline.refresh_from_db()
        self.assertEqual(order.status,30)

        
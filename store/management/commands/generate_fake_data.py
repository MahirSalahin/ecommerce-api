from django.core.management.base import BaseCommand
from store import factories


class Command(BaseCommand):
    help = 'Generate fake data using factories'

    def handle(self, *args, **kwargs):
        self.stdout.write('Generating promotions...')
        promotions = [factories.PromotionFactory.create() for _ in range(10)]

        self.stdout.write('Generating collections and products...')
        for _ in range(10):
            collection = factories.CollectionFactory.create()
            products = [factories.ProductFactory.create(
                collection=collection) for _ in range(100)]
            for product in products:
                product.promotions.add(*promotions)


        #
        self.stdout.write('Generating customers...')
        customers = [factories.CustomerFactory.create() for _ in range(100)]

        self.stdout.write('Generating orders and order items...')
        for customer in customers:
            order = factories.OrderFactory.create(customer=customer)
            [factories.OrderItemFactory.create(order=order) for _ in range(3)]

        self.stdout.write('Generating addresses...')
        [factories.AddressFactory.create() for _ in range(50)]

        self.stdout.write('Generating carts and cart items...')
        for _ in range(5):
            cart = factories.CartFactory.create()
            [factories.CartItemFactory.create(cart=cart) for _ in range(3)]

        self.stdout.write(self.style.SUCCESS(
            'Successfully generated fake data'))

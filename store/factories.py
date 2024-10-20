import factory
from faker import Faker
from store.models import (
    Promotion,
    Collection,
    Product,
    Customer,
    Order,
    OrderItem,
    Address,
    Cart,
    CartItem
)

fake = Faker()


class PromotionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Promotion

    description = factory.LazyAttribute(lambda _: fake.text(max_nb_chars=20))
    discount = factory.LazyAttribute(
        lambda _: round(fake.random_number(digits=2), 2))


class CollectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Collection

    title = factory.LazyAttribute(lambda _: fake.text(max_nb_chars=20))
    featured_product = None


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    title = factory.LazyAttribute(lambda _: fake.text(max_nb_chars=20))
    slug = factory.LazyAttribute(lambda _: fake.slug())
    description = factory.LazyAttribute(lambda _: fake.text())
    price = factory.LazyAttribute(lambda _: round(
        fake.random_number(digits=4) / 100, 2))
    inventory = factory.LazyAttribute(
        lambda _: fake.random_int(min=0, max=1000))
    last_update = factory.LazyAttribute(lambda _: fake.date_time_this_year())
    collection = factory.SubFactory(CollectionFactory)

    @factory.post_generation
    def promotions(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for promotion in extracted:
                self.promotions.add(promotion)


class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Customer

    first_name = factory.LazyAttribute(lambda _: fake.first_name())
    last_name = factory.LazyAttribute(lambda _: fake.last_name())
    email = factory.LazyAttribute(lambda _: fake.email())
    phone = factory.LazyAttribute(lambda _: fake.phone_number())
    birth_date = factory.LazyAttribute(
        lambda _: fake.date_of_birth(minimum_age=18, maximum_age=80))
    membership = factory.LazyAttribute(
        lambda _: fake.random_element(elements=Customer.MEMBERSHIP_CHOICES)[0])


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    placed_at = factory.LazyAttribute(lambda _: fake.date_time_this_year())
    payment_status = factory.LazyAttribute(
        lambda _: fake.random_element(elements=Order.PAYMENT_STATUS_CHOICES)[0])
    customer = factory.SubFactory(CustomerFactory)


class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=10))
    unit_price = factory.LazyAttribute(
        lambda _: round(fake.random_number(digits=4) / 100, 2))


class AddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Address

    street = factory.LazyAttribute(lambda _: fake.street_address())
    city = factory.LazyAttribute(lambda _: fake.city())
    customer = factory.SubFactory(CustomerFactory)


class CartFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cart

    created_at = factory.LazyAttribute(lambda _: fake.date_time_this_year())


class CartItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CartItem

    cart = factory.SubFactory(CartFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=10))

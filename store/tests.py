from django.test import TestCase, Client
from django.urls import reverse
from store.models import Category, Product, Cart, CartItem, Order

class AmazonStoreTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="Electronics", slug="electronics")
        self.product = Product.objects.create(
            title="Samsung Neo QLED 65 TV",
            category=self.category,
            brand="Samsung",
            description="4K Smart TV",
            price=149990.00,
            original_price=189900.00,
            stock=10,
            main_image="https://example.com/tv.jpg",
            is_deal_of_the_day=True
        )

    def test_homepage_status_code(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Samsung Neo QLED")

    def test_search_products(self):
        response = self.client.get(reverse('product_list') + '?q=Samsung')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Samsung Neo QLED")

    def test_add_to_cart_and_checkout(self):
        # Add to cart
        response = self.client.post(reverse('add_to_cart', args=[self.product.id]), {'quantity': 2})
        self.assertRedirects(response, reverse('cart'))

        # Check cart page
        cart_response = self.client.get(reverse('cart'))
        self.assertEqual(cart_response.status_code, 200)
        self.assertContains(cart_response, "Samsung Neo QLED")

        # Place Order
        order_data = {
            'full_name': 'Poorak Pandey',
            'email': 'poorak@example.com',
            'mobile': '+91 9876543210',
            'address_line': 'Sector 15',
            'city': 'Sonipat',
            'state': 'Haryana',
            'pincode': '131021',
            'payment_method': 'Amazon Pay Balance / UPI'
        }
        checkout_response = self.client.post(reverse('place_order'), order_data)
        self.assertEqual(checkout_response.status_code, 200)
        self.assertContains(checkout_response, "Order Placed, Thank You!")
        
        # Verify order created in DB with 408- format
        order = Order.objects.first()
        self.assertIsNotNone(order)
        self.assertTrue(order.order_id.startswith('408-'))
        self.assertEqual(order.items.count(), 1)

from django.core.management.base import BaseCommand
from store.models import Category, Product, ProductImage, Address, Review
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = "Seeds initial database for Amazon.in clone with realistic Indian e-commerce products"

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Seeding database..."))

        # Create or update default user
        user, created = User.objects.get_or_create(
            username="poorak",
            defaults={
                "email": "poorak@example.com",
                "first_name": "Poorak",
                "last_name": "Pandey",
                "is_staff": True,
                "is_superuser": True
            }
        )
        if created:
            user.set_password("amazon123")
            user.save()
            self.stdout.write(self.style.SUCCESS("Created admin user: poorak (pass: amazon123)"))

        # Seed Address
        Address.objects.get_or_create(
            user=user,
            defaults={
                "full_name": "Poorak Pandey",
                "mobile_number": "+91 9876543210",
                "pincode": "131021",
                "flat_house": "House No 42, Sector 15",
                "area_street": "Near Model Town",
                "town_city": "Sonipat",
                "state": "Haryana",
                "is_default": True
            }
        )

        # Categories
        cat_data = [
            {"name": "Electronics & Photo", "slug": "electronics", "icon": "fa-plug", "image_url": "https://images.unsplash.com/photo-1526738549149-8e07eca6c147?w=500&q=80", "is_featured": True},
            {"name": "Smart Home & Alexa", "slug": "smart-home", "icon": "fa-microphone", "image_url": "https://images.unsplash.com/photo-1543512214-318c7553f230?w=500&q=80", "is_featured": True},
            {"name": "Mobile & Accessories", "slug": "mobile-accessories", "icon": "fa-mobile-screen-button", "image_url": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=500&q=80", "is_featured": True},
            {"name": "Musical Instruments", "slug": "musical-instruments", "icon": "fa-guitar", "image_url": "https://images.unsplash.com/photo-1510915361894-db8b60106cb1?w=500&q=80", "is_featured": True},
            {"name": "Men's Wallets & Accessories", "slug": "mens-wallets", "icon": "fa-wallet", "image_url": "https://images.unsplash.com/photo-1627123424574-724758594e93?w=500&q=80", "is_featured": True},
            {"name": "Home & Kitchen", "slug": "home-kitchen", "icon": "fa-house", "image_url": "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=500&q=80", "is_featured": True},
            {"name": "Fresh & Grocery", "slug": "grocery", "icon": "fa-apple-whole", "image_url": "https://images.unsplash.com/photo-1542838132-92c53300491e?w=500&q=80", "is_featured": True},
        ]

        categories_dict = {}
        for c in cat_data:
            cat_obj, _ = Category.objects.get_or_create(
                slug=c["slug"],
                defaults={
                    "name": c["name"],
                    "icon": c["icon"],
                    "image_url": c["image_url"],
                    "is_featured": c["is_featured"]
                }
            )
            categories_dict[c["slug"]] = cat_obj

        # Products
        products_data = [
            {
                "title": "Samsung Neo QLED 163 cm (65 inches) 4K Smart TV",
                "category": categories_dict["electronics"],
                "brand": "Samsung",
                "price": 149990.00,
                "original_price": 189900.00,
                "rating": 4.6,
                "rating_count": 1280,
                "stock": 15,
                "main_image": "https://images.unsplash.com/photo-1593784991095-a205069470b6?w=800&q=80",
                "badge": "Great Indian Festival",
                "is_prime": True,
                "is_deal_of_the_day": True,
                "delivery_days": 1,
                "description": "Experience deep blacks and vibrant colors with Samsung Neo Quantum Processor 4K. Features Quantum Matrix Technology, Dolby Atmos, and Smart Hub with built-in voice assistants.",
                "specifications": {
                    "Screen Size": "65 Inches",
                    "Resolution": "4K Ultra HD (3840 x 2160)",
                    "Refresh Rate": "120 Hz",
                    "Display Technology": "Neo QLED",
                    "Warranty": "2 Years Comprehensive"
                },
                "additional_images": [
                    "https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=800&q=80",
                    "https://images.unsplash.com/photo-1577979749830-f1d742b96791?w=800&q=80"
                ]
            },
            {
                "title": "ŌURA Ring Gen 3 Horizon Smart Ring - Heritage Gold",
                "category": categories_dict["electronics"],
                "brand": "ŌURA",
                "price": 27999.00,
                "original_price": 34999.00,
                "rating": 4.5,
                "rating_count": 890,
                "stock": 25,
                "main_image": "https://images.unsplash.com/photo-1605100804763-247f67b3557e?w=800&q=80",
                "badge": "Up to 30% off Smart Rings",
                "is_prime": True,
                "is_deal_of_the_day": True,
                "delivery_days": 2,
                "description": "Accurate sleep tracking, heart rate monitoring, readiness score, and body temperature sensor wrapped in a sleek titanium ring. Up to 7 days battery life.",
                "specifications": {
                    "Material": "Titanium with PVD Coating",
                    "Battery Life": "Up to 7 Days",
                    "Water Resistance": "100m",
                    "Sensors": "Optical Heart Rate, Temp, SpO2"
                },
                "additional_images": [
                    "https://images.unsplash.com/photo-1603561591411-07134e71a2a9?w=800&q=80"
                ]
            },
            {
                "title": "Echo Dot (5th Gen, 2023 release) | Smart Speaker with Alexa (Black)",
                "category": categories_dict["smart-home"],
                "brand": "Amazon",
                "price": 4499.00,
                "original_price": 5499.00,
                "rating": 4.4,
                "rating_count": 28450,
                "stock": 100,
                "main_image": "https://images.unsplash.com/photo-1543512214-318c7553f230?w=800&q=80",
                "badge": "#1 Best Seller",
                "is_prime": True,
                "is_deal_of_the_day": False,
                "delivery_days": 1,
                "description": "Our best sounding Echo Dot yet. Enjoy an improved audio experience compared to any previous Echo Dot with Alexa for clearer vocals, deeper bass and vibrant sound in any room.",
                "specifications": {
                    "Audio": "1.73 inch front-firing speaker",
                    "Connectivity": "Dual-band Wi-Fi, Bluetooth",
                    "Dimensions": "100 x 100 x 89 mm",
                    "Voice Assistant": "Alexa Built-in"
                },
                "additional_images": [
                    "https://images.unsplash.com/photo-1518444065439-e933c06ce9cd?w=800&q=80"
                ]
            },
            {
                "title": "boAt Deuce USB 300 Type C to Type C 65W Fast Charging Cable (1.5m, Black)",
                "category": categories_dict["mobile-accessories"],
                "brand": "boAt",
                "price": 399.00,
                "original_price": 999.00,
                "rating": 4.3,
                "rating_count": 15420,
                "stock": 200,
                "main_image": "https://images.unsplash.com/photo-1583863788434-e58a36330cf0?w=800&q=80",
                "badge": "Starting ₹399",
                "is_prime": True,
                "is_deal_of_the_day": True,
                "delivery_days": 1,
                "description": "Nylon braided ultra-tough charging cable supporting 65W Power Delivery fast charging. Compatible with smartphones, laptops, tablets and audio devices.",
                "specifications": {
                    "Length": "1.5 Meters",
                    "Power Output": "65W (20V/3.25A)",
                    "Material": "Braided Nylon",
                    "Warranty": "2 Years"
                },
                "additional_images": []
            },
            {
                "title": "AGARO Powerglide 10000mAh 22.5W Fast Charging Power Bank with Digital Display",
                "category": categories_dict["mobile-accessories"],
                "brand": "AGARO",
                "price": 899.00,
                "original_price": 1899.00,
                "rating": 4.2,
                "rating_count": 4320,
                "stock": 80,
                "main_image": "https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?w=800&q=80",
                "badge": "53% OFF",
                "is_prime": True,
                "is_deal_of_the_day": True,
                "delivery_days": 1,
                "description": "Compact 10000mAh Lithium Polymer power bank with Quick Charge 3.0 & PD 22.5W output. Features clear digital LED battery percentage indicator.",
                "specifications": {
                    "Capacity": "10000 mAh",
                    "Outputs": "Dual USB-A + Type-C PD",
                    "Weight": "220g",
                    "Warranty": "1 Year"
                },
                "additional_images": []
            },
            {
                "title": "Yamaha F280 Acoustic Guitar, Natural Finish",
                "category": categories_dict["musical-instruments"],
                "brand": "Yamaha",
                "price": 7990.00,
                "original_price": 9990.00,
                "rating": 4.6,
                "rating_count": 9850,
                "stock": 30,
                "main_image": "https://images.unsplash.com/photo-1510915361894-db8b60106cb1?w=800&q=80",
                "badge": "Top Rated",
                "is_prime": True,
                "is_deal_of_the_day": False,
                "delivery_days": 2,
                "description": "Designed specifically for India with rich resonance, durable spruce top, and comfortable fretboard. Perfect for beginners and intermediate players alike.",
                "specifications": {
                    "Body Shape": "Traditional Western",
                    "Top Material": "Spruce",
                    "Back & Sides": "Locally Sourced Tonewood",
                    "Frets": "20"
                },
                "additional_images": []
            },
            {
                "title": "Fastrack Limitless FS1 Smart Watch | 1.95\" Large Display | BT Calling",
                "category": categories_dict["electronics"],
                "brand": "Fastrack",
                "price": 1499.00,
                "original_price": 3995.00,
                "rating": 4.1,
                "rating_count": 18290,
                "stock": 150,
                "main_image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&q=80",
                "badge": "62% OFF",
                "is_prime": True,
                "is_deal_of_the_day": True,
                "delivery_days": 1,
                "description": "1.95 inch Horizon Curve Display, Advanced Single-chip BT Calling, 100+ Sports Modes, AI Voice Assistant, Stress & SpO2 Monitor.",
                "specifications": {
                    "Screen Size": "1.95 Inches",
                    "Battery Life": "Up to 7 Days",
                    "Waterproof Rating": "IP68",
                    "Compatibility": "Android & iOS"
                },
                "additional_images": []
            },
            {
                "title": "Fastrack Men's Genuine Leather RFID Blocking Wallet (Brown)",
                "category": categories_dict["mens-wallets"],
                "brand": "Fastrack",
                "price": 799.00,
                "original_price": 1495.00,
                "rating": 4.4,
                "rating_count": 6120,
                "stock": 60,
                "main_image": "https://images.unsplash.com/photo-1627123424574-724758594e93?w=800&q=80",
                "badge": "Deal for You",
                "is_prime": True,
                "is_deal_of_the_day": False,
                "delivery_days": 2,
                "description": "Crafted from 100% genuine top-grain leather with built-in RFID blocking shield to safeguard your cards from electronic pickpocketing. Includes 6 card slots and 2 currency compartments.",
                "specifications": {
                    "Material": "100% Top Grain Leather",
                    "Dimensions": "11 x 9 x 2 cm",
                    "RFID Protection": "Yes",
                    "Color": "Tan Brown"
                },
                "additional_images": []
            },
            {
                "title": "Fender Champion 20 Guitar Combo Amplifier",
                "category": categories_dict["musical-instruments"],
                "brand": "Fender",
                "price": 11490.00,
                "original_price": 13999.00,
                "rating": 4.7,
                "rating_count": 2100,
                "stock": 12,
                "main_image": "https://images.unsplash.com/photo-1544717305-2782549b5136?w=800&q=80",
                "badge": "Amazon Choice",
                "is_prime": True,
                "is_deal_of_the_day": False,
                "delivery_days": 2,
                "description": "20-watt compact guitar amplifier with 8-inch Special Design speaker. Features multiple amp voicings from clean Tweed to heavy metal overdrive, plus built-in digital effects.",
                "specifications": {
                    "Wattage": "20 Watts",
                    "Speaker": "1 x 8 inch Fender Special Design",
                    "Effects": "Reverb, Delay, Chorus, Tremolo",
                    "Inputs": "1/4 inch Instrument, 1/8 inch Aux"
                },
                "additional_images": []
            },
            {
                "title": "AmazonBasics 4-Tier Modular Storage Drawer Organizer Unit",
                "category": categories_dict["home-kitchen"],
                "brand": "AmazonBasics",
                "price": 1299.00,
                "original_price": 2499.00,
                "rating": 4.3,
                "rating_count": 7890,
                "stock": 45,
                "main_image": "https://images.unsplash.com/photo-1595428774223-ef52624120d2?w=800&q=80",
                "badge": "AmazonBasics",
                "is_prime": True,
                "is_deal_of_the_day": False,
                "delivery_days": 1,
                "description": "Multipurpose storage drawer tower made from durable BPA-free plastic. Ideal for organizing kitchen supplies, clothes, stationery, and toys.",
                "specifications": {
                    "Number of Drawers": "4 Tier",
                    "Material": "Heavy-duty Plastic",
                    "Dimensions": "38 x 30 x 85 cm",
                    "Wheels": "Included"
                },
                "additional_images": []
            },
            {
                "title": "Apple iPhone 15 Pro (128 GB) - Natural Titanium",
                "category": categories_dict["mobile-accessories"],
                "brand": "Apple",
                "price": 127990.00,
                "original_price": 134900.00,
                "rating": 4.8,
                "rating_count": 5420,
                "stock": 20,
                "main_image": "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=800&q=80",
                "badge": "Great Indian Festival",
                "is_prime": True,
                "is_deal_of_the_day": True,
                "delivery_days": 1,
                "description": "Forged in titanium with A17 Pro chip, customizable Action button, 48MP Main camera with 3x Telephoto lens, and USB-C connection.",
                "specifications": {
                    "Display": "6.1 inch Super Retina XDR ProMotion",
                    "Processor": "A17 Pro Bionic Chip",
                    "Camera": "48MP + 12MP + 12MP",
                    "Connector": "USB-C (USB 3 speeds)"
                },
                "additional_images": []
            },
            {
                "title": "Sony WH-1000XM5 Wireless Industry Leading ANC Headphones (Black)",
                "category": categories_dict["electronics"],
                "brand": "Sony",
                "price": 26990.00,
                "original_price": 34990.00,
                "rating": 4.6,
                "rating_count": 8940,
                "stock": 40,
                "main_image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&q=80",
                "badge": "Save ₹8000",
                "is_prime": True,
                "is_deal_of_the_day": True,
                "delivery_days": 1,
                "description": "Magnificent sound & industry-leading Noise Canceling powered by two processors and 8 microphones. 30 hours battery life with quick charge.",
                "specifications": {
                    "Noise Cancellation": "Auto NC Optimizer",
                    "Battery Life": "30 Hours",
                    "Quick Charge": "3 mins = 3 hours playback",
                    "Bluetooth": "v5.2 with LDAC"
                },
                "additional_images": []
            }
        ]

        for p_data in products_data:
            add_imgs = p_data.pop("additional_images", [])
            product, created = Product.objects.get_or_create(
                title=p_data["title"],
                defaults=p_data
            )
            if created:
                for img_url in add_imgs:
                    ProductImage.objects.create(product=product, image_url=img_url)

                # Add sample review
                Review.objects.create(
                    product=product,
                    user=user,
                    title="Outstanding quality! Exactly as expected from Amazon",
                    rating=5,
                    comment="Build quality and delivery speed were incredible. Delivered to Sonipat in less than 24 hours. Highly recommended!",
                    verified_purchase=True
                )

        self.stdout.write(self.style.SUCCESS(f"Successfully seeded database with {len(products_data)} products and categories!"))

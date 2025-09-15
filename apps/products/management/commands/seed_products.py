from django.core.management.base import BaseCommand
from apps.products.models import Product

# A list of product data to be seeded.
PRODUCTS_TO_SEED = [
    {
        "name": "Fascia Massage Gun",
        "description": "Powerful muscle relief with multiple attachments.",
        "price": 129.99,
        "image_url": "https://example.com/images/massage-gun.jpg",
        "category": "Health & Wellness",
    },
    {
        "name": "Smart Water Bottle",
        "description": "Tracks your hydration and glows to remind you to drink.",
        "price": 45.00,
        "image_url": "https://example.com/images/smart-bottle.jpg",
        "category": "Gadgets",
    },
    {
        "name": "Ergonomic Office Chair",
        "description": "Designed for maximum comfort and support during long work hours.",
        "price": 249.50,
        "image_url": "https://example.com/images/ergonomic-chair.jpg",
        "category": "Home & Office",
    },
    # ...add more product data as needed
]

class Command(BaseCommand):
    help = "Seeds initial product data into the database. Updates existing products based on a unique name."

    def handle(self, *args, **options):
        self.stdout.write("Starting product seeding process...")

        for item in PRODUCTS_TO_SEED:
            # Use update_or_create to prevent duplicates and update if product exists.
            product, created = Product.objects.update_or_create(
                name=item["name"],  # Name is used as the unique key to check for existence
                defaults=item
            )
            
            status = "Created" if created else "Updated"
            self.stdout.write(self.style.SUCCESS(f"{status}: {product.name}"))

        self.stdout.write("Product seeding completed successfully.")

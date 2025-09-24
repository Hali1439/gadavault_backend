# apps/products/management/commands/seed_products.py

from django.core.management.base import BaseCommand
from django.utils.text import slugify
from decimal import Decimal
from apps.products.models import Product, Category

# ✅ Product data to seed
PRODUCTS_TO_SEED = [
    {
        "name": "Qorii",
        "price": "180.00",
        "description": "Qorii is a wooden container used for food storage and serving.",
        "image_url": "https://res.cloudinary.com/dxmxjdval/image/upload/v1757544835/qori_poll60.png",
        "category": "Home & Kitchen",
    },
    {
        "name": "Madiba Shirt",
        "price": "450.00",
        "description": "A distinctive, patterned shirt made popular by Nelson Mandela.",
        "image_url": "https://res.cloudinary.com/dxmxjdval/image/upload/v1757630241/Madiba_Shirt_xph6qn.jpg",
        "category": "Clothing",
    },
    {
        "name": "Ndebele Beaded Aprons",
        "price": "60.00",
        "description": "A vibrant apron with beadwork, part of Ndebele cultural attire.",
        "image_url": "https://res.cloudinary.com/dxmxjdval/image/upload/v1757630565/Ndebele_Beaded_Aprons_2_vhqm0k.jpg",
        "category": "Clothing",
    },
    {
        "name": "Zulu Shield and Spear",
        "price": "175.00",
        "description": "A traditional Zulu shield and spear set, symbolizing strength and heritage.",
        "image_url": "https://res.cloudinary.com/dxmxjdval/image/upload/v1757897228/Zulu_shield_and_spear_kdoufo.jpg",
        "category": "Cultural Artifacts",
    },
    # ... add the rest of your products here ...
]


class Command(BaseCommand):
    help = "Seeds authentic African product data into the database. Updates existing products by unique name."

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("🚀 Starting product seeding process..."))

        for fields in PRODUCTS_TO_SEED:
            # ✅ Ensure category exists (create if not)
            category_name = fields.pop("category", None)
            category_obj = None
            if category_name:
                slug = slugify(category_name)
                category_obj, _ = Category.objects.get_or_create(
                    name=category_name,
                    defaults={"slug": slug},
                )

            # ✅ Ensure Decimal type for price
            if "price" in fields:
                fields["price"] = Decimal(fields["price"])

            # ✅ Update or create by unique name
            product, created = Product.objects.update_or_create(
                name=fields["name"],
                defaults={**fields, "category": category_obj},
            )

            status = "🟢 Created" if created else "🟡 Updated"
            self.stdout.write(self.style.SUCCESS(f"{status}: {product.name}"))

        self.stdout.write(self.style.SUCCESS("✅ Product seeding completed successfully."))
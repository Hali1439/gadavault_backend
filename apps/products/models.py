from django.db import models

class Product(models.Model):
    """
    Represents a single product in the GadaVault e-commerce store.
    """
    name = models.CharField(max_length=255, unique=True, help_text="The name of the product.")
    description = models.TextField(blank=True, help_text="A detailed description of the product.")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="The price of the product.")
    image_url = models.URLField(max_length=200, blank=True, help_text="URL for the main product image.")
    category = models.CharField(max_length=100, help_text="The product's category (e.g., 'electronics', 'accessories').")

    def __str__(self):
        return self.name

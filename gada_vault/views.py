from django.shortcuts import render

def home(request):
    base = request.build_absolute_uri("/")[:-1]  # works for localhost + prod

    endpoints = [
        ("Admin", f"{base}/admin/"),
        ("Swagger UI", f"{base}/swagger/"),
        ("Swagger JSON", f"{base}/swagger.json"),
        ("Swagger YAML", f"{base}/swagger.yaml"),
        ("Redoc UI", f"{base}/redoc/"),

        # Users
        ("Users List", f"{base}/api/users/"),
        ("User Detail", f"{base}/api/users/1/"),
        ("Signup", f"{base}/api/users/signup/"),
        ("Contact", f"{base}/api/users/contact/"),
        ("Users List v1", f"{base}/api/v1/users/"),
        ("User Detail v1", f"{base}/api/v1/users/1/"),
        ("Signup v1", f"{base}/api/v1/users/signup/"),
        ("Contact v1", f"{base}/api/v1/users/contact/"),

        # Products
        ("Products List", f"{base}/api/products/"),
        ("Product Detail", f"{base}/api/products/1/"),
        ("Artisans List", f"{base}/api/products/artisans/"),
        ("Artisan Detail", f"{base}/api/products/artisans/1/"),
        ("Products List v1", f"{base}/api/v1/products/"),
        ("Product Detail v1", f"{base}/api/v1/products/1/"),
        ("Artisans List v1", f"{base}/api/v1/products/artisans/"),
        ("Artisan Detail v1", f"{base}/api/v1/products/artisans/1/"),

        # Designers
        ("Designers List", f"{base}/api/designers/"),
        ("Designer Detail", f"{base}/api/designers/1/"),
        ("Designers List v1", f"{base}/api/v1/designers/"),
        ("Designer Detail v1", f"{base}/api/v1/designers/1/"),
    ]

    return render(request, "home.html", {"endpoints": endpoints})

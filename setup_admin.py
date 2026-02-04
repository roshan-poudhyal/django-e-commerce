import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')
django.setup()

from django.contrib.auth.models import User
from store.models import Category, Product

# Create default admin user
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(username='admin', email='admin@ecommerce.com', password='admin123')
    print("✓ Admin user created successfully!")
    print("  Username: admin")
    print("  Password: admin123")
else:
    print("✓ Admin user already exists")

# Create sample categories
categories = [
    {'name': 'Electronics', 'description': 'Electronic devices and gadgets'},
    {'name': 'Clothing', 'description': 'Apparel and fashion items'},
    {'name': 'Home & Garden', 'description': 'Home and garden products'},
    {'name': 'Sports', 'description': 'Sports and fitness equipment'},
]

for cat_data in categories:
    Category.objects.get_or_create(
        name=cat_data['name'],
        defaults={'description': cat_data['description']}
    )

print("✓ Sample categories created!")

# Create sample products
sample_products = [
    {
        'name': 'Wireless Headphones',
        'description': 'High-quality wireless headphones with noise cancellation',
        'price': 79.99,
        'stock': 50,
        'category_name': 'Electronics'
    },
    {
        'name': 'Cotton T-Shirt',
        'description': 'Comfortable 100% cotton t-shirt',
        'price': 19.99,
        'stock': 100,
        'category_name': 'Clothing'
    },
    {
        'name': 'Desk Lamp',
        'description': 'LED desk lamp with adjustable brightness',
        'price': 34.99,
        'stock': 30,
        'category_name': 'Home & Garden'
    },
    {
        'name': 'Yoga Mat',
        'description': 'Non-slip yoga mat for exercise',
        'price': 29.99,
        'stock': 40,
        'category_name': 'Sports'
    },
]

for prod_data in sample_products:
    category = Category.objects.get(name=prod_data['category_name'])
    Product.objects.get_or_create(
        name=prod_data['name'],
        defaults={
            'description': prod_data['description'],
            'price': prod_data['price'],
            'stock': prod_data['stock'],
            'category': category
        }
    )

print("✓ Sample products created!")
print("\n✅ Setup complete! Your e-commerce site is ready.")

# Zain Market — Django + MySQL

Full e-commerce app: product catalog, cart, orders, admin dashboard.

## Stack
- **Backend:** Django 5.0
- **Database:** MySQL
- **Frontend:** Bootstrap 5 + Django Templates
- **Auth:** Django built-in (custom User model)

---

## Setup Steps

### 1. Python environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

pip install -r requirements.txt
```

### 2. MySQL database banao
```sql
CREATE DATABASE zain_market_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. Settings update karo
`zain_market/settings.py` mein:
```python
DATABASES = {
    'default': {
        'NAME': 'zain_market_db',
        'USER': 'root',
        'PASSWORD': 'apna_password',  # <-- yahan
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 4. Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Admin user banao
```bash
python manage.py createsuperuser
```
Superuser banne ke baad Django admin (`/admin`) se us user ka role 'admin' set karo.

### 6. Demo data (optional)
```bash
python manage.py shell
```
```python
from apps.products.models import Category, Product
cat = Category.objects.create(name="Electronics")
Product.objects.create(name="Laptop", price=85000, stock=10, category=cat, description="Gaming laptop")
Product.objects.create(name="Phone", price=45000, stock=3, category=cat, description="Android phone")
```

### 7. Server run karo
```bash
python manage.py runserver
```
Site: http://127.0.0.1:8000

---

## URLs

| URL | Description |
|-----|-------------|
| `/` | Product catalog |
| `/accounts/register/` | Register |
| `/accounts/login/` | Login |
| `/cart/` | Shopping cart |
| `/orders/checkout/` | Checkout |
| `/orders/my-orders/` | Order history |
| `/dashboard/` | Admin dashboard |
| `/manage/products/` | Product management |
| `/admin/` | Django admin panel |

## Demo Accounts (after createsuperuser)
- **Admin:** createsuperuser se banao, role = admin set karo
- **Customer:** /accounts/register/ se banao

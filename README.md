# 🌾 AgriConnect

**Bridging Farmers and Restaurants - A Direct Farm-to-Table Platform**

AgriConnect is a web application that connects local farmers directly with restaurants, eliminating middlemen and ensuring fresh produce reaches kitchens faster at fair prices.

![Django](https://img.shields.io/badge/Django-6.0-green)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [API Endpoints](#-api-endpoints)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### For Farmers 👨‍🌾
- **Register & Login** - Create a farmer account with farm details
- **Add Produce** - List available produce with quantity, price, and availability date
- **Contact Number** - Provide contact details for each produce listing
- **Manage Listings** - View and track all produce listings
- **Receive Orders** - Get order requests from restaurants
- **Accept/Reject Orders** - Manage incoming supply requests
- **Dashboard Stats** - View total listings, available items, and pending requests

### For Restaurants 🍽️
- **Register & Login** - Create a restaurant account with business details
- **Browse Produce** - View all available produce from local farmers
- **Request Supply** - Send supply requests to farmers with desired quantity
- **Track Orders** - Monitor order status (Pending/Accepted/Rejected)
- **Dashboard Stats** - View available farmers, produce items, and order status

### General Features
- **Role-based Authentication** - Separate dashboards for farmers and restaurants
- **Profile Management** - View registered profile information
- **Logout Confirmation** - Warning modal before logging out
- **Responsive Design** - Works on desktop and mobile devices
- **Real-time Updates** - Instant status updates on orders

---

## 🛠 Tech Stack

| Category | Technology |
|----------|------------|
| **Backend** | Django 6.0, Python 3.11 |
| **Database** | SQLite (Development), PostgreSQL (Production) |
| **Frontend** | HTML5, CSS3, JavaScript |
| **Authentication** | Django Auth with Custom User Model |
| **Static Files** | WhiteNoise |
| **Deployment** | Gunicorn, Railway/Render/Heroku |

---

## 🚀 Installation

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- Git

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/agriconnect.git
cd agriconnect/myproject
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### Step 6: Run the Server
```bash
python manage.py runserver
```

### Step 7: Open in Browser
Navigate to `http://127.0.0.1:8000/`

---

## 📖 Usage

### Getting Started

1. **Visit the Homepage** - Choose to register as a Farmer or Restaurant

2. **For Farmers:**
   - Register with your farm details (name, location, phone)
   - Login to access your dashboard
   - Add produce with name, quantity, price, availability date, and contact number
   - View and manage your listings
   - Accept or reject incoming orders from restaurants

3. **For Restaurants:**
   - Register with your restaurant details (name, type, address, GST)
   - Login to access your dashboard
   - Browse available produce from farmers
   - Click "Request Supply" and enter desired quantity
   - Track your orders in "My Orders" section

### Demo Accounts
After running migrations, you can create test accounts:

**Farmer Account:**
- Email: farmer@test.com
- Password: (set during registration)

**Restaurant Account:**
- Email: restaurant@test.com
- Password: (set during registration)

---

## 📁 Project Structure

```
myproject/
├── agriconnect/              # Project settings
│   ├── __init__.py
│   ├── settings.py           # Django settings
│   ├── urls.py               # Main URL routing
│   └── wsgi.py               # WSGI configuration
│
├── core/                     # Main application
│   ├── migrations/           # Database migrations
│   ├── __init__.py
│   ├── admin.py              # Admin panel configuration
│   ├── backends.py           # Custom email authentication
│   ├── forms.py              # Django forms
│   ├── models.py             # Database models
│   ├── urls.py               # App URL routing
│   └── views.py              # View functions
│
├── templates/                # HTML templates
│   ├── index.html            # Landing page
│   ├── login.html            # Login page
│   ├── register.html         # Registration page
│   ├── farmer_dashboard.html # Farmer dashboard
│   └── restaurant_dashboard.html # Restaurant dashboard
│
├── static/                   # Static files
│   └── style.css             # Global styles
│
├── staticfiles/              # Collected static files (production)
├── db.sqlite3                # SQLite database
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── Procfile                  # Heroku/Railway deployment
├── runtime.txt               # Python version
└── README.md                 # This file
```

---

## 🔗 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Landing page |
| `/register/farmer/` | GET, POST | Farmer registration |
| `/register/restaurant/` | GET, POST | Restaurant registration |
| `/login/` | GET, POST | User login |
| `/logout/` | GET | User logout |
| `/dashboard/` | GET | Redirect to role-based dashboard |
| `/farmer/dashboard/` | GET | Farmer dashboard |
| `/farmer/add-produce/` | POST | Add new produce |
| `/farmer/order/<id>/<status>/` | GET | Accept/Reject order |
| `/restaurant/dashboard/` | GET | Restaurant dashboard |
| `/restaurant/request/<id>/` | POST | Request supply |
| `/admin/` | GET | Django admin panel |

---

## 📊 Database Models

### User (Custom)
- Email-based authentication
- Role: Farmer or Restaurant
- Phone number

### FarmerProfile
- Farm name
- Location
- Description

### RestaurantProfile
- Restaurant name
- Restaurant type
- Address
- GST number

### Produce
- Name, Quantity, Price
- Availability date
- Contact number
- Status (Available/Pending/Sold)

### Order
- Restaurant, Farmer, Produce references
- Quantity requested
- Total price
- Status (Pending/Accepted/Rejected)

---

## 🌐 Deployment

### Railway (Recommended)
1. Push code to GitHub
2. Connect to Railway
3. Add environment variables:
   ```
   DEBUG=False
   SECRET_KEY=your-secret-key
   ALLOWED_HOSTS=your-app.railway.app
   ```

### Render
1. Create new Web Service
2. Connect GitHub repository
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `gunicorn agriconnect.wsgi`

### Environment Variables
```env
DEBUG=False
SECRET_KEY=your-super-secret-key-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com
DATABASE_URL=postgres://user:password@host:5432/dbname
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---


#   a g r i t e c h - - e x p e r i m e n t  
 
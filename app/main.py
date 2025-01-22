from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from .database import engine, SessionLocal
from .models import Base, Product
from .routes import auth, protected_route, product  # Ensure this import is correct

app = FastAPI()

# Add session middleware with a strong secret key
app.add_middleware(SessionMiddleware, secret_key="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")

# Create tables
Base.metadata.create_all(bind=engine)

# Add sample products
def add_sample_products():
    db = SessionLocal()
    car_images = [
        # {"name": "Red Sports Car", "description": "A beautiful red sports car.", "price": 50000.0, "image_url": "https://images.unsplash.com/photo-1549921296-3a6b5a4b4d9d"},
        # {"name": "Blue Sedan", "description": "A sleek blue sedan.", "price": 30000.0, "image_url": "https://images.unsplash.com/photo-1511391409280-9cbfba6fab6e"},
        # {"name": "Black SUV", "description": "A powerful black SUV.", "price": 45000.0, "image_url": "https://images.unsplash.com/photo-1503376780353-7e6692767b70"},
        # {"name": "White Convertible", "description": "A stylish white convertible.", "price": 60000.0, "image_url": "https://images.unsplash.com/photo-1502877338535-766e1452684a"},
        # {"name": "Green Hatchback", "description": "A compact green hatchback.", "price": 20000.0, "image_url": "https://images.unsplash.com/photo-1525609004556-c46c7d6cf023"},
        # {"name": "Yellow Coupe", "description": "A sporty yellow coupe.", "price": 35000.0, "image_url": "https://images.unsplash.com/photo-1519643225200-94e79e383724"},
        # {"name": "Silver Minivan", "description": "A spacious silver minivan.", "price": 40000.0, "image_url": "https://images.unsplash.com/photo-1541446654331-0af808871cc0"},
        # {"name": "Orange Truck", "description": "A rugged orange truck.", "price": 55000.0, "image_url": "https://images.unsplash.com/photo-1518397387277-7843f7251311"},
        # {"name": "Purple Luxury Car", "description": "A luxurious purple car.", "price": 70000.0, "image_url": "https://images.unsplash.com/photo-1512820790803-83ca734da794"},
        # {"name": "Brown Classic Car", "description": "A classic brown car.", "price": 25000.0, "image_url": "https://images.unsplash.com/photo-1503736334956-4c8f8e92946d"}
    ]

    for car in car_images:
        existing_product = db.query(Product).filter(Product.name == car["name"]).first()
        if not existing_product:
            sample_product = Product(
                name=car["name"],
                description=car["description"],
                price=car["price"],
                image_url=car["image_url"]
            )
            db.add(sample_product)
            db.commit()
    db.close()

# Call the function only once during initial setup
add_sample_products()

# Include routes
app.include_router(auth.router)
app.include_router(protected_route.router)
app.include_router(product.router)  # Ensure this route is included

# Initialize Jinja2 Templates
templates = Jinja2Templates(directory="app/templates")

# Serve static files (CSS, JS, images, etc.)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})
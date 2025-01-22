from fastapi import APIRouter, Depends, HTTPException, Form, status, Request
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
import jwt
from .. import models, schemas
from ..database import SessionLocal
from fastapi.templating import Jinja2Templates

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter(prefix="/auth", tags=["auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

templates = Jinja2Templates(directory="app/templates")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/register", response_model=schemas.UserOut)
def register(
    username: str = Form(...), 
    email: str = Form(...),
    password: str = Form(...),
    role_id: int = Form(...), 
    db: Session = Depends(get_db)
):
    # Check if the email already exists
    existing_user = db.query(models.User).filter(models.User.email == email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    hashed_password = pwd_context.hash(password)
    db_user = models.User(username=username, email=email, password=hashed_password, role_id=role_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return RedirectResponse(url="/", status_code=303)

@router.post("/login")
def login(
    request: Request,
    username_or_email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(
        (models.User.username == username_or_email) | (models.User.email == username_or_email)
    ).first()
    if not user or not pwd_context.verify(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    request.session["access_token"] = access_token
    return RedirectResponse(url="/products", status_code=303)

# @router.get("/products/create")
# def create_product_form(request: Request):
#     return templates.TemplateResponse("create_product.html", {"request": request})

# @router.post("/products/create")
# def create_product(
#     request: Request,
#     url: str = Form(...),
#     name: str = Form(...),
#     price: float = Form(...),
#     description: str = Form(...),
#     db: Session = Depends(get_db)
# ):
#     new_product = models.Product(name=name, description=description, price=price, image_url=url)
#     db.add(new_product)
#     db.commit()
#     return RedirectResponse(url="/products", status_code=303)

@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)

def get_current_user(request: Request, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = request.session.get("access_token")
    if not token:
        raise credentials_exception
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except jwt.PyJWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user
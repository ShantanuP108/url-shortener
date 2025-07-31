import random, string
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from app.core.database import SessionLocal
from app.models.url import ShortURL
from app.schemas.url import URLCreate, URLInfo
from app.core.security import SECRET_KEY

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Helper to decode token and get current user ID
def get_current_user_id(token: str, secret_key: str = SECRET_KEY):
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return UUID(payload.get("sub"))
    except (JWTError, TypeError):
        raise HTTPException(status_code=401, detail="Invalid or expired token")


# 🔗 Generate short code
def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


@router.post("/shorten", response_model=URLInfo)
def shorten_url(
    url: URLCreate,
    request: Request,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    # Auth token from header
    user_id = get_current_user_id(token)

    short_code = generate_short_code()
    while db.query(ShortURL).filter(ShortURL.short_code == short_code).first():
        short_code = generate_short_code()

    short_url = ShortURL(
        short_code=short_code,
        target_url=url.target_url,
        owner_id=user_id
    )
    db.add(short_url)
    db.commit()
    db.refresh(short_url)
    return short_url


@router.get("/s/{short_code}")
def redirect_url(short_code: str, db: Session = Depends(get_db)):
    record = db.query(ShortURL).filter(ShortURL.short_code == short_code).first()
    if not record:
        raise HTTPException(status_code=404, detail="Short URL not found")

    record.clicks += 1
    db.commit()

    return {"target_url": record.target_url}

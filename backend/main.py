import sys
import os
import site

# Add user site-packages to path
user_site = site.getusersitepackages()
if user_site not in sys.path:
    sys.path.append(user_site)

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

from . import models, schemas, database, auth
from . import email_service
from .config import EmailConfig
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Dianping Clone API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Serve index.html at root
@app.get("/")
async def read_index():
    return FileResponse(os.path.join(frontend_dir, "index.html"))

# 注意：静态文件路由必须放在所有API端点之后定义
# 否则会拦截API请求

@app.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        # 验证至少提供了邮箱或手机号中的一个
        if not user.email and not user.phone:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Please provide either email or phone number"
            )
        
        # 验证用户名是否已存在
        db_user = db.query(models.User).filter(models.User.username == user.username).first()
        if db_user:
            raise HTTPException(status_code=400, detail="Username already registered")
        
        # 验证邮箱是否已存在（如果提供了邮箱）
        if user.email:
            db_user = db.query(models.User).filter(models.User.email == user.email).first()
            if db_user:
                raise HTTPException(status_code=400, detail="Email already registered")
        
        # 验证手机号是否已存在（如果提供了手机号）
        if user.phone:
            db_user = db.query(models.User).filter(models.User.phone == user.phone).first()
            if db_user:
                raise HTTPException(status_code=400, detail="Phone number already registered")
        
        # 验证密码长度
        if len(user.password) > 72:
            raise HTTPException(status_code=400, detail="Password cannot be longer than 72 characters")
        
        hashed_password = auth.get_password_hash(user.password)
        db_user = models.User(
            username=user.username,
            email=user.email,
            phone=user.phone,
            hashed_password=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except HTTPException:
        # 重新抛出 HTTP 异常
        raise
    except Exception as e:
        print(f"Registration error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # 尝试通过用户名、邮箱或手机号查找用户
    user = db.query(models.User).filter(
        (models.User.username == form_data.username) | 
        (models.User.email == form_data.username) | 
        (models.User.phone == form_data.username)
    ).first()
    
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username, email, phone or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=schemas.User)
async def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user

@app.put("/users/me", response_model=schemas.User)
async def update_user_me(user_update: schemas.UserUpdate, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    """Update current user's profile"""
    # Update user fields
    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(current_user, key, value)
    
    db.commit()
    db.refresh(current_user)
    return current_user

@app.get("/users/me/stats")
async def read_user_stats(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    """Get user stats: reviews count, favorites count, points"""
    # Calculate reviews count
    reviews_count = db.query(models.Review).filter(models.Review.user_id == current_user.id).count()
    
    # Calculate favorites count
    favorites_count = db.query(models.Favorite).filter(models.Favorite.user_id == current_user.id).count()
    
    # Calculate points (placeholder, assuming 10 points per review and 5 points per favorite)
    points = (reviews_count * 10) + (favorites_count * 5)
    
    return {
        "reviews": reviews_count,
        "favorites": favorites_count,
        "points": points
    }

@app.get("/users/me/reviews", response_model=List[schemas.Review])
async def read_user_reviews(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    """Get user's reviews with merchant information"""
    from sqlalchemy.orm import joinedload
    reviews = db.query(models.Review).filter(models.Review.user_id == current_user.id).options(joinedload(models.Review.merchant)).order_by(models.Review.created_at.desc()).all()
    return reviews

@app.get("/users/me/favorites", response_model=List[schemas.Merchant])
async def read_user_favorites(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    """Get user's favorite merchants"""
    favorites = db.query(models.Favorite).filter(models.Favorite.user_id == current_user.id).all()
    # Extract merchant ids from favorites
    merchant_ids = [fav.merchant_id for fav in favorites]
    # Get merchants by ids
    merchants = db.query(models.Merchant).filter(models.Merchant.id.in_(merchant_ids)).all()
    return merchants

@app.post("/users/me/favorites/{merchant_id}")
async def add_favorite(merchant_id: int, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    """Add a merchant to user's favorites"""
    # Check if merchant exists
    merchant = db.query(models.Merchant).filter(models.Merchant.id == merchant_id).first()
    if not merchant:
        raise HTTPException(status_code=404, detail="Merchant not found")
    
    # Check if already in favorites
    existing_favorite = db.query(models.Favorite).filter(
        models.Favorite.user_id == current_user.id,
        models.Favorite.merchant_id == merchant_id
    ).first()
    
    if existing_favorite:
        return {"message": "Already in favorites"}
    
    # Create new favorite
    new_favorite = models.Favorite(user_id=current_user.id, merchant_id=merchant_id)
    db.add(new_favorite)
    db.commit()
    
    return {"message": "Added to favorites"}

@app.delete("/users/me/favorites/{merchant_id}")
async def remove_favorite(merchant_id: int, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    """Remove a merchant from user's favorites"""
    # Find the favorite
    favorite = db.query(models.Favorite).filter(
        models.Favorite.user_id == current_user.id,
        models.Favorite.merchant_id == merchant_id
    ).first()
    
    if not favorite:
        raise HTTPException(status_code=404, detail="Not in favorites")
    
    # Delete the favorite
    db.delete(favorite)
    db.commit()
    
    return {"message": "Removed from favorites"}

def generate_verification_code():
    """生成6位纯数字验证码"""
    import random
    return str(random.randint(100000, 999999))

# Password reset endpoints
@app.post("/password-reset-request")
def request_password_reset(reset_request: schemas.PasswordResetRequest, db: Session = Depends(get_db)):
    """Request a password reset code by email"""
    # 验证提供了邮箱
    if not reset_request.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="请提供邮箱地址"
        )
    
    # 查找用户
    user = db.query(models.User).filter(models.User.email == reset_request.email).first()
    
    # 生成6位验证码
    verification_code = generate_verification_code()
    
    # 计算过期时间（15分钟）
    from datetime import datetime, timedelta
    expires_at = datetime.utcnow() + timedelta(minutes=15)
    
    # 将邮件发送信息入库
    password_reset_email = models.PasswordResetEmail(
        email=reset_request.email,
        verification_code=verification_code,
        sent_at=datetime.utcnow(),
        expires_at=expires_at,
        user_id=user.id if user else None,
        is_used=0
    )
    db.add(password_reset_email)
    db.commit()
    db.refresh(password_reset_email)
    
    # 发送邮件
    email_sent, email_message = email_service.send_password_reset_email(
        reset_request.email, 
        verification_code
    )
    
    # 构建响应
    response = {
        "message": "验证码已发送到您的邮箱",
        "email": reset_request.email
    }
    
    # 如果邮件服务未启用，返回验证码供测试使用
    if not EmailConfig.ENABLE_EMAIL_SENDING:
        response["verification_code"] = verification_code
        response["note"] = "邮件服务未启用，此验证码仅用于测试"
    
    return response

@app.post("/password-reset")
def reset_password(reset_data: schemas.PasswordReset, db: Session = Depends(get_db)):
    """Reset password using verification code"""
    # 验证邮箱
    if not reset_data.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="请提供邮箱地址"
        )
    
    # 验证验证码
    if not reset_data.verification_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="请提供验证码"
        )
    
    # 从数据库查找最新的有效验证码
    from datetime import datetime
    reset_record = db.query(models.PasswordResetEmail).filter(
        models.PasswordResetEmail.email == reset_data.email,
        models.PasswordResetEmail.verification_code == reset_data.verification_code,
        models.PasswordResetEmail.is_used == 0,
        models.PasswordResetEmail.expires_at > datetime.utcnow()
    ).order_by(models.PasswordResetEmail.created_at.desc()).first()
    
    if not reset_record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="验证码无效或已过期，请重新获取"
        )
    
    # 查找用户
    user = None
    if reset_record.user_id:
        user = db.query(models.User).filter(models.User.id == reset_record.user_id).first()
    else:
        # 尝试通过邮箱查找用户
        user = db.query(models.User).filter(models.User.email == reset_data.email).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 验证密码长度
    if len(reset_data.new_password) > 72:
        raise HTTPException(status_code=400, detail="密码不能超过72个字符")
    
    # 更新密码
    hashed_password = auth.get_password_hash(reset_data.new_password)
    user.hashed_password = hashed_password
    
    # 标记验证码为已使用
    reset_record.is_used = 1
    
    db.commit()
    
    return {"message": "密码重置成功"}

@app.post("/users/me/change-password")
def change_user_password(password_data: schemas.PasswordChange, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    """Change password for logged-in user"""
    # 验证当前密码
    if not auth.verify_password(password_data.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    # 验证新密码长度
    if len(password_data.new_password) > 72:
        raise HTTPException(status_code=400, detail="Password cannot be longer than 72 characters")
    
    # 更新密码
    hashed_password = auth.get_password_hash(password_data.new_password)
    current_user.hashed_password = hashed_password
    db.commit()
    
    return {"message": "Password has been changed successfully"}

@app.get("/merchants", response_model=List[schemas.Merchant])
def get_merchants(category: Optional[str] = None, q: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(models.Merchant)
    if category:
        query = query.filter(models.Merchant.category == category)
    if q:
        query = query.filter(models.Merchant.name.contains(q) | models.Merchant.description.contains(q))
    return query.all()

@app.post("/merchants", response_model=schemas.Merchant)
def create_merchant(merchant: schemas.MerchantCreate, db: Session = Depends(get_db)):
    """Create a new merchant"""
    db_merchant = models.Merchant(**merchant.dict())
    db.add(db_merchant)
    db.commit()
    db.refresh(db_merchant)
    return db_merchant

@app.get("/merchants")
def get_merchants(category: Optional[str] = None, db: Session = Depends(database.get_db)):
    """Get all merchants, optionally filtered by category"""
    query = db.query(models.Merchant)
    if category:
        query = query.filter(models.Merchant.category == category)
    merchants = query.all()
    # Convert to list of dictionaries instead of using Pydantic model
    return [{
        "id": merchant.id,
        "name": merchant.name,
        "description": merchant.description,
        "address": merchant.address,
        "category": merchant.category,
        "phone": merchant.phone,
        "rating": merchant.rating,
        "reviews_count": merchant.reviews_count,
        "image_url": merchant.image_url,
        "created_at": merchant.created_at.isoformat()
    } for merchant in merchants]

@app.get("/merchants/{merchant_id}")
def get_merchant(merchant_id: int, db: Session = Depends(get_db)):
    merchant = db.query(models.Merchant).filter(models.Merchant.id == merchant_id).first()
    if not merchant:
        raise HTTPException(status_code=404, detail="Merchant not found")
    
    # 获取商家的评价
    reviews = db.query(models.Review).filter(models.Review.merchant_id == merchant_id).all()
    
    # 返回包含评价的完整商家信息
    return {
        "id": merchant.id,
        "name": merchant.name,
        "description": merchant.description,
        "address": merchant.address,
        "category": merchant.category,
        "phone": merchant.phone,
        "rating": merchant.rating,
        "reviews_count": merchant.reviews_count,
        "image_url": merchant.image_url,
        "created_at": merchant.created_at.isoformat(),
        "reviews": [
            {
                "id": review.id,
                "content": review.content,
                "rating": review.rating,
                "user_id": review.user_id,
                "merchant_id": review.merchant_id,
                "created_at": review.created_at.isoformat(),
                "author": {
                    "username": review.author.username,
                    "avatar": review.author.avatar
                }
            } for review in reviews
        ]
    }

@app.post("/merchants/{merchant_id}/reviews", response_model=schemas.Review)
def create_review(
    merchant_id: int, 
    review: schemas.ReviewBase, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    merchant = db.query(models.Merchant).filter(models.Merchant.id == merchant_id).first()
    if not merchant:
        raise HTTPException(status_code=404, detail="Merchant not found")
    
    db_review = models.Review(
        **review.dict(),
        user_id=current_user.id,
        merchant_id=merchant_id
    )
    db.add(db_review)
    
    # Update merchant rating and reviews count
    merchant.reviews_count += 1
    # Calculate new rating more safely
    if merchant.reviews_count == 1:
        # First review
        merchant.rating = review.rating
    else:
        # Existing reviews - use current rating to calculate new total
        total_rating = (merchant.rating * (merchant.reviews_count - 1)) + review.rating
        merchant.rating = total_rating / merchant.reviews_count
    
    db.commit()
    # 手动设置商家关系，确保返回的对象包含商家信息
    db_review.merchant = merchant
    return db_review

# Seed data for testing
@app.post("/seed")
def seed_data(db: Session = Depends(get_db)):
    if db.query(models.Merchant).count() > 0:
        return {"message": "Data already seeded"}
    
    merchants = [
        models.Merchant(
            name="老北京涮肉",
            description="地道的北京风味涮羊肉，传统铜锅。",
            address="朝阳区三里屯1号",
            category="美食",
            phone="010-12345678",
            image_url="https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=800&auto=format&fit=crop"
        ),
        models.Merchant(
            name="悦己SPA",
            description="高端水疗体验，放松身心。",
            address="海淀区中关村大街2号",
            category="休闲娱乐",
            phone="010-87654321",
            image_url="https://images.unsplash.com/photo-1600334129128-685c5582fd35?w=800&auto=format&fit=crop"
        ),
        models.Merchant(
            name="光影电影院",
            description="IMAX巨幕，极致视听享受。",
            address="朝阳区大望路3号",
            category="电影",
            phone="010-13572468",
            image_url="https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=800&auto=format&fit=crop"
        )
    ]
    db.add_all(merchants)
    db.commit()
    return {"message": "Seeded successfully"}

# Mount static files at the end to avoid intercepting API routes
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

# Catch-all route for static files (must be last)
@app.get("/{file_path:path}")
async def read_static_file(file_path: str):
    file_path = os.path.join(frontend_dir, file_path)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        raise HTTPException(status_code=404, detail="File not found")

from fastapi import APIRouter,Depends,HTTPException,status

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database.database import get_db 
from app.models.user import User
from app.schemas.user import UserRead,UserCreate

router=APIRouter(prefix="/users",tags=["users"])

@router.get("",response_model=list[UserRead])
def list_users(db:Session=Depends(get_db)) ->list[User]:
    return db.query(User).all()

@router.post("",response_model=UserRead,status_code=status.HTTP_201_CREATED)
def create_user(payload:UserCreate,db:Session=Depends(get_db))->User:
        user=User(name=payload.name,email=payload.email)
        db.add(user)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email Already Exists"
            )
        db.refresh(user)
        return user
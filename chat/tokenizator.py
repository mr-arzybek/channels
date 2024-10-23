import jwt
from datetime import datetime, timedelta


ALGORITHM = "HS256"
access_token_jwt_subject = "access"


def create_token(user_id: int) -> dict:
    access_token_expires = timedelta(minutes=60)
    return {
        "access_token": create_access_token(
            data={"user_id": user_id}, expires_delta=access_token_expires
        ),
        "token_type": "Token",
    }


def create_access_token(data: dict, expires_delta: timedelta = None):
    """Создание токена"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=3)
    to_encode.update({"exp": expire, "sub": access_token_jwt_subject})
    encoded_jwt = jwt.encode(to_encode, "fdsadqw3f32w45756yfhhndg<43g3hv$%#@%F$gfgF$$F$F", algorithm=ALGORITHM)
    return encoded_jwt


token = create_token(2)
print(token)

import os
from datetime import datetime

import django
from jwt import ExpiredSignatureError, InvalidTokenError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

import jwt
from channels.auth import AuthMiddlewareStack
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware

from django.contrib.auth.models import User
from django.db import close_old_connections
import logging

ALGORITHM = "HS256"


@database_sync_to_async
def get_user(token):
    try:
        payload = jwt.decode(token, "fdsadqw3f32w45756yfhhndg<43g3hv$%#@%F$gfgF$$F$F", algorithms=[ALGORITHM])
        print('payload', payload)
    except Exception as e:
        print(f'Unexpected error: {e}')
        return AnonymousUser()

    token_exp = datetime.fromtimestamp(payload['exp'])
    if token_exp < datetime.utcnow():
        print("Token has expired")
        return AnonymousUser()

    try:
        user = User.objects.get(id=payload['user_id'])
    except User.DoesNotExist:
        print('User does not exist')
        return AnonymousUser()

    return user


class TokenAuthMiddleware(BaseMiddleware):

    async def __call__(self, scope, receive, send):
        close_old_connections()
        token_key = None
        query_string = scope.get('query_string', b'').decode()

        # Пробуем получить токен из query_string
        if query_string:
            token_dict = dict((x.split('=') for x in query_string.split("&")))
            token_key = token_dict.get('token', None)

        if token_key:
            scope['user'] = await get_user(token_key)
        else:
            scope['user'] = AnonymousUser()

        return await super().__call__(scope, receive, send)


def JwtAuthMiddlewareStack(inner):
    return TokenAuthMiddleware(inner)
    # return TokenAuthMiddleware(AuthMiddlewareStack(inner))

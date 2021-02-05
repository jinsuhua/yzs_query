from django.utils.deprecation import MiddlewareMixin
from rest_framework_jwt.utils import  jwt_decode_handler
from .config import *
from .models import AccessLog

"""
    访问uri记录日志表
"""
class LogMid(MiddlewareMixin):

    def process_request(self, request):
        try:
            uri = request.path
            if uri in log_access_uris:
                auth = request.META['HTTP_AUTHORIZATION']
                if auth:
                    token = auth.split(" ")[1]
                    decoded_token = jwt_decode_handler(token)
                    token_type = decoded_token.get('token_type')
                    user_id = decoded_token.get('user_id')
                    # 记录日志
                    if token_type == 'access' and user_id is not None:
                        log = AccessLog()
                        log.user_id = user_id
                        log.uri = uri
                        log.save()
        except:
            return None








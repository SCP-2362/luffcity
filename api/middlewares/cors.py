

from .base import MiddlewareMixin


class CORSMiddleware(MiddlewareMixin):
    """CORS中间件"""
    def process_response(self, request, response):
        if request.method == "OPTIONS":
            response['Access-Control-Allow-Origin'] = '*'
            response['Access-Control-Allow-Headers'] = '*'
        else:
            response['Access-Control-Allow-Origin'] = '*'
        return response

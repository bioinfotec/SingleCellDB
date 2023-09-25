class UserIpMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 获取用户的IP地址
        user_ip = request.META.get('REMOTE_ADDR', None)
        
        # 将IP地址添加到request的上下文中
        request.user_ip = user_ip

        response = self.get_response(request)
        return response

from rest_framework import permissions

class CustomedPermission(permissions.BasePermission):
    message = 'You are not allowed here' # 自定义错误信息
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated:
            self.message = "Hello"
            return True
        else:
            self.message = "You are not allowed here"
            return False
        
        
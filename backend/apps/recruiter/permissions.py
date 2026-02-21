from rest_framework.permissions import BasePermission


class IsRecruiter(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type in ["recruiter", "admin"]


class IsCompanyAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.company_id == obj.id

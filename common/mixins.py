from rest_framework.authentication import SessionAuthentication


class NoneCSRFSessionAuthentication(SessionAuthentication):
    # 直接给一个pass就行了
    def enforce_csrf(self, request):
        pass

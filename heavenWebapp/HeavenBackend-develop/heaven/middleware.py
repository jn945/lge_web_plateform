import logging

logger = logging.getLogger(__name__)


class RequestUserLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 유저가 인증되어 있을 경우에만 로깅합니다.
        if request.user.is_authenticated:
            logger.info(f"request user: {request.user}")
        else:
            logger.info("요청 유저: 익명 사용자")
        try:
            logger.info(f"request user: {request.url}")
            logger.info(f"request data: {request.data}")
        except:
            pass

        response = self.get_response(request)
        return response

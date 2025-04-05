import traceback


class CustomException(Exception):
    def __init__(self, message: str, http_status_code: int, error_code='custom'):
        super().__init__(message)  # 기본 예외 메시지를 설정
        self.message = message
        self.http_status_code = http_status_code  # 추가 속성 설정
        self.trace_info = traceback.format_exc()  # traceback 정보 저장
        self.error_code = error_code

    def __str__(self):
        # 예외가 발생했을 때 출력되는 메시지 형식 커스터마이징
        return f"Error Code {self.http_status_code}: {self.message}"

    def get_trace_back(self) -> str:
        return f"Traceback: {self.trace_info}"

    def get_code(self) -> str:
        return self.error_code


class DomainException(CustomException):
    def __init__(self, message: str, http_status_code=500, error_code: str = 'domain'):
        super().__init__(message=message, http_status_code=http_status_code, error_code=error_code)


class UseCaseException(CustomException):
    def __init__(self, message: str, http_status_code: int = 404, error_code='use case'):
        super().__init__(message=message, http_status_code=http_status_code, error_code=error_code)


class PresentationException(CustomException):
    def __init__(self, message: str, http_status_code: int = 400, error_code='use case'):
        super().__init__(message=message, http_status_code=http_status_code, error_code=error_code)


class InfraException(CustomException):
    def __init__(self, message: str, http_status_code: int = 500, error_code='infra'):
        super().__init__(message=message, http_status_code=http_status_code, error_code=error_code)
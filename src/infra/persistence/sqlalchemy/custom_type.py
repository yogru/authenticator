from sqlalchemy import TypeDecorator, String


class StringEnumSqlAlchemyType(TypeDecorator):
    impl = String
    cache_ok = True

    def __init__(self, enumclass, *args, **kwargs):
        self._enumclass = enumclass
        super().__init__(*args, **kwargs)

    def process_bind_param(self, value, dialect):
        if isinstance(value, self._enumclass):
            return value.value  # Enum을 문자열로 변환
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return self._enumclass(value)  # 문자열을 Enum으로 변환
        return value

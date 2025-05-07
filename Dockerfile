# 베이스 이미지로 Python 3.13 사용
FROM python:3.12.10-slim-bullseye


# docker build -t db-persona-content-authenticator .
# docker run -d --name db-authenticator-server --rm -p 22501:22501 db-persona-content-authenticator
# 작업 디렉토리 설정
WORKDIR /app

# 필요한 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    libpq-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Poetry 버전 지정 및 설치
ENV POETRY_VERSION=1.8.5
RUN curl -sSL https://install.python-poetry.org | python3 - --version $POETRY_VERSION

# Poetry 경로 환경 변수 설정
ENV PATH="/root/.local/bin:$PATH"

# pyproject.toml과 poetry.lock을 복사
COPY pyproject.toml poetry.lock* /app/

# Poetry 가상환경 없이 설치
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi


# 애플리케이션 코드 복사
COPY . /app

COPY run-prod.sh /app/run-prod.sh

# 스크립트에 실행 권한 부여
RUN chmod +x /app/run-prod.sh

# 컨테이너 시작 시 uvicorn 실행
CMD ["/app/run-prod.sh"]
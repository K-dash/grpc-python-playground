ARG PYTHON_VERSION="3.13.1"

FROM ghcr.io/astral-sh/uv:python${PYTHON_VERSION%.*}-bookworm-slim

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never \
    UV_PYTHON=python${PYTHON_VERSION%.*}

WORKDIR /service
COPY protobufs/ /service/protobufs/
COPY marketplace/ /service/marketplace/
WORKDIR /service/marketplace

RUN --mount=type=cache,target=/root/.cache \
    set -ex && \
    uv sync --frozen --no-install-project

RUN uv run python -m grpc_tools.protoc -I /service/protobufs --python_out=. \
    --grpc_python_out=. /service/protobufs/recommendations.proto

EXPOSE 8001
ENV FLASK_APP=marketplace.py
CMD ["uv", "run", "flask", "run", "--host=0.0.0.0", "--port=8001"]

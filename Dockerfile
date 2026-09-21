FROM python:3.12

LABEL org.opencontainers.image.url=https://github.com/Teahouse-Studios/akari-bot
LABEL org.opencontainers.image.documentation=https://bot.teahouse.team/
LABEL org.opencontainers.image.source=https://github.com/Teahouse-Studios/akari-bot
LABEL org.opencontainers.image.vendor="Teahouse Studios"
LABEL org.opencontainers.image.licenses=AGPL-3.0-or-later
LABEL org.opencontainers.image.title="AkariBot"
LABEL maintainer="Teahouse Studios <admin@teahou.se>"

ARG VERSION
LABEL version=$VERSION

RUN pip install uv

WORKDIR /akari-bot

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# 实例目录显式声明：未声明时由进程 cwd 决定，改动 WORKDIR 或在别处启动会静默改变
# 配置、日志与数据库的落点。
ENV AKARI_INSTANCE_DIR=/akari-bot

RUN apt-get update && apt-get install -y \
    fonts-noto-cjk \
    fonts-noto-color-emoji \
    fonts-dejavu \
    && rm -rf /var/lib/apt/lists/*

# 源码与全部成员 pyproject 一并入镜像后按 workspace 安装：members 以 .pth editable 落地，
# python bot.py 因此能解析 akaribot.*。依赖缓存由 BuildKit 的 uv cache mount 承担。
COPY . .
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen --no-dev

ENV PATH="/akari-bot/.venv/bin:$PATH"
CMD ["python", "./bot.py"]

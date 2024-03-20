FROM python:3.9.18-slim-bullseye
LABEL \
    author="songweiquan" \
    descirbe="django base image"

EXPOSE 8877

WORKDIR /app

COPY ./ /app

ENV LC_ALL=C.UTF-8 \
    LANG=C.UTF-8

# 直接将虚拟环境的添加到PATH中就行了
ENV PATH="/opt/venv/bin:$PATH"

# 安装nginx
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list && \
    apt-get update -y && \
    apt install nginx -y && \
    apt clean && \
    rm -rf /var/lib/apt/list/* 
# 复制nginx配置文件
COPY nginx.conf /etc/nginx/nginx.conf

# 创建虚拟环境
# 安装项目依赖
# --no-cache-dir 避免pip缓存包含到镜像中
RUN python3 -m venv /opt/venv && \
    pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip3 install --no-cache-dir -U pip && \
    pip3 install --no-cache-dir -r requirements.txt

# 调用脚本运行项目
ENTRYPOINT ["bash", "/app/start.sh"]

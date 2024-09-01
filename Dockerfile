# 这是一个带web桌面环境的ubuntu镜像
FROM dorowu/ubuntu-desktop-lxde-vnc
LABEL authors="qiudeng"
WORKDIR /root/Desktop

# 换源，安装chrome依赖，安装chrome，安装python3.12和本项目的Python依赖
RUN curl -sSL https://linuxmirrors.cn/main.sh | /bin/bash \
          --source mirrors.tuna.tsinghua.edu.cn \
          --protocol http \
          --intranet false \
          --install-epel false \
          --close-firewall false \
          --backup true \
          --upgrade-software true \
          --clean-cache true \
          --ignore-backup-tips

# 安装chrome依赖
RUN apt update -y; apt install -y \
        wget  \
        build-essential  \
        libreadline-dev  \
        libncursesw5-dev  \
        libssl-dev  \
        libsqlite3-dev \
        tk-dev \
        libgdbm-dev \
        libc6-dev \
        libbz2-dev \
        libffi-dev \
        zlib1g-dev ;\
    # 安装chrome
    wget 'https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb' -O google.deb ;\
    dpkg -i google.deb && apt install --fix-broken -y ;\
    #安装Python
    add-apt-repository ppa:deadsnakes/ppa -y && ;\
    apt update; apt install -y python3.12-full ;\
    # 创建虚拟环境 安装项目的Python依赖
    python3.12 -m venv .venv ;\
    .venv/bin/pip install DrissionPage ;\

ENTRYPOINT sleep infinity
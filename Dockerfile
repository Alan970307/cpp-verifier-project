# 使用一个包含基础构建工具的Ubuntu镜像
FROM ubuntu:22.04

# 避免安装过程中出现交互式提问，让它全自动化
ENV DEBIAN_FRONTEND=noninteractive

# 安装我们C++项目需要的所有工具：编译器、构建工具、版本控制、打补丁工具和Python
RUN apt-get update && apt-get install -y \
    g++ \
    cmake \
    git \
    patch \
    python3 \
    && rm -rf /var/lib/apt/lists/*

# --- 以下是根据反馈进行的修改 ---

# 1. 解决【问题一】：将工作区从/app改为/testbed
WORKDIR /testbed

# 2. 解决【问题三】：为了能使用git apply，我们需要一个Git仓库。
#    因此，我们只把编译所需的基础C++代码复制进去，然后立即初始化成一个Git仓库。
#    这样，容器内部就自带了一个干净的、有初始版本的代码库。
COPY calculator.cpp calculator.h CMakeLists.txt main.cpp ./
RUN git init && \
    git config --global user.email "test@example.com" && \
    git config --global user.name "Test User" && \
    git add . && \
    git commit -m "Initial commit of the base code"

# 3. 解决【问题二】：移除CMD指令。
#    我们不再让容器启动就自动运行某个脚本，而是让它启动后保持运行，
#    并给我们一个可以操作的命令行界面(bash)，等待我们从外部传入指令和文件。
CMD ["/bin/bash"]
# 使用一个包含基础构建工具的Ubuntu镜像
# 这是我们的“地基”，指定了我们要在一个干净的Ubuntu 22.04系统里进行所有操作。
FROM ubuntu:22.04

# 避免安装过程中出现交互式提问，让它全自动化
ENV DEBIAN_FRONTEND=noninteractive

# 这是在“装修”，安装我们C++项目需要的所有工具：编译器、构建工具、版本控制、打补丁工具和Python
RUN apt-get update && apt-get install -y \
    g++ \
    cmake \
    git \
    patch \
    python3 \
    && rm -rf /var/lib/apt/lists/*

# 这是在划分“工作区”，之后的所有命令都会在这个/app文件夹里执行
WORKDIR /app

# 这是把我们本地的“原材料”（全部6个文件）都搬到“车间”里
COPY . .

# 这是设定“启动按钮”，当“车间”启动时，自动运行我们的核心验证脚本
CMD ["python3", "run_verification.py"]
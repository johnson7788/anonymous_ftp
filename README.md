# Anonymous HTTP File Server

基于 Python 的匿名 HTTP 文件共享服务器，使用 HTTP 协议替代传统 FTP，支持文件上传、下载和目录浏览。

## 特性

- **上传/下载** — 通过标准 HTTP 方法（PUT / GET）操作文件
- **目录浏览** — 自动生成文件列表页面，支持层级导航
- **路径安全** — 内置路径穿越防护
- **Docker 部署** — 一行命令即可启动

## 快速开始

### 构建镜像

```bash
docker build -t anonymous-http .
```

### 启动服务

```bash
docker run -d \
  --name anonymous-http \
  -p 8088:8088 \
  -v $(pwd)/ftp_data:/data \
  anonymous-http
```

## 使用示例

```bash
# 上传文件
curl -T file.txt http://127.0.0.1:8088/file.txt

# 下载文件
curl -O http://127.0.0.1:8088/file.txt

# 浏览目录（浏览器访问更佳）
curl http://127.0.0.1:8088/
```

## 端口

| 端口  | 用途     |
|-------|---------|
| 8088  | HTTP 服务 |

## 目录结构

```
.
├── Dockerfile        # 容器构建文件
├── http_server.py    # 服务端入口
├── ftp_data/         # 挂载的共享数据目录
└── README.md
```

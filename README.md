# 构建镜像
docker build -t anonymous-ftp .

# 启动
docker run -d \
  --name anonymous-ftp \
  -p 21:21 \
  -p 30000-30009:30000-30009 \
  -v $(pwd)/ftp_data:/ftp \
  anonymous-ftp

# 测试上传
curl -T logo.png ftp://127.0.0.1/

测试下载
wget ftp://127.0.0.1/logo.png

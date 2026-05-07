# 构建镜像
docker build -t anonymous-http .

# 启动
docker run -d \
  --name anonymous-http \
  -p 8080:8080 \
  -v $(pwd)/ftp_data:/app/ftp_root \
  anonymous-http

# 上传文件
curl -T file.txt http://127.0.0.1:8080/file.txt

# 下载文件
curl -O http://127.0.0.1:8080/file.txt

# 浏览目录
curl http://127.0.0.1:8080/

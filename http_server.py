import http.server
import os
import urllib.parse
import html

# HTTP 共享目录
ROOT_DIR = "/data"

# 自动创建目录
os.makedirs(ROOT_DIR, exist_ok=True)


class HTTPFileHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT_DIR, **kwargs)

    def do_PUT(self):
        """处理文件上传"""
        path = urllib.parse.unquote(self.path.lstrip("/"))
        if not path:
            self.send_error(400, "Missing file path")
            return

        filepath = os.path.join(ROOT_DIR, path)
        # 防止路径穿越
        realpath = os.path.realpath(filepath)
        if not realpath.startswith(os.path.realpath(ROOT_DIR) + os.sep) and realpath != os.path.realpath(ROOT_DIR):
            self.send_error(403, "Access denied")
            return

        # 自动创建父目录
        parent = os.path.dirname(filepath)
        os.makedirs(parent, exist_ok=True)

        content_length = int(self.headers.get("Content-Length", 0))
        data = self.rfile.read(content_length)

        with open(filepath, "wb") as f:
            f.write(data)

        self.send_response(201)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(f"OK: {path} ({len(data)} bytes)\n".encode())

    def do_GET(self):
        """处理文件下载和目录浏览"""
        path = urllib.parse.unquote(self.path.split("?", 1)[0].lstrip("/"))
        filepath = os.path.join(ROOT_DIR, path)

        # 防止路径穿越
        realpath = os.path.realpath(filepath)
        if not realpath.startswith(os.path.realpath(ROOT_DIR) + os.sep) and realpath != os.path.realpath(ROOT_DIR):
            self.send_error(403, "Access denied")
            return

        if os.path.isdir(filepath):
            self._list_directory(filepath, path)
        elif os.path.isfile(filepath):
            self._download_file(filepath)
        else:
            self.send_error(404, "Not found")

    def _download_file(self, filepath):
        """下载文件"""
        filename = os.path.basename(filepath)
        file_size = os.path.getsize(filepath)

        self.send_response(200)
        self.send_header("Content-Type", "application/octet-stream")
        self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
        self.send_header("Content-Length", str(file_size))
        self.end_headers()

        with open(filepath, "rb") as f:
            self.wfile.write(f.read())

    def _list_directory(self, dirpath, relpath):
        """生成目录文件列表 HTML"""
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()

        items = os.listdir(dirpath)
        items.sort()

        body = ['<html><head><meta charset="utf-8"><title>Index of /</title>']
        body.append('<style>body{font-family:monospace;padding:20px;max-width:800px;margin:0 auto}')
        body.append('a{text-decoration:none;color:#0366d6}a:hover{text-decoration:underline}')
        body.append('tr:hover{background:#f6f8fa}td{padding:6px 12px}</style></head>')
        body.append(f'<body><h1>Index of /{html.escape(relpath)}</h1><hr>')

        if relpath:
            parent = "/" + os.path.dirname(relpath).replace("\\", "/")
            if parent == "/" and relpath:
                parent = "/"
            body.append(f'<p><a href="{html.escape(parent)}">..</a> (parent)</p>')

        body.append('<table>')
        body.append('<tr><th>Name</th><th>Size</th></tr>')
        for name in items:
            full = os.path.join(dirpath, name)
            href = "/" + os.path.join(relpath, name).replace("\\", "/")
            if os.path.isdir(full):
                body.append(f'<tr><td><a href="{html.escape(href)}/">📁 {html.escape(name)}/</a></td><td>-</td></tr>')
            else:
                size = os.path.getsize(full)
                body.append(f'<tr><td><a href="{html.escape(href)}">📄 {html.escape(name)}</a></td><td>{size:,}</td></tr>')

        body.append('</table><hr></body></html>')
        self.wfile.write("\n".join(body).encode())

    def log_message(self, format, *args):
        """日志格式"""
        print(f"[{self.log_date_time_string()}] {args[0]}")


# 监听地址和端口
address = ("0.0.0.0", 8088)

server = http.server.ThreadingHTTPServer(address, HTTPFileHandler)

print("匿名 HTTP 文件服务器已启动")
print(f"共享目录: {os.path.abspath(ROOT_DIR)}")
print("端口: 8088")
print("")
print("用法示例:")
print(f"  上传: curl -T file.txt http://127.0.0.1:8088/file.txt")
print(f"  下载: curl -O http://127.0.0.1:8088/file.txt")
print(f"  浏览: curl http://127.0.0.1:8088/")

server.serve_forever()

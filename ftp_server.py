from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import os

FTP_ROOT = "/ftp"

os.makedirs(FTP_ROOT, exist_ok=True)

authorizer = DummyAuthorizer()

# 匿名用户
authorizer.add_anonymous(
    FTP_ROOT,
    perm="elradfmwMT"
)

handler = FTPHandler
handler.authorizer = authorizer

# 被动模式端口
handler.passive_ports = range(30000, 30010)

# Docker/NAT环境必须配置
handler.masquerade_address = os.environ.get("PUBLIC_IP")

address = ("0.0.0.0", 21)

server = FTPServer(address, handler)

print("Anonymous FTP server started")
print(f"FTP ROOT: {FTP_ROOT}")

server.serve_forever()

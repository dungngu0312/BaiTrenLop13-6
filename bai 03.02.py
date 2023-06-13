import socket
import threading
from queue import Queue

# Một hàng đợi để lưu trữ các client đang kết nối
client_queue = Queue()

def handle_client(client_socket):
    # Chờ đến khi có đủ 2 client kết nối
    client_queue.put(client_socket)
    if client_queue.qsize() == 2:
        client1 = client_queue.get()
        client2 = client_queue.get()
        start_chat(client1, client2)

def start_chat(client1, client2):
    while True:
        # Nhận tin nhắn từ client1
        message = client1.recv(1024).decode().strip()
        if not message:
            break
        # Gửi tin nhắn từ client1 cho client2
        client2.send(message.encode())

        # Nhận tin nhắn từ client2
        message = client2.recv(1024).decode().strip()
        if not message:
            break
        # Gửi tin nhắn từ client2 cho client1
        client1.send(message.encode())

    # Đóng kết nối khi một client ngắt kết nối
    client1.close()
    client2.close()

def start_server(host, port):
    # Tạo socket server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Server is listening on {host}:{port}")

    while True:
        # Chấp nhận kết nối từ client
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr[0]}:{addr[1]}")

        # Tạo một luồng mới để xử lý client
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    host = "127.0.0.1"  # Địa chỉ IP của máy chạy server
    port = 1234  # Cổng lắng nghe

    start_server(host, port)

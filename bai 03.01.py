import os
import socket
import multiprocessing

# Đường dẫn thư mục chứa các file
FILES_DIRECTORY = "/path/to/files/directory"

def send_file_list(client_socket):
    file_list = os.listdir(FILES_DIRECTORY)
    if len(file_list) > 0:
        file_count = len(file_list)
        file_names = "\r\n".join(file_list)
        response = f"OK {file_count}\r\n{file_names}\r\n\r\n"
        client_socket.send(response.encode())
    else:
        response = "ERROR No files to download \r\n"
        client_socket.send(response.encode())
        client_socket.close()

def send_file(client_socket, file_name):
    file_path = os.path.join(FILES_DIRECTORY, file_name)
    if os.path.exists(file_path):
        file_size = os.path.getsize(file_path)

        # Gửi thông báo OK và kích thước file cho client
        response = f"OK {file_size}\r\n"
        client_socket.send(response.encode())

        # Gửi nội dung file cho client
        with open(file_path, "rb") as file:
            data = file.read(1024)
            while data:
                client_socket.send(data)
                data = file.read(1024)

        client_socket.close()
    else:
        response = "ERROR File does not exist \r\n"
        client_socket.send(response.encode())
        handle_client(client_socket)  # Yêu cầu client gửi lại tên file

def handle_client(client_socket):
    send_file_list(client_socket)

    # Nhận tên file từ client
    file_name = client_socket.recv(1024).decode().strip()

    # Kiểm tra và gửi file cho client
    send_file(client_socket, file_name)

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

        # Sử dụng đa tiến trình để xử lý nhiều client cùng lúc
        process = multiprocessing.Process(target=handle_client, args=(client_socket,))
        process.start()

if __name__ == "__main__":
    host = "127.0.0.1"  # Địa chỉ IP của máy chạy server
    port = 1234  # Cổng lắng nghe

    start_server(host, port)

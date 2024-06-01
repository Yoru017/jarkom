import socket
import sys

def get_index(server_ip, server_port):
    # Buat socket untuk menghubungkan ke server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Hubungkan ke server menggunakan alamat IP dan port
        client_socket.connect((server_ip, server_port))
        
        # Kirim permintaan HTTP GET ke server untuk mengambil file index.html
        request = "GET / HTTP/1.1\r\nHost: {}\r\n\r\n".format(server_ip)
        client_socket.sendall(request.encode())
        
        # Terima respons dari server
        response = client_socket.recv(4096).decode()
        
        # Cetak respons dari server
        print(response)
    except ConnectionRefusedError:
        print("Koneksi ditolak. Pastikan server berjalan dan alamat IP serta port benar.")
    except TimeoutError:
        print("Koneksi waktu habis. Pastikan server berjalan dan alamat IP serta port benar.")
    finally:
        # Tutup socket
        client_socket.close()

if __name__ == "__main__":
    # Pastikan argumen command line diberikan
    if len(sys.argv) != 3:
        print("Usage: python client.py <server_ip> <server_port>")
    else:
        server_ip = sys.argv[1]
        server_port = int(sys.argv[2])

        get_index(server_ip, server_port)

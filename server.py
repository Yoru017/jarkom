from socket import *
import threading

# Definisikan port dan alamat server
PORT = 80
SERVER = gethostbyname(gethostname())
ADDR = (SERVER, PORT)

# Buat objek socket menggunakan IPv4 dan TCP
server = socket(AF_INET, SOCK_STREAM)
server.bind(ADDR)

def ngambil(msg):
    # Fungsi ini memparsing permintaan HTTP dan mengambil konten file yang diminta

    # Pisahkan permintaan HTTP menjadi header
    headers = msg.split('\n')
    # Ekstrak nama file dari baris pertama permintaan
    filename = headers[0].split()[1]

    # Set direktori root untuk melayani index.html jika tidak ada file khusus yang diminta
    if filename == '/':
        filename = '/index.html'

    try:
        # Coba buka file yang diminta dan baca isinya
        with open(f".{filename}", "r") as file:
            content = file.read()
        # Jika file ditemukan, siapkan respons HTTP yang berhasil
        response = "HTTP/1.1 200 OK\n\n" + content
    except FileNotFoundError:
        # Jika file tidak ditemukan, siapkan respons 404 Not Found
        response = "HTTP/1.1 404 Not Found\n\nFile Not Found!"

    return response

def handle_client(connectionSocket, adr):
    # Fungsi ini menangani koneksi klien

    print(f"[NEW CONNECTION] {adr} connected!")
    connected = True
    while connected:
        # Terima pesan dari klien
        msg = connectionSocket.recv(1024).decode()
        if msg:
            # Dapatkan konten file yang diminta
            content = ngambil(msg)
            # Kirim konten kembali ke klien
            connectionSocket.sendall(content.encode())
            # Tutup koneksi setelah mengirim respons
            connected = False
    connectionSocket.close()

def start():
    # Fungsi ini memulai server dan mendengarkan koneksi masuk

    server.listen()
    print(f"Server listening...")
    print(f"Request : http://{SERVER}/index.html")
    while True:
        # Terima koneksi baru
        connectionSocket, adr = server.accept()
        # Buat thread baru untuk menangani koneksi klien
        thread = threading.Thread(target=handle_client, args=(connectionSocket, adr))
        thread.start()
        # Cetak jumlah koneksi aktif
        print(f"[SUCCES] koneksi sedang aktif")

# Cetak pesan yang menunjukkan bahwa server sedang dimulai
print("[Start] Server dimulai...")
# Mulai server
start()

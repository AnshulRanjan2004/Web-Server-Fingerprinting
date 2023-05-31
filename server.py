import socket
import requests
from urllib.parse import urlparse
import threading

HOST = "192.168.61.2"
PORT = 65432

def handle_request(conn, addr):
    with conn:
        data = conn.recv(1024)
        if not data:
            return
        url = data.decode()

        result = ""
        try:
            response = requests.head(url)
        except requests.exceptions.RequestException:
            result += "<strong>" + "Invalid URL or Server is down </strong>" + "<br>"
            conn.sendall(result.encode())
            return
        
        response.raise_for_status()
        if response.status_code >= 200 and response.status_code < 400:
                result += "<strong>" + "Valid URL and Server is up with status code " + str(response.status_code) + "</strong>" + "<br> <br>"
        else:
                result += "<strong>"+ "Valid URL but Server is down with status code " + str(response.status_code) + "</strong>" + "<br> <br>"
        domain_name = urlparse(url).netloc
        domain_parts = domain_name.split(".")
        server = domain_parts[-2] + "." + domain_parts[-1]
        
        req = requests.get('http://www.' + server)

        print(req.headers)

        some_headers = ['Server', 'Date', 'Via', 'Cache-Control','Content-Encoding','ETag','X-XSS-Protection']
        for header in some_headers:
            try:
                result += "<strong>" + header + "</strong> : " + req.headers[header] + "<br>"
            except:
                result += "<strong>" + header + "</strong> : Not found<br>"

        try:
            result += "<br><strong>Probable Server Type</strong><br>"
            data = list(req.headers)
            for i in range(len(data)):
                if(data[i]=='Date' or data[i]=='date'):
                    d=i
                if(data[i]=='Server' or data[i]=='server'):
                    s=i

            if(d>s):
                result += "Might be Apache<br><br>"
            else:
                result += "Might be IIS/Netscape<br><br>"
        except:
            result += "Could not find probable server type<br>"

        conn.sendall(result.encode())

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f'Server listening on {HOST}:{PORT}...')

        while True:
            conn, addr = s.accept()
            print(f'Connected by {addr}')
            thread = threading.Thread(target=handle_request, args=(conn, addr))
            thread.start()

if __name__ == '__main__':
    start_server()

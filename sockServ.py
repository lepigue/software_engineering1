import socket

s = socket.socket()
host = 'localhost'
port = 8005

s.bind((host, port))

s.listen(5)

while True:
    c, addr = s.accept()
    print('got connection from address: ', addr)
    data = c.recv(1024)
    nums = data.decode('utf8')
    nums = eval(str(nums))*100
    nums = str(nums)
    print(f"The answer being sent to the client is {nums} %")
    nums = nums.encode('utf8')
    c.send(nums)
    c.close
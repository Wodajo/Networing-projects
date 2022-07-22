### ip, default gateway ip, netmask
`show ip`
```
NAME        : PC1[1]
IP/MASK     : 0.0.0.0/0
GATEWAY     : 0.0.0.0
DNS         :
MAC         : 00:50:79:66:68:00
LPORT       : 10002
RHOST:PORT  : 127.0.0.1:10003
MTU:        : 1500
```
there is a lot to cover:D

`PC1> ip 192.168.10.10/24 192.168.10.1`
```
Checking for duplicate address...
PC1 : 192.168.10.10 255.255.255.0 gateway 192.168.10.1
```
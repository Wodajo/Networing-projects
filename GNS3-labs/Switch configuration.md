`user EXEC mode` at start (like in router)

It would be easier to modify `startup-config` files of these devices, but for now it's a nice practice

```
IOU2>en
Password:
IOU2#
*Dec  7 12:32:56.222: %CDP-4-DUPLEX_MISMATCH: duplex mismatch discovered on Ethernet0/3 (not full duplex), with R1 FastEthernet0/0 (full duplex).
IOU2#conf t
Enter configuration commands, one per line.  End with CNTL/Z.
IOU2(config)#hostname SW1
SW1(config)#do show int status

Port      Name               Status       Vlan       Duplex  Speed Type
Et0/0                        connected    1            auto   auto unknown
Et0/1                        connected    1            auto   auto unknown
Et0/2                        connected    1            auto   auto unknown
Et0/3                        connected    1            auto   auto unknown
Et1/0                        connected    1            auto   auto unknown
Et1/1                        connected    1            auto   auto unknown
Et1/2                        connected    1            auto   auto unknown
Et1/3                        connected    1            auto   auto unknown
```

`do show int status` - NOT working on the routers
	Name - description
	Status - connected / notconnect  (switch default startup-config make all of them seem connected).
	Switch interfaces are NOT shutdown on default


```
SW1(config)#int et0/0
SW1(config-if)#duplex full
SW1(config-if)#desc ## to SW2 ##
```

shutdown unused interfaces:
```
SW1(config-if)#int range et1/0 - 3, et2/0 - 3, et3/0 - 3
SW1(config-if-range)#shutdown
SW1(config-if-range)#desc ## not used ##
SW1(config-if-range)#do show int status

Port      Name               Status       Vlan       Duplex  Speed Type
Et0/0     ## to SW2 ##       connected    1            auto   auto unknown
Et0/1     ## to end hosts ## connected    1            auto   auto unknown
Et0/2     ## to end hosts ## connected    1            auto   auto unknown
Et0/3     ## to R1 ##        connected    1            auto   auto unknown
Et1/0     ## not used ##     disabled     1            auto   auto unknown
Et1/1     ## not used ##     disabled     1            auto   auto unknown
Et1/2     ## not used ##     disabled     1            auto   auto unknown
Et1/3     ## not used ##     disabled     1            auto   auto unknown
Et2/0     ## not used ##     disabled     1            auto   auto unknown
Et2/1     ## not used ##     disabled     1            auto   auto unknown
```
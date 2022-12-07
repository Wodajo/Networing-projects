default `startup-config` has  
```
privilege level 15
```
That's why router automatically start in `privileged EXEC mode`

#### user EXEC mode at start
by default `startup-config` router start with `privileged EXEC mode`. We want `user EXEC mode`

`configure terminal` to enter `global config mode`
`line console 0` - direct changes in `running-config`
`no privilege level 15`
`exit` to privileged EXEC mode
`write` to write `running config` into `startup-config` (or `write memory` or `copy running-config startup-config`)
`exit` to user EXEC mode

#### change hostname
in `global config mode` :
`hostname Router1` change name to `Router1`

#### make a password
1. no encryption
in `global config mode` :
`enable password CCNA` to make a "CCNA" password
(it is written to `running-config`)
It works, but it can be viewed in cleartext in configs

to view/write configs you have to be in `privileged EXEC mode` or prepend command with `do` :
`do write` to write to `startup-conif`
`do show startup-config` to see

2. encrypt password with `Vigenere cipher` (type 7)
   (which can be easly reversed - only secure form someone looing from behind)
in `global config mode` :
`service password-encryption`
`do write`

3. encrypt with `MD5` (type 5)
in `global config mode` (obviously):
`enable secret CCNA` make a "CCNA" password and store it's `MD5` hash

If both `enable secret` and `enable password` are configured - only `enable secret` can be used

#### configure ip
`show ip interface brief` - to see what we have. output explanaition in "intro to cli" note
`interface FastEthernet0/0` - configure that interface
`ip address 10.255.255.254 255.0.0.0` - assign IP address with that subnet mask
`no shutdown` - router interfaces are shutdown-disabled bydefault. BUT not switches
`do show ip interface brief` - check how are things now. 
```
R1>show ip interface brief
Interface                  IP-Address      OK? Method Status                Protocol
FastEthernet0/0            unassigned      YES unset  administratively down down
FastEthernet1/0            unassigned      YES unset  administratively down down
R1>en
Password:
R1#conf t
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#interface FastEthernet 0/0
R1(config-if)#ip address 10.255.255.254 ?
  A.B.C.D  IP subnet mask

R1(config-if)#ip address 10.255.255.254 255.0.0.0
R1(config-if)#no shutdown
R1(config-if)#
*Sep 26 18:37:14.203: %LINK-3-UPDOWN: Interface FastEthernet0/0, changed state to up      ---> Layer 1 status change
*Sep 26 18:37:15.203: %LINEPROTO-5-UPDOWN: Line protocol on Interface FastEthernet0/0, changed state to up   ---> Layer 2 status change
R1(config-if)#do show ip interface brief
Interface                  IP-Address      OK? Method Status                Protocol
FastEthernet0/0            10.255.255.254  YES manual up                    up
FastEthernet1/0            unassigned      YES unset  administratively down down
```

`speed 100` since that's Fast Ethernet (WHAT WITH `speed auto` option?)
`duplex full` - it's attached to switches. half-duplex is only necessairy if connected to a hub

`interface range fa1/0 - 1` 
`description SOMETHING` - (e.g. ## not in use ##)

to check changes:
`show interfaces description` - interface, status (L1), protocol(L2), description
`do show interfaces fa0/0` -  details about interface
`do show run`
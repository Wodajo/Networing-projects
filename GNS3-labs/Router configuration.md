default `startup-config` has  
```
priviledge level 15
```
That's why router automatically start in `privileged EXEC mode`

#### user EXEC mode at start
by default `startup-config` router start with `privileged EXEC mode`. We want `user EXEC mode`

`configure terminal` to enter `global config mode`
`line console 0` - direct changes in `running-config`
`no privilege level 15`
`exit` to privileged EXEC mdoe
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

#### 
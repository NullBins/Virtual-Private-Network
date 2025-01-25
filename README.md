<div align="center">
  <h1>[ 🔐가상사설망🛡Virtual Private Network ]</h1>
</div>

###### 📚 Repository for records of how to setup VPN [ *Written by NullBins* ]

## ❓❓❓EASY❓❓❓ VPN for Cisco Router
#### { 🌐 (LAN: 192.168.1.0/24) [R1/L2TP-VPN-Server] (.1) <- (1.1.12.0/30) -> (.2) [R2] (.2) <- (1.1.23.0) -> (.1) [R3/NAT] (LAN: 172.16.1.0/24) [PC1/DHCP] 🌐 }

<br/>

- *1) R1 Router EVS(Easy VPN Server) Configuration*

### [R1]
- (AAA Server)
```cmd
R1(config)#aaa new-model
R1(config)#aaa authentication login default line none
R1(config)#aaa authentication login EASYVPN-AAA local
R1(config)#aaa authorization network EASYVPN-AAA local
R1(config)#username easyuser password P@$$w0rd
R1(config)#service password-encryption
```
- (IKE 1 Phase)
```cmd
R1(config)#crypto iaskmp fragmentation
R1(config)#crypto iaskmp policy 10
R1(config-iaskmp)#encryption aes 256
R1(config-iaskmp)#authentication pre-share
R1(config-iaskmp)#group 5
R1(config-iaskmp)#exit
```
- (EVC IP Address Pool)
```cmd
R1(config)#ip local pool EVC-POOL 192.168.1.101 192.168.1.149
```
- (Security Traffic)
```cmd
R1(config)#ip access-list extended EASYVPN-TRAFFIC
R1(config-ext-nacl)#permit ip 192.168.1.0 0.0.0.255 any
R1(config-ext-nacl)#exit
```
- (EasyVPN Client Group)
```cmd
R1(config)#crypto iaskmp client configuration group EASYVPN-GROUP
R1(config-isakmp-group)#acl EASYVPN-TRAFFIC
R1(config-isakmp-group)#key P@$$w0rd
R1(config-isakmp-group)#dns 192.168.1.1
R1(config-isakmp-group)#domain vdi.local
R1(config-isakmp-group)#pool EVC-POOL
R1(config-isakmp-group)#banner *
! ! ! AUTHORIZED ACCESS ONLY ! ! !
*
R1(config-isakmp-group)#exit
```
- (IKE 2 Phase)
```cmd
R1(config)#crypto ipsec transform-set EASYVPN-PHASE2 esp-aes 256 esp-sha-hmac
R1(cfg-crypto-trans)#exit
```
- (Dynamic Crypto Map)
```cmd
R1(config)#crypto dynamic-map EASYVPN-DMAP 10
R1(config-crypto-map)#set transform-set EASYVPN-PHASE2
R1(config-crypto-map)#reverse-route
R1(config-crypto-map)#exit
```
- (Dynamic Crypto Map)
```cmd
R1(config)#crypto dynamic-map EASYVPN-DMAP 10
R1(config-crypto-map)#set transform-set EASYVPN-PHASE2
R1(config-crypto-map)#reverse-route
R1(config-crypto-map)#exit
```
- (Static Crypto Map)
```cmd
R1(config)#crypto map EASYVPN client authentication list EASYVPN-AAA
R1(config)#crypto map EASYVPN client configuration address respond
R1(config)#crypto map EASYVPN isakmp authorization list EASYVPN-AAA
R1(config)#crypto map EASYVPN 10 ipsec-isakmp dynamic EASYVPN-DMAP
```
- (Enable Interface for EasyVPN)
```cmd
R1(config)#int gig 1
R1(config-if)#crypto map EASYVPN
```

<br/>

- *2) PC1 Client EVC(Easy VPN Client) Settings*
 
### [PC1]
- 1) Install Cisco VPN Program
  2) Enable to Cisco VPN Interface
  3) Connection Entry [Host: 1.1.12.1, Name: EASYVPN-GROUP, Password: P@$$w0rd]
  4) Connect to Entry [Username: easyuser, Password: P@$$w0rd]
  5) Banner Info (! ! ! AUTHORIZED ACCESS ONLY ! ! !)

## GRE-over-IPsec VPN (Cisco Router)
- IPsec IKE phase 1-2 & Cryto-Map profile
```cmd
(config)#crypto isakmp policy 10
(config-isakmp)#encryption aes
(config-isakmp)#authentication pre-share
(config-isakmp)#exit
(config)#crypto isakmp key P@$$w0rd address 1.1.20.1
(config)#crypto isakmp keepalive 10
```
```cmd
(config)#ip access-list extended VPN-TARGET
(config-ext-nacl)#permit gre host 1.1.10.1 1.1.20.1
(config-ext-nacl)#exit
```
```cmd
(config)#crypto ipsec transform-set PHASE2-POLICY esp-aes esp-md5-hmac
(cfg-crypto-trans)#exit
```
```cmd
(config)#crypto map GRE-IPSEC-VPN 10 ipsec-isakmp
(config-crypto-map)#match address VPN-TARGET
(config-crypto-map)#set peer 1.1.20.1
(config-crypto-map)#set transform-set PHASE2-POLICY
(config-crypto-map)#exit
```

<div align="center">
  <h1>[ 📲가상사설망🛡Virtual Private Network ]</h1>
</div>
Repository for records of how to setup VPN

## GRE-over-IPsec VPN (Cisco Router)
- IPsec IKE phase 1-2 & Cryto-Map profile
```cmd
(config)#crypto isakmp policy 10
(config-isakmp)#encryption aes
(config-isakmp)#authentication pre-share
(config-isakmp)#exit
(config)#crypto isakmp key admin12!@# address 1.1.20.1
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

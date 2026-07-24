# 交换机互联链路聚合模板
interface Eth-Trunk 1
 mode lacp-static
 port trunk allow-pass vlan all

interface GigabitEthernet 0/0/23
 eth-trunk 1
interface GigabitEthernet 0/0/24
 eth-trunk 1
#!/bin/bash
PRIVATE_IP=$(curl -s http://169.254.169.254/latest/meta-data/local-ipv4)

curl -O https://raw.githubusercontent.com/angristan/openvpn-install/master/openvpn-install.sh
chmod +x openvpn-install.sh
AUTO_INSTALL=y ./openvpn-install.sh <<EOF
yes
${PRIVATE_IP}
1
1194
1
1
vpnclient
EOF
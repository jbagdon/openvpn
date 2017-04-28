from fabric.api import *
from fabric.contrib.files import sed

def deploy_openvpn():
    sudo('apt-get update')
    sudo('apt-get -y install openvpn easy-rsa')
    run('make-cadir ~/openvpn-ca')
    put('vars', '~/openvpn-ca/vars', mode=0644)
    with cd('~/openvpn-ca'):
        with prefix('source vars'):
            run('./clean-all')
            run('./build-ca')
            run('./build-key-server server')
            run('./build-dh')
            run('openvpn --genkey --secret keys/ta.key')
            run('./build-key client1')
    with cd('~/openvpn-ca/keys'):
        sudo('cp ca.crt ca.key server.crt server.key ta.key dh2048.pem /etc/openvpn')
    put('server.conf', '/etc/openvpn/server.conf', mode=0644, use_sudo=True)
    sed('/etc/sysctl.conf', '#net.ipv4.ip_forward=1', 'net.ipv4.ip_forward=1', use_sudo=True)
    sudo('sysctl -p')
    put('before.rules', '/etc/ufw/before.rules', mode=0640, use_sudo=True)
    sed('/etc/default/ufw', 'DEFAULT_FORWARD_POLICY=.*', 'DEFAULT_FORWARD_POLICY="ACCEPT"', use_sudo=True)
    sudo('ufw allow 1194/udp')
    sudo('ufw allow OpenSSH')
    sudo('ufw disable')
    sudo('ufw enable')
    sudo('systemctl enable openvpn@server')
    sudo('systemctl start openvpn@server')
    run('mkdir -p ~/client-configs/files')
    run('chmod 700 ~/client-configs/files')
    put('base.conf', '~/client-configs', mode=0644)
    put('make_config.sh','~/client-configs', mode=0700)
    with cd('~/client-configs'):
        run('./make_config.sh client1')

# openvpn
Python Fabric script to install openvpn

This script could be used in your own infrastructure or in the cloud to make a private connection. You will first have to change a couple of settings. In the vars file, there is a section that sets the settings for the certificate, change these to match your name and email if you want. The other item that is rather important is in the base.conf file you need to change the server IP. This is the file that the openvpn config file is generated from and you'll want to connect to the correct IP.

Then just run the Fabric script:
fab -H 172.16.0.4 -u root -i ~/.ssh/id_rsa deploy_openvpn

The -H option is the IP address of the destination server that you are deploying to.
The -u is the username that you are logging in with.
The -i is the ssh key that you are using to login with.
And, the deploy_openvpn is the name of the function within the Fabric script that you are deploying.

Don't go too quickly and read the prompts. There will be a few critical prompts to answer yes to or it will not work.

After it has ran you should end up with a client config file located in your user directory at ~/client-configs/files/client1.ovpn

Have fun!

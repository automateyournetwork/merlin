# Merlin on a Cisco DevNet Sandbox

You can now run Merlin against a Nexus 9000 in the Cisco DevNet Sandbox.  We have included a custom script and pre-configured testbed file for this purpose.

>To get started, sign up for a Cisco DevNet account at: https://devnetsandbox.cisco.com/RM/Topology

>Once you are signed in, search for "Nexus" in the search dialog at the top left of the screen.

![DevNet Search](images/03_devnetsb-01.png)

>Select one of the reserved instances - We recommend using the instance running the latest version of NXOS.

![DevNet Reserve](images/03_devnetsb-02.png)

>Click "Reserve" after reviewing the reservation details.

![DevNet Reserve](images/03_devnetsb-03.png)

You will receive an email from Cisco confirming the reservation along with links to download the Cisco AnyConnect VPN Client and instructions for its installation.

**Cisco AnyConnect VPN Client:**

https://developer.cisco.com/site/sandbox/anyconnect/

**Installation guide for Cisco AnyConnect VPN Client:**

https://devnetsandbox.cisco.com/Docs/VPN_Access/AnyConnect_Installation_Guide.pdf

>Click the "VPN Access" tab in the DevNet console and review the information in it.

![DevNet VPN Access](images/01_devnetsb-04.png)

**Note:** If this is your first time using the Cisco DevNet Sandbox, make sure to review the information in each of the tabs.

In about 15 to 20 minutes, you should receive another email from Cisco with the VPN credentials for your sandbox, including:

* VPN address and port for the connection
* VPN username
* VPN password

>Connect to the DevNet Sandbox VPN using the Cisco AnyConnect VPN Client

![AnyConnect](images/01_devnetsb-05.png)

Once connected, you will have direct network access to the Nexus 9000 in DevNet.

The "NXOS on Nexus 9k" tab in the DevNet console will show you the details you need to connect to the device, however we have already added this information to the `testbed/testbed_DevNet_Nexus9k_Sandbox.yaml` file.

You can confirm it to be sure.

![AnyConnect](images/03_devnetsb-06.png)

```yaml
devices:
    sbx-n9kv:
      alias: 'DevNet_Sandbox_Nexus9k'
      type: Nexus 9000
      os: 'nxos'
      credentials:
        default:
          username: admin
          password: Cisco123
      connections:        
        cli:
          protocol: ssh
          ip: 10.10.20.58
          port: 22
          arguments:
            connection_timeout: 360
```

You're now ready to run Merlin against the DevNet Nexus 9000!

* To transform at least 16 common commands run the following pyATS job:

```console
pyats run job DevNet_Sandbox_Nexus9k_merlin_job.py --testbed-file testbed/testbed_DevNet_Nexus9k_Sandbox.yaml
```

[Back to the main project](https://github.com/automateyournetwork/merlin)
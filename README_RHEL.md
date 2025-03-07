The following steps replace steps 3-5 in the main README in order to use Red Hat Enterprise Linux and podman.

## Step 3. Create your Red Hat Enterprise Linux 9.3 instance of Linux VM

Note: For details or troubleshooting refer the official documentation from IBM LinuxONE Community Cloud  [here](https://ibm.biz/BdPcL8)

1. Deploying LinuxONE virtual server.
    a. Go to the **Home page**, **Service Catalog** section and **Virtual Servers** service.
    b. Click **Manage Instances**.

     ![alt text](images/manage-instance.png "Manange instances")

    c. Click **Create**.
    
2. Provide instance specifications
    a. **Instance Name**, without any spaces or special characters.
    b. Desired **Linux image** as **RHEL 9.3**.
    c. **SSH key** to use.
    d. Verify that all the information is correct and click **Create**.

3. Confirm your instance is ACTIVE. 

    - Newly deployed instance will go through several phases until becoming ACTIVE
 
## Step 4. Open a secure shell connection and install podman

1. Open a terminal on your local computer

    - On Mac OS X or Linux use Terminal.
    - On Windows use PuTTY.
    Note: Instructions on how to use ssh terminal or PuTTY can be found here [here](https://github.com/linuxone-community-cloud/technical-resources/blob/master/faststart/PUTTY_Set_up.pdf)

2. Ensure that you have the SSH private key used to deploy the server. 
    
3. Use SSH to access the Linux guest.
    ```ssh -i <your_key>.pem linux1@148.100.xx.xx```

4. Install podman: ```sudo dnf -y install podman```

6. Start podman service
    ```sudo systemctl start podman```

## Step 5. Start Jupyter Lab container on the port 38888
In this section, you will use the Jupyter Lab tool that is installed in container along with popular ML packages. This tool allows you to write and submit Python code, and view the output within a web GUI.

1. Pull down the latest container image
    ```podman pull registry.linuxone.cloud.marist.edu/l1cc/jupyterlab-image-s390x:latest```
2. Start the Jupyer Lab container on port 38888
```
    mkdir shared && chmod a+w shared

    podman run -p 38888:8888 --name notebook -v /home/linux1/shared:/home/jovyan/shared:z \
    -d registry.linuxone.cloud.marist.edu/l1cc/jupyterlab-image-s390x:latest \
    jupyter lab --ServerApp.token='Your_Token'
``` 

3. Open TCP port 38888 on the firewall: ```sudo iptables -I INPUT -p tcp --dport 38888 -j ACCEPT```

4. (Optional) To make the above firewall changes persistent across reboots, run the following: ```sudo bash -c "iptables-save > /etc/sysconfig/iptables.save"```


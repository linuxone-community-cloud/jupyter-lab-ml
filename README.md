# Running AI/ML in Jupyter Lab on IBM LinuxONE/zSystems servers
## Overview
The following guidelines can be used to explore Machine Learning applications using Jupyter Lab and Python ML libraries for IBM LinuxONE/zSystems. IBM LinuxONE/zSystems servers are designed to be more powerful than x86, through a combination of processor architecture, clock speed, cache, optimization, and I/O offloading. IBM z16 generation comes with Telum central processor with a new dedicated on-chip accelerator for AI inference. This design enables real time AI/ML processing embedded directly in transactional workloads. Jupyter Lab is packaged as a container that includes popular ML libraries such as Keras, Tensorflow, PyTorch ans SciKit-Learn. It also comes with several ML examples and sample data to train and validate the models.   

   1. The first example demonstrates a client retention analysis using SciKit-Learn.
   2. The second example demonstrates MNIST handwritten digits recogniton using Keras and Tensorflow.
   3. Both examples demonstrate exporting of the trained model to portable ONNX format for inferencing in a sample production.

## Architecture
   ![alt text](images/jupyter-lab-ml-ibmz.png "Jupyter Lab ML on IBM zSystems")

## Steps

1. Register in LinuxONE Community Cloud
2. Log in to the Self Service Portal.
3. Create your Ubuntu 20.04 instance
4. Open a secure shell connection and install docker runtime
5. Start Jupyter Lab container on the port 38888
6. Open Jupyter Lab in the Browser using the public IP address of your instance
7. Run Demo notebooks 
8. Use case #1: Run a client retention analysis notebook.
9. Use case #2: Run a MNIST handwritten digits recogniton notebook.
10. Use case #3: Export the trained model to a portable ONNX format.

## Step 1. Sign up for an IBM LinuxONE Community Cloud account

Note: Refer the official documentation from IBM LinuxONE Community Cloud  [here](https://ibm.biz/BdPcL8)

1. If you have not done so already, go to [IBM LinuxONE Community Cloud](https://linuxone.cloud.marist.edu/) and register for a free trial account. 
2. Select **Register** link. 
3. Fill out and submit the registration form.
4. You will receive an email containing credentials to access the self-service portal. This is where you can request VM instance of Linux on IBM LinuxONE servers.
![alt text](images/l1cc-register.png "Registration form")


## Step 2. Log in to the Self Service Portal

1. Open a web browser and access the [IBM LinuxONE Community Cloud](https://linuxone.cloud.marist.edu/). 
   
    a. Enter your Portal User ID and Portal Password
    b. Click **'Sign In'**
       You will see the home page for the IBM LinuxONE Community Cloud self-service portal.  
       
2. For deploying LinuxONE virtual server the first time, you must set your ssh key for secure shell access.
    a. Select the **Virtual Servers** in the upper left corner of the page.

    b. Next click your **username** from the upper right corner of the Home page.

    c. Select **Manage SSH Key Pairs** and import your key for accessing the Linux VMs.

## Step 3. Create your Ubuntu 20.04 instance of Linux VM

1. Deploying LinuxONE virtual server.
    a. Go to the **Home page**, **Service Catalog** section and **Virtual Servers** service.
    b. Click **Manage Instances**.

     ![alt text](images/manage-instance.png "Manange instances")

    c. Click **Create**.
    
2. Provide instance specifications
    a. **Instance Name**, without any spaces or special characters.
    b. Desired **Linux image** as **Ubuntu 20.04**.
    c. **SSH key** to use.
    d. Verify that all the information is correct and click **Create**.

3. Confirm your instance is ACTIVE. 

    - Newly deployed instance will go through several phases until becoming ACTIVE
 
## Step 4. Open a secure shell connection and install docker runtime

1. Open a terminal on your local computer

    - On Mac OS X or Linux use Terminal.
    - On Windows use PuTTY.

2. Ensure that you have the SSH private key used to deploy the server. 
    
3. Use SSH to access the Linux guest.
    ```ssh -i <your_key>.pem linux1@148.100.xx.xx```

4. Download the latest docker installer script and run it
    ```curl -fsSL https://test.docker.com -o test-docker.sh && sudo sh test-docker.sh```
5. Add current user to the docker goup and grant permissions

    ```sudo usermod -aG docker $USER; newgrp docker```
6. Start docker service and refresh bash session 
    ```sudo systemctl start docker```
    ```exec bash   # or exit and reconnect via ssh```

## Step 5. Start Jupyter Lab container on the port 38888
In this section, you will use the Jupyter Lab tool that is installed in container along with popular ML packages. This tool allows you to write and submit Python code, and view the output within a web GUI.

1. Login to the private container registry in IBM LinuxONE Community Cloud
    docker login -u l1cc registry.linuxone.cloud.marist.edu
    (Refer event information for password)
    ```docker login -u l1cc registry.linuxone.cloud.marist.edu```
2. Pull down the latest container image
    ```docker pull registry.linuxone.cloud.marist.edu/jupyterlab-image-s390x:latest```
3. Start the Jupyer Lab container on port 38888
```
    docker run -p 38888:8888 --name notebook -v /home/linux1/jupyter:/home/jovyan/shared \
    -d registry.linuxone.cloud.marist.edu/jupyterlab-image-s390x:latest jupyter lab --ServerApp.token='Your_Tocken' 
``` 

## Step 6. Open Jupyter Lab in the Browser using the public IP address of your instance
    URL: http://148.100.X.X:38888
    The first page requires you to authenticate before getting to the main Jupyter Lab IDE. Tocken is the one you specified in the docker run command: Your_Tocken
## Step 7. Run Demo notebooks 
Jupyter Lab container comes with 2 demo notebooks and sample data. Once in the Jupyter Lab IDE, left side panel lists the notebooks and CSV data files. Click on each of them to open in the right side panel. 
## Step 8. Use case #1: Run a client retention analysis notebook.

This Demo notebook runs Random Forest ML on IBM LinuxONE accessing data from CSV files. The data in customer CSV consists of 6,001 rows of customer information.  The data in transaction CSV consists of 20,000 rows of transaction data. The data is transformed and joined in a Pandas DataFrame, which is used to perform exploratory analyses. A Random Forest algorithm is then used to predict customer churn.

1. Click **'ML_LinuxONE_Demo.ipynb'**

      ![alt text](images/notebook-ml-l1.png "ML_LinuxONE_Demo")

The environment is divided into input cells labeled with **‘In [#]:’**.  

2. Execute the Python code in the first cell.
    
    a. Click on the first **‘In [ ]:’**
    
    The left border will change to blue when a cell is in command mode.
    b. Click **Run** to execute the lines of Python code in the cell

3. Click and run the second cell **‘In [ ]:’**.

    If no error messages appear, the cell run was successful.

4.	Click and run the third cell **‘In [ ]:’** etc.

    Check the explanation of each Cell and The output from it.
    Continue stepping trhouth the notebook


## Step 9. Use case #2: Run a MNIST handwritten digits recogniton notebook.
This Demo notebook performs single digit recognition using MNIST dataset and neural network model in Tensorflow.  

1. Click **'MNIST_Tensorflow.ipynb'**

      ![alt text](images/notebook-ml-l2.png "MNIST_Tensorflow")

The environment is divided into input cells labeled with **‘In [#]:’**.  

2. Execute the Python code in the first cell.
    
    a. Click on the first **‘In [ ]:’**
    
    The left border will change to blue when a cell is in command mode.
    b. Click **Run** to execute the lines of Python code in the cell

3. Click and run the second cell **‘In [ ]:’**.

    If no error messages appear, the cell run was successful.

4.	Click and run the third cell **‘In [ ]:’** etc.

    Check the explanation of each Cell and The output from it.
    Continue stepping trhouth the notebook
## Step 10. Use case #3: Export the trained model to a portable ONNX format.
Both Demo notebooks contain steps to export the trained ML model into portable open format ONNX. sklearn-onnx and tf2onnz convert models in ONNX format which can be then used to compute predictions with another backend on a different platform. Such as training can be done on an x86 system and then inference on IBM LinuxONE. 

![alt text](images/model-to-onnx.png "Model export to ONNX")




The following steps replace steps 4-17 in the main README in order to use Red Hat Enterprise Linux and podman.

## Step 4. Open a secure shell connection and install podman

1. Open a terminal on your local computer

    - On Mac OS X or Linux use Terminal.
    - On Windows use PuTTY.
    Note: Instructions on how to use ssh terminal or PuTTY can be found here [here](https://github.com/linuxone-community-cloud/technical-resources/blob/master/faststart/PUTTY_Set_up.pdf)

2. Ensure that you have the SSH private key used to deploy the server. 
    
3. Use SSH to access the Linux guest.
    ```ssh linux1@148.100.xx.xx```

4. Install podman: ```sudo dnf -y install podman```

5. Start podman service
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


## Step 6. Open Jupyter Lab in the Browser using the public IP address of your instance
   ``` URL: http://148.100.X.X:38888```
    The first page requires you to authenticate before getting to the main Jupyter Lab IDE. Tocken is the one you specified in the podman run command: Your_Token

![alt text](images/jupyter_login.png "ML_Demo")

## Step 7. Run Demo notebooks 
Jupyter Lab container comes with 2 demo notebooks and sample data. Once in the Jupyter Lab IDE, left side panel lists the notebooks and CSV data files. Click on each of them to open in the right side panel. 


## Step 8. Use case #1: Run a notebook with LSTM model to detect fraudlent credit card transactions.
This Demo notebook performs a training and validation of a credit card fraud detection model in Keras/Tensorflow.  
 Refer **'Fraud_LSTM_Keras_TF.ipynb'** notebook and csv dataset included in the Jupyter Lab environment.   


## Step 9. Use case #2: Run a client retention analysis notebook.

This Demo notebook runs Random Forest ML on IBM LinuxONE accessing data from CSV files. The data in customer CSV consists of 6,001 rows of customer information.  The data in transaction CSV consists of 20,000 rows of transaction data. The data is transformed and joined in a Pandas DataFrame, which is used to perform exploratory analyses. A Random Forest algorithm is then used to predict customer churn.

1. Click **'Churn_Scikit_PyTorch.ipynb'**

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


## Step 10. Use case #3: Run a MNIST handwritten digits recogniton notebook.
This Demo notebook performs single digit recognition using MNIST dataset and neural network model in Tensorflow.  

1. Click **'Digit_Class_TensorFlow.ipynb'**

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

## Step 11. Use case #4: Export the trained model to a portable PMML or ONNX format.
Both Demo notebooks contain steps to export the trained ML model into portable open formats either PMML or ONNX. sklearn2pmml and tf2onnz convert models in portable format which can be then used to compute predictions with another backend on a different platform. Such as training can be done on an x86 system and then inference on IBM LinuxONE. 
![alt text](images/model-to-onnx.png "Model export to ONNX")

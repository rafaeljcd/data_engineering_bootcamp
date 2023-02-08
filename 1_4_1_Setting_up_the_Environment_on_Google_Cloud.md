- [Introduction](#introduction)
- [SSH key](#ssh-key)
    - [Documentation](#documentation)
    - [Instructions](#instructions)
- [Create Virtual Machine Instance](#create-virtual-machine-instance)
- [Connect to Virtual Machine Instance via SSH](#connect-to-virtual-machine-instance-via-ssh)
- [Set up SSH Config for VM Instance access](#set-up-ssh-config-for-vm-instance-access)
- [Configure VSCode to connect to the Virtual Machine Instance](#configure-vscode-to-connect-to-the-virtual-machine-instance)
    - [Remote SSH code 255 in windows](#remote-ssh-code-255-in-windows)
        - [Error](#error)
        - [Pre-requisite](#pre-requisite)
        - [Solution](#solution)
- [Set up the Virtual Machine Instance](#set-up-the-virtual-machine-instance)
- [Port Forwarding to local machine](#port-forwarding-to-local-machine)
    - [Port Forwarding Instructions](#port-forwarding-instructions)
    - [Testing on Local Machine](#testing-on-local-machine)
    - [Port Forwarding Jupyter Notebook](#port-forwarding-jupyter-notebook)
        - [Open the Jupyter Notebook Port](#open-the-jupyter-notebook-port)
        - [Jupyter Notebook Usage](#jupyter-notebook-usage)
- [Terraform on Virtual Machine](#terraform-on-virtual-machine)
    - [Install Terraform](#install-terraform)
    - [Transfer the GCP Service Account Key](#transfer-the-gcp-service-account-key)
        - [For Windows Transfer via WinSCP](#for-windows-transfer-via-winscp)
        - [For SFTP transfer via CLI](#for-sftp-transfer-via-cli)
    - [Perform Terraform](#perform-terraform)
        - [Login the gcloud service account in CLI](#login-the-gcloud-service-account-in-cli)
        - [Terraform commands](#terraform-commands)
- [Virtual Machine Actions](#virtual-machine-actions)
    - [Turn off virtual machine](#turn-off-virtual-machine)
    - [Turn on virtual machine](#turn-on-virtual-machine)
    - [Delete Virtual Machine](#delete-virtual-machine)
- [Page](#page)

---

## Introduction

To start with, we must enable the `Compute Engine API`

Go to https://console.cloud.google.com/marketplace/product/google/compute.googleapis.com and then click `enable`

![](https://i.imgur.com/ex44mof.png)

After enabling the Compute Engine, we can check the `Compute Engine` by clicking in the hamburger menu `Compute Engine`

![](https://i.imgur.com/ckytcQC.png)

As you can see here, there is currently no Virtual Machine created.

![](https://i.imgur.com/MNKuV1p.png)

So with this lesson, we are going to create Virtual Machine Instance, but we must generate ssh key first.

---

## SSH key

### Documentation

Following from this official documentation given by the
GCP https://cloud.google.com/compute/docs/connect/create-ssh-keys

### Instructions

1. We must first create an ssh directory, and then go into it.

   ```shell
   mkdir ~/.ssh/
   cd ~/.ssh/
   ```

2. Now we are going to generate the ssh key, this command is found in the documentation, and leave the password empty
   for now.

   Template command

    ```shell
    ssh-keygen -t rsa -f ~/.ssh/KEY_FILENAME -C USERNAME -b 2048
    ```

   ```shell
   ssh-keygen -t rsa -f ~/.ssh/gcp -C rafael -b 2048
   ```

   ![](https://i.imgur.com/1hXIFww.png)

   and we now create two keys, one is a private key and the other is the public key.

   ![](https://i.imgur.com/kn04U1n.png)

   We must ensure that we must not expose the private key to the public.

3. Now we are going to put the `public key` to our Google Cloud.

   In the `Compute Engine` scroll down on the left side until you found the `Metadata`

   ![](https://i.imgur.com/9gMQruv.png)

4. In the `Metadata`, Click the `SSH KEYS` tab and then click the `ADD SSH KEY`

   ![](https://i.imgur.com/TAbdk4x.png)

5. Now we are going to check our `public key` and copy it.

   ![](https://i.imgur.com/48lS2i3.png)

6. Paste the public key into the GCP and then hit `save`

   ![](https://i.imgur.com/qbQ0RqZ.png)

7. Now all Virtual Machine Instances can be used with the SSH key.

   ![](https://i.imgur.com/9QX8y1k.png)

---

## Create Virtual Machine Instance

1. In the `Compute Engine` > `VM Instance`. Click the `Create Instance`.

   ![](https://i.imgur.com/BJavtIl.png)

2. Give the Instance `name` and `Region`.

   ![](https://i.imgur.com/D8PAAiq.png)

   You can also see how much it would cost `monthly estimate` on the right side as well as the `cost per hour`.

   ![](https://i.imgur.com/Z5gjcmy.png)

   Just be careful to not get overboard with the free credit given by the GCP.

3. Select a better machine configuration but still under the GCP credit.

   ![](https://i.imgur.com/IpgGbue.png)

   Since it is better machine configuration, it will also cost higher. As soon as you choose the new configuration, the
   estimate will instantly update with the new cost.

4. Select the Operating system as well as the disk capacity at the `boot disk`. Ubuntu is fairly familiar linux
   distribution.

   ![](https://i.imgur.com/bmwVJIy.png)

5. Review all the configuration, and then we can hit the `Create` Button.

   ![](https://i.imgur.com/z6MhkxE.png)

    1. Alternatively, we can also check the `Equivalent code` to use it for our CLI. Click the `Equivalent code`.

       ![](https://i.imgur.com/5R6mo2K.png)

    2. Now you can either `copy` it, and run in the already opened Cloud shell or click the `run in cloud shell`.

       ![](https://i.imgur.com/u4mlqEg.png)

6. Wait for the Instance to be created.

   ![](https://i.imgur.com/7jSxgWP.png)

7. The Virtual Machine Instance is now created. You can now also see the External IP for us to access the instance.

   ![](https://i.imgur.com/GCehM2u.png)

---

## Connect to Virtual Machine Instance via SSH

1. To connect to the Virtual Machine Instance via SSH, typed in the terminal.

   ```shell
   ssh -i ~/.ssh/<PRIVATE-KEY> <USERNAME>@<IP-Address>
   ```

   ```shell
   ssh -i ~/.ssh/gcp rafael@<IP-Address>
   ```

   The IP Address here is the external ip given by the Virtual Machine Instance.

2. Typed in `yes` to connect.

   ![](https://i.imgur.com/3U9Pb7I.png)

3. Wait to established connection, and then you'll be able to be connected.

   ![](https://i.imgur.com/NR2Jlcb.png)

And since this is deployed to GCP, it also has already a pre-installed gcloud CLI

## Set up SSH Config for VM Instance access

1. Create config file.

   ```shell
   cd ~/.ssh
   touch config
   ```
2. Now edit the `config` file.

   ```
   Host <alias>
    Hostname <IP-Address>
    User <USERNAME>
    IdentityFile <PATH-TO-PRIVATE KEY>
   ```
3. Now you can connect via

   ```shell
   ssh <host-alias>
   ```

   ![](https://i.imgur.com/uqnEYrO.png)

---

## Configure VSCode to connect to the Virtual Machine Instance

1. Check on the Extensions if you got `Remote SSH` Extension

   ![](https://i.imgur.com/UyRMVW4.png)

2. Press `Ctrl + Shift + P` to show the `Command Palette` and then typed in `Remote SSH`. Find the Connect to Host.

   ![](https://i.imgur.com/Sn3SAkp.png)

3. Select the `de-zoomcamp` from the configured ssh host

   ![](https://i.imgur.com/5o4Iwng.png)

   Just in case, If using WSL and you didn't see it, make sure to restart vscode.

### Remote SSH code 255 in windows

The version used during this time is `0.96.0`

#### Error

![](https://i.imgur.com/vifpFy1.png)

The caused of this error is due to the `cmd.exe` not finding the `ssh.exe` even though if you use powershell it will be
able to find the `ssh.exe` with no problems.

#### Pre-requisite

In order to resolve this issue, users must ensure that they have the following installed in their system.

- OpenSSH
    - [Install SSH in windows](https://learn.microsoft.com/en-us/windows-server/administration/openssh/openssh_install_firstuse?tabs=gui)
- Git
    - [Install Git in windows](https://git-scm.com/downloads)

#### Solution

1. Check the environmental path.

   Windows Search > environmental variables > User variables for <USER> > Locate Path > Click `Edit`

2. Add this to Git SSH to the end.

   `C:\Program Files\Git\usr\bin`

   On the next time it is reboot, you will do the opposite and remove that `C:\Program Files\Git\usr\bin` at the very
   end.

3. Open `cmd.exe` and confirm with

   ```
   ssh
   ```

   If there is an output that indicates the usage of `ssh`, it means it is successful.

   ![](https://i.imgur.com/OJ8z93C.png)

   [Source - freebsd](https://man.freebsd.org/cgi/man.cgi?query=ssh&sektion=1&manpath=OpenBSD)

---

## Set up the Virtual Machine Instance

1. Download Anaconda from the website and install it.

   https://www.anaconda.com/products/distribution#Downloads

   ```shell
   wget https://repo.anaconda.com/archive/Anaconda3-2022.10-Linux-x86_64.sh
   ```

   Install Anaconda

   ```shell
   bash Anaconda3-2022.10-Linux-x86_64.sh
   ```

   ![](https://i.imgur.com/vxCJKz2.png)

2. Scroll down the license terms, and typed in `yes` to the agreement.

   ![](https://i.imgur.com/ar4D4Bz.png)

3. Agree to making Anaconda Initilizer.

   ![](https://i.imgur.com/viS2IZl.png)

4. Now restart to connect to the Virtual Machine Instance, and you'll be able to log in with the Anaconda env.

   ![](https://i.imgur.com/uqnEYrO.png)

   Alternatively, you can use `source ~/.bashrc` to reload the terminal.

   ```shell
   source ~/.bashrc
   ```

5. Install `Docker` and `docker compose` to the Virtual Machine Instance.

   https://docs.docker.com/engine/install/ubuntu/#install-using-the-convenience-script

   ```shell
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   ```

   Invoke the command to check if `docker` is installed correctly.

   ```
   docker
   ```

   Invoke the command to check if `docker compose` is installed correctly.

   ```
   docker compose
   ```

6. Perform adding user to the docker group to invoke docker without sudo.

   https://github.com/sindresorhus/guides/blob/main/docker-without-sudo.md

    1. create docker group

       ```shell
       sudo groupadd docker
       ```

    2. Add user to the docker group

       ```shell
       sudo gpasswd -a $USER docker
       ```
    3. restart docker service

       ```shell
       sudo service docker restart
       ```

       or alternatively, you can reboot the VM to take effect.

   ![](https://i.imgur.com/AGT0J0a.png)

7. Copy the Data Engineering Course repository.

   ```shell
   git clone https://github.com/DataTalksClub/data-engineering-zoomcamp.git
   ```

8. Run the docker compose for the pgadmin and postgres database

    1. Go to the folder

       ```shell
       cd data-engineering-zoomcamp/week_1_basics_n_setup/2_docker_sql
       ```

    2. Run the docker compose

       ```shell
       docker compose up -d
       ```

    3. Check if it is running

       ```
       docker ps
       ```

9. Install the postgres cli and check if it is running.
    1. Install

       ```shell
       pip install pgcli
       ```

    2. Connect to the database

       ```shell
       pgcli -h localhost -U root -d ny_taxi
       ```

    3. Check if the table is created.

       ```shell
       \dt
       ```

       ![](https://i.imgur.com/Sw0vOMh.png)

---

## Port Forwarding to local machine

### Port Forwarding Instructions

We're going to port forward the remote VM to our local machine in order to interact with our local machine.

1. Open the Remote SSH to our GCP Virtual Machine

2. Open New Terminal or use

   ```
   Ctrl+Shift+`
   ```

   ![](https://i.imgur.com/tGGel2g.png)

3. On the new terminal, Go to the `Ports` tab and then click `forward port`.

   ![](https://i.imgur.com/ZncKMxw.png)

4. Now add the following ports
    1. `5432` for postgres database
    2. `8080` for pgadmin

   ![](https://i.imgur.com/OK8IFvX.png)

### Testing on Local Machine

Opening the browser and Go to `localhost:8080`, and you'll see that the pgadmin works.

![](https://i.imgur.com/UiVpkCc.png)

You can also add the new server in order to check if the postgres database is also available on the local machine.

Check the container name by using `docker ps`

![](https://i.imgur.com/hM01Fmn.png)

Copy the container name and use that for the `Hostname` in the pgadmin.

![](https://i.imgur.com/gq7IDar.png)

You can now see that the Database is loaded successfully.

![](https://i.imgur.com/0Kx92yz.png)

---

### Port Forwarding Jupyter Notebook

#### Open the Jupyter Notebook Port

1. Open New Terminal or use

   ```
   Ctrl+Shift+`
   ```

   ![](https://i.imgur.com/tGGel2g.png)

2. On the new terminal, Go to the `Ports` tab and then click `forward port`.

   ![](https://i.imgur.com/ZncKMxw.png)

3. Now add the following ports

   `8888` for Jupyter Notebook

   ![](https://i.imgur.com/5CVaIQO.png)

#### Jupyter Notebook Usage

1. On the terminal enter the command to open a jupyter notebook

   ```shell
   jupyter notebook
   ```

   ![](https://i.imgur.com/016p36W.png)

2. Copy the link and Enter it on the browser. Now you can use Jupyter Notebook hosted on VM.

   ![](https://i.imgur.com/A6oFo1W.png)

---

## Terraform on Virtual Machine

### Install Terraform

Follow the Setup on the another Markdown for installation

The WSL setup should be the same as the Linux.

[Install Terraform on Linux](1_3_1_Introduction_to_Terraform_Concepts_and_GCP_Pre-Requisites.md#wsl)

### Transfer the GCP Service Account Key

#### For Windows Transfer via WinSCP

1. Download the Winscp.

   https://winscp.net/eng/download.php

2. Enter the following details:
    1. `Host Name` for the VM Ip address
    2. `User name` for the User of the VM
    3. `Password` for the password of the VM. But this is optional since we didn't add password.

   Afterwards, Click the advanced

   ![](https://i.imgur.com/xdNAqnY.png)

3. Select the private key and let the WinSCP convert it to PuTTY private key format and then hit save.

   ![](https://i.imgur.com/xm4kzbr.png)

4. Click `ok` and then click `Login`

   ![](https://i.imgur.com/9gUQQAH.png)

   ![](https://i.imgur.com/DycoJy2.png)

5. Proceed to locate the file and then transfer it to the VM by drag-and-drop.

#### For SFTP transfer via CLI

Since we already have ssh config we can just call

Make sure where we call the `sftp` command is the same directory where `<SERVICE-ACCOUNT>.json` is located for easier
uploading of file.

```
sftp de-zoomcamp
```

![](https://i.imgur.com/LHJRXXB.png)

And then use `put` command to upload the file

```
put <SERVICE-ACCOUNT>.json
```

![](https://i.imgur.com/RW7QbVI.png)

After uploading use `exit` to exit the `sftp`

### Perform Terraform

#### Login the gcloud service account in CLI

Perform the steps in the other page for login

[Login with gcloud CLI](1_3_1_Introduction_to_Terraform_Concepts_and_GCP_Pre-Requisites.md#alternate-setup)

#### Terraform commands

Perform testing if you can use the terraform commands.

The instructions should be the same as the previous lesson before that is hyperlink below.

[Terraform Commands](1_3_2_Creating_GCP_Infrastructure_with_Terraform.md#terraform-commands)

---

## Virtual Machine Actions

### Turn off virtual machine

Since the VM is Linux you can run the command to turn off the Virtual Machine.

```
sudo shutdown -h now
```

Alternatively, you can go to the browser and Click the Kehab menu and click `Stop` in order to turn off the Virtual
Machine.

![](https://i.imgur.com/IotL8VU.png)

Once you can no longer the external IP then it is already stopped.

### Turn on virtual machine

To turn it on from the off state. Click the Kehab Menu and the click `Start/Resume`

![](https://i.imgur.com/RI6DSyL.png)

### Delete Virtual Machine

This action will delete all files on the Virtual Machine.

![](https://i.imgur.com/cAHJlQo.png)

---

## Page

| Previous                                                                                          | table of contents      | Next                                     |
|---------------------------------------------------------------------------------------------------|------------------------|------------------------------------------|
| [Creating GCP Infrastructure with Terraform](1_3_2_Creating_GCP_Infrastructure_with_Terraform.md) | [Readme.md](README.md) | [ 2.1.1 - Data Lake](2_1_1_Data_Lake.md) |
- [Introduction](#introduction)
- [SSH key](#ssh-key)
    - [Documentation](#documentation)
    - [Instructions](#instructions)
- [Create Virtual Machine Instance](#create-virtual-machine-instance)
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

So with this lesson, we are going to created Virtual Machine Instance but we must generate ssh key first.

---

## SSH key

### Documentation

Following from this official documentation given by the
GCP https://cloud.google.com/compute/docs/connect/create-ssh-keys

### Instructions

1. We must first create a ssh directory, and then go into it.

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

   In the `Compute Engine` scroll down in the left side until you found the `Metadata`

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

   You can also see how much it would cost `monthly estimate` at the right side as well as the `cost per hour`.

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

6. And now, the Virtual Machine Instance is now created.

---

## Page

| Previous                                                                                          | Return to table of contents |
| ------------------------------------------------------------------------------------------------- | --------------------------- |
| [Creating GCP Infrastructure with Terraform](1_3_2_Creating_GCP_Infrastructure_with_Terraform.md) | [Readme.md](README.md)      |
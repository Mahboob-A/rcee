                         
<br/>
<div align="center">
<a href="https://github.com/Mahboob-A/algocode">
<img src="https://github.com/Mahboob-A/algocode/assets/109282492/072ec437-4f1a-4fd5-ba50-45d44de5fb6e" alt="Logo" width="700" height="400">
</a>
<h3 align="center">Algocode - The Leetcode for Hackers</h3>
<p align="center">
Algocode is a DSA practice platform just like Leetcode!
<br/>
<br/>
<a href="https://imehboob.medium.com/my-experience-building-a-leetcode-like-online-judge-and-how-you-can-build-one-7e05e031455d"  target="_blank" ><strong>Read the blog »</strong> </a>
<br/>
<br/>
<a href="https://github.com/Mahboob-A/algocode-auth">Algocode Auth Service .</a>  
<a href="https://github.com/Mahboob-A/code-manager">Code Manager Service .</a>
<a href="https://github.com/Mahboob-A/rcee/">RCE Engine Service</a>
</p>
</div>

<h3 align="center">General Information</h3>

Algocode is an online data structure and algorithm practice backend built in microservices architecture. 


*Algocode currently has three services*: <a href="https://github.com/Mahboob-A/algocode-auth">Algocode Auth Service .</a> <a href="https://github.com/Mahboob-A/code-manager">Code Manager Service .</a> and <a href="https://github.com/Mahboob-A/rcee/">RCE Engine Service</a>
<br/> <br/>

RCE Engine Service is responsible to `execute` the `user submitted code` in the Algocode Platform.  The current RCE Engine has `C++ Judge` that can  `compile`,`execute` and `compare testcases` against the `output` of the code execution. 

RCE Engine for `Java Judge` and RCE Engine for `Python Judge` are under development.

The <a href="https://github.com/Mahboob-A/code-manager">Code Manager</a> service publishes the `user codes` in `RabbitMQ instance`, the RCE Engine listen to `C++ queue` and compiles, executes and compares the testcases with the code execution output. Once a result is produced either comparing the testcases, or any error occurred during the code execution, RCE Engine publishes the result to a `unified result queue` which is consumed by the <a href="https://github.com/Mahboob-A/code-manager">Code Manager</a> service to finally `cache` the result in `Redis` and store the result in `MongoDB` for persistence.  

To learn more about _Algocode and the architecture_, please `READ-THE-BLOG-URL` or visit <a href="https://github.com/Mahboob-A/algocode">Algocode</a> here. 


#### _NOTE_

**A. About the Judge**

> Algocode is built from scratch. `No 3rd party APIs` or `3rd party packages` has been used to implement the `Judge`.
It is purely a docker implementation with secure and protected environment. 

**B. Connectivity**

> The `RCE Engine` is completely isolated service. No API has been exposed in the `RCE Engine`.  It is only connected through the `Message Queue`.

**C. Documentation**

> As the `RCE Engine` does not have any API to interact with, there's no dedicated _documentation_ page for RCE Engine. However, adequate comment has been added in the codebase. 

**D. Deployment**

> The service is deployed in AWS EC2 Ubuntu 22.04 server.

**E. About Algocode**

> This is RCE Engine Service specific guideline.
>> **Please visit <a href="https://github.com/Mahboob-A/algocode">Algocode</a> to learn the mircroservices architecture of Algocode and more in-depth guideline how to submit a solution to Algocode platform.**


<br/> <br/><details>
<summary><h3 align="center">Production</h3></summary>

#### Production Stage RCE Engine (C++ Judge) 

The Algocode RCE Engine (C++ Judge) uses the following services to serve the request during Production Stage.  

    a. Docker to securely execute the user submitted code
    b. Portainer to manage and monitor docker container in RCE Engine
    c. RabbitMQ for asynchronous message processig.
    d. Django as backend. 
    e. Docker to containerize the service. 

#### Deployment

The Code Manager Service is deployed in AWS EC2 Ubuntu 22.04 Server. 

<br/>
<br/>  

</details><details>
<summary><h3 align="center">Code Execution</h3></summary>

#### Overview 

RCE Engine is the heart behind the Algocode platform. It `executes` the user submitted code that was published by  <a href="https://github.com/Mahboob-A/code-manager">Code Manager Service</a> to a RabbitMQ instance, and finally publishes the result to a `unified result queue` that is consumed by the Code Manager service. 

The client can not directly interact with the <a href="https://github.com/Mahboob-A/rcee/">RCE Engine Service</a> as RCE Engine is  `isolated`, `secure` service and it is only accessible to `Message Queue`.  

#### Code Execution 

The `C++ Judge` in the RCE Engine works in `sibling containers` architecture. The host docker container for the RCE Engine is capable of spawning `sibling containers` to execute the code submitted by the user. The sibling container spawned by the host docker container is `secure`, `non-privileged` and `restricted` container. The sibling containers are capable of fighting any potential `malicious code execution` such as `fork-bomb`, `resource exhaustion` `file-hijacking` etc. 

> Please visit <a href="https://github.com/Mahboob-A/online-judge">Online Judge</a>, it is a `PoC` of the `C++ Judge` implemented in the RCE Engine. You will find more in-depth analytical documentation on the various state of `C++ Judge` in the <a href="https://github.com/Mahboob-A/online-judge">Prototype of C++ Judge</a>.

#### Prototype 

A separate light-weight `prototype` for the `C++ Judge` is also available. This prototype is a `PoC` for the `C++ Judge` and easier to test and manage. It can handle API requests as well as preset question to test the `PoC` of `C++ Judge`. 

**Please visit the <a href="https://github.com/Mahboob-A/online-judge?tab=readme-ov-file#faq">FAQ of Online Judge</a> to learn more about the `Prototype` of the `C++ Judge`. It has more detailed and analytical comparisons between the various state of the `C++ Judge`.**


<br/>
<br/>  

</details>



<details>
<summary><h3 align="center">Watch In Action</h3></summary>


#### A. Long Video (Describes all the features and architecture)
- Watch from `16:30` for code execution begin and  `18:30` for code submission result. 

<a href="https://www.youtube.com/watch?v=TbiRWL-11Fo&t=990s" target="_blank">
  <img src="https://img.youtube.com/vi/TbiRWL-11Fo/0.jpg" alt="Watch the video">
</a>

#### B. Short Video (Only core features) 
- Watch from `09:30` for code execution begin and  `11:30` for code submission result. 

<a href="https://www.youtube.com/watch?v=EgtAEjH53BA&t=571s" target="_blank">
  <img src="https://img.youtube.com/vi/EgtAEjH53BA/0.jpg" alt="Watch the video">
</a>


</details>




<details>
<summary><h3 align="center">Workflow - RCE Engine</h3></summary>


##### Workflow 

The <a href="https://github.com/Mahboob-A/code-manager">Code Manager Service</a> publishes the user submitted code to `C++ Queue` and the RCE Engine consumes from a `C++ Queue` to execute the code.

Once the RCE Engine consumes from the queue, it processes the data and prepares for the code execution. 

As the pre-processing is completed, the `C++ Judge` `compiles` and `executes` the code. 

Finally, the RCE Engine compares the `testcases` against the `code execution output`, if the code execution is successful, or it processes the error occurred during the `compilation` or `execution` stage, and publishes the final result to a `unified result queue`.  

This `unified result queue` is consumed by the <a href="https://github.com/Mahboob-A/code-manager">Code Manager Service</a> to `cache` the result in `Redis` and finally store the result in `MongoDB` database for persistence. 

<br/>
<br/>  

</details><details>
<summary><h3 align="center">Run Locally and Contribution</h3></summary>

#### Run Locally

Please `fork` and `clone` this <a href="https://github.com/Mahboob-A/rcee/tree/development">development branch</a> of Algocode RCE Engine `(C++ Judge)` Service, and follow along with the `envs-examples`. 

`cd` to `src` and create a `virtual environment`. Activate the virtual environment. 

Run `make docker-up` and the development setup will start running. Please install `make` in your host machine. 

If you use `Windows` Operating System, please run the  respective `docker commands` from the **`dev.yml`** docker compose file.

#### Contribution 

You are always welcome to contribute to the project. Please `open an issue` or `raise a PR` on the project.  

<br/>
<br/>  

</details>
<details>
  <summary><h3 align="center">Code Submission Result Examples</h3></summary>

<br/>

#### Some Code Submission Result Snapshots

<br/> 

##### A. AC Solution 

 ![dd8dbfe4-621b-49f1-b3a6-7ab2a892db87](https://github.com/Mahboob-A/algocode/assets/109282492/378d23ae-e059-47eb-866d-7c73d329b430) 
<br/>
<br/>

##### B. WA Solution 

  ![bedb4255-86c9-4417-b920-5976e6129cbb](https://github.com/Mahboob-A/algocode/assets/109282492/69bce2c1-5e16-4685-9069-23492068b55e)
<br/>
<br/>

##### C. Compilation Error

![1c5edd39-8ccd-4e23-a61d-66ae9564ca85](https://github.com/Mahboob-A/algocode/assets/109282492/9df40b17-b3f9-48d4-9662-3acdc1f594b8) 
<br/>
<br/>


##### D. Segmentation Fault 

![WhatsApp Image 2024-06-05 at 11 42 42 PM (1)](https://github.com/Mahboob-A/algocode/assets/109282492/0a3e1d3f-bafb-41a4-8f30-29eb5a9133e5)
<br/>
<br/>


##### E. Memory Limit Exceed

![WhatsApp Image 2024-06-05 at 11 42 03 PM (1)](https://github.com/Mahboob-A/algocode/assets/109282492/766f01f7-e97a-4aa7-858a-d7dddbf89b7d)
<br/>
<br/>


##### F. Time Limit Exceed 

![WhatsApp Image 2024-06-05 at 11 42 03 PM (1)](https://github.com/Mahboob-A/algocode/assets/109282492/766f01f7-e97a-4aa7-858a-d7dddbf89b7d)
<br/>
<br/>

<br/>

</details><br/>

<a href="https://www.linux.org/" target="blank">
<img align="center" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/linux/linux-original.svg" alt="Linux" height="40" width="40" />
</a>
<a href="https://postman.com" target="blank">
<img align="center" src="https://www.vectorlogo.zone/logos/getpostman/getpostman-icon.svg" alt="Postman" height="40" width="40" />
</a>
<a href="https://www.w3schools.com/cpp/" target="blank">
<img align="center" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/cplusplus/cplusplus-original.svg" alt="C++" height="40" width="40" />
</a>
<a href="https://www.java.com" target="blank">
<img align="center" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/java/java-original.svg" alt="Java" height="40" width="40" />
</a>
<a href="https://www.python.org" target="blank">
<img align="center" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="Python" height="40" width="40" />
</a>
<a href="https://www.djangoproject.com/" target="blank">
<img align="center" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/django/django-original.svg" alt="Django" height="40" width="40" />
</a>
<a href="https://aws.amazon.com" target="blank">
<img align="center" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/amazonwebservices/amazonwebservices-original-wordmark.svg" alt="AWS" height="40" width="40" />
</a>
<a href="https://www.docker.com/" target="blank">
<img align="center" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/docker/docker-original-wordmark.svg" alt="Docker" height="40" width="40" />
</a>
<a href="https://www.gnu.org/software/bash/" target="blank">
<img align="center" src="https://www.vectorlogo.zone/logos/gnu_bash/gnu_bash-icon.svg" alt="Bash" height="40" width="40" />
</a>
<a href="https://azure.microsoft.com/en-in/" target="blank">
<img align="center" src="https://www.vectorlogo.zone/logos/microsoft_azure/microsoft_azure-icon.svg" alt="Azure" height="40" width="40" />
</a>
<a href="https://circleci.com" target="blank">
<img align="center" src="https://www.vectorlogo.zone/logos/circleci/circleci-icon.svg" alt="CircleCI" height="40" width="40" />
</a>
<a href="https://nodejs.org" target="blank">
<img align="center" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/nodejs/nodejs-original-wordmark.svg" alt="Node.js" height="40" width="40" />
</a>
<a href="https://kafka.apache.org/" target="blank">
<img align="center" src="https://www.vectorlogo.zone/logos/apache_kafka/apache_kafka-icon.svg" alt="Kafka" height="40" width="40" />
</a>
<a href="https://www.rabbitmq.com" target="blank">
<img align="center" src="https://www.vectorlogo.zone/logos/rabbitmq/rabbitmq-icon.svg" alt="RabbitMQ" height="40" width="40" />
</a>
<a href="https://www.nginx.com" target="blank">
<img align="center" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/nginx/nginx-original.svg" alt="Nginx" height="40" width="40" />
</a>
<br/>

#### 🔗 Links

[![Email Me](https://img.shields.io/badge/mahboob-black?style=flat&logo=gmail)](mailto:connect.mahboobalam@gmail.com?subject=Hello) 
  <a href="https://twitter.com/imahboob_a" target="_blank">
    <img src="https://img.shields.io/badge/Twitter-05122A?style=flat&logo=twitter&logoColor=white" alt="Twitter">
  </a>
  <a href="https://linkedin.com/in/i-mahboob-alam" target="_blank">
    <img src="https://img.shields.io/badge/LinkedIn-05122A?style=flat&logo=linkedin&logoColor=white" alt="LinkedIn">
  </a>
  <a href="https://hashnode.com/@imehboob" target="_blank">
    <img src="https://img.shields.io/badge/Hashnode-05122A?style=flat&logo=hashnode&logoColor=white" alt="Hashnode">
  </a>
  <a href="https://medium.com/@imehboob" target="_blank">
    <img src="https://img.shields.io/badge/Medium-05122A?style=flat&logo=medium&logoColor=white" alt="Medium">
  </a>
  <a href="https://dev.to/imahboob_a" target="_blank">
    <img src="https://img.shields.io/badge/Dev.to-05122A?style=flat&logo=dev.to&logoColor=white" alt="Devto">
  </a>
  <a href="https://www.leetcode.com/mahboob-alam" target="_blank">
    <img src="https://img.shields.io/badge/LeetCode-05122A?style=flat&logo=leetcode&logoColor=white" alt="LeetCode">
  </a>

<br/>
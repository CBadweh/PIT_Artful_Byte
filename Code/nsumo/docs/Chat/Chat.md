## **Big Picture**

- **Same**: You still build a Docker image, run a container, download the MSP430 toolchain *inside* that container, then commit/push the image.
- **Different**: You **don’t install Docker with apt** and you **don’t manage Linux groups** on Windows. Docker Desktop + WSL 2 handle that.

---

## **1) Installing Docker + permissions**

**Lesson (Linux):**

sudo apt install docker.io

sudo groupadd docker

sudo usermod -aG docker $USER

newgrp docker

**Your Windows equivalent:**

- Install **Docker Desktop for Windows** (GUI installer).
- Enable WSL 2 integration in Docker Desktop settings.
- No groupadd/usermod steps needed.

---

## **2) Editing Dockerfile and building the image**

**Lesson (Linux):**

cd tools

rm PLACEHOLDE

vim dockerfile

docker build -t msp430-gcc .

docker images

**Your Windows options:**

- **Option A (WSL 2 terminal):**

Do the *same commands* inside your WSL Ubuntu shell.

Example: open Ubuntu terminal → cd /mnt/c/Users/.../tools → same commands.

- **Option B (PowerShell):**

You can run docker build directly from PowerShell too, as long as Docker Desktop is running.

**Same outcome**: a Docker image named msp430-gcc.

---

## **3) Running the container**

**Lesson (Linux):**

docker run --interactive --tty msp430-gcc /bin/bash

**Your Windows equivalent:**

- Same command works in **PowerShell** or **WSL**.
- Result: you’re inside a **Linux shell** *in the container*.

---

## **4) Downloading toolchain inside the container**

These **must run inside the container**, so it’s identical for you:

wget ...

tar ...

unzip ...

mv ...

Even though your host is Windows, the container is **Linux**, so the commands are the same.

---

## **5) Commit the container to a new image**

**Lesson (Linux):**

docker ps -a

docker commit <id> artful-bytes-msp430-9.3.1.11:latest

docker images

**Your Windows equivalent:**

- Same commands, run from PowerShell or WSL.

---

## **6) Push to Docker Hub**

**Lesson (Linux):**

docker login

docker push artfulbytes/msp430-gcc-9.3.1.11:latest

**Your Windows equivalent:**

- Same commands, run from PowerShell or WSL.

---

## **Summary: What’s the same vs different**

**Same**

- Docker commands (build, run, commit, push)
- Toolchain download steps inside the container
- Final image and CI usage

**Different**

- You **don’t use apt** or Linux user groups on Windows
- Docker is installed via **Docker Desktop**
- Your Linux shell comes from **WSL 2**, not the host OS
# cloud-parser
a cloud parser with cloud server environment setup (Ali-Cloud)


# Step 1

用sudo su root 来查看地址，再用sudo vi /etc/hosts 把第一行的localhost改成地址.

# Step 2 ---- 安装Python3.7.3 在Ubuntu 16.04

先用 以下代码 安装好dependent环境文件

> sudo apt-get install zlib1g-dev libbz2-dev libssl-dev libncurses5-dev libsqlite3-dev libreadline-dev tk-dev libgdbm-dev libdb-dev libpcap-dev xz-utils libexpat1-dev liblzma-dev libffi-dev libc6-dev

> wget 'https://www.python.org/ftp/python/3.7.3/Python-3.7.3.tgz'

> tar zxvf Python-3.7.3.tgz

> cd Python-3.7.3/

> sudo mkdir -p /usr/local/python3

> ./configure --prefix=/usr/local/python3 --enable-optimizations

> make

> sudo make install

此时 Python 3.7.3已经安装完毕，接着就是处理原来的softlink和pip3的链接 

> sudo rm -rf /usr/bin/python3

> sudo rm -rf /usr/bin/pip3 (这一条未必需要，因为默认系统可能没有pip3）

> sudo ln -s /usr/local/python3/bin/python3.7 /usr/bin/python3

> sudo ln -s /usr/local/python3/bin/pip3.7 /usr/bin/pip3


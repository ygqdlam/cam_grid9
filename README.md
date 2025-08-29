# cam_grid9

该项目需要在腾讯云上面运行。运行环境：Ubuntu系统、Python3.12。 [腾讯云链接](https://console.cloud.tencent.com/lighthouse/instance/index?rid=8)

## 在安装腾讯云时遇到的问题

### 1. 端口号必须是8888，这个可以发布到公网的端口号是固定的，通过腾讯云查询。
### 2. 需要创建Python虚拟环境
  ①  创建虚拟环境。在你的项目目录下（比如 ~/point_label_app_grid9），运行：
```bash
python3 -m venv venv
```
  ② 激活虚拟环境。运行以下命令激活虚拟环境：
```bash
source venv/bin/activate
```
  ③ 退出虚拟环境（用完之后可以输入）：
```bash
deactivate
```
  ④ 需要下载以下依赖：
```bash
Pillow、flask、numpy
```

  ⑤ 挂载后端运行：
```bash
nohup python app.py > output.log 2>&1 &
```
  ⑥ 查看进程
```bash
ps aux | grep python
```
```bash
ps -ef
```
  ⑦ 查看进程占用端口号
```bash
netstat -tulnp | grep :8888
```
```bash
lsof -i :8888
```

  ⑧ 下载文件到本地：
```bash
scp ubuntu@XX.XXX.XXX.XXX:/home/ubuntu/point_label_app_grid9/annotations.csv /Users/yanggq/yanggq/伪装项目/annotations.csv
```

### 3.遇到的一些报错
  ① 正在使用以下命令尝试通过 scp 上传文件：
```bash
scp /Users/yanggq/yanggq/伪装项目/point_label_app_grid9.zip ubuntu@XX.XXX.XXX.XXX:/home/ubuntu/
```
但遇到以下错误：
```bash
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
...
Host key for 49.233.133.133 has changed and you have requested strict checking.
Host key verification failed.
scp: Connection closed
```
这是因为再次链接服务器时，SSH主机密钥发生变化，和本地保存的不一样，因此，需要删除旧的记录（推荐，最常用）：
```bash
ssh-keygen -R 49.233.133.133
```







默认安装的netdata可能阉割了功能，这里的netdata使用本地安装方法，版本为1.47  
安装后配置开机自启动
```bash
systemctl start netdata && systemctl enable netdata
```
安装好后修改默认的netdata配置文件  
```
cat > /opt/netdata/etc/netdata/netdata.conf << EOF
#1.47版本
[global]
        hostname = 192.168.1.157 # 本机ip或者hostname
        send anonymous statistics = no # 禁止发送主机匿名信息
[global statistics]
        update every = 8
[plugins]
        netdata monitoring extended = no
        idlejitter = no
        netdata monitoring = no
        profile = no
        tc = no
        diskspace = yes
        proc = yes
        cgroups = yes
        timex = no
        enable running new plugins = no
        statsd = no
        check for new plugins every = 600000
        slabinfo = no
        python.d = no
        ebpf = no
        apps = no
        network-viewer = no
        nfacct = no
        perf = no
        go.d = yes # 需要开启监控docker
        charts.d = no
        debugfs = no
        ioping = no
[web]
        #bind = * # 所有ip可以访问，不建议开启
        mode = none # 关闭web模式
```
配置netdat监控数据导出到Prometheus，可以直接使用下方配置文件：
```
# ./edit-config exporting.conf # 会生成模版
cat > /opt/netdata/etc/netdata/exporting.conf << EOF
[exporting:global]
  enabled = yes
  send configured labels = yes
  send automatic labels = no
  update every = 10
[prometheus_remote_write:my_prometheus_remote_write_instance]
  enabled = yes
  destination = control-server.com:9090 # 修改成真实ip或域名
  remote write URL path = /api/v1/write
  update every = 1 # 此处可以修改
EOF
```
开启监控docker
```
cat > /opt/netdata/etc/netdata/go.d/docker.conf << EOF
## All available configuration options, their descriptions and default values:
## https://github.com/netdata/netdata/tree/master/src/go/plugin/go.d/modules/docker#readme

jobs:
  - name: local
    address: 'unix:///var/run/docker.sock'
    timeout: 2
    collect_container_size: no
EOF
```
重启netdata后开始手机监控
```bash
systemctl restart netdata
```
增加一个会常用的命令，因为默认配置关闭了许多功能，如果开启可以使用ansible开启
```
ansible total -m shell -a "sed -i 's/go.d = no[[:space:]]*$/go.d = yes/g' /opt/netdata/etc/netdata/netdata.conf"
ansible total -m copy -a 'src=/opt/netdata/etc/netdata/docker.conf dest=/opt/netdata/etc/netdata/docker.conf'
ansible total -m shell -a 'systemctl restart netdata'
```
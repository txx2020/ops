#!/bin/bash
ip='192.168.1.160'
user='tongtu'
password='ttyj7890'

data_time=$(date +%Y%m%d)
back_dir=/root/server/back_dir
back_files='/root/server/openvpn /root/server/docker-compose.yml /root/server/user'
file_name='openvpn_backup_'$data_time'.tar.gz'
#echo $file_name

if test -d $back_dir;then
   echo "目录存在";
else 
   mkdir $back_dir;
   echo "正在创建";
fi

tar -czvf "$back_dir"/"$file_name" $back_files -C $back_dir  > /dev/null 2>&1
#del_name=$(find $back_dir -mtime +31 -type f -name "*tar.gz")
#echo $del_name
#rm -f $del_name
ftp -n $ip  <<EOF
user $user $password
binary
cd "I/openvpn_数据备份"
ls
put "$back_dir"/"$file_name" "$file_name"
ls
bye
EOF
echo "download from ftp successfully"

#!/bin/bash
docker exec -it gitlab bash -c 'gitlab-rake gitlab:backup:create'
# 目标服务器详细信息
SFTP_HOST="10.253.129.12"
SFTP_PORT="22"
SFTP_USER="tongtu"
REMOTE_PATH="/home/tongtu/gitlab_backup_dir"

# 本地目录
LOCAL_DIR="/opt/gitlab/data/backups"
LOG_DIR="/home/tongtu/gitlab-ce/logs"

# 日志文件，包含当前日期
LOG_FILE="$LOG_DIR/sftp_$(date '+%Y-%m-%d').log"

# 确保日志目录存在
mkdir -p "$LOG_DIR"

# 获取今天的日期
TODAY=$(date '+%Y-%m-%d')

# 查找本地目录中当天最新的文件
LOCAL_FILE=$(find "$LOCAL_DIR" -type f -newermt "$TODAY 00:00" ! -newermt "$TODAY 23:59" -printf "%T+ %p\n" | sort -r | head -n 1 | awk '{print $2}')

# 检查是否找到文件
if [ -z "$LOCAL_FILE" ]; then
  echo "$(date '+%Y-%m-%d %H:%M:%S') 未找到当天的文件。" | tee -a "$LOG_FILE"
  exit 1
fi

# 记录文件传输开始日志
echo "$(date '+%Y-%m-%d %H:%M:%S') 开始传输文件：$LOCAL_FILE 到 $SFTP_USER@$SFTP_HOST:$REMOTE_PATH" | tee -a "$LOG_FILE"

# 使用 sftp 进行文件传输并记录日志
sftp -oPort=$SFTP_PORT $SFTP_USER@$SFTP_HOST <<EOF 2>&1 | tee -a "$LOG_FILE"
put $LOCAL_FILE $REMOTE_PATH
bye
EOF

# 记录文件传输完成日志
echo "$(date '+%Y-%m-%d %H:%M:%S') 文件传输完成：$LOCAL_FILE 到 $SFTP_USER@$SFTP_HOST:$REMOTE_PATH" | tee -a "$LOG_FILE"

# 删除目标服务器上 14 天之前的文件并记录日志
echo "$(date '+%Y-%m-%d %H:%M:%S') 开始删除目标服务器上 14 天之前的文件。" | tee -a "$LOG_FILE"
sftp -oPort=$SFTP_PORT $SFTP_USER@$SFTP_HOST <<EOF 2>&1 | tee -a "$LOG_FILE"
cd $REMOTE_PATH
# 列出文件并删除超过 14 天的文件
ls -l | grep -E '^-.*' | awk -v date="$(date -d '14 days ago' '+%Y-%m-%d')" '{print $6"-"$7"-"$8" "$9}' | while read file_info; do
  file_date=$(echo $file_info | awk '{print $1}')
  file_name=$(echo $file_info | awk '{print $2}')
  if [[ $file_date < $date ]]; then
    echo "删除文件: $file_name"
    rm $file_name
  fi
done
bye
EOF

# 记录删除文件操作完成日志
echo "$(date '+%Y-%m-%d %H:%M:%S') 删除目标服务器上 14 天之前的文件完成。" | tee -a "$LOG_FILE"

# 定期归档日志文件并删除已打包的日志
ARCHIVE_INTERVAL_DAYS=7
find "$LOG_DIR" -type f -name "*.log" -mtime +$ARCHIVE_INTERVAL_DAYS -exec tar -czf "$LOG_DIR/archive_$(date '+%Y-%m-%d_%H-%M-%S').tar.gz" {} + -exec rm {} +

echo "$(date '+%Y-%m-%d %H:%M:%S') 归档并删除旧日志完成。" | tee -a "$LOG_FILE"


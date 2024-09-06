export HBASE_HEAPSIZE=3G
export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-amd64
export HBASE_OPTS="$HBASE_OPTS -XX:+UseConcMarkSweepGC"
export HBASE_MASTER_OPTS="$HBASE_MASTER_OPTS -XX:PermSize=128m -XX:MaxPermSize=128m"
export HBASE_REGIONSERVER_OPTS="$HBASE_REGIONSERVER_OPTS -XX:PermSize=128m -XX:MaxPermSize=128m"
export HBASE_THRIFT_OPTS="$HBASE_THRIFT_OPTS -Xmx1g -Xms1g -Xmn512m"
export HBASE_PID_DIR=/data/data1/server/hbase-2.2.5/pids
export HBASE_MANAGES_ZK=false

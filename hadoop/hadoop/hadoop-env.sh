export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-amd64
export HADOOP_CONF_DIR=${HADOOP_CONF_DIR:-"/etc/hadoop"}
for f in $HADOOP_HOME/contrib/capacity-scheduler/*.jar; do
  if [ "$HADOOP_CLASSPATH" ]; then
    export HADOOP_CLASSPATH=$HADOOP_CLASSPATH:$f
  else
    export HADOOP_CLASSPATH=$f
  fi
done
export HADOOP_HEAPSIZE=32768 # add by txx 20240821
export HADOOP_OPTS="$HADOOP_OPTS -Djava.net.preferIPv4Stack=true"
export HADOOP_NAMENODE_OPTS="-server -Xms32768m -Xmx32768m -XX:+UseG1GC -Dhadoop.security.logger=${HADOOP_SECURITY_LOGGER:-INFO,RFAS} -Dhdfs.audit.logger=${HDFS_AUDIT_LOGGER:-INFO,NullAppender} $HADOOP_NAMENODE_OPTS" # fixed by txx 20240821
export HADOOP_DATANODE_OPTS="-server -Xms16384m -Xmx16384m -XX:+UseG1GC -Dhadoop.security.logger=ERROR,RFAS $HADOOP_DATANODE_OPTS"                                                                                       # fixed by txx 20240821
export HADOOP_SECONDARYNAMENODE_OPTS="-Dhadoop.security.logger=${HADOOP_SECURITY_LOGGER:-INFO,RFAS} -Dhdfs.audit.logger=${HDFS_AUDIT_LOGGER:-INFO,NullAppender} $HADOOP_SECONDARYNAMENODE_OPTS"
export HADOOP_NFS3_OPTS="$HADOOP_NFS3_OPTS"
export HADOOP_PORTMAP_OPTS="-Xmx1024m $HADOOP_PORTMAP_OPTS" # fixed by txx 20240821
export HADOOP_CLIENT_OPTS="$HADOOP_CLIENT_OPTS"
if [ "$HADOOP_HEAPSIZE" = "" ]; then
  export HADOOP_CLIENT_OPTS="-Xmx512m $HADOOP_CLIENT_OPTS"
fi
export HADOOP_SECURE_DN_USER=${HADOOP_SECURE_DN_USER}
export HADOOP_PID_DIR=${HADOOP_PID_DIR}
export HADOOP_SECURE_DN_PID_DIR=${HADOOP_PID_DIR}
export HADOOP_IDENT_STRING=$USER

Name:		mysql
Version:	5.7.43
Release:	1%{?dist}
Summary:	mysql
 
License:	GPL
Source0:	%{name}-boost-%{version}.tar.gz
Source1:	my.cnf
Source2:	mysqld.service
BuildRequires:  cmake /sbin/useradd /sbin/groupadd /bin/bash /bin/sh /bin/chown
Requires:	ncurses ncurses-devel pcre numactl-libs numactl bison libaio libaio-devel
BuildRoot: 	%{_topdir}/BUILDROOT
%define 	_prefix 	/app/mysql
%define 	_datadir 	/app/mysql/data
%define 	MYSQL_USER 	mysql 
%define 	MYSQL_GROUP 	mysql 
%define		mysql_conf	/etc/my.cnf
%define		mysql_server	/usr/lib/systemd/system/mysqld.service
%define		mysqld		/etc/init.d/mysqld
%description
The MySQL(TM) software delivers a very fast, multi-threaded, multi-user, 
and robust SQL (Structured Query Language) database server. MySQL Server 
is intended for mission-critical, heavy-load production systems as well 
as for embedding into mass-deployed software. 
 
%prep
rm -rf $RPM_BUILD_ROOT/%{name}-%{version}
%setup -q -n %{name}-%{version}
id $user >& /dev/null
if [ $? -ne 0 ];then
  groupadd %{MYSQL_GROUP}
  useradd -g %{MYSQL_GROUP} %{MYSQL_USER} -s /bin/nologin >/dev/null 2>&1 
fi
%build
cmake \
-DCMAKE_INSTALL_PREFIX=%{_prefix} \
-DMYSQL_DATADIR=%{_datadir} \
-DMYSQL_TCP_PORT=3306 \
-DWITH_BOOST=boost \
-DMYSQL_UNIX_ADDR=/tmp/mysql.sock \
-DSYSCONFDIR=/etc \
-DENABLED_LOCAL_INFILE=1 \
-DENABLE_DTRACE=0 \
-DDEFAULT_CHARSET=utf8mb4 \
-DDEFAULT_COLLATION=utf8mb4_general_ci \
-DWITH_EMBEDDED_SERVER=0  \
-DEXTRA_CHARSETS=all \
-DWITH_ZLIB=bundled \
-DWITH_SSL=system \
-DWITH_NUMA=ON \
-DINSTALL_MYSQLTESTDIR= 
 
make -j `cat /proc/cpuinfo | grep processor| wc -l`
 
%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
%{__install} -p -D -m 0644 %{SOURCE1} %{buildroot}/etc/my.cnf
%{__install} -p -D -m 0755 %{SOURCE2} %{buildroot}/usr/lib/systemd/system/mysqld.service
%{__install} -p -D -m 0755 %{buildroot}/%{_prefix}/support-files/mysql.server %{buildroot}/etc/init.d/mysqld
 
%pre  
useradd -s /bin/nologin -M mysql >/dev/null 2>&1
 
%post  
chkconfig mysqld on
%{_prefix}/bin/mysqld --initialize-insecure --basedir=%{_prefix} --datadir=%{_datadir} --user=mysql 
%{_prefix}/bin/mysql_ssl_rsa_setup --uid=%{MYSQL_USER}
chown -R mysql:mysql %{_prefix}
systemctl start mysqld
 
%preun  
systemctl stop mysqld
chkconfig --del mysqld
 
%postun  
rm -rf /app/mysql >/dev/null 2>&1 
rm -rf /app/mysql/data >/dev/null 2>&1 
rm -rf /etc/init.d/mysql >/dev/null 2>&1 
rm -rf /etc/my.cnf >/dev/null 2>&1 
rm -rf /etc/my.cnf.d >/dev/null 2>&1 
rm -rf /etc/mysql >/dev/null 2>&1
rm -rf /var/run/mysqld.pid >/dev/null 2>&1
userdel -r mysql >/dev/null 2>&1 
 
%files  
%defattr(-,mysql,mysql)
%doc
%{_prefix}
%{mysql_conf}
%{mysqld}
%{mysql_server}
 
%changelog
 

Name:           mysql
Version:        5.7.43
Release:        1%{?dist}
Summary:        MySQL is a fast, stable and true multi-user, multi-threaded SQL database server

License:        GPL
URL:            https://dev.mysql.com/
Source0:        %{name}-boost-%{version}.tar.gz
Source1:        my.cnf
Source2:        mysqld.service

BuildRequires:  cmake
BuildRequires:  /sbin/useradd
BuildRequires:  /sbin/groupadd
BuildRequires:  /bin/bash
BuildRequires:  /bin/sh
BuildRequires:  /bin/chown
BuildRequires:  ncurses-devel
BuildRequires:  libaio-devel
BuildRequires:  bison

Requires:       ncurses
Requires:       pcre
Requires:       numactl-libs
Requires:       numactl
Requires:       libaio

BuildRoot:      %{_topdir}/BUILDROOT

# %define _prefix /app/mysql
# %define _datadir /app/mysql/data
# %define MYSQL_USER mysql
# %define MYSQL_GROUP mysql
# %define mysql_conf /etc/my.cnf
# %define mysql_server /usr/lib/systemd/system/mysqld.service
# %define mysqld /etc/init.d/mysqld

%define _prefix /usr
%define _datadir /var/lib/mysql
%define MYSQL_USER mysql
%define MYSQL_GROUP mysql
%define mysql_conf /etc/my.cnf
%define mysql_server /usr/lib/systemd/system/mysqld.service
%define mysqld /etc/init.d/mysqld



%description
The MySQL(TM) software delivers a very fast, multi-threaded, multi-user, 
and robust SQL (Structured Query Language) database server. MySQL Server 
is intended for mission-critical, heavy-load production systems as well 
as for embedding into mass-deployed software.

%prep
%setup -q -n %{name}-%{version}

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
    -DWITH_EMBEDDED_SERVER=0 \
    -DEXTRA_CHARSETS=all \
    -DWITH_ZLIB=bundled \
    -DWITH_SSL=system \
    -DWITH_NUMA=ON

make -j$(nproc)

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

%{__install} -p -D -m 0644 %{SOURCE1} %{buildroot}/etc/my.cnf
%{__install} -p -D -m 0755 %{SOURCE2} %{buildroot}/usr/lib/systemd/system/mysqld.service
%{__install} -p -D -m 0755 %{buildroot}/%{_prefix}/support-files/mysql.server %{buildroot}/etc/init.d/mysqld

%pre
getent group %{MYSQL_GROUP} >/dev/null || groupadd -r %{MYSQL_GROUP}
getent passwd %{MYSQL_USER} >/dev/null || useradd -r -g %{MYSQL_GROUP} -s /sbin/nologin -d %{_prefix} -M %{MYSQL_USER}

%post
systemctl enable mysqld
%{_prefix}/bin/mysqld --initialize-insecure --basedir=%{_prefix} --datadir=%{_datadir} --user=%{MYSQL_USER}
%{_prefix}/bin/mysql_ssl_rsa_setup --uid=%{MYSQL_USER}
chown -R %{MYSQL_USER}:%{MYSQL_GROUP} %{_prefix}
systemctl start mysqld

%preun
systemctl stop mysqld
systemctl disable mysqld

%postun
userdel -r %{MYSQL_USER} >/dev/null 2>&1 || :
groupdel %{MYSQL_GROUP} >/dev/null 2>&1 || :
rm -rf %{_prefix} %{_datadir} %{mysql_conf} %{mysql_server} %{mysqld} /var/run/mysqld.pid >/dev/null 2>&1 || :

%files
%defattr(-,mysql,mysql)
%doc
%{_prefix}
%{mysql_conf}
%{mysqld}
%{mysql_server}

%changelog
* Wed Jun 05 2024 Your Name <you@example.com> - 5.7.43-1
- Initial package

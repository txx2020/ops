This is a typical database for Brownfield Airlines.

Get image:
download Dockerfile docker pull rohitbasu77/oracle11g:latest

Run Container:
docker run -d --name oracle11g -p 40022:22 -p 41521:1521 -p 48080:8080 rohitbasu77/oracle11g:latest

Connect database:
hostname: localhost or docker machine ip
port: 41521
sid: xe
username: system
password: oracle
Password for SYS & SYSTEM is oracle
Password for fareuser, searchuser, bookinguser, checkinuser is rohit123

Login by SSH:
ssh root@docker_machine_ip -p 40022

password: admin
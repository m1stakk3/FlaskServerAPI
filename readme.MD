# Project info

Simple Flask server with API and static site. When launched get **ip:port/api** to read docs.

---
# How to launch?

1. Install Docker Engine
2. Build image: **docker build . -t flask-app:v0.1**
3. Check container id by **docker images** and copy it
4. Run container: **docker run -p local_pc_port:8999 -d *cont_id***
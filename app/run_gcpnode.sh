sudo docker build -t diplay-stock .
sudo docker container run -d -e PORT=80 -e ALLOWED_HOSTS=35.233.248.252 -p 80:80 display-stock

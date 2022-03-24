# mercury-exporter-docker

run in docker
```
docker run -d -it -p 3000:3000 -e mercury_rpc=http://mercury-mainnet.ckbapp.dev jiangxianliang/mercury-exporter:0.1

curl http://127.0.0.1:3000/metrics/mercury
```

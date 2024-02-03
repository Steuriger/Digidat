HOWTO BUILD and RUN

docker build -t yourimagename .

docker run -p 127.0.0.1:5000:5000 yourimagename


Test:

someBrowser http://127.0.0.1:5000

------------------------------------------------

Online Image:

docker pull steuriger/opensensemap:digidat

docker run -d steuriger/opensensemap:digidat

Test (not working (tg)):

????someBrowser http://127.0.0.1:5000???

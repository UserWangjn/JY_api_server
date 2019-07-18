pip install -r req.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

taskkill /F /IM python.exe /t
rmdir /s /q api_server

git clone http://172.16.101.32/TD/Automatic/api_server.git

cd api_server
python run.py
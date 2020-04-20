import requests,time
name=input("请输入e学堂用户名：")
passwd=input("请输入密码：")
url='http://wrggka.whvcse.edu.cn/api/M_User/Login?username='+name+'&password='+passwd+'&accessKey=1&secretKey=1'
res = requests.get(url).json()
user=res['trueName']
print('正在为您刷课......')
time.sleep(10) 
print('你好'+user+'，作业自己做')
input('输入任意字符回车结束窗口')

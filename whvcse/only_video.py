print('说明：本程序为交流Python学习使用，禁止外传，禁止用于违规用途，禁止商业用途;若因使用本程序造成违法行为，本人概不负责')
import requests,json,time,random
from jsonpath import jsonpath
name=input("请输入你的用户名：")
cloud=int(name)                                        #重新定义一个变量，将name进行数据类型转换，用于判断是否在指定学号内
while cloud<2018030830 or cloud>2018030876:
    print('对不起，仅限云计算1801使用')
    input('请关闭本程序')

passwd=input("请输入密码：")
url="http://wrggka.whvcse.edu.cn/api/M_User/Login?username="+name+"&password="+passwd+"&accessKey=1&secretKey=1"
res = requests.get(url).json()
#print(res)
#登录状态
status=res['status']
#print(status)

#错误循环
while status!='1':
    name = input('用户名或密码错误,请重新输入用户名：')
    passwd = input('请输入密码：')
    url ="http://wrggka.whvcse.edu.cn/api/M_User/Login?username="+name+"&password="+passwd+"&accessKey=1&secretKey=1"
    res = requests.get(url).json()
    status = res['status']              #这里要对状态重新赋值，否则会陷入死循环

#初始化信息
user=res['trueName']
uid=res['uid']
url = "http://wrggka.whvcse.edu.cn/api/M_Semester/GetStudentLearningRecord?studentId=" + uid + "&accessKey=0&secretKey=0"
res_class=requests.get(url).json()
#print(res_class)

passedCourseCount=res_class['passedCourseCount']
acquisitionCrdicts=res_class['acquisitionCrdicts']
class_num=len(res_class['courseList'])    #获取课程列表长度，即所选课程数
print('你好'+user+'\n你总共选课：'+str (class_num)+'门；'+'\n已通过：'+str (passedCourseCount)+'门，'+'\n获得学分：'+str(acquisitionCrdicts))  #这几个类型一定要加str ！！！

#获取课程状态
i=0
while i<class_num :
    class_name=res_class['courseList'][i]['courseName']      #课程名
    class_success=res_class['courseList'][i]['isNoSuccess']  #通过状态
    semesterName=res_class['courseList'][i]['semesterName']  #学期
    print('编号：'+str(i)+'；课程名：' + class_name + '；状态：' + class_success+'；学期：'+semesterName)
    i=i+1

text=input('请输入您要刷的课程编号，用空格作分隔符：')
text_end=text.split(" ") #split函数：分隔符对字符串进行切片；转化为列表，使len函数能读出元素个数；在这里使用空格作为分隔符，这样就可以不用考虑输入法状态了~
#print(text_end)
text_long=len(text_end)
#print(text_long)
#print(text_end[0])
k=0
while k<text_long:
    y=int(text_end[k])
    class_name = res_class['courseList'][y]['courseName']  # 课程名
    class_success = res_class['courseList'][y]['isNoSuccess']  # 通过状态
    print("正在刷<" + str(class_name) + ">.......")
    if class_success == '未通过':
        courseId = res_class['courseList'][y]['courseId']
        courseClassId = res_class['courseList'][y]['courseClassId']
        url = "http://wrggka.whvcse.edu.cn/api/M_Course/GetCourseSPZT?userId=" + str(uid) + "&courseId=" + str(courseId) + "&courseClassId=" + str(courseClassId) + "&accessKey=1&secretKey=1"
        r = requests.get(url).json()
        resID = jsonpath(r, "$..resID")
        videoID = list(set(resID))
        vidnum = len(videoID)
        x = 0
        while x < vidnum:
            videoID_num = videoID[x]
            print('正在完成第：' + str(x + 1) + '/' + str(vidnum) + '个资源')
            videotime = random.randint(150, 700)
            url = "http://wrggka.whvcse.edu.cn/api/M_Course/IsNoStudyvideo?userId=" + str(uid) + "&videoid=" + str(
                videoID_num) + "&videotime=" + str(videotime) + "&accessKey=1&secretKey=1"
            time.sleep(0.1)  # ip防封
            res_video = requests.get(url).json()
            status_video = res['status']
            if status_video == '1':
                print('提交成功')
            else:
                print('提交失败')
            x = x + 1
    print("该课程视频已全部完成")
    k= k + 1
print('视频已全部看完')
time.sleep(1000)
input("请关闭窗口")

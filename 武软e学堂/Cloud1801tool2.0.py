print('       ___                        ___ _                                        ')
print('      / __\__  _ __ _ __ ___     / __\ |__   ___ _ __   __ _ _   _ _   _  ___  ')
print('''     / _\/ _ \| '__| '_ ` _ \   / /  | '_ \ / _ \ '_ \ / _` | | | | | | |/ _ \     ''')
print('    / / | (_) | |  | | | | | | / /___| | | |  __/ | | | (_| | |_| | |_| |  __/ ')
print('    \/   \___/|_|  |_| |_| |_| \____/|_| |_|\___|_| |_|\__, |\__, |\__,_|\___| ')
print('                                                       |___/ |___/             ')
print('说明：本程序为云计算1801班交流Python学习使用，禁止外传，禁止用于违规用途，禁止商业用途;\n若因使用本程序造成违法行为，本人概不负责')
import requests,json,time,random
from jsonpath import jsonpath
name=input("请输入你的用户名：")
cloud=int(name)                                        #重新定义一个变量，将name进行数据类型转换，用于判断是否在指定学号内
while cloud<2018030830 or cloud>2018030876:
    print('对不起，仅限云计算1801使用')
    input('请关闭本程序')


passwd=input("请输入密码：")
url='http://wrggka.whvcse.edu.cn/api/M_User/Login?username='+name+'&password='+passwd+'&accessKey=1&secretKey=1'
res = requests.get(url).json()
#print(res)
#登录状态
status=res['status']
# print(status)

#错误循环
while status!='1':
    name = input('用户名或密码错误,请重新输入用户名：')
    passwd = input('请输入密码：')
    url = 'http://wrggka.whvcse.edu.cn/api/M_User/Login?username=' + name + '&password=' + passwd + '&accessKey=1&secretKey=1'
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
print('你好'+user+'\n你总共选课：'+str (class_num)+'门；'+'\n已通过：'+str (passedCourseCount)+'门，'+'\n获得学分：'+str(acquisitionCrdicts))  #这几个类型一定要加str进行类型转换！！

#获取课程状态
i=0
while i<class_num :
    class_name=res_class['courseList'][i]['courseName']      #课程名
    class_success=res_class['courseList'][i]['isNoSuccess']  #通过状态
    print('课程名：' + class_name + '；状态：' + class_success)
    i=i+1

input('确认无误后按回车键继续')
y=0
while y < class_num:
    class_name = res_class['courseList'][y]['courseName']  # 课程名
    class_success = res_class['courseList'][y]['isNoSuccess']  # 通过状态
    if class_success=='未通过':
        print("正在刷："+str(class_name))
        courseId= res_class['courseList'][y]['courseId']
        courseClassId=res_class['courseList'][y]['courseClassId']
        url = "http://wrggka.whvcse.edu.cn/api/M_Course/GetCourseSPZT?userId=" + str(uid) + "&courseId=" + str(courseId)+ "&courseClassId=" + str(courseClassId) + "&accessKey=1&secretKey=1"
        r = requests.get(url).json()
        resID = jsonpath(r, "$..resID")
        videoID = list(set(resID))
        vidnum = len(videoID)
        x=0
        while x<vidnum:
            videoID_num=videoID[x]
            print('视频编号：'+videoID_num)
            videotime=random.randint(150, 700)
            url="http://wrggka.whvcse.edu.cn/api/M_Course/IsNoStudyvideo?userId="+str(uid)+"&videoid="+str(videoID_num)+"&videotime="+str(videotime)+"&accessKey=1&secretKey=1"
            time.sleep(1)
            res_video=requests.get(url).json()
            status_video = res['status']
            if status_video=='1':
                print('提交成功')
            else:
                print('提交失败')
            x=x+1
    y=y+1
input('视频已全部看完，按回车开始做题')
negriuwg=0
while negriuwg < class_num:
    class_name = res_class['courseList'][negriuwg]['courseName']  # 课程名
    class_success = res_class['courseList'][negriuwg]['isNoSuccess']  # 通过状态
    if class_success=='未通过':
        print("正在进行<"+str(class_name)+">的考试")
        courseId = res_class['courseList'][negriuwg]['courseId']
        courseClassId = res_class['courseList'][negriuwg]['courseClassId']
        url = "http://wrggka.whvcse.edu.cn/api/M_Course/GetCourseSPZT?userId="+str(uid)+"&courseId="+str(courseId)+"&courseClassId="+str(courseClassId)+"&accessKey=1&secretKey=1"  # get paperID
        res_paper = requests.get(url).json()
        tesID = jsonpath(res_paper, "$..testID")
        # print(tesID)
        paper1 = tesID[0]
        paper2 = tesID[1]
        print('正在初始化<'+str(class_name)+'>的第一张试卷...')
        time.sleep(1)
        url = "http://wrggka.whvcse.edu.cn/api/M_Course/GetChapterTestInfo?userId=3689&courseId=734&courseClassId=477&chapterId=0&paperId=" + paper1 + "&accessKey=1&secretKey=1"  # get examCountID
        res_test = requests.get(url).json()
        # print(res_test)
        examID = str(jsonpath(res_test, "$..examCountId"))
        examID = examID[0]
        # print('这是examID'+str(examID))
        url = "http://wrggka.whvcse.edu.cn/api/M_Course/GetPaperQuestions3?paperId=" + paper1 + "&accessKey=1&secretKey=1"  # get question_info
        res_question = requests.get(url).json()
        #print(res_question)
        # 单选
        print("正在做单选题......")
        y = []
        for i in res_question:  # 判断单选题题目类型；顺序输出
            if i['ItemType'] == '1':
                y.append(i['ItemID'])
        chang = len(y)
        # print(chang)
        q = 0
        while q < chang:
            d = 0
            questionID = y[q]  # 第q个题目ID
            print('第' + str(q + 1) + '个题目ID为：' + questionID)
            stay = res_question[q]['ItemOptions'][d]['ItemIsCorrect']  # 正确答案所在的数组的定位 q值和d值
            # print((stay))
            while stay != '1':
                d = d + 1
                stay = res_question[q]['ItemOptions'][d]['ItemIsCorrect']
                # print(stay)
            answerID = res_question[q]['ItemOptions'][d]['ItemID']  # 答案ID
            print('第' + str(q + 1) + '个答案ID为：' + answerID)
            url = "http://wrggka.whvcse.edu.cn/api/M_Course/SubmitQuestionAnswer2?userId="+str(uid)+"&courseClassId=" + str(courseClassId) + "&courseId=" + str(courseId) + "&chapterId=0&paperId=" + str(paper1) + "&questionId=" + str(questionID) + "&examTimes=0&examCountId=" + str(examID) + "&userAnswers=" + str(answerID) + "&accessKey=1&secretKey=1"
            res = requests.get(url).json()
            # print(res)
            status_test = res['result']
            if status_test == '1':
                print('提交成功')
            else:
                print('提交失败')
            q = q + 1

        print("正在做多选题......")
        z = []
        for i in res_question:  # 判断多选题目类型；顺序输出
            if i['ItemType'] == '2':
                z.append(i['ItemID'])
        # print(z)
        chang_duo = len(z)
        # print(chang_duo)

        q = 0
        while q < chang_duo:
            g = ''  # 在每次循环之前都要初始化g变量
            d = 0
            questionID = z[q]  # 第q个题目ID
            print('第' + str(q + 1) + '个题目ID为：' + questionID)
            stay = res_question[q + chang]['ItemOptions'][d]['ItemIsCorrect']  # 正确答案所在的数组的定位 q值和d值
            test_long=len(res_question[q+chang]['ItemOptions'])
            print(test_long)
            if test_long=='5':
                if stay == '1':  # 这是一个巨他妈傻逼的算法，有很大的局限性
                    answerID = res_question[q + chang]['ItemOptions'][d]['ItemID']
                    g = answerID + ','
                    # print('答案为：' + str(answerID))
                    d = d + 1
                    stay = res_question[q + chang]['ItemOptions'][d]['ItemIsCorrect']
                else:
                    d = d + 1
                    stay = res_question[q + chang]['ItemOptions'][d]['ItemIsCorrect']
                if stay == '1':
                    answerID = res_question[q + chang]['ItemOptions'][d]['ItemID']
                    g = g + ',' + answerID
                    # print('答案为：' + str(answerID))
                    d = d + 1
                    stay = res_question[q + chang]['ItemOptions'][d]['ItemIsCorrect']
                else:
                    d = d + 1
                    stay = res_question[q + chang]['ItemOptions'][d]['ItemIsCorrect']
                if stay == '1':
                    answerID = res_question[q + chang]['ItemOptions'][d]['ItemID']
                    g = g + ',' + answerID
                    d = d + 1
                    stay = res_question[q + chang]['ItemOptions'][d]['ItemIsCorrect']
                    # print('答案为：' + str(answerID))
                else:
                    d = d + 1
                    stay = res_question[q + chang]['ItemOptions'][d]['ItemIsCorrect']
                if stay == '1':
                    answerID = res_question[q + chang]['ItemOptions'][d]['ItemID']
                    g = g + ',' + answerID
                    d = d + 1
                    stay = res_question[q + chang]['ItemOptions'][d]['ItemIsCorrect']
                else:
                    d = d + 1
                    stay = res_question[q + chang]['ItemOptions'][d]['ItemIsCorrect']
                if stay == '1':
                    answerID = res_question[q + chang]['ItemOptions'][d]['ItemID']
                    g = g + ',' + answerID
                    print('答案为：' + str(g[1:]))
                    url = "http://wrggka.whvcse.edu.cn/api/M_Course/SubmitQuestionAnswer2?userId=" + str(uid) + "&courseClassId=" + str(courseClassId) + "&courseId=" + str(courseId) + "&chapterId=0&paperId=" + str(paper1) + "&questionId=" + str(questionID) + "&examTimes=0&examCountId=" + str(examID) + "&userAnswers=" + str(g[1:]) + "&accessKey=1&secretKey=1"
                    res = requests.get(url).json()
                    status_test = res['result']
                    if status_test == '1':
                        print('提交成功')
                    else:
                        print('提交失败')
                else:
                    print('答案为：' + str(g[1:]))
                    url = "http://wrggka.whvcse.edu.cn/api/M_Course/SubmitQuestionAnswer2?userId=" + str(uid) + "&courseClassId=" + str(courseClassId) + "&courseId=" + str(courseId) + "&chapterId=0&paperId=" + str(paper1) + "&questionId=" + str(questionID) + "&examTimes=0&examCountId=" + str(examID) + "&userAnswers=" + str(g[1:]) + "&accessKey=1&secretKey=1"
                    res = requests.get(url).json()
                    status_test = res['result']
                    if status_test == '1':
                        print('提交成功')
                    else:
                        print('提交失败')
            q = q + 1
            if test_long=='4':
                if stay == '1':  # 这是一个巨他妈傻逼的算法，有很大的局限性
                    answerID = res_question[q + chang]['ItemOptions'][d]['ItemID']
                    g = answerID + ','
                    # print('答案为：' + str(answerID))
                    d = d + 1
                    stay = res_question[q + chang]['ItemOptions'][d]['ItemIsCorrect']
                else:
                    d = d + 1
                    stay = res_question[q + chang]['ItemOptions'][d]['ItemIsCorrect']
                if stay == '1':
                    answerID = res_question[q + chang]['ItemOptions'][d]['ItemID']
                    g = g + ',' + answerID
                    d = d + 1
                    stay = res_question[q + chang]['ItemOptions'][d]['ItemIsCorrect']
                    # print('答案为：' + str(answerID))
                else:
                    d = d + 1
                    stay = res_question[q + chang]['ItemOptions'][d]['ItemIsCorrect']
                if stay == '1':
                    answerID = res_question[q + chang]['ItemOptions'][d]['ItemID']
                    g = g + ',' + answerID
                    d = d + 1
                    stay = res_question[q + chang]['ItemOptions'][d]['ItemIsCorrect']
                    # print('答案为：' + str(answerID))
                else:
                    d = d + 1
                    stay = res_question[q + chang]['ItemOptions'][d]['ItemIsCorrect']
                if stay == '1':
                    answerID = res_question[q + chang]['ItemOptions'][d]['ItemID']
                    g = g + ',' + answerID
                    print('答案为：' + str(g[1:]))
                    url = "http://wrggka.whvcse.edu.cn/api/M_Course/SubmitQuestionAnswer2?userId=" + str(uid) + "&courseClassId=" + str(courseClassId) + "&courseId=" + str(courseId) + "&chapterId=0&paperId=" + str(paper1) + "&questionId=" + str(questionID) + "&examTimes=0&examCountId=" + str(examID) + "&userAnswers=" + str(g[1:]) + "&accessKey=1&secretKey=1"
                    res = requests.get(url).json()
                    status_test = res['result']
                    if status_test == '1':
                        print('提交成功')
                    else:
                        print('提交失败')
                else:
                    print('答案为：' + str(g[1:]))
                    url = "http://wrggka.whvcse.edu.cn/api/M_Course/SubmitQuestionAnswer2?userId=" + str(uid) + "&courseClassId=" + str(courseClassId) + "&courseId=" + str(courseId) + "&chapterId=0&paperId=" + str(paper1) + "&questionId=" + str(questionID) + "&examTimes=0&examCountId=" + str(examID) + "&userAnswers=" + str(g[1:]) + "&accessKey=1&secretKey=1"
                    res = requests.get(url).json()
                    status_test = res['result']
                    if status_test == '1':
                        print('提交成功')
                    else:
                        print('提交失败')
            q = q + 1
        print("正在做判断题......")
        o = []
        for i in res_question:  # 判断判断题目类型；顺序输出
            if i['ItemType'] == '6':
                o.append(i['ItemID'])
        print(o)
        chang_pan = len(o)
        # print(chang)
        q = 0
        while q < chang_pan:
            d = 0
            questionID = o[q]  # 第q个题目ID
            print('第' + str(q + 1) + '个题目ID为：' + questionID)
            stay = res_question[q + chang + chang_duo]['ItemOptions'][d]['ItemIsCorrect']  # 正确答案所在的数组的定位 q值和d值
            # print((stay))
            while stay != '1':
                d = d + 1
                stay = res_question[q + chang + chang_duo]['ItemOptions'][d]['ItemIsCorrect']
                # print(stay)
            answerID = res_question[q + chang + chang_duo]['ItemOptions'][d]['ItemID']  # 答案ID
            print('第' + str(q + 1) + '个答案ID为：' + answerID)
            url = "http://wrggka.whvcse.edu.cn/api/M_Course/SubmitQuestionAnswer2?userId=" + str(uid) + "&courseClassId=" + str(courseClassId) + "&courseId=" + str(courseId) + "&chapterId=0&paperId=" + str(paper1) + "&questionId=" + str(questionID) + "&examTimes=1&examCountId=" + str(examID) + "&userAnswers=" + str(answerID) + "&accessKey=1&secretKey=1"
            res = requests.get(url).json()
            # print(res)
            status_test = res['result']
            if status_test == '1':
                print('提交成功')
            else:
                print('提交失败')
            q = q + 1
        # 提交试卷
        url = "http://wrggka.whvcse.edu.cn/api/M_Course/SubmitPaper?userId=" + str(uid) + "&courseClassId=" + str(courseClassId) + "&courseId=" + str(courseId) + "&chapterId=0&paperId=" + str(paper1) + "&accessKey=1&secretKey=1"
        res = requests.get(url).json()
        print(res)
        print('正在初始化<'+str(class_name)+'>的第二张试卷...')
        time.sleep(1)
        url = "http://wrggka.whvcse.edu.cn/api/M_Course/GetChapterTestInfo?userId=3689&courseId=734&courseClassId=477&chapterId=0&paperId=" + paper2 + "&accessKey=1&secretKey=1"  # get examCountID
        res_test = requests.get(url).json()
        # print(res_test)
        examID = str(jsonpath(res_test, "$..examCountId"))
        examID = examID[0]
        # print('这是examID'+str(examID))
        url = "http://wrggka.whvcse.edu.cn/api/M_Course/GetPaperQuestions3?paperId=" + paper2 + "&accessKey=1&secretKey=1"  # get question_info
        res_question = requests.get(url).json()
        # print(res_question)
        # 单选
        print("正在做单选题......")
        y = []
        for i in res_question:  # 判断单选题题目类型；顺序输出
            if i['ItemType'] == '1':
                y.append(i['ItemID'])
        chang = len(y)
        # print(chang)
        q = 0
        while q < chang:
            d = 0
            questionID = y[q]  # 第q个题目ID
            print('第' + str(q + 1) + '个题目ID为：' + questionID)
            stay = res_question[q]['ItemOptions'][d]['ItemIsCorrect']  # 正确答案所在的数组的定位 q值和d值
            # print((stay))
            while stay != '1':
                d = d + 1
                stay = res_question[q]['ItemOptions'][d]['ItemIsCorrect']
                # print(stay)
            answerID = res_question[q]['ItemOptions'][d]['ItemID']  # 答案ID
            print('第' + str(q + 1) + '个答案ID为：' + answerID)
            url = "http://wrggka.whvcse.edu.cn/api/M_Course/SubmitQuestionAnswer2?userId=" + str(
                uid) + "&courseClassId=" + str(courseClassId) + "&courseId=" + str(
                courseId) + "&chapterId=0&paperId=" + str(paper2) + "&questionId=" + str(
                questionID) + "&examTimes=0&examCountId=" + str(examID) + "&userAnswers=" + str(
                answerID) + "&accessKey=1&secretKey=1"
            res = requests.get(url).json()
            # print(res)
            status_test = res['result']
            if status_test == '1':
                print('提交成功')
            else:
                print('提交失败')
            q = q + 1

        print("正在做多选题......")
        z = []
        for i in res_question:  # 判断多选题目类型；顺序输出
            if i['ItemType'] == '2':
                z.append(i['ItemID'])
        # print(z)
        chang_duo = len(z)
        # print(chang_duo)

        q = 0
        while q < chang_duo:
            g = ''  # 在每次循环之前都要初始化g变量
            d = 0
            questionID = z[q]  # 第q个题目ID
            print('第' + str(q + 1) + '个题目ID为：' + questionID)
            stay = res_question[q + chang]['ItemOptions'][d]['ItemIsCorrect']  # 正确答案所在的数组的定位 q值和d值
            test_long = len(res_question[q + chang]['ItemOptions'])
            print(test_long)
            if test_long == '5':
                if stay == '1':  # 这是一个巨他妈傻逼的算法，有很大的局限性
                    answerID = res_question[q + chang]['ItemOptions'][d]['ItemID']
                    g = answerID + ','
                    # print('答案为：' + str(answerID))
                    d = d + 1
                    stay = res_question[q + chang]['ItemOptions'][d]['ItemIsCorrect']
                else:
                    d = d + 1
                    stay = res_question[q + chang]['ItemOptions'][d]['ItemIsCorrect']
                if stay == '1':
                    answerID = res_question[q + chang]['ItemOptions'][d]['ItemID']
                    g = g + ',' + answerID
                    # print('答案为：' + str(answerID))
                    d = d + 1
                    stay = res_question[q + chang]['ItemOptions'][d]['ItemIsCorrect']
                else:
                    d = d + 1
                    stay = res_question[q + chang]['ItemOptions'][d]['ItemIsCorrect']
                if stay == '1':
                    answerID = res_question[q + chang]['ItemOptions'][d]['ItemID']
                    g = g + ',' + answerID
                    d = d + 1
                    stay = res_question[q + chang]['ItemOptions'][d]['ItemIsCorrect']
                    # print('答案为：' + str(answerID))
                else:
                    d = d + 1
                    stay = res_question[q + chang]['ItemOptions'][d]['ItemIsCorrect']
                if stay == '1':
                    answerID = res_question[q + chang]['ItemOptions'][d]['ItemID']
                    g = g + ',' + answerID
                    d = d + 1
                    stay = res_question[q + chang]['ItemOptions'][d]['ItemIsCorrect']
                else:
                    d = d + 1
                    stay = res_question[q + chang]['ItemOptions'][d]['ItemIsCorrect']
                if stay == '1':
                    answerID = res_question[q + chang]['ItemOptions'][d]['ItemID']
                    g = g + ',' + answerID
                    print('答案为：' + str(g[1:]))
                    url = "http://wrggka.whvcse.edu.cn/api/M_Course/SubmitQuestionAnswer2?userId=" + str(
                        uid) + "&courseClassId=" + str(courseClassId) + "&courseId=" + str(
                        courseId) + "&chapterId=0&paperId=" + str(paper2) + "&questionId=" + str(
                        questionID) + "&examTimes=0&examCountId=" + str(examID) + "&userAnswers=" + str(
                        g[1:]) + "&accessKey=1&secretKey=1"
                    res = requests.get(url).json()
                    status_test = res['result']
                    if status_test == '1':
                        print('提交成功')
                    else:
                        print('提交失败')
                else:
                    print('答案为：' + str(g[1:]))
                    url = "http://wrggka.whvcse.edu.cn/api/M_Course/SubmitQuestionAnswer2?userId=" + str(
                        uid) + "&courseClassId=" + str(courseClassId) + "&courseId=" + str(
                        courseId) + "&chapterId=0&paperId=" + str(paper2) + "&questionId=" + str(
                        questionID) + "&examTimes=0&examCountId=" + str(examID) + "&userAnswers=" + str(
                        g[1:]) + "&accessKey=1&secretKey=1"
                    res = requests.get(url).json()
                    status_test = res['result']
                    if status_test == '1':
                        print('提交成功')
                    else:
                        print('提交失败')
            q = q + 1
            if test_long == '4':
                if stay == '1':  # 这是一个巨他妈傻逼的算法，有很大的局限性
                    answerID = res_question[q + chang]['ItemOptions'][d]['ItemID']
                    g = answerID + ','
                    # print('答案为：' + str(answerID))
                    d = d + 1
                    stay = res_question[q + chang]['ItemOptions'][d]['ItemIsCorrect']
                else:
                    d = d + 1
                    stay = res_question[q + chang]['ItemOptions'][d]['ItemIsCorrect']
                if stay == '1':
                    answerID = res_question[q + chang]['ItemOptions'][d]['ItemID']
                    g = g + ',' + answerID
                    d = d + 1
                    stay = res_question[q + chang]['ItemOptions'][d]['ItemIsCorrect']
                    # print('答案为：' + str(answerID))
                else:
                    d = d + 1
                    stay = res_question[q + chang]['ItemOptions'][d]['ItemIsCorrect']
                if stay == '1':
                    answerID = res_question[q + chang]['ItemOptions'][d]['ItemID']
                    g = g + ',' + answerID
                    d = d + 1
                    stay = res_question[q + chang]['ItemOptions'][d]['ItemIsCorrect']
                    # print('答案为：' + str(answerID))
                else:
                    d = d + 1
                    stay = res_question[q + chang]['ItemOptions'][d]['ItemIsCorrect']
                if stay == '1':
                    answerID = res_question[q + chang]['ItemOptions'][d]['ItemID']
                    g = g + ',' + answerID
                    print('答案为：' + str(g[1:]))
                    url = "http://wrggka.whvcse.edu.cn/api/M_Course/SubmitQuestionAnswer2?userId=" + str(
                        uid) + "&courseClassId=" + str(courseClassId) + "&courseId=" + str(
                        courseId) + "&chapterId=0&paperId=" + str(paper2) + "&questionId=" + str(
                        questionID) + "&examTimes=0&examCountId=" + str(examID) + "&userAnswers=" + str(
                        g[1:]) + "&accessKey=1&secretKey=1"
                    res = requests.get(url).json()
                    status_test = res['result']
                    if status_test == '1':
                        print('提交成功')
                    else:
                        print('提交失败')
                else:
                    print('答案为：' + str(g[1:]))
                    url = "http://wrggka.whvcse.edu.cn/api/M_Course/SubmitQuestionAnswer2?userId=" + str(
                        uid) + "&courseClassId=" + str(courseClassId) + "&courseId=" + str(
                        courseId) + "&chapterId=0&paperId=" + str(paper2) + "&questionId=" + str(
                        questionID) + "&examTimes=0&examCountId=" + str(examID) + "&userAnswers=" + str(
                        g[1:]) + "&accessKey=1&secretKey=1"
                    res = requests.get(url).json()
                    status_test = res['result']
                    if status_test == '1':
                        print('提交成功')
                    else:
                        print('提交失败')
            q = q + 1

        print("正在做判断题......")
        o = []
        for i in res_question:  # 判断判断题目类型；顺序输出
            if i['ItemType'] == '6':
                o.append(i['ItemID'])
        print(o)
        chang_pan = len(o)
        # print(chang)
        q = 0
        while q < chang_pan:
            d = 0
            questionID = o[q]  # 第q个题目ID
            print('第' + str(q + 1) + '个题目ID为：' + questionID)
            stay = res_question[q + chang + chang_duo]['ItemOptions'][d]['ItemIsCorrect']  # 正确答案所在的数组的定位 q值和d值
            # print((stay))
            while stay != '1':
                d = d + 1
                stay = res_question[q + chang + chang_duo]['ItemOptions'][d]['ItemIsCorrect']
                # print(stay)
            answerID = res_question[q + chang + chang_duo]['ItemOptions'][d]['ItemID']  # 答案ID
            print('第' + str(q + 1) + '个答案ID为：' + answerID)
            url = "http://wrggka.whvcse.edu.cn/api/M_Course/SubmitQuestionAnswer2?userId=" + str(
                uid) + "&courseClassId=" + str(courseClassId) + "&courseId=" + str(
                courseId) + "&chapterId=0&paperId=" + str(paper2) + "&questionId=" + str(
                questionID) + "&examTimes=1&examCountId=" + str(examID) + "&userAnswers=" + str(
                answerID) + "&accessKey=1&secretKey=1"
            res = requests.get(url).json()
            # print(res)
            status_test = res['result']
            if status_test == '1':
                print('提交成功')
            else:
                print('提交失败')
            q = q + 1
        # 提交试卷
        url = "http://wrggka.whvcse.edu.cn/api/M_Course/SubmitPaper?userId=" + str(uid) + "&courseClassId=" + str(courseClassId) + "&courseId=" + str(courseId) + "&chapterId=0&paperId=" + str(paper2) + "&accessKey=1&secretKey=1"
        res = requests.get(url).json()
        print(res)
    negriuwg=negriuwg+1

input("所有视频考试均已完成，请关闭窗口")






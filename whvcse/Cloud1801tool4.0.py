print('说明：本程序为交流Python学习使用，禁止外传，禁止用于违规用途，禁止商业用途;若因使用本程序造成违法行为，本人概不负责')
import requests,json,time,random
from jsonpath import jsonpath

#判断学号范围
def get_class():
    name = input("请输入你的学号：")
    cloud = int(name)  # 重新定义一个变量，将name进行数据类型转换，用于判断是否在指定学号内
    if cloud <2017999999 or cloud > 2018000001:
        print('对不起，仅限**使用')
        input('请关闭本程序')
        exit(1)
    else:
        return name

#登录
def begin():
    #name=get_class()   判断学号范围
    name = input("请输入你的学号：")
    passwd=input("请输入密码：")
    url="http://wrggka.whvcse.edu.cn/api/M_User/Login?username="+name+"&password="+passwd+"&accessKey=1&secretKey=1"
    res = requests.get(url).json()
    status=res['status']           #获取登录状态
    while status!='1':             #错误循环
        name = input('用户名或密码错误,请重新输入用户名：')
        passwd = input('请输入密码：')
        url ="http://wrggka.whvcse.edu.cn/api/M_User/Login?username="+name+"&password="+passwd+"&accessKey=1&secretKey=1"
        res = requests.get(url).json()
        status = res['status']              #这里要对状态重新赋值，否则会陷入死循环
    return res

# 初始化信息
def first():
    user = res['trueName']
    uid = res['uid']
    url = "http://wrggka.whvcse.edu.cn/api/M_Semester/GetStudentLearningRecord?studentId=" + uid + "&accessKey=0&secretKey=0"
    res_class = requests.get(url).json()
    passedCourseCount = res_class['passedCourseCount']
    acquisitionCrdicts = res_class['acquisitionCrdicts']
    class_num = len(res_class['courseList'])  # 获取课程列表长度，即所选课程数
    print('你好' + user + '\n你总共选课：' + str(class_num) + '门；' + '\n已通过：' + str(passedCourseCount) + '门，' + '\n获得学分：' + str(acquisitionCrdicts))  # 这几个类型一定要加str ！！！
    return res_class,uid

#课程状态
def class_status():
    class_num = len(res_class['courseList'])  # 获取课程列表长度，即所选课程数
    i = 0
    while i < class_num:
        class_name = res_class['courseList'][i]['courseName']  # 课程名
        class_success = res_class['courseList'][i]['isNoSuccess']  # 通过状态
        semesterName = res_class['courseList'][i]['semesterName']  # 学期
        print( str(i) + '.' + class_name + '；状态：' + class_success + '；学期：' + semesterName)
        i = i + 1

#课程选择
def class_xz():
    text = input('请输入您将要完成的课程编号，用空格作分隔符：')
    text_end = text.split(" ")  # split函数：分隔符对字符串进行切片；转化为列表，使len函数能读出元素个数；在这里使用空格作为分隔符，这样就可以不用考虑输入法状态了~
    text_long = len(text_end)
    return text_end,text_long

#视频主函数
def class_video():
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

#考试主函数
def class_exam():
    print("正在进行<" + str(class_name) + ">的考试")
    courseId = res_class['courseList'][y]['courseId']
    courseClassId = res_class['courseList'][y]['courseClassId']
    url = "http://wrggka.whvcse.edu.cn/api/M_Course/GetCourseSPZT?userId=" + str(uid) + "&courseId=" + str(
        courseId) + "&courseClassId=" + str(courseClassId) + "&accessKey=1&secretKey=1"  # get paperID
    res_paper = requests.get(url).json()
    tesID = jsonpath(res_paper, "$..testID")
    # print(tesID)
    paper1 = tesID[0]
    paper2 = tesID[1]
    def first_exam():
        print('正在初始化<' + str(class_name) + '>的第'+str(cishu)+'张试卷...')
        url = "http://wrggka.whvcse.edu.cn/api/M_Course/GetChapterTestInfo?userId=" + str(uid) + "&courseId=" + str(
        courseId) + "&courseClassId=" + str(
        courseClassId) + "&chapterId=0&paperId=" + paper + "&accessKey=1&secretKey=1"  # get examCountID
        res_test = requests.get(url).json()
        # print(res_test)
        examID = str(jsonpath(res_test, "$..examCountId"))
        examID = examID[0]
        # print('这是examID'+str(examID))
        url = "http://wrggka.whvcse.edu.cn/api/M_Course/GetPaperQuestions3?paperId=" + paper + "&accessKey=1&secretKey=1"  # get question_info
        res_question = requests.get(url).json()
        # print(res_question)
        # 单选
        print("正在做单选题......")
        y = []
        t = []
        for i in res_question:  # 判断单选题题目类型；顺序输出
            if i['ItemType'] == '1':
                y.append(i['ItemID'])
                t.append(i['ItemTitle'])
        chang = len(y)
        # print(chang)
        q = 0
        while q < chang:
            d = 0
            questionID = y[q]  # 第q个题目ID
            questionText = t[q]
            print('第' + str(q + 1) + '题为：' + questionText)
            stay = res_question[q]['ItemOptions'][d]['ItemIsCorrect']  # 正确答案所在的数组的定位 q值和d值
            # print((stay))
            try:
                while stay != '1':
                    d = d + 1
                    stay = res_question[q]['ItemOptions'][d]['ItemIsCorrect']
            except IndexError:
                print("此题异常终止！！！")
                q = q + 1
            else:
                answerID = res_question[q]['ItemOptions'][d]['ItemID']  # 答案ID
                answerText = res_question[q]['ItemOptions'][d]['ItemTitle']
                print('第' + str(q + 1) + '题答案为：' + answerText)
                url = "http://wrggka.whvcse.edu.cn/api/M_Course/SubmitQuestionAnswer2?userId=" + str(
                    uid) + "&courseClassId=" + str(courseClassId) + "&courseId=" + str(
                    courseId) + "&chapterId=0&paperId=" + str(paper) + "&questionId=" + str(
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
        t = []
        for i in res_question:  # 判断多选题目类型；顺序输出
            if i['ItemType'] == '2':
                z.append(i['ItemID'])
                t.append(i['ItemTitle'])
        # print("多选题ID："+str(z))
        chang_duo = len(z)
        # print("多选题数："+str(chang_duo))

        q = 0
        while q < chang_duo:
            g = ''  # 在每次循环之前都要初始化g变量
            Tt = ''
            d = 0
            questionID = z[q]  # 第q个题目ID
            questionText = t[q]
            print('第' + str(q + 1) + '题为：' + questionText)
            stay = res_question[q + chang]['ItemOptions'][d]['ItemIsCorrect']  # 正确答案所在的数组的定位 q值和d值
            test_long = len(res_question[q + chang]['ItemOptions'])
            # 以下是一个憨憨算法
            if test_long == 5:
                if stay == '1':
                    answerID = res_question[q + chang]['ItemOptions'][d]['ItemID']
                    answerText = res_question[q + chang]['ItemOptions'][d]['ItemTitle']
                    g = answerID + ','
                    Tt = answerText + ','
                    # print('答案为：' + str(answerID))
                    d = d + 1
                    stay = res_question[q + chang]['ItemOptions'][d]['ItemIsCorrect']
                else:
                    d = d + 1
                    stay = res_question[q + chang]['ItemOptions'][d]['ItemIsCorrect']
                if stay == '1':
                    answerID = res_question[q + chang]['ItemOptions'][d]['ItemID']
                    answerText = res_question[q + chang]['ItemOptions'][d]['ItemTitle']
                    g = g + answerID + ','
                    Tt = Tt + answerText + ','
                    # print('答案为：' + str(answerID))
                    d = d + 1
                    stay = res_question[q + chang]['ItemOptions'][d]['ItemIsCorrect']
                else:
                    d = d + 1
                    stay = res_question[q + chang]['ItemOptions'][d]['ItemIsCorrect']
                if stay == '1':
                    answerID = res_question[q + chang]['ItemOptions'][d]['ItemID']
                    answerText = res_question[q + chang]['ItemOptions'][d]['ItemTitle']
                    g = g + answerID + ','
                    Tt = Tt + answerText + ','
                    d = d + 1
                    stay = res_question[q + chang]['ItemOptions'][d]['ItemIsCorrect']
                    # print('答案为：' + str(answerID))
                else:
                    d = d + 1
                    stay = res_question[q + chang]['ItemOptions'][d]['ItemIsCorrect']
                if stay == '1':
                    answerID = res_question[q + chang]['ItemOptions'][d]['ItemID']
                    answerText = res_question[q + chang]['ItemOptions'][d]['ItemTitle']
                    g = g + answerID + ','
                    Tt = Tt + answerText + ','
                    d = d + 1
                    stay = res_question[q + chang]['ItemOptions'][d]['ItemIsCorrect']
                else:
                    d = d + 1
                    stay = res_question[q + chang]['ItemOptions'][d]['ItemIsCorrect']
                if stay == '1':
                    answerID = res_question[q + chang]['ItemOptions'][d]['ItemID']
                    answerText = res_question[q + chang]['ItemOptions'][d]['ItemTitle']
                    g = g + answerID
                    Tt = Tt + answerText
                    print('答案为：' + str(Tt))
                    url = "http://wrggka.whvcse.edu.cn/api/M_Course/SubmitQuestionAnswer2?userId=" + str(
                        uid) + "&courseClassId=" + str(courseClassId) + "&courseId=" + str(
                        courseId) + "&chapterId=0&paperId=" + str(paper) + "&questionId=" + str(
                        questionID) + "&examTimes=0&examCountId=" + str(examID) + "&userAnswers=" + str(
                        g) + "&accessKey=1&secretKey=1"
                    res = requests.get(url).json()
                    status_test = res['result']
                    if status_test == '1':
                        print('提交成功')
                    else:
                        print('提交失败')
                    q = q + 1
                else:
                    print('答案为：' + str(Tt[:-1]))  # 这个时候还是带了一个逗号
                    url = "http://wrggka.whvcse.edu.cn/api/M_Course/SubmitQuestionAnswer2?userId=" + str(
                        uid) + "&courseClassId=" + str(courseClassId) + "&courseId=" + str(
                        courseId) + "&chapterId=0&paperId=" + str(paper) + "&questionId=" + str(
                        questionID) + "&examTimes=0&examCountId=" + str(examID) + "&userAnswers=" + str(
                        g[:-1]) + "&accessKey=1&secretKey=1"
                    res = requests.get(url).json()
                    status_test = res['result']
                    if status_test == '1':
                        print('提交成功')
                    else:
                        print('提交失败')
                    q = q + 1
            if test_long == 4:
                if stay == '1':
                    answerID = res_question[q + chang]['ItemOptions'][d]['ItemID']
                    answerText = res_question[q + chang]['ItemOptions'][d]['ItemTitle']
                    g = answerID + ','
                    Tt = answerText + ','
                    # print('答案为：' + str(answerID))
                    d = d + 1
                    stay = res_question[q + chang]['ItemOptions'][d]['ItemIsCorrect']
                else:
                    d = d + 1
                    stay = res_question[q + chang]['ItemOptions'][d]['ItemIsCorrect']
                if stay == '1':
                    answerID = res_question[q + chang]['ItemOptions'][d]['ItemID']
                    answerText = res_question[q + chang]['ItemOptions'][d]['ItemTitle']
                    g = g + answerID + ','
                    Tt = Tt + answerText + ','
                    d = d + 1
                    stay = res_question[q + chang]['ItemOptions'][d]['ItemIsCorrect']
                    # print('答案为：' + str(answerID))
                else:
                    d = d + 1
                    stay = res_question[q + chang]['ItemOptions'][d]['ItemIsCorrect']
                if stay == '1':
                    answerID = res_question[q + chang]['ItemOptions'][d]['ItemID']
                    answerText = res_question[q + chang]['ItemOptions'][d]['ItemTitle']
                    g = g + answerID + ','
                    Tt = Tt + answerText + ','
                    d = d + 1
                    stay = res_question[q + chang]['ItemOptions'][d]['ItemIsCorrect']
                    # print('答案为：' + str(answerID))
                else:
                    d = d + 1
                    stay = res_question[q + chang]['ItemOptions'][d]['ItemIsCorrect']
                if stay == '1':
                    answerID = res_question[q + chang]['ItemOptions'][d]['ItemID']
                    answerText = res_question[q + chang]['ItemOptions'][d]['ItemTitle']
                    g = g + answerID
                    Tt = Tt + answerText
                    print('答案为：' + str(Tt))
                    url = "http://wrggka.whvcse.edu.cn/api/M_Course/SubmitQuestionAnswer2?userId=" + str(
                        uid) + "&courseClassId=" + str(courseClassId) + "&courseId=" + str(
                        courseId) + "&chapterId=0&paperId=" + str(paper) + "&questionId=" + str(
                        questionID) + "&examTimes=0&examCountId=" + str(examID) + "&userAnswers=" + str(
                        g) + "&accessKey=1&secretKey=1"
                    res = requests.get(url).json()
                    status_test = res['result']
                    if status_test == '1':
                        print('提交成功')
                    else:
                        print('提交失败')
                    q = q + 1
                else:
                    print('答案为：' + str(Tt[:-1]))
                    url = "http://wrggka.whvcse.edu.cn/api/M_Course/SubmitQuestionAnswer2?userId=" + str(
                        uid) + "&courseClassId=" + str(courseClassId) + "&courseId=" + str(
                        courseId) + "&chapterId=0&paperId=" + str(paper) + "&questionId=" + str(
                        questionID) + "&examTimes=0&examCountId=" + str(examID) + "&userAnswers=" + str(
                        g[-1]) + "&accessKey=1&secretKey=1"
                    res = requests.get(url).json()
                    status_test = res['result']
                    if status_test == '1':
                        print('提交成功')
                    else:
                        print('提交失败')
                    q = q + 1
            if test_long == 3:
                if stay == '1':
                    answerID = res_question[q + chang]['ItemOptions'][d]['ItemID']
                    answerText = res_question[q + chang]['ItemOptions'][d]['ItemTitle']
                    g = answerID + ','
                    Tt = answerText + ','
                    # print('答案为：' + str(answerID))
                    d = d + 1
                    stay = res_question[q + chang]['ItemOptions'][d]['ItemIsCorrect']
                else:
                    d = d + 1
                    stay = res_question[q + chang]['ItemOptions'][d]['ItemIsCorrect']
                if stay == '1':
                    answerID = res_question[q + chang]['ItemOptions'][d]['ItemID']
                    answerText = res_question[q + chang]['ItemOptions'][d]['ItemTitle']
                    g = g + answerID + ','
                    Tt = Tt + answerText + ','
                    d = d + 1
                    stay = res_question[q + chang]['ItemOptions'][d]['ItemIsCorrect']
                    # print('答案为：' + str(answerID))
                else:
                    d = d + 1
                    stay = res_question[q + chang]['ItemOptions'][d]['ItemIsCorrect']
                if stay == '1':
                    answerID = res_question[q + chang]['ItemOptions'][d]['ItemID']
                    answerText = res_question[q + chang]['ItemOptions'][d]['ItemTitle']
                    g = g + answerID
                    Tt = Tt + answerText + ','
                    print('答案为：' + str(Tt))
                    url = "http://wrggka.whvcse.edu.cn/api/M_Course/SubmitQuestionAnswer2?userId=" + str(
                        uid) + "&courseClassId=" + str(courseClassId) + "&courseId=" + str(
                        courseId) + "&chapterId=0&paperId=" + str(paper) + "&questionId=" + str(
                        questionID) + "&examTimes=0&examCountId=" + str(examID) + "&userAnswers=" + str(
                        g) + "&accessKey=1&secretKey=1"
                    res = requests.get(url).json()
                    status_test = res['result']
                    if status_test == '1':
                        print('提交成功')
                    else:
                        print('提交失败')
                    q = q + 1
                else:
                    print('答案为：' + str(Tt[:-1]))
                    url = "http://wrggka.whvcse.edu.cn/api/M_Course/SubmitQuestionAnswer2?userId=" + str(
                        uid) + "&courseClassId=" + str(courseClassId) + "&courseId=" + str(
                        courseId) + "&chapterId=0&paperId=" + str(paper) + "&questionId=" + str(
                        questionID) + "&examTimes=0&examCountId=" + str(examID) + "&userAnswers=" + str(
                        g[:-1]) + "&accessKey=1&secretKey=1"
                    res = requests.get(url).json()
                    status_test = res['result']
                    if status_test == '1':
                        print('提交成功')
                    else:
                        print('提交失败')
                    q = q + 1
        print("正在做判断题......")
        o = []
        t = []
        for i in res_question:  # 判断判断题目类型；顺序输出
            if i['ItemType'] == '6':
                o.append(i['ItemID'])
                t.append(i['ItemTitle'])
        # print(o)
        chang_pan = len(o)
        # print(chang)
        q = 0
        while q < chang_pan:
            d = 0
            questionID = o[q]  # 第q个题目ID
            questionText = t[q]
            print('第' + str(q + 1) + '题为：' + questionText)
            stay = res_question[q + chang + chang_duo]['ItemOptions'][d]['ItemIsCorrect']  # 正确答案所在的数组的定位 q值和d值
            # print((stay))
            while stay != '1':
                d = d + 1
                stay = res_question[q + chang + chang_duo]['ItemOptions'][d]['ItemIsCorrect']
                # print(stay)
            answerID = res_question[q + chang + chang_duo]['ItemOptions'][d]['ItemID']  # 答案ID
            answerText = res_question[q + chang + chang_duo]['ItemOptions'][d]['ItemTitle']
            print('答案为：' + answerText)
            url = "http://wrggka.whvcse.edu.cn/api/M_Course/SubmitQuestionAnswer2?userId=" + str(
                uid) + "&courseClassId=" + str(courseClassId) + "&courseId=" + str(
                courseId) + "&chapterId=0&paperId=" + str(paper) + "&questionId=" + str(
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
        url = "http://wrggka.whvcse.edu.cn/api/M_Course/SubmitPaper?userId=" + str(uid) + "&courseClassId=" + str(
            courseClassId) + "&courseId=" + str(courseId) + "&chapterId=0&paperId=" + str(
            paper) + "&accessKey=1&secretKey=1"
        res = requests.get(url).json()
        print("第"+str(cishu)+"张试卷：" + res['message'])
    cishu=1
    paper=paper1
    first_exam()
    cishu=2
    paper=paper2
    first_exam()

if __name__ == "__main__":
    res = begin()
    res_class,uid=first()
    class_status()
    text_end,text_long=class_xz()
    k = 0
    while k < text_long:
        y = int(text_end[k])
        class_name = res_class['courseList'][y]['courseName']  # 课程名
        class_success = res_class['courseList'][y]['isNoSuccess']  # 通过状态
        print("正在完成<" + str(class_name) + ">.......")
        if class_success == '已通过':
            print('该课程已通过，无需操作')
            k = k + 1
        else:
            class_video()
            class_exam()
            k=k+1
    print("选择的课程已全部完成,请手动关闭窗口，或100秒后自动关闭")
    time.sleep(100)
    input("exit")
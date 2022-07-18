import pandas as pd
import datetime
import seaborn as sns
import matplotlib.pyplot as plt

from person import Person
from grapher import cnMap
from mystat import ChiSquareTest

# Form map between choices and scalars/vectors

namemap = {"source": ["(空)|(跳过)", "微信", "其他"], "gender": ["(空)|(跳过)", "女", "男", "其他"],
           "profession": ["(空)|(跳过)", "水电安装|电工|木工|暖通|钢筋|钢筋工|机械员|务农|普工|装修工|泥工|装修工|装修木工|测量|外架",
                          "施工|施工员|建筑业|建筑|劳务|建筑工地",
                          "资料员|管理人员|预算员|施工管理|成本管理|建筑木工管理|外架管理",
                          "经理"],
           "educationBackground": ["(空)|(跳过)", "小学", "初中", "高中", "专科", "本科", "其他"],
           "workDuration": ["(空)|(跳过)", "三个月～六个月", "六个月～一年", "一年～两年", "两年～三年", "三年～五年", "五年以上"],
           "locationDuringPandamic": ["(空)|(跳过)", "工地及配套宿舍", "居家或其他地方"],
           "isTherePositiveDuringPandamic": ["(空)|(跳过)", "有", "没有"],
           "positivePolicy": ["(空)|(跳过)", "工地封闭管理", "转运至方舱", "转运至隔离酒店", "其他"],
           "transferCostResponsibility": ["(空)|(跳过)", "您", "公司", "政府"],
           "goodCostResponsibility": ["(空)|(跳过)", "自行承担", "公司、政府承担", "自己，公司、政府共同承担", "不了解"],
           "precautionarySchemeTime": ["(空)|(跳过)", "一周以内", "一周以后-4/1日之前", "4/1日之后（大概多久）"],
           "incomeSchemeTime": ["(空)|(跳过)", "一周以内", "一周以后-4/1日之前", "4/1日之后（大概多久）"],
           "income": ["(空)|(跳过)", "低于2590元", "高于2590元", "没有收入"],
           "incomePolicy": ["(空)|(跳过)", "没有听说过", "听说过，没有落实", "部分落实，工资没达到要求", "完全落实", "超标准落实"],
           "isLocal": ["(空)|(跳过)", "是", "不是"],
           "whyShanghai": ["(空)|(跳过)", "工作机会多", "人脉丰富", "工资较高", "其他"],
           "workDurationInShanghai": ["(空)|(跳过)", "三个月～六个月", "六个月～一年", "一年～两年", "两年～三年", "三年～五年", "五年以上"],
           "changeMind": ["(空)|(跳过)", "会", "不会", "不好说"],
           "interviewWillingness": ["(空)|(跳过)", "是", "否"]}

gnamemap = namemap

def choice2num(question, choice):
    return [choice in tmpstr.split('|') for tmpstr in namemap[question]].index(True)

def choice2vec(question, choices):
    choices = choices.split('┋');
    retvec = []
    for choice in choices:
        retvec.append(choice2num(question, choice))
    return retvec;

def num2choice(question, num):
    return gnamemap[question][num]

# Initialization

people = []

# Data reading

dataframe = pd.read_excel('./workerdata.xlsx').values

for dataseries in dataframe:
    name = dataseries[4].split('[')[0]
    
    questionnaireDateTmp = dataseries[1].split(' ')[0].split('/') + dataseries[1].split(' ')[1].split(':')
    questionnaireDate = datetime.datetime(int(questionnaireDateTmp[0]), int(questionnaireDateTmp[1]),
                                      int(questionnaireDateTmp[2]), int(questionnaireDateTmp[2]),
                                      int(questionnaireDateTmp[4]), int(questionnaireDateTmp[5]))
    
    questionnaireDuration = int(dataseries[2].split('秒')[0])
    questionnaireLocation = dataseries[5].split('(')[1].split("-")[0]
    
    source = choice2num("source", dataseries[3])
    ip = dataseries[5].split('(')[0]
    gender = choice2num("gender", dataseries[6])
    profession = choice2num("profession", dataseries[7])
    educationBackground = choice2num("educationBackground", dataseries[8])
    workDuration = choice2num("workDuration", dataseries[9])
    locationDuringPandamic = choice2num("locationDuringPandamic", dataseries[10])
    isTherePositiveDuringPandamic = choice2num("isTherePositiveDuringPandamic", dataseries[11])
    positivePolicy = choice2num("positivePolicy", dataseries[12])
    transferCostResponsibility = choice2vec("transferCostResponsibility", dataseries[13])
    goodCostResponsibility = choice2num("goodCostResponsibility", dataseries[14])
    precautionarySchemeTime = choice2num("precautionarySchemeTime", dataseries[15].split("〖")[0])
    incomeSchemeTime = choice2num("incomeSchemeTime", dataseries[16].split("〖")[0])
    income = choice2num("income", dataseries[17])
    incomePolicy = choice2num("incomePolicy", dataseries[18])
    isLocal = choice2num("isLocal", dataseries[19])
    hometown = dataseries[20].split("省")[0].split("遵")[0]
    if len(hometown.split("在")) > 1:
        hometown = hometown.split("在")[1]
    if hometown == "(跳过)":
        hometown = "上海"
    whyShanghai = choice2vec("whyShanghai", dataseries[21].split("〖")[0])
    workDurationInShanghai = choice2num("workDurationInShanghai", dataseries[22])
    changeMind = choice2num("changeMind", dataseries[23].split("〖")[0])
    interviewWillingness = choice2num("interviewWillingness", dataseries[24])
    contact = dataseries[25]
    
    people.append(Person(name, questionnaireDate, questionnaireDuration, questionnaireLocation, source,
                         ip, gender, profession, educationBackground, workDuration, locationDuringPandamic,
                         isTherePositiveDuringPandamic, positivePolicy, transferCostResponsibility,
                         goodCostResponsibility, precautionarySchemeTime, incomeSchemeTime, income,
                         incomePolicy, isLocal, hometown, whyShanghai, workDurationInShanghai, changeMind,
                         interviewWillingness, contact))

# Analysis
print("<Analysis>\n")

# Locations

ipLocation = {}
hometownLocation = {}

leaveShanghai = 0
localLeaveShanghai = 0
atHometown = 0
localAtHometown = 0
lied = 0

for person in people:
    if person.questionnaireLocation in ipLocation.keys():
        ipLocation[person.questionnaireLocation] += 1
    else:
        ipLocation[person.questionnaireLocation] = 1
    
    if person.hometown in hometownLocation.keys():
        hometownLocation[person.hometown] += 1
    else:
        hometownLocation[person.hometown] = 1
    
    if person.questionnaireLocation != "上海":
        leaveShanghai += 1
        if person.hometown == "上海":
            localLeaveShanghai += 1
    
    if person.hometown == person.questionnaireLocation:
        atHometown += 1
        if person.hometown == "上海":
            localAtHometown += 1
    
    if person.questionnaireLocation != "上海" and person.changeMind == 2:
        lied += 1

ipLocationLst = []

for location in ipLocation.keys():
    ipLocationLst.append((location, ipLocation[location]))

hometownLocationLst = []

for location in hometownLocation.keys():
    hometownLocationLst.append((location, hometownLocation[location]))

print("--- Information based on locations ---")
print(str(leaveShanghai) + " workers have left Shanghai, including " + str(localLeaveShanghai) + " Shanghainese.")
print(str(atHometown) + " workers are at their hometown right now, including " + str(localAtHometown) + " Shanghainese.")
print("Meaning that " + str(leaveShanghai - atHometown - localLeaveShanghai + localAtHometown) + " workers have left Shanghai and started to work at other cities beside their hometown.")
print("Above the ones that claimed not leaving Shanghai in the questionnaire, " + str(lied) + " lied.")

cnMap("IP", "IP related physical location", ipLocationLst, 0, max(ipLocation.values()))
cnMap("hometown", "Hometown location", hometownLocationLst, 0, max(hometownLocation.values()))

print("\n")

# Treatments

print("--- Treatments ---")

print("1. H0: salaries have nothing to do with worker's profession.")

salaryProfessionMatrix = [[0 for j in range(3)] for i in range(4)]

for person in people:
    if person.income == 0 or person.profession == 0:
        continue;
    salaryProfessionMatrix[person.profession - 1][person.income - 1] += 1

df, x2, pValue = ChiSquareTest(salaryProfessionMatrix)

if pValue < 0.05:
    print("   H0 is incorrect as p value is %.3f, less than 0.050." % pValue)
else:
    print("   H0 is correct as p value is %.3f, greater than 0.050." % pValue)

print("2. H0: salaries have nothing to do with the worker's hometown.")

hometown2num = {}
cnt = 0
for person in people:
    if person.hometown not in hometown2num.keys():
        hometown2num[person.hometown] = cnt
        cnt += 1

salaryHometownMatrix = [[0 for j in range(3)] for i in range(len(hometown2num.keys()))]

for person in people:
    if person.income == 0:
        continue;
    salaryHometownMatrix[hometown2num[person.hometown]][person.income - 1] += 1

df, x2, pValue = ChiSquareTest(salaryHometownMatrix)

if pValue < 0.05:
    print("   H0 is incorrect as p value is %.3f, less than 0.050." % pValue)
else:
    print("   H0 is correct as p value is %.3f, greater than 0.050." % pValue)

print("3. H0: salaries have nothing to do with the worker's working duration in Shanghai.")

salaryWSDurationMatrix = [[0 for j in range(3)] for i in range(6)]

for person in people:
    if person.income == 0 or person.workDurationInShanghai == 0:
        continue;
    salaryWSDurationMatrix[person.workDurationInShanghai - 1][person.income - 1] += 1

df, x2, pValue = ChiSquareTest(salaryWSDurationMatrix)

if pValue < 0.05:
    print("   H0 is incorrect as p value is %.3f, less than 0.050." % pValue)
else:
    print("   H0 is correct as p value is %.3f, greater than 0.050." % pValue)

print("4. H0: salaries have nothing to do with the worker's education background.")

salaryEduMatrix = [[0 for j in range(3)] for i in range(6)]

for person in people:
    if person.income == 0 or person.educationBackground == 0:
        continue;
    salaryEduMatrix[person.educationBackground - 1][person.income - 1] += 1

df, x2, pValue = ChiSquareTest(salaryEduMatrix)

if pValue < 0.05:
    print("   H0 is incorrect as p value is %.3f, less than 0.050." % pValue)
else:
    print("   H0 is correct as p value is %.3f, greater than 0.050." % pValue)
    
print("5. H0: the responsibility of transfer cost have nothing to do with the worker's profession.")

transferCostResponsibilityMatrix = [[0 for j in range(3)] for i in range(4)]

for person in people:
    if person.transferCostResponsibility == 0 or person.profession == [0]:
        continue;
    for j in range(len(person.transferCostResponsibility)):
        transferCostResponsibilityMatrix[person.profession - 1][person.transferCostResponsibility[j] - 1] += 1

df, x2, pValue = ChiSquareTest(transferCostResponsibilityMatrix)

if pValue < 0.05:
    print("   H0 is incorrect as p value is %.3f, less than 0.050." % pValue)
else:
    print("   H0 is correct as p value is %.3f, greater than 0.050." % pValue)

print("6. H0: the responsibility of good cost have nothing to do with the worker's profession.")

goodCostResponsibilityMatrix = [[0 for j in range(4)] for i in range(4)]

for person in people:
    if person.goodCostResponsibility == 0 or person.profession == 0:
        continue;
    goodCostResponsibilityMatrix[person.profession - 1][person.goodCostResponsibility - 1] += 1

df, x2, pValue = ChiSquareTest(goodCostResponsibilityMatrix)

if pValue < 0.05:
    print("   H0 is incorrect as p value is %.3f, less than 0.050." % pValue)
else:
    print("   H0 is correct as p value is %.3f, greater than 0.050." % pValue)

print("7. H0: the worker's profession have nothing to do with the worker's education background.")

professionEduMatrix = [[0 for j in range(4)] for i in range(6)]

for person in people:
    if person.profession == 0 or person.educationBackground == 0:
        continue;
    professionEduMatrix[person.educationBackground - 1][person.profession - 1] += 1

df, x2, pValue = ChiSquareTest(professionEduMatrix)

if pValue < 0.05:
    print("   H0 is incorrect as p value is %.3f, less than 0.050." % pValue)
else:
    print("   H0 is correct as p value is %.3f, greater than 0.050." % pValue)

# p values of all combinations
province2num = {}
cnt = 0
for person in people:
    if person.hometown not in province2num.keys():
        province2num[person.hometown] = cnt
        cnt += 1
    if person.questionnaireLocation not in province2num.keys():
        province2num[person.questionnaireLocation] = cnt
        cnt += 1


personalInfoMatrix = []
for person in people:
    personalInfoMatrix.append(person.personalInfo())

personalInfoLength = len(personalInfoMatrix[0])
personalInfoPMatrix = [[0 for j in range(personalInfoLength)] for i in range(personalInfoLength)]

personalInfoNameVector = people[0].personalInfoName()

matrixBuffer = [[None for j in range(personalInfoLength)] for i in range(personalInfoLength)]

for i in range(personalInfoLength):
    for j in range(personalInfoLength):
        type1 = type(personalInfoMatrix[0][i])
        type2 = type(personalInfoMatrix[0][j])
        if personalInfoNameVector[i] in namemap.keys():
            size1 = len(namemap[personalInfoNameVector[i]]) - 1
        else:
            size1 = cnt
        if personalInfoNameVector[j] in namemap.keys():
            size2 = len(namemap[personalInfoNameVector[j]]) - 1
        else:
            size2 = cnt
        
        matrix = [[0 for j in range(size2)] for i in range(size1)]
        
        if type1 == list and type2 == list:
            for personalInfoVec in personalInfoMatrix:
                if personalInfoVec[i] == [0] or personalInfoVec[j] == [0]:
                    continue
                for x in range(len(personalInfoVec[i])):
                    for y in range(len(personalInfoVec[j])):
                        matrix[personalInfoVec[i][x] - 1][personalInfoVec[j][y] - 1] += 1
        if type1 == list and type2 == int:
            for personalInfoVec in personalInfoMatrix:
                if personalInfoVec[i] == [0] or personalInfoVec[j] == 0:
                    continue
                for x in range(len(personalInfoVec[i])):
                    matrix[personalInfoVec[i][x] - 1][personalInfoVec[j] - 1] += 1
        if type1 == list and type2 == str:
            for personalInfoVec in personalInfoMatrix:
                if personalInfoVec[i] == [0]:
                    continue
                for x in range(len(personalInfoVec[i])):
                    matrix[personalInfoVec[i][x] - 1][province2num[personalInfoVec[j]]] += 1
        if type1 == int and type2 == list:
            for personalInfoVec in personalInfoMatrix:
                if personalInfoVec[i] == 0 or personalInfoVec[j] == [0]:
                    continue
                for y in range(len(personalInfoVec[j])):
                    matrix[personalInfoVec[i] - 1][personalInfoVec[j][y] - 1] += 1
        if type1 == int and type2 == int:
            for personalInfoVec in personalInfoMatrix:
                if personalInfoVec[i] == 0 or personalInfoVec[j] == 0:
                    continue
                matrix[personalInfoVec[i] - 1][personalInfoVec[j] - 1] += 1
        if type1 == int and type2 == str:
            for personalInfoVec in personalInfoMatrix:
                if personalInfoVec[i] == 0:
                    continue
                matrix[personalInfoVec[i] - 1][province2num[personalInfoVec[j]]] += 1
        if type1 == str and type2 == list:
            for personalInfoVec in personalInfoMatrix:
                if personalInfoVec[j] == [0]:
                    continue
                for y in range(len(personalInfoVec[j])):
                    matrix[province2num[personalInfoVec[i]]][personalInfoVec[j][y] - 1] += 1
        if type1 == str and type2 == int:
            for personalInfoVec in personalInfoMatrix:
                if personalInfoVec[j] == 0:
                    continue
                matrix[province2num[personalInfoVec[i]]][personalInfoVec[j] - 1] += 1
        if type1 == str and type2 == str:
            for personalInfoVec in personalInfoMatrix:
                matrix[province2num[personalInfoVec[i]]][province2num[personalInfoVec[j]]] += 1
        df, x2, pValue = ChiSquareTest(matrix)
        personalInfoPMatrix[i][j] = pValue
        matrixBuffer[i][j] = matrix.copy()

sns.set(rc={'figure.figsize':(15,13)})
sns.heatmap(data=personalInfoPMatrix, annot=True, fmt=".3f")
plt.show()

sns.set(rc={'figure.figsize':(5,4)})
for i in range(len(personalInfoPMatrix)):
    for j in range(i + 1, len(personalInfoPMatrix)):
        if personalInfoPMatrix[i][j] < 0.05:
            sns.heatmap(data = matrixBuffer[i][j], cmap = "YlGnBu", annot = True)
            plt.xlabel(personalInfoNameVector[j])
            plt.ylabel(personalInfoNameVector[i])
            plt.show()
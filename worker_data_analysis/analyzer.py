import pandas as pd
import datetime

from person import Person

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

    print(people[len(people) - 1].personalInfoVectorlize())
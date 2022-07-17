import pandas as pd
import datetime

from person import Person

# Form map between choices and scalars/vectors

namemap = {"source": ["(空)|(跳过)", "微信", "其他"], "gender": ["(空)|(跳过)", "女", "男", "其他"],
           "profession": ["(空)|(跳过)", "水电安装|电工|木工|暖通|钢筋|钢筋工|机械员|务农|普工|装修工|泥工|装修工|装修木工|测量|外架",
                          "施工|施工员|建筑业|建筑|劳务|建筑工地",
                          "资料员|管理人员|预算员|施工管理|成本管理|建筑木工管理|外架管理",
                          "经理"]}

gnamemap = namemap

def choice2num(question, choice):
    return [choice in tmpstr.split('|') for tmpstr in namemap[question]].index(True)

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
    
    print(name, questionnaireDate, questionnaireDuration, questionnaireLocation, source, ip, gender, profession, educationBackground)
class Person:
    def __init__(self, _name, _questionnaireDate, _questionnaireDuration, _questionnaireLocation,
                 _source, _ip, _gender, _profession, _educationBackground, _workDuration,
                 _locationDuringPandamic, _isTherePositiveDuringPandamic, _positivePolicy,
                 _transferCostResponsibility, _goodCostResponsibility, _precautionarySchemeTime,
                 _incomeSchemeTime, _income, _incomePolicy, _isLocal, _hometown, _whyShanghai,
                 _workDurationInShanghai, _changeMind, _interviewWillingness, _contact):
        self.name = _name
        self.questionnaireDate = _questionnaireDate
        self.questionnaireDuration = _questionnaireDuration
        self.questionnaireLocation = _questionnaireLocation
        self.source = _source
        self.ip = _ip
        self.gender = _gender
        self.profession = _profession
        self.educationBackground = _educationBackground
        self.workDuration = _workDuration
        self.locationDuringPandamic = _locationDuringPandamic
        self.isTherePositiveDuringPandamic = _isTherePositiveDuringPandamic
        self.positivePolicy = _positivePolicy
        self.transferCostResponsibility = _transferCostResponsibility
        self.goodCostResponsibility = _goodCostResponsibility
        self.precautionarySchemeTime = _precautionarySchemeTime
        self.incomeSchemeTime = _incomeSchemeTime
        self.income = _income
        self.incomePolicy = _incomePolicy
        self.isLocal = _isLocal
        self.hometown = _hometown
        self.whyShanghai = _whyShanghai
        self.workDurationInShanghai = _workDurationInShanghai
        self.changeMind = _changeMind
        self.interviewWillingness = _interviewWillingness
        self.contact = _contact
    
    def personalInfoVectorlize(self):
        return [self.gender, self.profession, self.educationBackground, self.workDuration,
                self.locationDuringPandamic, self.isTherePositiveDuringPandamic, self.positivePolicy,
                self.transferCostResponsibility, self.precautionarySchemeTime, self.incomeSchemeTime,
                self.income, self.incomePolicy, self.isLocal, self.hometown, self.whyShanghai,
                self.workDurationInShanghai, self.changeMind, self.interviewWillingness];
        
    def personalInfoVectorlizeMap(self):
        return ["gender", "profession", "educationBackground", "workDuration",
                "locationDuringPandamic", "isTherePositiveDuringPandamic", "positivePolicy",
                "transferCostResponsibility", "precautionarySchemeTime", "incomeSchemeTime",
                "income", "incomePolicy", "isLocal", "hometown", "whyShanghai",
                "workDurationInShanghai", "changeMind", "interviewWillingness"];
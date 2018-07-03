# get industry dummy variables
industry_LevelDict = {
    '交运设备': 1,
    '交通运输': 2,
    '休闲服务': 3,
    '传媒': 4,
    '信息服务': 5,
    '公用事业': 6,
    '农林牧渔': 7,
    '化工': 8,
    '医药生物': 9,
    '商业贸易': 10,
    '国防军工': 11,
    '家用电器': 12,
    '建筑建材': 13,
    '建筑材料': 14,
    '建筑装饰': 15,
    '房地产': 16,
    '有色金属': 17,
    '机械设备': 18,
    '汽车': 19,
    '电子': 20,
    '电气设备': 21,
    '纺织服装': 22,
    '综合': 23,
    '计算机': 24,
    '轻工制造': 25,
    '通信': 26,
    '采掘': 27,
    '钢铁': 28,
    '银行': 29,
    '非银金融': 30,
    '食品饮料': 31
}

industry['Industry'] = industry['Industry'].map(industry_LevelDict)
industry['Industry'].drop_duplicates()
dummies = pd.get_dummies(industry, columns=['Industry'],prefix=['Industry'],prefix_sep="_",dummy_na=False,drop_first=False)

import json
import os
import re
import jieba
import time
import pkuseg
from expMap import *

count = {}  # 统计词频
# 以默认配置加载模型
seg = pkuseg.pkuseg( user_dict='userdict.txt')

province_dict = ['河北', '山西', '辽宁', '吉林', '黑龙江', '江苏', '浙江', '安徽',
            '福建', '江西', '山东', '河南', '湖北','湖南', '广东', '海南', 
            '四川', '贵州', '云南', '陕西', '甘肃', '青海', '台湾', '香港', '澳门', 
            '内蒙古', '广西' '西藏', '宁夏', '新疆', '北京', '天津', '上海', '重庆']

class Official:

    # profile为json格式的官员信息
    def __init__(self, profile):
        self.profile = profile
        # 个人信息的初始化
        self.introduction = profile['introduction']
        self.experience = profile['experience']
        self.name = ''  # 姓名
        self.gender = 1  # 1表示男，0表示女
        self.race = ''  # 表示民族
        self.born_year = ''  # 出生年份
        self.born_locate = ''  # 出生地
        self.education = 0  # 教育水平 本科1，硕士2，博士3
        self.work_time = ''  # 工作年份
        self.whether_ccp = 0  # 是否入党 1为入党
        self.join_time = ''  # 入党年份
        self.experienceList = []  # 全部处理成：(年龄, 官职) 元组，地点待定
        self.cut = ''

    # 从profile文件中获得个人信息
    def attribute_init(self):
        # print(self.introduction)
        intro_split = self.introduction.split('，')
        if len(intro_split) < 3:
            intro_split = self.introduction.split(',')
        # set name
        self.name = intro_split[0]
        # set gender
        for item in intro_split:
            if '男' in item:
                self.gender = 1
                break
            if '女' in item:
                self.gender = 0
                break
        # set race
        for item in intro_split:
            if '族' in item:
                self.race = item
                break
        # set born_locate
        for item in intro_split:
            if '人' in item:
                self.born_locate = item[:-1]
                mark = 0
                for item in province_dict:
                    if item in self.born_locate:
                        self.born_locate = item
                        mark = 1
                        break
                if mark == 0:
                    self.born_locate = ''
        # set born_year
        for item in intro_split:
            if '生' in item:
                pattern = '.*?([0-9]*)年'
                try:
                    res = re.match(pattern, item)
                    res = str(res.group(1))
                except:
                    continue
                self.born_year = res
                break
        # set education
        for item in intro_split:
            if ('本科' in item or '学士' in item or '大学' in item) and self.education < 2:
                self.education = 1
            if ('硕士' in item or '研究生' in item) and self.education < 3:
                self.education = 2
            if '博士' in item:
                self.education = 3
        # set year begin work
        for item in intro_split:
            if '工作' in item:
                partten = '.*?([0-9]*)年'
                res = re.match(pattern, item)
                self.work_time = res.group(1)
                break
        # set year join party
        for item in intro_split:
            if '党' in item:
                partten = '.*?([0-9]*)年'
                self.whether_ccp = 1
                try:
                    res = re.match(pattern, item)
                    self.join_time = res.group(1)
                except:
                    continue
                break

    def experience_init(self):
        for item in self.experience:
            new_text = {'exp': [], 'position': 999, 'degrade': 0, 'tmp_position': 999, 'upgrade':0}  # position为映射完的阶级
            res_set = {'time': 0, 'position': 0}  # 储存最后结果
            cno = item.find('，')
            dno = item.find('、')
            if cno > 0 or dno > 0:
                if cno > 0 and dno > 0:
                    if cno > dno:
                        tmpstr = item[0:dno]
                    else:
                        tmpstr = item[0:cno]
                else:
                    if cno > 0:
                        tmpstr = item[0:cno]
                    else:
                        tmpstr = item[0:dno]
            else:
                tmpstr = item
            # print(tmpstr)
            explist = seg.cut(tmpstr)
            # print(explist[0])
            time_item = expMap.time_init(explist[0])
            # print(time_item)
            if len(time_item) == 0:  # 没有任职年份直接跳过
                continue
            new_text['time'] = time_item
            # 关注词
            with open('userdict.txt', encoding='utf-8') as f:
                focuswords = f.read()
            for w in explist:
                if w in focuswords:
                    new_text['exp'].append(w)
            # print(new_text)
            if len(new_text['time']) > 0 and len(new_text['exp']) >= 1:
                expMap.degrade(new_text)  # 降级判断应该最先，因为有直接的会清空列表
                expMap.upgrade(new_text)
                expMap.position_init(new_text)
                expMap.decorate_init(new_text)
                expMap.tmp_init(new_text)
                expMap.final(res_set, new_text)
            if res_set['position'] > 0:
                self.experienceList.append(res_set)
            # 统计词频
            # for word in explist:
            #     count[word] = count.get(word, 0) + 1
            # print(self.experienceList)

    def get_name(self):
        return self.name

    def get_gender(self):
        return self.gender

    def get_race(self):
        return self.race

    def get_born_year(self):
        return self.born_year

    def get_born_locate(self):
        return self.born_locate

    def get_education(self):
        return self.education

    def get_work_time(self):
        return self.work_time

    def get_join_time(self):
        return self.join_time

    def get_ccp(self):
        return self.whether_ccp

    def get_experienceList(self):
        return self.experienceList


if __name__ == '__main__':
    root = 'data/'
    count = 0
    for filename in os.listdir(root):
        if filename == '.DS_Store':
            continue

        filenames = os.listdir(os.path.join(root, filename))
        
        for file in filenames:
            if file == '.DS_Store':
                continue
            path_ = os.path.join(root, filename)
            with open(os.path.join(path_, file), 'r', encoding='utf-8') as file:
                data = json.load(file)
                if len(data['experience']) < 10:
                    continue
                person = Official(data)
                person.attribute_init()
                person.experience_init()
                print('姓名:', person.get_name())
                print('性别:', person.get_gender())
                print('民族:', person.get_race())
                print('出生地:', person.get_born_locate())
                print('出生年份:', person.get_born_year())
                print('最高学历:', person.get_education())
                print('工作年份:', person.get_work_time())
                print('是否党员', person.get_ccp())
                print('入党年份:', person.get_join_time())
                print(person.experience)
                print('工作经历：', person.get_experienceList())
                # -----------------------------------
                # 统计职级升降人数
                judgeList = person.get_experienceList()
                judge = True
                
                for i in range(len(judgeList)-2):
                    if int(judgeList[i]['position'])>int(judgeList[i+1]['position']):
                        judge = False 
                        print('工作经历：', person.get_experienceList())
                        break 
                if judge == True:
                    count += 1
                    
                print('--------------------')
    print(count)
    # list = list(count.items())  # 将字典的所有键值对转化为列表
    # list.sort(key=lambda x: x[1], reverse=True)  # 对列表按照词频从大到小的顺序排序
    # print(list)

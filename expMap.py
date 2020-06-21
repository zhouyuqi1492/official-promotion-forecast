import re

# 官职分十二级 对十二级的常见官职建立dict 为官职：级别格式
# 直接对应型,一旦出现，直接进入检查有没有减一词语
position_dict = {
    '省委': 10,
    '市委': 8,
    '县委': 6,
    '州委': 8,
    '区委': 6,
    '厅长': 8,
    '省长': 10,
    '市长': 8,
    '县长': 6,
    '部长': 10,
    '州长': 8,
    '处长': 6,
    '科长': 4,
    '乡长': 4,
    '镇长': 4,
    '股长': 3,
    '办事员': 1,
    '科员': 2,
    '调研员': 6,
    '巡视员': 8
}

# 地方修饰，用于定义待定词
decorate_dict = {
    '内蒙古': 10,
    '新疆维吾尔': 10,
    '广西壮族': 10,
    '宁夏回族': 10,
    '西藏': 10,
    '中央': 12,
    '省': 10,
    '市': 8,
    '州': 8,
    '县': 6,
    '乡': 4,
    '区': 6,
    '镇': 4,
    '国': 12,
    '部': 10,
    '厅': 8,
    '处': 6,
    '科': 4,
}

# 待定列表
tmp_list = ['处长', '局长', '秘书长', '人大常委会主任', '主任', '主席']
# 8+处长是4，单独处长是6,6+局长是4,8+局长是6，position有效的话秘书长相当于降1，无效和decorate平级，主任和de平级，主席和de平级
degrade_list = ['副', '助理', '常委']

upgrade_list = ['北京', '天津', '上海','重庆']  # 直辖市升两级


# 出现副、助理、常委字眼，级别自动减一
# 出现直辖市级别自动加一
# 出现自治区，当作省处理，州当作市处理
# 出现处长、局长、秘书长、人大常委会主任、主任、主席由于二义性，需要找他们的限定词

class expMap:
    def time_init(time_str):
        re.sub(r'年', '.', time_str, count=0, flags=0)
        no = re.search(r'\d+\.\d+', time_str)
        time_sp = ''
        if no is not None:
            time_sp = no.group()
        return time_sp  # time

    # 处理掉直接定义型的词，取小的
    def position_init(new_text):
        for item in new_text['exp'][:]:
            if position_dict.__contains__(item) is True and position_dict[item] < new_text['position']:
                new_text['position'] = position_dict[item]

    # 处理修饰词，可能有多个但是我们只要最小的那个
    def decorate_init(new_text):
        new_text['decorate'] = 999
        for item in new_text['exp'][:]:  # 删除列表得切片
            if decorate_dict.__contains__(item) is True and decorate_dict[item] < new_text['decorate']:
                new_text['decorate'] = decorate_dict[item]
                new_text['exp'].remove(item)

    # 根据修饰词处理，待定词,这里需要分类处理，还挺复杂
    def tmp_init(new_text):
        for item in new_text['exp'][:]:
            if item == tmp_list[0]:
                if new_text['decorate'] == 8:
                    new_text['tmp_position'] = 4
                else:
                    new_text['tmp_position'] = 6
            if item == tmp_list[1]:
                if new_text['decorate'] == 8:
                    new_text['tmp_position'] = 6
                if new_text['decorate'] == 6:
                    new_text['tmp_position'] = 4
            if item == tmp_list[2]:
                if new_text['position'] < 13:
                    new_text['tmp_position'] = new_text['position'] - 1
                else:
                    new_text['tmp_position'] = new_text['decorate']
            if item == tmp_list[3] or item == tmp_list[4] or item == tmp_list[5]:
                new_text['tmp_position'] = new_text['decorate']
        new_text['exp'].clear()

    def degrade(new_text):
        for item in new_text['exp'][:]:
            if item in degrade_list:
                new_text['degrade'] -= 1
                new_text['exp'].remove(item)

    def upgrade(new_text):
        for item in new_text['exp'][:]:
            if item in upgrade_list:
                new_text['upgrade'] += 2
                new_text['exp'].remove(item)

    def final(res_set, new_text):
        res_set['time'] = new_text['time']
        position = min(new_text['position'], new_text['tmp_position']) - new_text['degrade'] + new_text['upgrade']
        if 0 < position < 13:
            res_set['position'] = position

    if __name__ == '__main__':
        time = '2001.07－2003.03'
        time_del = time_init(time)
        list = [1, 2, 3, 4, 5]
        list.remove(1)
        print(list)

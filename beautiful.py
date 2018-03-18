import re
from bs4 import BeautifulSoup


def load_file(filepath):

    soup = BeautifulSoup(open(filepath), "lxml")
    a = soup.tbody.children
    reg = re.compile(("<[^>]*>"))   # 清除html标签,提取文本
    row0 = []       # row0用于保存上一行的信息
    flag = True     # row0未初始化
    for child in a:
        row = []    # 保存表格提取结果
        if child.find('th'):    # 提取表格字段
            for value in child.children:
                st = reg.sub('', str(value))    # 正则匹配替换
                row.append((st.strip('\n')))
            row = '-'.join(row)
            print(row)
            continue
        if child.find('td'):    # 提取每一行
            while child.find('sup'):    # 先清洗可能存在的上标符号
                child.find('sup').extract()
            for value in child.children:
                st = reg.sub('', str(value))
                row.append(st.strip('\n'))
            if flag:
                flag = False
            if len(row) < len(row0):    # 与上一行比较,分析是否需要处理字段缺省的情况
                row_temp = row0[0:len(row0)-len(row)]
                for i in range(len(row)):
                    row_temp.append(row[i])
                row0 = row_temp
                row_temp = '-'.join(row_temp)   # 将列表保存的字段连接起来
                print(row_temp)
                continue
            row0 = row
            row = '-'.join(row)
            print(row)

if __name__ == '__main__':
    load_file('data/2333.txt')
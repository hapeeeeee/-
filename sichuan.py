#!C:\Users\Administrator\AppData\Local\Programs\Python\Python37\python.exe
# -*- coding:utf-8 -*-


class City:

    def __init__(self, name, controller=None):
        self.name = name
        self.down = []
        self.controller = controller

    def __str__(self):
        return "地区信息：{}：{}；负责人信息：{}：联系人：{}，电话：{}".format(self.name,
                                                         list(map(lambda x:x.name,self.down)),
                                                         self.name,
                                                         self.controller.name if self.controller else None,
                                                         self.controller.tel if self.controller else None)

class Controller:

    def __init__(self, name, tel):
        self.name = name
        self.tel = tel

sichuan = City("四川")

#初始化四川
first_city_name = ["成都市" , "自贡", "泸州", "攀枝花", "德阳"]
first_city_controller = [["张三", "1111111"], ["李四", "22222"], ["王五", "2222222"], ["赵六","444444"], ["田七", "555555"]]

for city_name in first_city_name:
    sichuan.down.append(City(city_name))

for i in range(len(first_city_controller)):
    new_controller = Controller(first_city_controller[i][0], first_city_controller[i][1])
    sichuan.down[i].controller = new_controller

    
secend_city_name = [["武侯区","青羊区","高新区","金牛区","成华区"],["荣县","富顺县"],["泸县", "合江县", "叙永县", "古蔺县"],
                     ["米易县", "盐边县"], ["中江县", "罗江县", "广汉市", "什邡市", "绵竹市"]]

secend_city_controller = [
                        [["张1", "1111111"], ["李1", "22222"], ["王1", "2222222"], ["赵1","444444"], ["田1", "555555"]],
                        [["张2", "1111111"], ["李2", "22222"]],
                        [["张3", "1111111"], ["李3", "22222"], ["王3", "2222222"], ["赵3","444444"]],
                        [["张4", "1111111"], ["李4", "22222"]],
                        [["张5", "1111111"], ["李5", "22222"], ["王5", "2222222"], ["赵5","444444"], ["田5", "555555"]]
                        ]
#初始化二级城市
def init_secend_city(city, city_name, city_controller):
    new_city = City(city_name)
    new_city_controller = Controller(city_controller[0], city_controller[1])
    new_city.controller = new_city_controller
    city.down.append(new_city)


for i in range(len(sichuan.down)):
    for j in range(len(secend_city_name[i])):
        init_secend_city(sichuan.down[i], secend_city_name[i][j],secend_city_controller[i][j])


from optparse import OptionParser
optParser = OptionParser()

#-c 查询城市 显示城市名字和下属城市和负责人信息
optParser.add_option('-c','--city',action = 'store',type = "string" ,dest = 'cityname')

##-d  删除城市和其下属城市
optParser.add_option("-d","--delete_city", action="store_true",dest="delete_city")

##-C  修改城市信息
optParser.add_option("-C","--change_city", action="store",dest="change_city")

##-a  增加城市下属城市
optParser.add_option("-a","--add_city", action="store",dest="add_city")

#负责人查询 -p姓名查询 -t电话查询
optParser.add_option("-p","--person", action="store",dest="controll_person")
optParser.add_option("-t","--tel", action="store",dest="controll_tel")

optParser.add_option("-P","--change_person", action="store",dest="change_person")
optParser.add_option("-T","--change_tel", action="store",dest="change_tel")
optParser.add_option("-D","--delete_controller", action="store_true",dest="delete_controller")


def search_city_name(city_name):
    global sichuan
    search_list = [sichuan,]
    while search_list:
        search_city = search_list.pop(0)
        for city in search_city.down:
            if city.name == city_name:
                return search_city,city

            if city.down:
                search_list.append(city)
    return

def search_city_controller(controller_person):
    global sichuan
    search_list = [sichuan,]
    while search_list:
        search_city = search_list.pop(0)
        for city in search_city.down:
            if city.controller.name == controller_person:
                return search_city,city

            if city.down:
                search_list.append(city)
    return

def search_city_tel(controller_tel):
    global sichuan
    search_list = [sichuan,]
    while search_list:
        search_city = search_list.pop(0)
        for city in search_city.down:
            if city.controller.tel == controller_tel:
                return search_city,city

            if city.down:
                search_list.append(city)
    return

#判断城市是否存在


def mymain(op):
    try:
        if op.cityname:
            father_city, user_in_city = search_city_name(op.cityname)

        elif op.controll_person:
            father_city, user_in_city = search_city_controller(op.controll_person)

        elif op.controll_tel:
            father_city, user_in_city = search_city_tel(op.controll_tel)

        else:
            print("城市不存在")
            return
    except TypeError:
        print("查询信息错误 请核对后再次输入")
        return
    print(user_in_city)

    #-P 修改负责人信息
    if op.change_person:
        user_in_city.controller.name = op.change_person

    # -P 修改负责人信息
    if op.change_tel:
        user_in_city.controller.tel = op.change_tel

    if op.delete_controller:
        user_in_city.controller = None

    #-a 增加下属城市 -a "北京市，赵兴，486453"
    if op.add_city:
        add_city_list = op.add_city.split(",")
        new_controller = Controller(add_city_list[1], add_city_list[2])
        new_city = City(add_city_list[0], new_controller)
        user_in_city.down.append(new_city)

    #-C "cityname=成都市1"
    if op.change_city:
        change_city_name = op.change_city.split("=")[1]
        user_in_city.name = change_city_name

    print(user_in_city)
    #-d存在。删除城市
    if op.delete_city:
        father_city.down.remove(user_in_city)





    # -c城市名字查询
    # -d删除城市
    # -C修改城市信息
    # -a增加下属城市

    # -p负责人姓名查询 -P负责人姓名修改
    # -t负责人电话查询 -T负责人电话修改
    # -D删除负责人

fakeArgs = ["-c", "成都市","-D"]

option, args = optParser.parse_args()
op, ar = optParser.parse_args(fakeArgs)
mymain(op)
print(sichuan)





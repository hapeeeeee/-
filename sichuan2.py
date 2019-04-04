#!C:\Users\Administrator\AppData\Local\Programs\Python\Python37\python.exe
#-*-coding:utf-8-*-

import json
import time


def search_city_name(citys_dict, city_name):
    search_list = [citys_dict, ]
    while search_list:
        search_city = search_list.pop(0)
        for city in search_city["down"]:
            if city["name"] == city_name:
                return search_city, city

            if city["down"]:
                search_list.append(city)
    return

def search_city_controller(citys_dict, city_controller):
    search_list = [citys_dict, ]
    while search_list:
        search_city = search_list.pop(0)
        for city in search_city["down"]:
            if city["controller"] == city_controller:
                return search_city, city

            if city["down"]:
                search_list.append(city)
    return

def search_city_tel(citys_dict, city_tel):
    search_list = [citys_dict, ]
    while search_list:
        search_city = search_list.pop(0)
        for city in search_city["down"]:
            if city["tel"] == city_tel:
                return search_city, city

            if city["down"]:
                search_list.append(city)
    return


def mymain(op, lock):
    # lock.acquire()
    file_path = op.file_path
    with open(file_path, "r", encoding='UTF-8') as f:
        citys_json = f.read()
        citys_dict = json.loads(citys_json)
        f.close()
        try:
            if search_city_name(citys_dict, op.cityname):
                father_city, user_in_city = search_city_name(citys_dict, op.cityname)

            elif search_city_controller(citys_dict, op.controll_person):
                father_city, user_in_city = search_city_controller(citys_dict, op.controll_person)

            elif search_city_tel(citys_dict, op.controll_tel):
                father_city, user_in_city = search_city_tel(citys_dict, op.controll_tel)

            else:
                print("城市不存在")
                return
        except TypeError:
            print("查询信息错误 请核对后再次输入")
            return
        print(user_in_city)

        # -P 修改负责人信息
        if op.change_person:
            user_in_city["controller"]["name"] = op.change_person

        # -P 修改负责人信息
        if op.change_tel:
            user_in_city["controller"]["tel"] = op.change_tel

        if op.delete_controller:
            user_in_city["controller"]["name"] = None
            user_in_city["controller"]["tel"] = None

        # -a 增加下属城市 -a "北京市，赵兴，486453"
        if op.add_city:
            add_city_list = op.add_city.split(",")
            new_controller = {"name":add_city_list[1], "tel":add_city_list[2]}
            new_city = {"name":add_city_list[0], "controller":new_controller, "down": []}

            if new_city not in user_in_city["down"]:
                user_in_city["down"].append(new_city)

        # -C "cityname=成都市1"
        if op.change_city:
            change_city_name = op.change_city.split("=")[1]
            user_in_city.name = change_city_name

        print(user_in_city)
        # -d存在。删除城市
        if op.delete_city:
            father_city["down"].remove(user_in_city)
            print(father_city)
            return

        res_list = []
        for down_city in user_in_city["down"]:
            res_list.append(down_city["name"])
        print(user_in_city["name"], res_list, user_in_city["controller"])

        with open('new.json', "w", encoding="utf-8") as f:
                print(citys_dict)
                citys_json = json.dumps(citys_dict,ensure_ascii=False)
                f.write(citys_json)
                f.close()
        time.sleep(5)
        # lock.release()




from optparse import OptionParser
optParser = OptionParser()

#文件所在位置
optParser.add_option('-f','--file_path',action = 'store',type = "string" ,dest = 'file_path')

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





from multiprocessing import Process, Lock

if __name__ == '__main__':
    lock = Lock()
    for i in range(4):
        city_name = "hhh" + str(i)
        new_city_controller = "哈哈哈" + str(i)
        new_city_tel = "0000000000" + str(i)

        city_info = city_name + "," + new_city_controller + "," + new_city_tel
        fakeArgs = ["-f", "new.json", "-c", "成都", "-a", city_info]
        op, ar = optParser.parse_args(fakeArgs)
        # mymain(op)
        p = Process(target=mymain, args=(op,lock))
        p.start()








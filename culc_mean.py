f = open('txt/thesis_data_20220123_01.txt', 'r', encoding='UTF-8')
datalist = f.readlines()

sum_of_count = int()
sum_of_time = float()
sum_of_decodetime = float()
log_info = list()
n = int()

for i, data in enumerate(datalist):
    
    if i % 2 == 0:
        elements = data.strip().split(',')
    else:
        elements = elements + data.strip().split(',')
        log_info.append(elements)

cut_id = input("please type cut_id : ")
device_id = input("please type device_id : ")

for i, element in enumerate(log_info):
    # print(i, element)
    
    if element[0] == cut_id:
        # print("cut_id = %s" % cut_id)
        if element[1] == device_id:
            is_fun_url = int(element[4])
            if is_fun_url == 0:
                continue
            # print("device_id = %s" % device_id)
            n += 1
            sum_of_count = sum_of_count + int(element[2])
            sum_of_decodetime = sum_of_decodetime + float(element[3])

            sum_of_time = sum_of_time + float(element[5])

average_of_decodetime = sum_of_decodetime / n
average_of_time = sum_of_time / n
average_of_count = sum_of_count / n

print("%d回 の平均" % n)
print("平均実行時間 %0.4fs" % average_of_time)
print("平均試行回数 %0.4f回" % average_of_count)
print('平均デコード時間 %0.4fs' % average_of_decodetime)

f.close()
f = open('packing.log', 'r', encoding='UTF-8')
datalist = f.readlines()

sum_of_count = int()
sum_of_time = float()
log_info = list()

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
            # print("device_id = %s" % device_id)
            sum_of_count = sum_of_count + int(element[2])
            sum_of_time = sum_of_time + float(element[3])



n = len(log_info)
average_of_time = sum_of_time / n
average_of_count = sum_of_count / n
print(n, sum_of_time, average_of_time, average_of_count)

f.close()
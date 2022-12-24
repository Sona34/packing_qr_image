f = open('packing.log', 'r', encoding='UTF-8')

datalist = f.readlines()
sum_of_time = float()
for i, data in enumerate(datalist):
    # print(i, data)
    if i % 2 == 1:
        time = data.split(',')
        print(time[0])
        sum_of_time = sum_of_time + float(time[0])


num = len(datalist) / 2.0
average_of_time = sum_of_time / num
print(sum_of_time, average_of_time)
f.close()
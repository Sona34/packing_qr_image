f = open('packing.log', 'r', encoding='UTF-8')
datalist = f.readlines()

sum_of_time = float()
sum_of_count = int()

for i, data in enumerate(datalist):
    if i % 2 == 0:
        elements = data.strip().split(',')
    else:
        elements = elements + data.strip().split(',')

        sum_of_count = sum_of_count + int(elements[2])
        sum_of_time = sum_of_time + float(elements[3])



num = len(datalist) / 2.0
average_of_time = sum_of_time / num
average_of_count = sum_of_count / num
print(num, sum_of_time, average_of_time, average_of_count)

f.close()
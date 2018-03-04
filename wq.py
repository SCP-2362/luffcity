# num_dict = {}
# max_num = max(num_list)
# min_num = min(num_list)
# new_list = []
#
# for tmp in range(min_num, max_num, d):
#     num_dict[tmp] = []
#
# for n, index in enumerate(num_list):
#     pass


# for i, index in enumerate(num_list):
# if num_list[index] - num_list

# 排序
# num_list.sort()

# for index, n in enumerate(num_list, 0):
#     # print(n, index)
#     if abs(num_list[index] - num_list[index+1]) == d:
#         print(num_list[index], num_list[index+1])

import time
import random

start = time.time()
# num_list = [random.randint(1, 1000) for _ in range(1000)]
d = 2
cnt = 0
#
# num_list.sort()
# i = 0
# j = 1
# cnt = 0
# while i <= len(num_list) - 1 and j <= len(num_list) - 1:
#     if i < j and abs(num_list[i] - num_list[j]) == d:
#         print(num_list[i], num_list[j])
#         cnt += 1
#         if num_list[i] == num_list[i+1]:
#             i += 1
#         else:
#             j += 1
#         continue
#     elif i < j and abs(num_list[i] - num_list[j]) > d:
#         i += 1
#     elif i < j and abs(num_list[i] - num_list[j]) < d:
#         j += 1
#
#     if i == j:
#         j += 1

# num_list = [3, 5, 8, 7, 8, 10]
# num_list = [1, 1, 1, 2, 3, 3, 3]
num_list = [1,1,1,2,3,4,5,6,7,7,7,7,7,7]

dd = {}
for num in num_list:
    if num not in dd:
        dd.setdefault(num, 1)
    else:
        dd[num] += 1
for num in dd:
    if num+d in dd:
        cnt += dd[num]*dd[num+d]

print(cnt)
print(time.time()-start)

import random

import random

rand_list =[]

for i in range(10):
    rand_list.append(random.randint(1,20))

print(rand_list)


list_comprehension_below_10 = [x for x in rand_list if x < 10]
print(list_comprehension_below_10)

list_using_filter = list(filter(lambda x: x < 10, rand_list))
print(list_using_filter)
# list_comprehension_below_10 =
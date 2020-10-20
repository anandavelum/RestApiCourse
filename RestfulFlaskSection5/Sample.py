def square(num):
    return num % 2 == 0


mylist = [1, 2, 3, 4, 5]

print(filter(lambda x:x/3==0, mylist))

for item in (filter(lambda x:x%2==0, mylist)):
    print(item)
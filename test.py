import time
# myVar = "Salam"
# print("before: ", myVar)
# max_time = 5
# start_time = time.time()
# print("start_time", start_time)
# while (time.time() - start_time) < max_time:
#     myVar = "Sagol"

# print("before: ", myVar)
# print("Life is contiunie")


from threading import Timer

myVal = "Salam"

print("myVal before: ", myVal)
def timeout():
    myVal = "sagol"
    print("myVal after 5 seconds: ", myVal)

t = Timer(10, timeout)
t.start()


print("myVal after: ", myVal)
print("life is contiunue!")
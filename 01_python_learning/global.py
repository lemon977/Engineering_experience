'''
在 main() 函数中，param 先被当做全局引用，并修改了他的类型，从 int 型变成了 str 型
在后面调用 test() 函数的时候，判定 param==10 结果为false
param = 10
 
def test():
    if (param == 10):
        print("equal 10")
    else:
        print("not equal 10")
 
def main():
    global param
    param = "hello world"
    test()
 
if __name__ == "__main__":
    main()
'''
param = 10

def test():
    print("param_value:%d\t param_id:%d" %(param, id(param)))
    if (param == 10):
        print("equal 10")
    else:
        print("not equal 10")

def main():
    global param
    print("param_value:%d\t param_id:%d" %(param, id(param)))
    param = 6
    print("param_value:%d\t param_id:%d" %(param, id(param)))
    test()

if __name__ == "__main__":
    print("param_value:%d\t param_id:%d" %(param, id(param)))
    main()
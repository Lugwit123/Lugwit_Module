class OnlyOnce_AssignValue:
    def __get__(self, instance, owner):
        return instance.__dict__.get('value', None)

    def __set__(self, instance, value):
        if not instance.__dict__.get('_assigned', False):
            instance.__dict__['value'] = value
            instance.__dict__['_assigned'] = True
            print(f"{instance} -> {value} 赋值成功")
        else:
            print(f"该属性已经被赋值，忽略后续赋值操作。")

class MyClass:
    let_value = OnlyOnce_AssignValue()
    def __init__(self):
        self.let_value = 'hello'

def test():
    obj = MyClass()
    print(obj.let_value)  # 输出 "hello"
    obj.let_value = 42    # 输出 "该属性已经被赋值，忽略后续赋值操作。"
    print(obj.let_value)  # 输出 "hello"
    obj.let_value = 100   # 输出 "该属性已经被赋值，忽略后续赋值操作。"
    print(obj.let_value)  # 输出 "hello"

if __name__ == '__main__':
    test()

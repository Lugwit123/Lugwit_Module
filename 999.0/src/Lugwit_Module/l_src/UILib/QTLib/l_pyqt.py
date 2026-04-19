import functools
def add_position_method(func):
    @functools.wraps(func)
    def wrapper(self, event):
        # 如果事件没有 'position()' 方法，则添加
        if not hasattr(event, 'position'):
            # 为原始事件添加 'position()' 方法
            def position():
                return event.pos()  # 在 PyQt5 中，返回 'pos()' 的结果

            # 将 'position()' 方法添加到事件对象
            event.position = position

        return func(self, event)  # 调用原始函数，传递修改后的事件
    return wrapper
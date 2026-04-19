# -*- coding: utf-8 -*-
u"""
LPrint插件管理基类

这个模块定义了通用的插件管理功能，供LPrint类继承使用。
遵循面向对象设计原则：单一职责、开闭原则。
"""

class LPrint_Plug(object):
    u"""LPrint插件管理基类
    
    提供通用的插件管理功能：
    1. 插件安装和调用入口
    2. 通用插件管理方法
    3. 插件生命周期管理
    
    设计原则：
    - 不针对特定插件，使用plugin_type参数
    - 支持未来插件类型扩展
    - 清晰的插件边界和职责分离
    """
    
    def __init__(self):
        u"""初始化插件管理基类"""
        super(LPrint_Plug, self).__init__()
        # 插件相关属性将在使用时动态添加
    
    # =============================================================================
    # 插件入口方法
    # =============================================================================
    
    def monitor(self, *args, **kwargs):
        u"""监控对象属性变化
        
        这是插件入口方法。第一次调用时会自动安装监控插件，然后调用监控功能。
        
        Args:
            obj: 要监控的对象
            name (unicode, optional): 对象显示名称，默认自动获取变量名
            attrs (list, optional): 要监控的属性列表，默认监控所有公共属性
            
        Returns:
            ObjectMonitor: 监控器实例
            
        Example:
            >>> lprint.monitor(my_object)  # 自动安装插件并开始监控
        """
        try:
            # 导入并使用插件
            from lprint_monitor_plugin import LPrintMonitorPlugin
            
            # 检查是否已经安装
            if not hasattr(self, '_monitor_plugin'):
                plugin = LPrintMonitorPlugin()
                success = plugin.install(self)
                if success:
                    self._monitor_plugin = plugin
                    # 使用父类的日志方法（如果可用）
                    if hasattr(self, '__call__'):
                        self(u"🔌 [插件] 监控插件已自动安装成功")
                else:
                    if hasattr(self, '__call__'):
                        self(u"❌ [插件错误] 监控插件自动安装失败")
                    return None
            
            # 调用插件的monitor方法
            return self._monitor_plugin.monitor(*args, **kwargs)
                    
        except ImportError as e:
            if hasattr(self, '__call__'):
                self(u"❌ [插件错误] 监控插件文件不存在: {}".format(e))
            return None
        except Exception as e:
            if hasattr(self, '__call__'):
                self(u"❌ [插件错误] 监控功能异常: {}".format(e))
            return None
    
    # =============================================================================
    # 通用插件管理方法 - 不针对特定插件
    # =============================================================================
    
    def list_plugins(self):
        u"""列出所有已安装的插件
        
        Returns:
            list: 已安装插件列表
                [{
                    'name': unicode,     # 插件名称
                    'type': unicode,     # 插件类型 
                    'status': unicode,   # 状态
                    'instance': object   # 插件实例
                }]
        """
        plugins = []
        
        # 检查监控插件
        if hasattr(self, '_monitor_plugin'):
            plugins.append({
                'name': u'监控插件',
                'type': u'monitor',
                'status': u'已安装',
                'instance': getattr(self, '_monitor_plugin', None)
            })
        
        # 可以扩展检查其他类型的插件
        
        return plugins
    
    def get_plugin_info(self, plugin_type):
        u"""获取指定类型插件的信息
        
        Args:
            plugin_type (unicode): 插件类型，如 u'monitor'
            
        Returns:
            dict or None: 插件信息字典，如果插件未安装返回None
                {
                    'name': unicode,
                    'type': unicode,
                    'status': unicode,
                    'instance': object,
                    'methods': list  # 插件提供的方法列表
                }
        """
        if plugin_type == u'monitor':
            if hasattr(self, '_monitor_plugin'):
                plugin_instance = getattr(self, '_monitor_plugin', None)
                if plugin_instance:
                    # 获取插件提供的方法
                    methods = [attr for attr in dir(plugin_instance) 
                              if not attr.startswith('_') and callable(getattr(plugin_instance, attr))]
                    
                    return {
                        'name': u'LPrint监控插件',
                        'type': u'monitor', 
                        'status': u'已安装',
                        'instance': plugin_instance,
                        'methods': methods
                    }
        
        return None
    
    def is_plugin_installed(self, plugin_type):
        u"""检查指定类型的插件是否已安装
        
        Args:
            plugin_type (unicode): 插件类型
            
        Returns:
            bool: True如果已安装，False如果未安装
        """
        if plugin_type == u'monitor':
            return hasattr(self, '_monitor_plugin')
        
        # 可以扩展检查其他插件类型
        return False
    
    def uninstall_plugin(self, plugin_type):
        u"""卸载指定类型的插件
        
        Args:
            plugin_type (unicode): 要卸载的插件类型
            
        Returns:
            bool: True如果卸载成功，False如果失败
        """
        if plugin_type == u'monitor':
            if hasattr(self, '_monitor_plugin'):
                try:
                    # 清理插件相关属性
                    delattr(self, '_monitor_plugin')
                    
                    if hasattr(self, '__call__'):
                        self(u"🔌 [插件] 监控插件已卸载")
                    return True
                except Exception as e:
                    if hasattr(self, '__call__'):
                        self(u"❌ [插件错误] 卸载监控插件失败: {}".format(e))
                    return False
            else:
                if hasattr(self, '__call__'):
                    self(u"⚠️ [插件] 监控插件未安装，无需卸载")
                return True
        
        return False
    
    def reinstall_plugin(self, plugin_type):
        u"""重新安装指定类型的插件
        
        Args:
            plugin_type (unicode): 要重新安装的插件类型
            
        Returns:
            bool: True如果重新安装成功，False如果失败
        """
        if plugin_type == u'monitor':
            # 先卸载
            self.uninstall_plugin(plugin_type)
            
            # 重新安装通过下次调用monitor时自动安装
            if hasattr(self, '__call__'):
                self(u"🔌 [插件] 监控插件已卸载，下次调用monitor时将自动重新安装")
            return True
        
        return False
    
    def get_available_plugins(self):
        u"""获取可用的插件列表（可以安装但未安装的）
        
        Returns:
            list: 可用插件列表
                [{
                    'name': unicode,
                    'type': unicode,
                    'description': unicode,
                    'available': bool
                }]
        """
        available_plugins = []
        
        # 检查监控插件是否可用
        try:
            import lprint_monitor_plugin
            is_installed = self.is_plugin_installed(u'monitor')
            available_plugins.append({
                'name': u'LPrint监控插件',
                'type': u'monitor',
                'description': u'对象属性监控功能',
                'available': True,
                'installed': is_installed
            })
        except ImportError:
            available_plugins.append({
                'name': u'LPrint监控插件',
                'type': u'monitor',
                'description': u'对象属性监控功能',
                'available': False,
                'installed': False
            })
        
        # 可以扩展检查其他插件
        
        return available_plugins 
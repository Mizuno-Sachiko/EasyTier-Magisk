# EasyTier for Magisk

通过Magisk以root运行内置的EasyTier客户端。

[下载模块](https://github.com/Mizuno-Sachiko/EasyTier-Magisk/releases/latest) · [配置示例](config.example.toml) · [GPL-3.0](LICENSE)

需要arm64设备、Android API31+、Magisk，以及Termux Python3.11+。

安装前，将[配置示例](config.example.toml)保存为手机上的`/data/adb/easytier/config.toml`，填写网络名称、密码、节点密钥和虚拟IP。安装后重启并解锁一次，模块自动启动；支持Magisk在线更新。

若另外使用EasyTier App，避免与模块同时运行同一份节点配置。

`config.toml`中的`[magisk.easytier]`包含模块的路由设置。`route_priority`设置访问EasyTier内网的规则优先级；`root_rule_priority`和`root_rule_target`设置root流量跳过Android VPN选路的规则。优先级数值决定系统执行这些规则的顺序。

模块脚本与[Magisk安装器](https://github.com/topjohnwu/Magisk)采用[GPL-3.0](LICENSE)；内核与CLI来自[EasyTier](https://github.com/EasyTier/EasyTier)，采用[LGPL-3.0](licenses/EasyTier.LICENSE)。

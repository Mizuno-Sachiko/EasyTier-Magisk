# EasyTier for Magisk

通过Magisk运行EasyTier，读取私有TOML配置，并管理Android VPN共存所需的策略路由。

[下载模块](https://github.com/Mizuno-Sachiko/EasyTier-Magisk/releases/latest) · [配置示例](config.example.toml) · [GPL-3.0](LICENSE)

需要arm64设备、Android API31+、Magisk，以及Termux Python3.11+。

私有配置保存在`/data/adb/easytier/config.toml`。安装后重启并首次解锁，保持EasyTier App中的VPN实例停止。以后可在Magisk内检查并安装更新。

策略路由优先级应按手机现有规则设置。模块为所有root进程设置VPN绕行规则，其他App保留原有行为。

当前内核来自[EasyTier2.7.0预发布版](https://github.com/EasyTier/EasyTier/releases/tag/v2.7.0)，包含节点重同步修复；相关通信节点也需升级。

推送`v内核版本-模块修订号`标签后，GitHub Actions校验官方程序包并自动打包发布，例如`v2.7.0-1`。

模块脚本与[Magisk安装器](https://github.com/topjohnwu/Magisk)采用[GPL-3.0](LICENSE)；未修改的内核与CLI来自[EasyTier源码](https://github.com/EasyTier/EasyTier/tree/v2.7.0)，采用[LGPL-3.0](licenses/EasyTier.LICENSE)。

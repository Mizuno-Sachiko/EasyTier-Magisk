SKIPMOUNT=false
PREFIX=/data/data/com.termux/files/usr
[ "$ARCH" = arm64 ] || abort "This module requires arm64."
[ "$API" -ge 31 ] || abort "This module requires Android API 31 or newer."
[ -x "$PREFIX/bin/python" ] || abort "Termux Python with tomllib is required."
[ -s /data/adb/easytier/config.toml ] || abort "Existing private EasyTier configuration is required."
set_perm_recursive "$MODPATH" 0 0 0700 0600
set_perm "$MODPATH/service.sh" 0 0 0700
set_perm "$MODPATH/easytier-core" 0 0 0700
set_perm "$MODPATH/easytier-cli" 0 0 0700
set_perm "$MODPATH/module.prop" 0 0 0644
set_perm_recursive "$MODPATH/system" 0 0 0755 0644
"$PREFIX/bin/python" "$MODPATH/run.py" --check-config || abort "Invalid EasyTier or module configuration."
ui_print "Private configuration is preserved."
ui_print "Starts after first unlock. Keep the EasyTier app VPN stopped."
ui_print "Reboot after disabling or uninstalling. Termux must remain installed."

#!/system/bin/sh
MODDIR=${0%/*}
# Termux Python is credential-encrypted and becomes available after first unlock.
while [ "$(getprop sys.boot_completed)" != "1" ] || \
      [ "$(getprop sys.user.0.ce_available)" != "true" ]; do
    sleep 5
done
[ ! -f "$MODDIR/disable" ] || exit 0
umask 077
exec /data/data/com.termux/files/usr/bin/python -u "$MODDIR/run.py" \
    > /data/adb/easytier/module-launch.log 2>&1

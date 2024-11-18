# Control Package

Backend processes that control and cordinate with the Web Interface, Remote Sensor Clusters, and Grafana/Prometheus stack.

## Service Unit Example

```ini
[Unit]
Description=Run My Python Script
After=network.target

[Service]
Type=simple
ExecStart=/opt/my_script/venv/bin/python /opt/my_script/my_script.py

# Sandbox Settings
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ProtectKernelModules=true
ProtectControlGroups=true
ProtectHostname=true
ReadOnlyPaths=/etc /usr /var
ReadWritePaths=/var/tmp
RestrictAddressFamilies=AF_INET AF_INET6 AF_UNIX
RestrictNamespaces=true
RestrictRealtime=true
LockPersonality=true

# Limit Capabilities
CapabilityBoundingSet=
AmbientCapabilities=

# User and Group
User=scriptuser
Group=scriptuser

[Install]
WantedBy=multi-user.target
```

import string

template = string.Template("""#
# Copyright (c) 2014 Juniper Networks, Inc. All rights reserved.
#
# DNS configuration options
#

[DEFAULT]
# collectors= # Provided by discovery server
# dns_config_file=contrail-dns.conf
# named_config_file=contrail-named.conf                 # named config file
# named_config_directory=/etc/contrail/dns              # named config directory
# named_log_file=/var/log/contrail/contrail-named.log   # named log file
# rndc_config_file=contrail-rndc.conf                   # rndc config file
# rndc_secret=secretkey                                 # rndc secret
  hostip=$__contrail_host_ip__ # Resolved IP of `hostname`
  hostname=$__contrail_hostname__ # Retrieved as `hostname`
# http_server_port=8092
# dns_server_port=53
# log_category=
# log_disable=0
  log_file=/var/log/contrail/contrail-dns.log
# log_files_count=10
# log_file_size=1048576 # 1MB
  log_level=SYS_NOTICE
  log_local=1
# test_mode=0

[DISCOVERY]
# port=5998
  server=$__contrail_discovery_ip__ # discovery-server IP address

[IFMAP]
  certs_store=$__contrail_cert_ops__
  password=$__contrail_ifmap_paswd__
# server_url= # Provided by discovery server, e.g. https://127.0.0.1:8443
  user=$__contrail_ifmap_usr__

""")

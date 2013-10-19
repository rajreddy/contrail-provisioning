#!/usr/bin/python

import argparse
import ConfigParser

import os
import sys

sys.path.insert(0, os.getcwd())
from contrail_setup_utils.setup import Setup

class SetupVncVrouter(object):
    def __init__(self, args_str = None):
        self._args = None
        if not args_str:
            args_str = ' '.join(sys.argv[1:])
        self._parse_args(args_str)

        cfgm_ip = self._args.cfgm_ip
        openstack_ip = self._args.openstack_ip
        service_token = self._args.service_token
        ncontrols = self._args.ncontrols
        non_mgmt_ip = self._args.non_mgmt_ip
        non_mgmt_gw = self._args.non_mgmt_gw
        if not self._args.openstack_mgmt_ip :
            openstack_mgmt_ip = openstack_ip
        else:
            openstack_mgmt_ip = self._args.openstack_mgmt_ip

        setup_args_str = "--role compute --compute_ip %s " %(self._args.self_ip)
        setup_args_str = setup_args_str + " --cfgm_ip %s " %(cfgm_ip)
        setup_args_str = setup_args_str + " --openstack_ip %s " %(openstack_ip)
        setup_args_str = setup_args_str + " --openstack_mgmt_ip %s " %(openstack_mgmt_ip)
        if service_token:
            setup_args_str = setup_args_str + " --service_token %s " %(service_token)
        setup_args_str = setup_args_str + " --ncontrols %s " %(ncontrols)
        if non_mgmt_ip: 
            setup_args_str = setup_args_str + " --non_mgmt_ip %s " %(non_mgmt_ip)
            setup_args_str = setup_args_str + " --non_mgmt_gw %s " %(non_mgmt_gw)

        setup_obj = Setup(setup_args_str)
        setup_obj.do_setup()
        setup_obj.run_services()
    #end __init__

    def _parse_args(self, args_str):
        '''
        Eg. python setup-vnc-vrouter.py --cfgm_ip 10.1.5.11 --openstack_ip 10.1.5.12
                   --self_ip 10.1.5.12 --service_token 'c0ntrail123' --ncontrols 1
        '''

        # Source any specified config/ini file
        # Turn off help, so we print all options in response to -h
        conf_parser = argparse.ArgumentParser(add_help = False)
        
        conf_parser.add_argument("-c", "--conf_file",
                                 help="Specify config file", metavar="FILE")
        args, remaining_argv = conf_parser.parse_known_args(args_str.split())

        global_defaults = {
            'cfgm_ip': '127.0.0.1',
            'openstack_ip': '127.0.0.1',
            'openstack_mgmt_ip': None,
            'service_token': '',
            'self_ip': '127.0.0.1',
            'ncontrols': '2',
            'non_mgmt_ip': None,
            'non_mgmt_gw': None,
        }

        if args.conf_file:
            config = ConfigParser.SafeConfigParser()
            config.read([args.conf_file])
            global_defaults.update(dict(config.items("GLOBAL")))

        # Override with CLI options
        # Don't surpress add_help here so it will handle -h
        parser = argparse.ArgumentParser(
            # Inherit options from config_parser
            parents=[conf_parser],
            # print script description with -h/--help
            description=__doc__,
            # Don't mess with format of description
            formatter_class=argparse.RawDescriptionHelpFormatter,
            )

        all_defaults = {'global': global_defaults}
        parser.set_defaults(**all_defaults)

        parser.add_argument("--cfgm_ip", help = "IP Address of the config node")
        parser.add_argument("--openstack_ip", help = "IP Address of the openstack node")
        parser.add_argument("--openstack_mgmt_ip", help = "Mgmt IP Address of the openstack node if it is different from openstack_IP")
        parser.add_argument("--service_token", help = "The service password to access keystone")
        parser.add_argument("--self_ip", help = "IP Address of this(compute) node")
        parser.add_argument("--ncontrols", help = "Number of control-nodes in the system")
        parser.add_argument("--non_mgmt_ip", help = "IP Address of non-management interface(fabric network) on the compute  node")
        parser.add_argument("--non_mgmt_gw", help = "Gateway Address of the non-management interface(fabric network) on the compute node")

        self._args = parser.parse_args(remaining_argv)

    #end _parse_args

#end class SetupVncVrouter

def main(args_str = None):
    SetupVncVrouter(args_str)
#end main

if __name__ == "__main__":
   main() 
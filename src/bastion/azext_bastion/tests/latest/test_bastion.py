# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#
# Code generated by aaz-dev-tools
# --------------------------------------------------------------------------------------------

# pylint: disable=line-too-long

from azure.cli.testsdk import *
from azure.cli.testsdk.scenario_tests import AllowLargeResponse


class BastionScenario(ScenarioTest):
    @AllowLargeResponse()
    @ResourceGroupPreparer(name_prefix="cli_test_bastion_host_", location="westus2")
    def test_bastion_host_crud(self):
        self.kwargs.update({
            "vnet_name": self.create_random_name("vnet-", 12),
            "subnet_name": self.create_random_name("subnet-", 12),
            "ip_name": self.create_random_name("ip-", 8),
            "vm_name": self.create_random_name("vm-", 8),
            "bastion_name": self.create_random_name("bastion-", 12),
        })
        self.cmd("network vnet create -n {vnet_name} -g {rg} --subnet-name AzureBastionSubnet")
        self.cmd("network vnet subnet create -n {subnet_name} -g {rg} --vnet-name {vnet_name} --address-prefixes 10.0.2.0/24")
        self.cmd("network public-ip create -n {ip_name} -g {rg} --sku Standard")
        self.cmd("vm create -n {vm_name} -g {rg} --vnet-name {vnet_name} --subnet {subnet_name} --nsg-rule None --image UbuntuLTS --authentication-type password --admin-username testadmin --admin-password TestPassword11!!")

        self.cmd(
            "network bastion create -n {bastion_name} -g {rg} --public-ip-address {ip_name} --vnet-name {vnet_name} "
            "--disable-copy-paste --enable-ip-connect --enable-tunneling --scale-units 21 --tags foo=bar",
            checks=[
                self.check("name", "{bastion_name}"),
                self.check("disableCopyPaste", True),
                self.check("enableIpConnect", True),
                self.check("enableTunneling", True),
                self.check("sku.name", "Standard"),
                self.check("tags.foo", "bar"),
                self.check("scaleUnits", 21),
                self.check("type", "Microsoft.Network/bastionHosts"),
            ]
        )
        self.cmd(
            "network bastion update -n {bastion_name} -g {rg} "
            "--disable-copy-paste false --enable-ip-connect false --enable-tunneling false --scale-units 42",
            checks=[
                self.check("disableCopyPaste", False),
                self.check("enableIpConnect", False),
                self.check("enableTunneling", False),
                self.check("scaleUnits", 42),
            ]
        )
        self.cmd("network bastion list")
        self.cmd(
            "network bastion list -g {rg}",
            checks=[
                self.check("length(@)", 1),
                self.check("[0].name", "{bastion_name}"),
            ]
        )
        self.cmd(
            "network bastion show -n {bastion_name} -g {rg}",
            checks=[
                self.check("name", "{bastion_name}"),
                self.check("type", "Microsoft.Network/bastionHosts"),
            ]
        )
        self.cmd("network bastion delete -n {bastion_name} -g {rg}")
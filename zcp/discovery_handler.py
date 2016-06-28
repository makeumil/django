"""
Class for polling Ceilometer

This class provides means to requests for authentication tokens to be used with OpenStack's Ceilometer, Nova and RabbitMQ
"""

__authors__ = "Keumil Ma."
__copyright__ = "Copyright (c) 2016 Keumil Ma."
__license__ = "Indivisual approval"
__contact__ = "makeumil@gmail.com"
__date__ = "03/21/2016"

__version__ = "1.0"

import urllib2
import json

class DiscoveryHandler:

    def __init__(self, ceilometer_api_port, template_name, ceilometer_api_host, zabbix_host,
                 zabbix_port, zabbix_proxy_name, keystone_auth):
        """
        TODO
        :type self: object
        """
        self.ceilometer_api_port = ceilometer_api_port
        self.template_name = template_name
        self.ceilometer_api_host = ceilometer_api_host
        self.zabbix_host = zabbix_host
        self.zabbix_port = zabbix_port
        self.zabbix_proxy_name = zabbix_proxy_name
        self.keystone_auth = keystone_auth

    def discovery_networks(self, host_id):

        links = []
        itemKeys = []
        self.token = self.keystone_auth.getToken()

        request = urllib2.urlopen(urllib2.Request(
            "http://" + self.ceilometer_api_host + ":" + self.ceilometer_api_port +
            "/v2/resources?q.field=metadata.instance_id&q.value=" + host_id,
            headers={"Accept": "application/json", "Content-Type": "application/json",
                     "X-Auth-Token": self.token})).read()

        for line in json.loads(request):
            for line2 in line['links']:
                if line2['rel'] in ('network.incoming.bytes', 'network.outgoing.bytes'):
                   links.append(line2)

        for line in links:
            itemKeys.append(self.query_ceilometer(host_id, line['rel'], line['href']))

        return itemKeys

    def query_ceilometer(self, resource_id, item_key, link):
        """
        TODO
        :param resource_id:
        :param item_key:
        :param link:
        """
        try:
            global contents

            contents = urllib2.urlopen(urllib2.Request(link + str("&limit=1"),
                                                       headers={"Accept": "application/json",
                                                                "Content-Type": "application/json",
                                                                "X-Auth-Token": self.token})).read()

        except urllib2.HTTPError, e:
            if e.code == 401:
                print "401"
                print "Error... \nToken refused! Please check your credentials"
            elif e.code == 404:
                print 'not found'
            elif e.code == 503:
                print 'service unavailable'
            else:
                print 'unknown error: '

        response = json.loads(contents)

        try:
            counter_volume = response[0]['counter_volume']
            #discovery item_key
            item_key = item_key + "[" + response[0]['resource_metadata']['name'] + "]"
            return item_key

        except:
            pass




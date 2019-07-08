# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html
from . import Aws
 

class Route53(Aws):
    _client_name = 'route53'
     
    def __init__(self, session=None, profile_name=None):
        super().__init__(session=session, profile_name=profile_name)
        self.set_current_client()
        self._zones = None
    
    def clear(self):
        self._zones = None

    @property
    def zones(self):
        if not self._zones:
            self._zones = self.client.list_hosted_zones() 
        return self._zones

    def get_zone_by_name(self, domain):
        # print(self.zones['HostedZones'])
        zones = list(filter(lambda i: i['Name'].startswith(domain), self.zones['HostedZones']))
        return zones and zones[0]

    def list_records(self, domain):
        zone = self.get_zone_by_name(domain)
        return zone and self.client.list_resource_record_sets(HostedZoneId=zone['Id'])

    def update_resource(self, domain, res_type, value):
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.change_resource_record_sets
        # https://docs.aws.amazon.com/ja_jp/Route53/latest/APIReference/API_ChangeResourceRecordSets.html
        zone = self.get_zone_by_name(domain)
        if not zone:
            return

        ChangeBatch = {
            'Action': 'UPSERT',
            'Type': res_type,
            "ResourceRecords": [
                {
                    'Value': value
                },
            ],
        }
        return self.client.change_resource_record_sets(
            HostedZoneId=zone['Id'],
            ChangeBatch=ChangeBatch, 
        )
import boto3
import hashlib
import json
import urllib2
# Name of the service, as seen in the ip-groups.json file, to extract inf
SERVICE = "CLOUDFRONT"
# Ports your application uses that need inbound permissions from the serv
INGRESS_PORTS = [ 80, 443 ]
# Tags which identify the security groups you want to update
SECURITY_GROUP_TAGS = { 'Name': 'cloudfront', 'AutoUpdate': 'true' }
def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    message = json.loads(event['Records'][0]['Sns']['Message'])
    # Load the ip ranges from the url
    ip_ranges = json.loads(get_ip_groups_json(message['url'], message['md']))
    # extract the service ranges
    cf_ranges = get_ranges_for_service(ip_ranges, SERVICE)
    # update the security groups
    result = update_security_groups(cf_ranges)
    return result

def get_ip_groups_json(url, expected_hash):
    print("Updating from " + url)
    response = urllib2.urlopen(url)
    ip_json = response.read()
    m = hashlib.md5()
    m.update(ip_json)
    hash = m.hexdigest()
    if hash != expected_hash:
        raise Exception('MD5 Mismatch: got ' + hash + ' expected ' + expected_hash)
    return ip_json

def get_ranges_for_service(ranges, service):
    service_ranges = list()
    for prefix in ranges['prefixes']:
        if prefix['service'] == service:
            print('Found ' + service + ' range: ' + prefix['ip_prefix'])
            service_ranges.append(prefix['ip_prefix'])
    return service_ranges
def update_security_groups(new_ranges):
    client = boto3.client('ec2')
    groups = get_security_groups_for_update(client)
    print ('Found ' + str(len(groups)) + ' SecurityGroups to update')
    result = list()
    updated = 0
    for group in groups:
        if update_security_group(client, group, new_ranges):
            updated += 1
            result.append('Updated ' + group['GroupId'])
    result.append('Updated ' + str(updated) + ' of ' + str(len(groups)) )
    return result
def update_security_group(client, group, new_ranges):
    added = 0
    removed = 0
    if len(group['IpPermissions']) > 0:
        for permission in group['IpPermissions']:
            if INGRESS_PORTS.count(permission['ToPort']) > 0:
                old_prefixes = list()
                to_revoke = list()
                to_add = list()
                for range in permission['IpRanges']:
                    cidr = range['CidrIp']
                    old_prefixes.append(cidr)
                    if new_ranges.count(cidr) == 0:
                        to_revoke.append(range)
                        print(group['GroupId'] + ": Revoking " + cidr + "
                for range in new_ranges:
                    if old_prefixes.count(range) == 0:
                        to_add.append({ 'CidrIp': range })
                        print(group['GroupId'] + ": Adding " + range + ":
                removed += revoke_permissions(client, group, permission,
                added += add_permissions(client, group, permission, to_ad
    else:
        for port in INGRESS_PORTS:
            to_add = list()
            for range in new_ranges:
                to_add.append({ 'CidrIp': range })
                print(group['GroupId'] + ": Adding " + range + ":" + str(
            permission = { 'ToPort': port, 'FromPort': port, 'IpProtocol'
            added += add_permissions(client, group, permission, to_add)
    print (group['GroupId'] + ": Added " + str(added) + ", Revoked " )
    return (added > 0 or removed > 0)
def revoke_permissions(client, group, permission, to_revoke):
    if len(to_revoke) > 0:
        revoke_params = {
            'ToPort': permission['ToPort'],
            'FromPort': permission['FromPort'],
            'IpRanges': to_revoke,
            'IpProtocol': permission['IpProtocol']
        }
        client.revoke_security_group_ingress(GroupId=group['GroupId'], 
        return len(to_revoke)
def add_permissions(client, group, permission, to_add):
    if len(to_add) > 0:
        add_params = {
            'ToPort': permission['ToPort'],
            'FromPort': permission['FromPort'],
            'IpRanges': to_add,
            'IpProtocol': permission['IpProtocol']
        }
        client.authorize_security_group_ingress(GroupId=group['GroupId'],
    return len(to_add)
def get_security_groups_for_update(client):
    filters = list();
    for key, value in SECURITY_GROUP_TAGS.iteritems():
        filters.extend(
            [
                { 'Name': "tag-key", 'Values': [ key ] },
                { 'Name': "tag-value", 'Values': [ value ] }
            ]
        )
    response = client.describe_security_groups(Filters=filters)
    return response['SecurityGroups']
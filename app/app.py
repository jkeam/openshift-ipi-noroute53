from flask import Flask, Response, request
from logging import DEBUG

app = Flask(__name__)
app.logger.setLevel(DEBUG)

# common endpoints
# route53:ListHostedZones
# route53:ListHostedZonesByName
# route53:ListResourceRecordSets
# route53:ListTagsForResource
# route53:ChangeTagsForResource
# route53:ChangeResourceRecordSets
# route53:UpdateHostedZoneComment
# route53:GetHostedZone
# route53:GetAccountLimit
# route53:GetChange

# only if using existing hostedZone in install-config.yaml
# tag:GetResources
# tag:UntagResources

global_not_supported_xml = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><NotSupported xmlns=\"https://route53.amazonaws.com/doc/2013-04-01/\"></NotSupported>"

# CHANGE: global_domain_name, global_hosted_zone, global_vpc_id, global_region
global_domain_name = 'jkeam.com'
global_hosted_zone = 'Z0363864JAYGVLIQQGUA'
global_vpc_id = 'vpc-0f1aac21e77a1aa6c'
global_region = 'us-east-2'

@app.route("/")
def home():
    app.logger.info('home')
    return "<p>Greetings!</p>"

# route53:ListHostedZones
# route53:CreateHostedZone
@app.route("/2013-04-01/hostedzone", methods=['GET', 'POST'])
@app.route("/2013-04-01/hostedzone/", methods=['GET', 'POST'])
def listhostedzone():
    app.logger.info('listhostedzone')
    if request.method == 'GET':
        xml = f"<?xml version=\"1.0\"?><ListHostedZonesResponse xmlns=\"https://route53.amazonaws.com/doc/2013-04-01/\"><HostedZones><HostedZone><Id>/hostedzone/{global_hosted_zone}</Id><Name>{global_domain_name}.</Name><CallerReference>750324a2-72dc-4334-9db1-cd26b84753a6</CallerReference><Config><PrivateZone>true</PrivateZone></Config><ResourceRecordSetCount>2</ResourceRecordSetCount></HostedZone></HostedZones><IsTruncated>false</IsTruncated><MaxItems>100</MaxItems></ListHostedZonesResponse>"
    else:
        xml = f"<?xml version=\"1.0\"?><CreateHostedZoneResponse xmlns=\"https://route53.amazonaws.com/doc/2013-04-01/\"><HostedZone><Id>/hostedzone/{global_hosted_zone}</Id><Name>{global_domain_name}.</Name><CallerReference>750324a2-72dc-4334-9db1-cd26b84753a7</CallerReference><Config><PrivateZone>true</PrivateZone></Config><ResourceRecordSetCount>2</ResourceRecordSetCount></HostedZone><ChangeInfo><Id>/change/C0208895PE2NZJ95LPMS</Id><Status>INSYNC</Status><SubmittedAt>2024-12-01T18:26:23.015Z</SubmittedAt></ChangeInfo><DelegationSet><NameServers><NameServer>ns-1024.awsdns-57.org</NameServer><NameServer>ns-1536.awsdns-13.co.uk</NameServer><NameServer>ns-512.awsdns-05.net</NameServer><NameServer>ns-0.awsdns-00.com</NameServer></NameServers></DelegationSet></CreateHostedZoneResponse>"
    return Response(xml, mimetype='text/xml')

# route53:ListHostedZonesByName
@app.route("/2013-04-01/hostedzonesbyname", methods=['GET'])
@app.route("/2013-04-01/hostedzonesbyname/", methods=['GET'])
def hostedzonesbyname():
    app.logger.info('hostedzonesbyname')
    if request.method == 'GET':
        xml = f"<?xml version=\"1.0\"?> <ListHostedZonesByNameResponse xmlns=\"https://route53.amazonaws.com/doc/2013-04-01/\"> <HostedZones> <HostedZone> <Id>/hostedzone/{global_hosted_zone}</Id> <Name>{global_domain_name}.</Name> <CallerReference>750324a2-72dc-4334-9db1-cd26b84753a6</CallerReference> <Config> <Comment></Comment> <PrivateZone>true</PrivateZone> </Config> <ResourceRecordSetCount>2</ResourceRecordSetCount> </HostedZone> </HostedZones> <IsTruncated>false</IsTruncated> <MaxItems>100</MaxItems> </ListHostedZonesByNameResponse>"
    return Response(xml, mimetype='text/xml')

# route53:GetHostedZone
# route53:UpdateHostedZoneComment
# route53:DeleteHostedZone
@app.route("/2013-04-01/hostedzone/<hostedzoneid>", methods=['GET', 'POST', 'DELETE'])
@app.route("/2013-04-01/hostedzone/<hostedzoneid>/", methods=['GET', 'POST', 'DELETE'])
def hostedzone(hostedzoneid):
    app.logger.info('hostedzone')
    if request.method == 'GET':
        xml = f"<?xml version=\"1.0\"?><GetHostedZoneResponse xmlns=\"https://route53.amazonaws.com/doc/2013-04-01/\"><HostedZone><Id>/hostedzone/{hostedzoneid}</Id><Name>{global_domain_name}.</Name><CallerReference>750324a2-72dc-4334-9db1-cd26b84753a6</CallerReference><Config><Comment>comment</Comment><PrivateZone>true</PrivateZone></Config><ResourceRecordSetCount>2</ResourceRecordSetCount></HostedZone><VPCs><VPC><VPCRegion>{global_region}</VPCRegion><VPCId>{global_vpc_id}</VPCId></VPC></VPCs><HostedZoneDeletionProtectionEnabled>false</HostedZoneDeletionProtectionEnabled></GetHostedZoneResponse>"
    elif request.method == 'POST':
        xml = f"<?xml version=\"1.0\"?><UpdateHostedZoneCommentResponse xmlns=\"https://route53.amazonaws.com/doc/2013-04-01/\"><HostedZone><Id>/hostedzone/{hostedzoneid}</Id><Name>{global_domain_name}.</Name><CallerReference>750324a2-72dc-4334-9db1-cd26b84753a6</CallerReference><Config><Comment>comment</Comment><PrivateZone>true</PrivateZone></Config><ResourceRecordSetCount>2</ResourceRecordSetCount></HostedZone></UpdateHostedZoneCommentResponse>"
    else:
        xml = "<?xml version=\"1.0\"?><DeleteHostedZoneResponse xmlns=\"https://route53.amazonaws.com/doc/2013-04-01/\"><ChangeInfo><Id>/change/C07010562BL4MTHD97OKE</Id><Status>INSYNC</Status><SubmittedAt>2024-12-01T18:48:01.403Z</SubmittedAt></ChangeInfo></DeleteHostedZoneResponse>"
    return Response(xml, mimetype='text/xml')

# route53:ListResourceRecordSets
# route53:ChangeResourceRecordSets
@app.route("/2013-04-01/hostedzone/<hostedzone>/rrset", methods=['GET', 'POST'])
@app.route("/2013-04-01/hostedzone/<hostedzone>/rrset/", methods=['GET', 'POST'])
def listresourcerecordsets(hostedzone):
    app.logger.info('listresourcerecordsets')
    name = request.args.get('name') 
    if request.method == 'GET':
        xml = f"<?xml version=\"1.0\"?><ListResourceRecordSetsResponse xmlns=\"https://route53.amazonaws.com/doc/2013-04-01/\"> <ResourceRecordSets> <ResourceRecordSet> <Name>{name}</Name> <Type>NS</Type> <TTL>172800</TTL> <ResourceRecords> <ResourceRecord> <Value>ns-1536.awsdns-00.co.uk.</Value> </ResourceRecord> <ResourceRecord> <Value>ns-0.awsdns-00.com.</Value> </ResourceRecord> <ResourceRecord> <Value>ns-1024.awsdns-00.org.</Value> </ResourceRecord> <ResourceRecord> <Value>ns-512.awsdns-00.net.</Value> </ResourceRecord> </ResourceRecords> </ResourceRecordSet> <ResourceRecordSet> <Name>{name}</Name> <Type>SOA</Type> <TTL>900</TTL> <ResourceRecords> <ResourceRecord> <Value>ns-1536.awsdns-00.co.uk. awsdns-hostmaster.amazon.com. 1 7200 900 1209600 86400</Value> </ResourceRecord> </ResourceRecords> </ResourceRecordSet> </ResourceRecordSets> <IsTruncated>false</IsTruncated> <MaxItems>100</MaxItems> </ListResourceRecordSetsResponse>"
    else:
        xml = "<?xml version=\"1.0\"?><ChangeResourceRecordSetsResponse xmlns=\"https://route53.amazonaws.com/doc/2013-04-01/\"><ChangeInfo><Id>/change/C03544601X8PH8623MUVC</Id><Status>INSYNC</Status><SubmittedAt>2024-12-01T17:47:43.541Z</SubmittedAt><Comment>comment</Comment></ChangeInfo></ChangeResourceRecordSetsResponse>"
    return Response(xml, mimetype='text/xml')

# route53:ListTagsForResource
# route53:ChangeTagsForResource
@app.route("/2013-04-01/tags/hostedzone/<hostedzone>", methods=['GET', 'POST'])
@app.route("/2013-04-01/tags/hostedzone/<hostedzone>/", methods=['GET', 'POST'])
def listtagsforresource(hostedzone):
    app.logger.info('listtagsforresource')
    if request.method == 'GET':
        xml = f"<?xml version=\"1.0\"?><ListTagsForResourceResponse xmlns=\"https://route53.amazonaws.com/doc/2013-04-01/\"><ResourceTagSet><ResourceType>hostedzone</ResourceType><ResourceId>{hostedzone}</ResourceId><Tags/></ResourceTagSet></ListTagsForResourceResponse>"
    else:
        xml = "<?xml version=\"1.0\"?><ChangeTagsForResourceResponse xmlns=\"https://route53.amazonaws.com/doc/2013-04-01/\"></ChangeTagsForResourceResponse>"
    return Response(xml, mimetype='text/xml')

# route53:GetAccountLimit
@app.route("/2013-04-01/accountlimit/<accounttype>", methods=['GET'])
@app.route("/2013-04-01/accountlimit/<accounttype>/", methods=['GET'])
def getaccountlimit(accounttype):
    app.logger.info(f"accountlimit/{accounttype}")
    if accounttype == 'MAX_HEALTH_CHECKS_BY_OWNER':
        value = 200
    elif accounttype == 'MAX_HOSTED_ZONES_BY_OWNER':
        value = 500
    elif accounttype == 'MAX_REUSABLE_DELEGATION_SETS_BY_OWNER':
        value = 100
    elif accounttype == 'MAX_TRAFFIC_POLICIES_BY_OWNER':
        value = 50
    elif accounttype == 'MAX_TRAFFIC_POLICY_INSTANCES_BY_OWNER':
        value = 5
    else:
        return Response(global_not_supported_xml, mimetype='text/xml')
    xml = "f<?xml version=\"1.0\"?><GetAccountLimitResponse xmlns=\"https://route53.amazonaws.com/doc/2013-04-01/\"><Limit><Type>{accounttype}</Type><Value>{value}</Value></Limit><Count>0</Count></GetAccountLimitResponse>"
    return Response(xml, mimetype='text/xml')

# route53:GetChange
@app.route("/2013-04-01/change/<changeid>", methods=['GET'])
@app.route("/2013-04-01/change/<changeid>/", methods=['GET'])
def getchange(changeid):
    app.logger.info(f"change/{changeid}")
    xml = "f<?xml version=\"1.0\"?><GetChangeResponse xmlns=\"https://route53.amazonaws.com/doc/2013-04-01/\"><ChangeInfo><Id>/change/f{changeid}</Id><Status>INSYNC</Status><SubmittedAt>2024-12-01T17:47:43.541Z</SubmittedAt><Comment>comment</Comment></ChangeInfo></GetChangeResponse>"
    return Response(xml, mimetype='text/xml')

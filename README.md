# OpenShift IPI No Route53

OpenShift IPI on AWS with no Route53

## Environment Setup

### AWS

1. Create VPC with DHCP Option Set and redirect route.amazonaws.com to some EC2 server running there

2. VPC should have public and private subnet

3. Public subnet needs an internet gateway to 0.0.0.0 and 10.0.0.0 to local and last one to s3 gateway

4. Private subnet needs 10.0.0.0 to local and 0.0.0.0 to nat gateway that goes through public subnet and last one to s3 gateway

5. VPC should also have private endpoints to ec2.us-east-2.amazonaws.com, elasticloadbalancing.us-east-2.amazonaws.com, tagging.us-east-2.amazonaws.com

### DNS Server

```shell
sudo dnf install dnsmasq
scp ./dns/dnsmasq.conf dnsserver:/etc/dnsmasq.conf
sudo systemctl restart dnsmasq.service
sudo systemctl enable dnsmasq.service
```

### Custom Route53 Service

#### Certs

Need to generate certs so that we can listen on https

```shell
openssl req -x509 \
            -nodes \
            -days 365 \
            -newkey rsa:2048 \
            -subj "/CN=route53.amazonaws.com" \
            -addext "subjectAltName = DNS:route53.amazonaws.com" \
            -out cert.pem \
            -keyout private.key

sudo cp ./cert.pem /etc/pki/ca-trust/source/anchors/
sudo update-ca-trust
```

#### Setup App

1. Setup python

    ```shell
    python3 -m venv venv
    source ./venv/bin/activate
    pip install --upgrade pip && pip install flask
    ```

2. Create `run.sh`

  ```shell
  # replace the cert and key path
  python -m flask run --host=0.0.0.0 -p 443 --cert=/home/ec2-user/app/cert.pem --key=/home/ec2-user/app/private.key
  ```

#### Running App

```shell
sudo ./run.sh > app.nohup 2>&1 &
```

## OpenShift

### Installation

```shell
mkdir install && cp ./install-config.yaml ./install
openshift-install create manifests --dir=install --log-level=debug

vi ./install/manifests/cluster-dns-02-config.yml  # remove reference to aws

nohup openshift-install create cluster --dir=install --log-level=debug > install.nohup 2>&1 &

less ./install.nohup

# wait for api load balancer to be created and add to /etc/hosts
sudo vi /etc/hosts
# some_ip_to_int_elb api.hello.jkeam.com
# some_ip_to_int_elb api-int.hello.jkeam.com
sudo systemctl restart dnsmasq.service

# wait for *.apps load balancer to be created
# and update line 87 and 88 in dnsmasq.conf
sudo systemctl restart dnsmasq.service

# then add the AWS secrets, replace with real values
oc apply -k ./secrets
```

### Destruction

```shell
openshift-install destroy cluster --dir=install --log-level=debug
rm -rf ./install
```

## Docs

### DNS Server

1. [Tips](https://www.linux.com/topic/networking/advanced-dnsmasq-tips-and-tricks/)
2. [Arch Docs](https://wiki.archlinux.org/title/Dnsmasq#DNS_server)
3. [AWS Custom DNS](https://repost.aws/knowledge-center/dns-resolution-failures-ec2-linux)
4. [Amazon DNS](https://docs.aws.amazon.com/vpc/latest/userguide/AmazonDNS-concepts.html#vpc-private-hosted-zones)

### Route53

1. [AWS Endpoints](https://docs.aws.amazon.com/general/latest/gr/r53.html)
2. [AWS Service Endpoints](https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints)
3. [AWS CLI Reference](https://docs.aws.amazon.com/cli/latest/reference/route53/)

### OpenShift

#### AWS

1. [AWS IPI](https://docs.openshift.com/container-platform/4.16/installing/installing_aws/ipi/ipi-aws-preparing-to-install.html)
2. [AWS UPI in Restricted Network](https://docs.openshift.com/container-platform/4.16/installing/installing_aws/upi/installing-restricted-networks-aws.html)

#### AWS

1. [Feature for customer managed DNS in AWS](https://issues.redhat.com/browse/OCPSTRAT-992)
2. [Epic for customer managed DNS](https://issues.redhat.com/browse/CORS-1874)

## Note

You will see keys in the `secrets` dir.  If you base64 decode them you will see they are just junk.

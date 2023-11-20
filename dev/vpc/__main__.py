import pulumi
import pulumi_aws as aws  

# Configurar la región de AWS
aws.config.region = 'eu-west-1'

# Crear una VPC
vpc = aws.ec2.Vpc('my-vpc',
                  cidr_block='10.0.0.0/16',
                  enable_dns_support=True,
                  enable_dns_hostnames=True,
                  tags={'Name': 'my-vpc'})

# Crear subredes públicas
public_subnets = []
for i in range(1, 4):
    subnet = aws.ec2.Subnet(f'public-subnet-{i}',
                            vpc_id=vpc.id,
                            cidr_block=f'10.0.{i}.0/24',
                            map_public_ip_on_launch=True,
                            availability_zone=f'eu-west-1a',
                            tags={'Name': f'public-subnet-{i}'})
    public_subnets.append(subnet)

# Crear subredes privadas
private_subnets = []
for i in range(4, 7):
    subnet = aws.ec2.Subnet(f'private-subnet-{i}',
                            vpc_id=vpc.id,
                            cidr_block=f'10.0.{i}.0/24',
                            availability_zone=f'eu-west-1a',
                            tags={'Name': f'private-subnet-{i}'})
    private_subnets.append(subnet)

# Exportar los IDs de las subredes
pulumi.export('public_subnet_ids', [subnet.id for subnet in public_subnets])
pulumi.export('private_subnet_ids', [subnet.id for subnet in private_subnets])

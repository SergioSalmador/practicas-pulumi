import pulumi
from pulumi import StackReference
import pulumi_aws as aws

# Usa StackReference para referenciar tu stack VPC
vpc_stack = StackReference("SergioSalmador/vpc/dev")

# Obtener los IDs de las subredes privadas exportadas del stack VPC
private_subnet_ids = vpc_stack.get_output("private_subnet_ids")

desired_subnet_id = private_subnet_ids.apply(
    lambda ids: next((id for id in ids if id == "subnet-01a1cc4cf1959370d"), None)
)

# Obtener el AMI más reciente
ami_result = aws.ec2.get_ami(most_recent=True,
                             owners=["137112412989"],
                             filters=[{"name":"name","values":["amzn-ami-hvm-*"]}])

# Asegúrate de acceder al ID del AMI a través de la propiedad 'id' del resultado
ami_id = ami_result.id

ec2_instance = desired_subnet_id.apply(lambda subnet_id: 
    aws.ec2.Instance("mi-ec2-instance",
                     instance_type="t2.micro",
                     ami=ami_id,
                     subnet_id=subnet_id
                     # Añade aquí otros parámetros necesarios
                    )
)

# Exportar el ID de la instancia EC2
pulumi.export('ec2_instance_id', ec2_instance.id)

from aws_cdk import Stack, CfnOutput
import aws_cdk.aws_ec2 as ec2
from constructs import Construct
    

from constructs import Construct

class newVpcStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)




        subnet1 = ec2.SubnetConfiguration(
                subnet_type=ec2.SubnetType.PUBLIC,
                name="eksPublic",
                cidr_mask=24)

        subnet2 = ec2.SubnetConfiguration(
                subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT,
                name="eksPrivate",
                cidr_mask=24)

        self.vpc = ec2.Vpc(self, "eksTestVPC",
            max_azs=3,
            cidr="10.0.0.0/16",
            subnet_configuration=[subnet1, subnet2],
            nat_gateways=3
            )
        CfnOutput(self, "Output",
                        value=self.vpc.vpc_id,)


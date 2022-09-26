from aws_cdk import Stack
from constructs import Construct
import aws_cdk.aws_eks as eks
from eks_test_project.newVpcStack import *


class eksCluster(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        cluster = eks.Cluster(self, "testingEksCDK",
                        vpc=vpc,
                        vpc_subnets=[ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT), ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC)],
                        version=eks.KubernetesVersion.V1_21,
                        default_capacity=3,
                        default_capacity_instance=ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.LARGE),
                        endpoint_access=eks.EndpointAccess.PRIVATE,
                        alb_controller=eks.AlbControllerOptions(
                            version=eks.AlbControllerVersion.V2_4_1
                            ),
                        ),

        

        app_label = {"app": "nginx"},
        deployment = {
            "api_version": "apps/v1",
            "kind": "Deployment",
            "metadata": {"name": "nginxDeploy"},
            "spec": {
                "replicas": 3,
                "selector": {"match_labels": app_label},
                "template": {
                    "metadata": {"labels": app_label},
                    "spec": {
                        "containers": [{
                            "name": "nginx",
                            "image": "nginx",
                            "ports": [{"container_port": 80}]
                        }                        ]          
                    }
                }
            }
        },

        albService = {
            "api_version": "v1",
            "kind": "Service",
            "metadata": {"name": "nginxService"},
            "spec": {
                "ports": [{
                   "port": 80,
                   "targetPort": 80,
                   "protocol": "tcp"
                }]
            }
        },

        ingressService = {
            "api_version": "networking.k8s.io/v1",
            "kind": "Ingress",
            "metadata": {"name": "nginxIngress"},
            "annotations": {"alb.ingress.kubernetes.io/scheme": "internet-facing",
            "alb.ingress.kubernetes.io/target-type": "ip"},
            "spec": {
                "ingressClassName": "alb",
                "rules":[{
                    "http": [{
                        "paths":[{
                            "path": "/",
                            "pathType": "Prefix",
                            "backend": [{
                                "service": {
                                    "name": "nginxService",
                                    "port":{
                                        "number": 80
                                    }
                                }
                            }]
                        }]
                    }]
                }]
            }
        },

        # ingressSevice.node.add_dependency(albService)
        # albService.node.add_dependeny(deployment)
        
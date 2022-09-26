#!/usr/bin/env python3
import os
import aws_cdk as cdk
from eks_test_project.newVpcStack import newVpcStack
from eks_test_project.eksCluster import eksCluster

env=cdk.Environment(account='285906620291', region='us-east-1'),

app = cdk.App()
vpcStack = newVpcStack(app, "cdkVpc")
eksStack = eksCluster(app, "cdkEks", vpc=vpcStack.vpc)

app.synth()

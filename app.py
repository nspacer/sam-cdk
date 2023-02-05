#!/usr/bin/env python3

import aws_cdk as cdk

from sam_cdk.sam_cdk_stack import SamCdkStack


app = cdk.App()
SamCdkStack(app, "sam-cdk")

app.synth()

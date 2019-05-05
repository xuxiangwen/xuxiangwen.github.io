### 5. 安装aws cli

<https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html>

~~~shell
pip3 install awscli --upgrade --user
~~~

[windows下安装](https://docs.aws.amazon.com/cli/latest/userguide/install-windows.html)

### 4. cli dms命令

#### 查询dms event subscription

~~~shell
aws dms describe-event-subscriptions --subscription-name dms-replication-instance
~~~

### 3. cli iam命令

#### 得到role信息

~~~shell
aws iam get-role --role-name dms-access-for-endpoint
aws iam get-role --role-name CSS_WeChat_PROD_Analysis
~~~

#### 得到role policy信息

只能得到在role中直接定义的policy信息，不能查询policies中的policy

```shell
aws iam get-role-policy --role-name CSS_WeChat_PROD_Analysis --policy-name sns    
```



#### 得到policy信息

~~~shell
aws iam get-policy --policy-arn arn:aws-cn:iam::aws:policy/AmazonSNSFullAccess
aws iam get-policy-version --policy-arn arn:aws-cn:iam::aws:policy/AmazonSNSFullAccess --version-id v1

# hpit
aws iam get-policy --policy-arn arn:aws-cn:iam::166752391405:policy/dms_fullaccess
aws iam get-policy-version --policy-arn arn:aws-cn:iam::166752391405:policy/dms_fullaccess --version-id v1
~~~

#### 创建一个policy

下面是创建用户对dms的必要权限，参见[IAM Permissions Needed to Use AWS DMS](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Security.IAMPermissions.html)。

~~~shell
cat << EOF > policy
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "dms:*",
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "kms:ListAliases", 
                "kms:DescribeKey"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "iam:GetRole",
                "iam:PassRole",
                "iam:CreateRole",
                "iam:AttachRolePolicy"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeVpcs",
                "ec2:DescribeInternetGateways",
                "ec2:DescribeAvailabilityZones",
                "ec2:DescribeSubnets",
                "ec2:DescribeSecurityGroups",
                "ec2:ModifyNetworkInterfaceAttribute",
                "ec2:CreateNetworkInterface",
                "ec2:DeleteNetworkInterface"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "cloudwatch:Get*",
                "cloudwatch:List*"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:DescribeLogGroups",
                "logs:DescribeLogStreams",
                "logs:FilterLogEvents",
                "logs:GetLogEvents"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "redshift:Describe*",
                "redshift:ModifyClusterIamRoles"
            ],
            "Resource": "*"
        }
    ]
} 
EOF

aws iam create-policy --policy-name mike-dms --policy-document file://policy
rm policy
~~~



#### [Namespace of AWS Service](https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html#genref-aws-service-namespaces)

| Service                                         | Namespace         |
| ----------------------------------------------- | ----------------- |
| API Gateway                                     | apigateway        |
| Amazon CloudWatch                               | cloudwatch        |
| Amazon CloudWatch Events                        | events            |
| Amazon CloudWatch Logs                          | logs              |
| AWS Database Migration Service (AWS DMS)        | dms               |
| Amazon DynamoDB                                 | dynamodb          |
| Amazon DynamoDB Accelerator (DAX)               | dax               |
| Amazon Elastic Compute Cloud (Amazon EC2)       | ec2               |
| Amazon Elastic Container Registry (Amazon ECR)  | ecr               |
| Amazon Elastic Container Service (Amazon ECS)   | ecs               |
| AWS Elastic Beanstalk                           | elasticbeanstalk  |
| Amazon EMR                                      | elasticmapreduce  |
| Amazon Elastic Transcoder                       | elastictranscoder |
| Amazon Elasticsearch Service (Amazon ES)        | es                |
| AWS Lambda                                      | lambda            |
| Amazon Redshift                                 | redshift          |
| Amazon Simple Email Service (Amazon SES)        | ses               |
| Amazon Simple Notification Service (Amazon SNS) | sns               |
| Amazon Simple Queue Service (Amazon SQS)        | sqs               |
| Amazon Simple Storage Service (Amazon S3)       | s3                |



### 2. AWS cli ec2命令

#### 得到所有可用区域

```shell
aws ec2 describe-regions
```

#### 描述security group

```shell
aws ec2 describe-security-groups --region cn-northwest-1  --vpc-name --group-names mike-tcph-test
```

#### 创建security group

```shell
aws ec2 create-security-group --region cn-north-1 --group-name mike-tcph-test --description "michael security group"
aws ec2 authorize-security-group-ingress --region cn-north-1 --group-name mike-tcph-test --ip-protocol tcp --from-port 22 --to-port 22 --cidr-ip 15.0.0.0/8
aws ec2 authorize-security-group-ingress --region cn-north-1 --group-name mike-tcph-test --ip-protocol tcp --from-port 3306 --to-port 3306 --cidr-ip 15.0.0.0/8
aws ec2 authorize-security-group-ingress --region cn-north-1 --group-name mike-tcph-test --ip-protocol tcp --from-port 5432 --to-port 5432 --cidr-ip 15.0.0.0/8
aws ec2 authorize-security-group-ingress --region cn-north-1 --group-name mike-tcph-test --ip-protocol tcp --from-port 5439 --to-port 5439 --cidr-ip 15.0.0.0/8
aws ec2 authorize-security-group-ingress --region cn-north-1 --group-name mike-tcph-test --ip-protocol tcp --from-port 3306 --to-port 3306 --cidr-ip 172.31.0.0/16
aws ec2 authorize-security-group-ingress --region cn-north-1 --group-name mike-tcph-test --ip-protocol tcp --from-port 5432 --to-port 5432 --cidr-ip 172.31.0.0/16
aws ec2 authorize-security-group-ingress --region cn-north-1 --group-name mike-tcph-test --ip-protocol tcp --from-port 5439 --to-port 5439 --cidr-ip 172.31.0.0/16
aws ec2 authorize-security-group-ingress --region cn-north-1 --group-name mike-tcph-test --ip-protocol tcp --from-port 3306 --to-port 3306 --cidr-ip 52.82.0.0/16
aws ec2 authorize-security-group-ingress --region cn-north-1 --group-name mike-tcph-test --ip-protocol tcp --from-port 3306 --to-port 3306 --cidr-ip 52.83.0.0/16

aws ec2 describe-security-groups --region cn-north-1   --group-names mike-tcph-test
```



### 1. Proxy

~~~shell
export HTTPS_PROXY=http://web-proxy.rose.hp.com:8080
~~~


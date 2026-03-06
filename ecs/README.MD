# ECS Deployment

This folder contains the configuration needed to deploy the **simple-python-api** container to AWS ECS using the AWS CLI.

## Files in this directory

`taskdef.json.template`
Template for the ECS task definition. It defines how the container runs, including the container image, CPU/memory allocation, exposed port, and logging configuration.

`service.json.template`
Template for the ECS service. It defines how ECS schedules and runs the container tasks, including networking and how many instances should run.

`.env.example`
Example environment configuration. Copy this file to `.env` and update the values for your AWS account and network.

`.env`
Your local configuration file containing account-specific values. This file should **not be committed**.

---

# Setup

### 1. Copy the environment template

```bash
cp .env.example .env
```

### 2. Edit `.env`

Fill in values for your AWS account and network resources.

Example:

```bash
ACCOUNT_ID=123456789012
REGION=us-east-2
IMAGE_TAG=latest

CLUSTER_NAME=my-ecs-cluster
SERVICE_NAME=simple-python-api

SUBNET1=subnet-xxxxxxxx
SUBNET2=subnet-yyyyyyyy

SECURITY_GROUP=sg-xxxxxxxx
```

These values correspond to:

| Variable          | Description                            |
| ----------------- | -------------------------------------- |
| ACCOUNT_ID        | AWS account ID                         |
| REGION            | AWS region                             |
| IMAGE_TAG         | Container tag pushed to ECR            |
| CLUSTER_NAME      | ECS cluster name                       |
| SERVICE_NAME      | ECS service name                       |
| SUBNET1 / SUBNET2 | Subnets where tasks will run           |
| SECURITY_GROUP    | Security group allowing inbound access |

---

# Load environment variables

```bash
set -a
source .env
set +a
```

This exports the variables so tools like `envsubst` can substitute them into templates.

---

# Render ECS configuration files

Generate the final ECS configuration files from the templates:

```bash
envsubst < taskdef.json.template > taskdef.json
envsubst < service.json.template > service.json
```

---

# Register the ECS task definition

```bash
aws ecs register-task-definition \
  --cli-input-json file://taskdef.json \
  --region $REGION
```

This creates a new **task definition revision** ECS can run.

---

# Create the ECS service

```bash
aws ecs create-service \
  --cli-input-json file://service.json \
  --region $REGION
```

The service launches the container tasks in your cluster.

---

# Verify the service

```bash
aws ecs describe-services \
  --cluster $CLUSTER_NAME \
  --services $SERVICE_NAME \
  --region $REGION
```

If the service started correctly you should see:

```
runningCount: 1
```

The container will now be running inside ECS using the task definition you registered earlier.


# Notes

The container image must already exist in ECR:

```
<ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/simple-python-api:<IMAGE_TAG>
```

Your security group must allow inbound traffic on:

```
TCP 8080
```

If `assignPublicIp` is enabled in the service configuration, the task will be reachable via its public IP.

---

# Typical workflow

1. Build and push the Docker image to ECR
2. Update `IMAGE_TAG` if needed
3. Render the ECS templates
4. Register a new task definition
5. Create or update the ECS service


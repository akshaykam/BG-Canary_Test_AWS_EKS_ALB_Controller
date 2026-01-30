# Blue-Green Deployment Setup

This directory contains the configuration files necessary for setting up a blue-green deployment for the Python application on an Amazon EKS cluster. 

## Overview

Blue-green deployment is a strategy that reduces downtime and risk by running two identical production environments called "blue" and "green." At any time, only one of the environments is live, serving all the production traffic. The other environment is idle and can be used for staging new releases.

## Directory Structure

- **deployments/**: Contains the deployment configurations for both blue and green versions of the application.
  - `deployment-blue.yaml`: Deployment configuration for the blue version.
  - `deployment-green.yaml`: Deployment configuration for the green version.

- **services/**: Contains the service configurations for both blue and green versions.
  - `service-blue.yaml`: Service configuration for the blue version.
  - `service-green.yaml`: Service configuration for the green version.

- **ingress/**: Contains the ingress configurations for routing traffic.
  - `ingress-alb.yaml`: ALB ingress configuration for routing traffic to the appropriate service.
  - `weights-config.yaml`: Configuration for traffic weights between blue and green services.

- **config/**: Contains configuration files for the application.
  - `configmap.yaml`: ConfigMap for non-sensitive configuration data.
  - `secret.yaml`: Secret for sensitive information.

- **hpa/**: Contains the Horizontal Pod Autoscaler configuration.
  - `hpa.yaml`: HPA configuration for scaling the application based on metrics.

- **network/**: Contains network-related configurations.
  - `namespace.yaml`: Namespace configuration for isolating the deployment resources.

## Deployment Instructions

1. **Create the Namespace**: Apply the `namespace.yaml` file to create a dedicated namespace for the blue-green deployment.
   ```
   kubectl apply -f k8s/blue-green/network/namespace.yaml
   ```

2. **Deploy the Blue Version**: Apply the blue deployment and service configurations.
   ```
   kubectl apply -f k8s/blue-green/deployments/deployment-blue.yaml
   kubectl apply -f k8s/blue-green/services/service-blue.yaml
   ```

3. **Deploy the Green Version**: Apply the green deployment and service configurations.
   ```
   kubectl apply -f k8s/blue-green/deployments/deployment-green.yaml
   kubectl apply -f k8s/blue-green/services/service-green.yaml
   ```

4. **Configure Ingress (ALB Controller)**: Apply the ingress configuration which uses an ALB "forward" action with weighted target groups for blue/green. Edit weights in the `alb.ingress.kubernetes.io/actions.forward-to-canary` annotation inside `ingress-alb.yaml`.
  ```
  kubectl apply -f k8s/blue-green/ingress/ingress-alb.yaml
  ```

5. **Adjust Traffic Weights**: Modify the `weight` values in the `forward-to-canary` annotation in `ingress-alb.yaml` (e.g., 80/20 to start canary). Re-apply the ingress to update routing.
  ```
  # Edit weights in ingress-alb.yaml then
  kubectl apply -f k8s/blue-green/ingress/ingress-alb.yaml
  ```

6. **Monitor and Scale**: Use the HPA configuration to automatically scale the application based on demand.
   ```
   kubectl apply -f k8s/blue-green/hpa/hpa.yaml
   ```

## Notes

- Ensure your EKS cluster has the AWS Load Balancer Controller installed and the required IAM roles (see repository `iam_policy.json` and `trust-policy.json`).
- Use `service-blue` and `service-green` in the `blue-green-deployment` namespace; ALB routes traffic via the forward action.
- Build and push the Docker image to ECR before deploying, and update the `image` fields in the deployments.

## Build and Push to ECR

1. Authenticate to ECR and create a repository (replace placeholders):
  ```bash
  aws ecr create-repository --repository-name my-python-app
  aws ecr get-login-password --region <AWS_REGION> | docker login --username AWS --password-stdin <ACCOUNT_ID>.dkr.ecr.<AWS_REGION>.amazonaws.com
  ```
2. Build and push blue/green tags from repo root:
  ```bash
  docker build -t my-python-app:blue .
  docker tag my-python-app:blue <ACCOUNT_ID>.dkr.ecr.<AWS_REGION>.amazonaws.com/my-python-app:blue
  docker push <ACCOUNT_ID>.dkr.ecr.<AWS_REGION>.amazonaws.com/my-python-app:blue

  docker build -t my-python-app:green .
  docker tag my-python-app:green <ACCOUNT_ID>.dkr.ecr.<AWS_REGION>.amazonaws.com/my-python-app:green
  docker push <ACCOUNT_ID>.dkr.ecr.<AWS_REGION>.amazonaws.com/my-python-app:green
  ```

3. Update `deployment-blue.yaml` and `deployment-green.yaml` `image` fields with the ECR URIs.
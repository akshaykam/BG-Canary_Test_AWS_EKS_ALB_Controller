# BG-Canary_Test_AWS_EKS_ALB_Controller

This repository contains a blue-green deployment setup for a Python application on AWS EKS using the Application Load Balancer (ALB) controller. The blue-green deployment strategy allows for seamless updates and rollbacks by maintaining two separate environments (blue and green) for the application.

## Project Structure

```
BG-Canary_Test_AWS_EKS_ALB_Controller
├── k8s
│   ├── blue-green
│   │   ├── deployments
│   │   │   ├── deployment-blue.yaml
│   │   │   └── deployment-green.yaml
│   │   ├── services
│   │   │   ├── service-blue.yaml
│   │   │   └── service-green.yaml
│   │   ├── ingress
│   │   │   ├── ingress-alb.yaml
│   │   │   └── weights-config.yaml
│   │   ├── config
│   │   │   ├── configmap.yaml
│   │   │   └── secret.yaml
│   │   ├── hpa
│   │   │   └── hpa.yaml
│   │   ├── network
│   │   │   └── namespace.yaml
│   │   └── README.md
└── README.md
```

## Setup Instructions

1. **Prerequisites**: Ensure you have the following installed:
   - AWS CLI
   - kubectl
   - eksctl
   - Helm (if needed for additional configurations)

2. **Create EKS Cluster**: Use `eksctl` to create an EKS cluster if you haven't already.

3. **Deploy the Application**:
   - Navigate to the `k8s/blue-green` directory.
   - Apply the namespace configuration:
     ```
     kubectl apply -f network/namespace.yaml
     ```
   - Deploy the blue version of the application:
     ```
     kubectl apply -f deployments/deployment-blue.yaml
     ```
   - Deploy the green version of the application:
     ```
     kubectl apply -f deployments/deployment-green.yaml
     ```
   - Create services for both blue and green deployments:
     ```
     kubectl apply -f services/service-blue.yaml
     kubectl apply -f services/service-green.yaml
     ```
   - Configure the ingress resource:
     ```
     kubectl apply -f ingress/ingress-alb.yaml
     ```
   - Set up traffic weights as needed:
     ```
     kubectl apply -f ingress/weights-config.yaml
     ```

4. **Scaling**: Use the Horizontal Pod Autoscaler to manage scaling:
   ```
   kubectl apply -f hpa/hpa.yaml
   ```

5. **Configuration**: Update the `configmap.yaml` and `secret.yaml` files as necessary to manage application configuration and sensitive data.

6. **Monitoring and Management**: Monitor the deployments and services using `kubectl get pods`, `kubectl get services`, and `kubectl get ingress`.

## Additional Information

Refer to the `k8s/blue-green/README.md` for more detailed instructions specific to the blue-green deployment setup.
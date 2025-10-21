# DefTech AI - AWS SageMaker Deployment Architecture

## Executive Summary

This document outlines the production deployment architecture for the DefTech AI Document Assistant on AWS SageMaker, providing a secure, scalable, and compliant solution for defense applications.

## 🎯 Deployment Overview

### Current Demo vs Production

| Aspect | Current Demo | Production (SageMaker) |
|--------|-------------|----------------------|
| **LLM Access** | Cohere Cloud API | SageMaker Endpoint in VPC |
| **Data Location** | Transits to Cohere | Stays in AWS VPC |
| **Network** | Public Internet | Private VPC |
| **Compliance** | Development only | FedRAMP, DoD compliant |
| **Cost Model** | Pay-per-API-call | Reserved capacity |
| **Latency** | ~2-5 seconds | ~500ms-1s |
| **Control** | Limited | Full control |

## 🏗️ Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                    AWS GovCloud / Commercial                         │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │                    VPC (10.0.0.0/16)                           │ │
│  │                                                                 │ │
│  │  ┌─────────────────┐                 ┌─────────────────┐      │ │
│  │  │  Public Subnet  │                 │  Private Subnet │      │ │
│  │  │  10.0.1.0/24    │                 │  10.0.10.0/24   │      │ │
│  │  │                 │                 │                 │      │ │
│  │  │  ┌───────────┐  │                 │  ┌───────────┐  │      │ │
│  │  │  │Application│  │                 │  │ SageMaker │  │      │ │
│  │  │  │Load       │  │    HTTPS        │  │ Endpoint  │  │      │ │
│  │  │  │Balancer   │──┼────────────────▶│  │           │  │      │ │
│  │  │  └───────────┘  │                 │  │Command-R+ │  │      │ │
│  │  │                 │                 │  │ Embed v3  │  │      │ │
│  │  └─────────────────┘                 │  └───────────┘  │      │ │
│  │                                      │                 │      │ │
│  │  ┌─────────────────┐                 │  ┌───────────┐  │      │ │
│  │  │  Public Subnet  │                 │  │  Qdrant   │  │      │ │
│  │  │  10.0.2.0/24    │                 │  │  Vector   │  │      │ │
│  │  │                 │                 │  │    DB     │  │      │ │
│  │  │  ┌───────────┐  │                 │  └───────────┘  │      │ │
│  │  │  │  Streamlit│  │                 │                 │      │ │
│  │  │  │    App    │  │                 │  ┌───────────┐  │      │ │
│  │  │  │  (ECS)    │  │                 │  │   RDS     │  │      │ │
│  │  │  └───────────┘  │                 │  │PostgreSQL │  │      │ │
│  │  │                 │                 │  │(Audit Log)│  │      │ │
│  │  └─────────────────┘                 │  └───────────┘  │      │ │
│  │                                      │                 │      │ │
│  │  ┌─────────────────┐                 │  ┌───────────┐  │      │ │
│  │  │  NAT Gateway    │                 │  │    S3     │  │      │ │
│  │  │                 │                 │  │ Documents │  │      │ │
│  │  └─────────────────┘                 │  │(Encrypted)│  │      │ │
│  │                                      │  └───────────┘  │      │ │
│  └──────────────────────────────────────────────────────────────── │ │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │                    Security & Compliance                        │ │
│  │  • AWS WAF  • Security Groups  • NACLs  • VPC Flow Logs       │ │
│  │  • CloudTrail  • GuardDuty  • KMS Encryption  • IAM Roles     │ │
│  └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘

External Users ──▶ CloudFront CDN ──▶ ALB ──▶ ECS (Streamlit) ──▶ Private Subnet
                                                    │
                                                    ├──▶ SageMaker (ML)
                                                    ├──▶ Qdrant (Vector DB)
                                                    ├──▶ RDS (Audit Logs)
                                                    └──▶ S3 (Documents)
```

## 📋 Component Details

### 1. **SageMaker ML Endpoints**

#### Command-R+ Inference Endpoint
```
Instance Type: ml.g5.12xlarge (4x NVIDIA A10G GPUs)
Model: Cohere Command-R+ (via Cohere AWS Partnership)
Deployment: Multi-AZ for high availability
Auto-scaling: 2-10 instances based on load
Endpoint: Private VPC endpoint (no internet access)
Encryption: TLS 1.3 in transit, KMS at rest
```

#### Embed v3 Inference Endpoint
```
Instance Type: ml.g5.2xlarge (1x NVIDIA A10G GPU)
Model: Cohere Embed v3
Deployment: Multi-AZ
Auto-scaling: 2-6 instances
Batch size: 96 documents
Endpoint: Private VPC endpoint
```

### 2. **Vector Database (Qdrant)**

```
Deployment: EC2 with EBS volumes
Instance Type: r6i.2xlarge (64GB RAM)
Storage: 500GB gp3 EBS (encrypted)
Replication: Multi-AZ with read replicas
Backup: Daily snapshots to S3
Network: Private subnet only
Access: VPC endpoint, no public IP
```

### 3. **Application Layer (ECS Fargate)**

```
Service: Streamlit Web UI
Container: Custom Docker image
CPU: 4 vCPU
Memory: 8GB
Networking: Private subnet with NAT gateway
Load Balancer: Application Load Balancer (ALB)
SSL/TLS: AWS Certificate Manager
Auto-scaling: 2-20 tasks based on CPU/memory
```

### 4. **Audit & Compliance**

```
Audit Logs: RDS PostgreSQL (Multi-AZ)
Instance: db.r6i.large
Storage: 100GB encrypted (gp3)
Retention: 7 years
Backup: Automated daily + point-in-time recovery
Compliance: FIPS 140-2 encryption
```

### 5. **Document Storage**

```
Service: S3 (Standard-IA for infrequent access)
Encryption: KMS with customer-managed keys
Versioning: Enabled
Replication: Cross-region for DR
Lifecycle: Glacier after 90 days
Access: VPC endpoint only, no public access
```

## 🔒 Security Architecture

### Network Security

```
┌──────────────────────────────────────┐
│         Internet Gateway             │
└──────────────┬───────────────────────┘
               │
        ┌──────▼──────┐
        │   AWS WAF   │  ◀── DDoS protection, SQL injection filtering
        └──────┬──────┘
               │
        ┌──────▼──────────┐
        │   CloudFront    │  ◀── CDN, DDoS protection
        └──────┬──────────┘
               │
        ┌──────▼──────────┐
        │ Application LB  │  ◀── SSL termination, health checks
        └──────┬──────────┘
               │
        ┌──────▼──────────┐
        │  Public Subnet  │  ◀── NACLs, Security Groups
        │   (ECS Tasks)   │
        └──────┬──────────┘
               │
        ┌──────▼──────────┐
        │ Private Subnet  │  ◀── No internet access
        │  (ML, DB, S3)   │  ◀── VPC endpoints only
        └─────────────────┘
```

### Security Controls

| Layer | Control | Implementation |
|-------|---------|----------------|
| **Network** | VPC Isolation | Private subnets for all ML/data |
| **Network** | Security Groups | Least-privilege access rules |
| **Network** | NACLs | Subnet-level filtering |
| **Network** | VPC Flow Logs | All traffic logged to S3 |
| **Application** | WAF | OWASP Top 10 protection |
| **Application** | Authentication | AWS Cognito / SAML integration |
| **Application** | Authorization | IAM roles with MFA |
| **Data** | Encryption at Rest | KMS with customer-managed keys |
| **Data** | Encryption in Transit | TLS 1.3 minimum |
| **Audit** | CloudTrail | All API calls logged |
| **Audit** | GuardDuty | Threat detection |
| **Audit** | Config | Compliance monitoring |

## 💰 Cost Estimation

### Monthly Costs (Steady State)

| Component | Specification | Monthly Cost |
|-----------|--------------|--------------|
| **SageMaker - Command-R+** | ml.g5.12xlarge × 2 | $8,640 |
| **SageMaker - Embed v3** | ml.g5.2xlarge × 2 | $1,440 |
| **ECS Fargate** | 4 vCPU, 8GB × 4 tasks | $350 |
| **RDS PostgreSQL** | db.r6i.large Multi-AZ | $580 |
| **Qdrant (EC2)** | r6i.2xlarge × 2 | $630 |
| **S3 Storage** | 500GB documents | $12 |
| **Data Transfer** | 1TB/month | $90 |
| **Load Balancer** | ALB | $23 |
| **CloudFront** | 1TB data transfer | $85 |
| **KMS** | 10 keys | $10 |
| **CloudWatch** | Logs & metrics | $150 |
| **Backups** | EBS & RDS snapshots | $100 |
| **NAT Gateway** | 2 AZs | $90 |
| **VPC Endpoints** | 5 endpoints | $75 |
| | **Total** | **~$12,275/month** |

### Cost Optimization Options

1. **Reserved Instances** - Save 30-50% on SageMaker
2. **Spot Instances** - Use for non-critical workloads
3. **Auto-scaling** - Scale down during off-hours
4. **S3 Lifecycle** - Move to Glacier after 90 days
5. **Right-sizing** - Monitor and adjust instance types

**Optimized Cost:** ~$7,500-8,500/month

## 🚀 Deployment Process

### Phase 1: Infrastructure Setup (Week 1)

```bash
# 1. VPC & Network
terraform apply -target=module.vpc

# 2. Security Groups & IAM
terraform apply -target=module.security

# 3. S3, RDS, Qdrant
terraform apply -target=module.data_stores
```

### Phase 2: ML Model Deployment (Week 2)

```python
# 1. Deploy Cohere models to SageMaker
import sagemaker

# Command-R+ deployment
command_r_endpoint = sagemaker.deploy_model(
    model_name="cohere-command-r-plus",
    instance_type="ml.g5.12xlarge",
    instance_count=2,
    vpc_config={
        'SecurityGroupIds': [...],
        'Subnets': [...]
    }
)

# Embed v3 deployment
embed_endpoint = sagemaker.deploy_model(
    model_name="cohere-embed-v3",
    instance_type="ml.g5.2xlarge",
    instance_count=2,
    vpc_config={...}
)
```

### Phase 3: Application Deployment (Week 3)

```bash
# 1. Build and push Docker image
docker build -t deftech-app .
aws ecr push deftech-app:latest

# 2. Deploy ECS service
aws ecs update-service --service deftech-app --force-new-deployment

# 3. Configure load balancer
aws elbv2 create-target-group ...
```

### Phase 4: Testing & Validation (Week 4)

- Security testing (penetration testing)
- Load testing (1000 concurrent users)
- Failover testing (multi-AZ)
- Compliance validation (FedRAMP)

## 📊 Performance Metrics

### Expected Performance (Production)

| Metric | Target | Current Demo |
|--------|--------|--------------|
| **Query Latency (p50)** | 800ms | 2-5s |
| **Query Latency (p99)** | 2s | 8-10s |
| **Throughput** | 500 QPS | 10 QPS |
| **Availability** | 99.95% | 99% |
| **Data Residency** | AWS VPC | Cohere Cloud |
| **Cold Start** | None (warm pool) | N/A |

### Scaling Limits

- **Max Concurrent Queries:** 5,000
- **Max Documents:** 10 million
- **Max Users:** 10,000 concurrent
- **Geographic Regions:** Multi-region capable

## 🔐 Compliance & Certifications

### Supported Compliance Frameworks

| Framework | Status | Notes |
|-----------|--------|-------|
| **FedRAMP Moderate** | ✅ Achievable | Using GovCloud |
| **FedRAMP High** | ✅ Achievable | Additional controls |
| **NIST 800-53** | ✅ Supported | AWS built-in |
| **ITAR** | ✅ Supported | GovCloud + controls |
| **DoD IL4** | ✅ Achievable | Standard config |
| **DoD IL5** | ⚠️ Requires work | Additional isolation |
| **CMMC Level 2** | ✅ Supported | AWS + app controls |

### Key Security Features for Defense

1. **Data Sovereignty**
   - All data stays in US AWS regions
   - No data transits to third parties
   - Cohere models deployed in your VPC

2. **Access Control**
   - CAC/PIV card integration (SAML/OIDC)
   - Multi-factor authentication required
   - Role-based access control (RBAC)

3. **Audit & Monitoring**
   - Complete audit trail (7-year retention)
   - Real-time security monitoring
   - Compliance dashboards

4. **Encryption**
   - FIPS 140-2 validated encryption
   - Customer-managed KMS keys
   - Perfect forward secrecy (TLS 1.3)

## 🔄 Disaster Recovery

### Backup Strategy

```
┌─────────────────────────────────────────┐
│         Primary Region (us-east-1)      │
│                                         │
│  ┌──────────┐      ┌──────────┐        │
│  │SageMaker │      │  Qdrant  │        │
│  │Endpoints │      │   Data   │        │
│  └────┬─────┘      └────┬─────┘        │
│       │                 │              │
│       │  Continuous     │              │
│       │  Snapshots      │              │
│       ▼                 ▼              │
│  ┌──────────────────────────┐         │
│  │    S3 Cross-Region       │         │
│  │    Replication           │         │
│  └──────────┬───────────────┘         │
└─────────────┼───────────────────────────┘
              │
              │ Replicate
              ▼
┌─────────────────────────────────────────┐
│      DR Region (us-west-2)              │
│                                         │
│  ┌──────────┐      ┌──────────┐        │
│  │SageMaker │      │  Qdrant  │        │
│  │Endpoints │      │   Data   │        │
│  │(Standby) │      │(Replica) │        │
│  └──────────┘      └──────────┘        │
└─────────────────────────────────────────┘
```

### Recovery Objectives

- **RTO (Recovery Time Objective):** 1 hour
- **RPO (Recovery Point Objective):** 5 minutes
- **Data Loss:** < 5 minutes of transactions
- **Failover:** Automated DNS failover

## 📈 Migration Path

### From Demo to Production

```
Phase 1: Pilot (Months 1-2)
├── Deploy to AWS in single AZ
├── Migrate 10% of documents
├── 50 pilot users
└── Performance testing

Phase 2: Staging (Months 3-4)
├── Multi-AZ deployment
├── Full document migration
├── Security hardening
└── Compliance validation

Phase 3: Production (Months 5-6)
├── Multi-region deployment
├── All users migrated
├── DR testing
└── FedRAMP authorization

Phase 4: Optimization (Month 6+)
├── Cost optimization
├── Performance tuning
├── Feature enhancements
└── Continuous improvement
```

## 🎯 Next Steps

### For DefTech Stakeholders

1. **Technical Review** (Week 1)
   - Review architecture with IT team
   - Validate security requirements
   - Confirm compliance needs

2. **AWS Account Setup** (Week 2)
   - Establish AWS GovCloud account
   - Set up billing and cost tracking
   - Create IAM structure

3. **Proof of Concept** (Weeks 3-6)
   - Deploy in sandbox environment
   - Test with sample documents
   - Validate performance

4. **Pilot Deployment** (Months 2-4)
   - Deploy to staging
   - Onboard pilot users
   - Gather feedback

5. **Production Launch** (Months 5-6)
   - Full deployment
   - Training and documentation
   - Go-live

## 📞 Support & Contact

For deployment support:
- **AWS Solutions Architects:** [Your AWS TAM]
- **Cohere Enterprise:** enterprise@cohere.com
- **Security Questions:** [Your CISO]

---

**Document Version:** 1.0
**Last Updated:** 2025-10-20
**Classification:** UNCLASSIFIED
**Author:** DefTech AI Team

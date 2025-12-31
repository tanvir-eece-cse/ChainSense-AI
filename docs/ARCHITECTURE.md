# ChainSense AI - System Architecture

## Overview

ChainSense AI is a cloud-native, microservices-based supply chain intelligence platform that leverages machine learning for predictive analytics, anomaly detection, and route optimization.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              CLIENTS                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   Web App   │  │ Mobile App  │  │  API Client │  │   Webhook   │        │
│  │  (React)    │  │  (Future)   │  │   (SDKs)    │  │  Consumers  │        │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘        │
└─────────┼────────────────┼────────────────┼────────────────┼────────────────┘
          │                │                │                │
          └────────────────┴────────────────┴────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         INGRESS / LOAD BALANCER                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │              NGINX Ingress Controller (TLS Termination)              │   │
│  │                    Rate Limiting | WAF | DDoS Protection             │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
          ┌─────────────────────────┴─────────────────────────┐
          │                                                   │
          ▼                                                   ▼
┌─────────────────────────────┐           ┌─────────────────────────────────┐
│      FRONTEND SERVICE       │           │         BACKEND SERVICE          │
│  ┌───────────────────────┐  │           │  ┌───────────────────────────┐  │
│  │   React + TypeScript  │  │           │  │    FastAPI Application    │  │
│  │   - Vite Build        │  │           │  │   - REST API Endpoints    │  │
│  │   - Tailwind CSS      │  │           │  │   - JWT Authentication    │  │
│  │   - Recharts          │  │           │  │   - Rate Limiting         │  │
│  │   - React Query       │  │           │  │   - Request Validation    │  │
│  └───────────────────────┘  │           │  └───────────────────────────┘  │
│  Replicas: 2-5              │           │  Replicas: 2-10                  │
└─────────────────────────────┘           └───────────────┬─────────────────┘
                                                          │
                    ┌─────────────────────────────────────┼───────────────────┐
                    │                                     │                   │
                    ▼                                     ▼                   ▼
┌─────────────────────────────┐   ┌──────────────────────────────┐   ┌───────────────┐
│       ML SERVICE            │   │         POSTGRESQL           │   │     REDIS     │
│  ┌───────────────────────┐  │   │  ┌────────────────────────┐  │   │  ┌─────────┐  │
│  │  FastAPI + ML Models  │  │   │  │  Primary Database      │  │   │  │ Cache   │  │
│  │  - Demand Forecasting │  │   │  │  - Users & Auth        │  │   │  │ Session │  │
│  │  - Anomaly Detection  │  │   │  │  - Suppliers           │  │   │  │ Queue   │  │
│  │  - Route Optimization │  │   │  │  - Products            │  │   │  └─────────┘  │
│  │  - Risk Assessment    │  │   │  │  - Inventory           │  │   │  Replicas: 1  │
│  └───────────────────────┘  │   │  │  - Shipments           │  │   └───────────────┘
│  Replicas: 2-5              │   │  │  - Audit Logs          │  │
│  GPU Support (Optional)     │   │  └────────────────────────┘  │
└─────────────────────────────┘   │  Replicas: 1 (Primary)       │
                                  │  Backup: Daily               │
                                  └──────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                          MONITORING & OBSERVABILITY                         │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐             │
│  │   Prometheus    │  │    Grafana      │  │  Alert Manager  │             │
│  │   (Metrics)     │  │  (Dashboards)   │  │   (Alerting)    │             │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Component Details

### Frontend Service

**Technology Stack:**
- React 18 with TypeScript
- Vite for build tooling
- Tailwind CSS for styling
- Recharts for data visualization
- React Query for server state management
- Zustand for client state management

**Key Features:**
- Server-side rendering ready
- PWA support
- Dark mode
- Responsive design
- Real-time updates via WebSocket

### Backend Service

**Technology Stack:**
- Python 3.11+
- FastAPI for REST API
- SQLAlchemy 2.0 with async support
- Pydantic for validation
- JWT for authentication
- Prometheus client for metrics

**Key Features:**
- Async/await throughout
- Connection pooling
- Rate limiting
- Request logging
- Security headers middleware

### ML Service

**Technology Stack:**
- Python 3.11+
- FastAPI for API layer
- scikit-learn for classical ML
- PyTorch for deep learning
- Prophet for time series
- OR-Tools for optimization

**ML Models:**

1. **Demand Forecasting**
   - LSTM Neural Network
   - Random Forest Ensemble
   - Prophet Time Series

2. **Anomaly Detection**
   - Isolation Forest
   - Autoencoder (planned)

3. **Route Optimization**
   - Graph Neural Network
   - OR-Tools VRP Solver
   - Haversine distance calculation

4. **Risk Assessment**
   - Gradient Boosting Classifier
   - Multi-factor scoring

### Database Layer

**PostgreSQL:**
- Primary data store
- ACID compliant
- Full-text search
- JSON support for flexible data
- Audit logging

**Redis:**
- Session storage
- Rate limit counters
- Cache layer
- Message queue (future)

## Data Flow

### Request Flow

```
1. Client Request
       │
       ▼
2. Ingress (TLS, Rate Limit)
       │
       ▼
3. Backend API (Auth, Validation)
       │
       ├──────────────────┐
       ▼                  ▼
4. Database/Cache    5. ML Service
       │                  │
       └────────┬─────────┘
                ▼
6. Response Processing
       │
       ▼
7. Client Response
```

### ML Inference Flow

```
1. API Request
       │
       ▼
2. Backend validates and forwards
       │
       ▼
3. ML Service loads model
       │
       ▼
4. Feature extraction
       │
       ▼
5. Model inference
       │
       ▼
6. Post-processing
       │
       ▼
7. Response with predictions
```

## Security Architecture

### Authentication Flow

```
┌──────────┐     ┌──────────┐     ┌──────────┐
│  Client  │────▶│  Login   │────▶│  JWT     │
│          │     │ Endpoint │     │ Issued   │
└──────────┘     └──────────┘     └──────────┘
      │                                 │
      │         ┌──────────────────────┘
      │         ▼
      │    ┌──────────┐     ┌──────────┐
      └───▶│Protected │────▶│  JWT     │
           │ Endpoint │     │ Verified │
           └──────────┘     └──────────┘
```

### Security Layers

1. **Network Security**
   - TLS 1.3 encryption
   - Network policies (K8s)
   - DDoS protection

2. **Application Security**
   - JWT authentication
   - RBAC authorization
   - Input validation
   - SQL injection prevention
   - XSS protection
   - CSRF protection

3. **Infrastructure Security**
   - Container security (non-root)
   - Secret management
   - Image scanning
   - Pod security policies

## Scalability

### Horizontal Scaling

| Service | Min Replicas | Max Replicas | Scaling Metric |
|---------|-------------|--------------|----------------|
| Frontend | 2 | 5 | CPU 70% |
| Backend | 2 | 10 | CPU 70%, Memory 80% |
| ML Service | 2 | 5 | CPU 60%, Memory 70% |

### Vertical Scaling

| Service | CPU Request | CPU Limit | Memory Request | Memory Limit |
|---------|-------------|-----------|----------------|--------------|
| Frontend | 50m | 200m | 64Mi | 256Mi |
| Backend | 250m | 1000m | 256Mi | 1Gi |
| ML Service | 500m | 2000m | 1Gi | 4Gi |

## Deployment

### Kubernetes Resources

```
Namespace: chainsense-ai
├── Deployments
│   ├── backend (3 replicas)
│   ├── frontend (2 replicas)
│   └── ml-service (2 replicas)
├── StatefulSets
│   └── postgres (1 replica)
├── Services
│   ├── backend (ClusterIP)
│   ├── frontend (ClusterIP)
│   ├── ml-service (ClusterIP)
│   ├── postgres (ClusterIP)
│   └── redis (ClusterIP)
├── Ingress
│   └── chainsense-ingress
├── ConfigMaps
│   └── chainsense-config
├── Secrets
│   └── chainsense-secrets
├── HorizontalPodAutoscalers
│   ├── backend-hpa
│   ├── frontend-hpa
│   └── ml-service-hpa
└── NetworkPolicies
    ├── default-deny-all
    ├── allow-frontend
    ├── allow-backend
    └── allow-ml-service
```

## Monitoring

### Metrics Collected

- Request latency (p50, p95, p99)
- Request rate
- Error rate
- CPU/Memory usage
- Database connections
- Cache hit rate
- ML model inference time
- Queue depth

### Alerting Rules

| Alert | Condition | Severity |
|-------|-----------|----------|
| High Error Rate | > 5% errors in 5m | Critical |
| High Latency | p99 > 2s for 5m | Warning |
| Pod Crash Loop | > 3 restarts in 10m | Critical |
| Database Connection Pool | > 80% used | Warning |
| ML Inference Slow | > 5s average | Warning |

## Disaster Recovery

### Backup Strategy

- **Database**: Daily full backup, WAL archiving for PITR
- **ML Models**: Versioned in object storage
- **Configuration**: Git repository

### Recovery Time Objectives

- **RTO (Recovery Time Objective)**: 4 hours
- **RPO (Recovery Point Objective)**: 1 hour

## Future Enhancements

1. **Event Sourcing** - Full audit trail with CQRS
2. **GraphQL API** - Flexible queries for mobile
3. **Real-time Updates** - WebSocket/SSE integration
4. **Multi-tenancy** - B2B SaaS model
5. **Mobile App** - React Native application
6. **Edge Computing** - IoT sensor integration

# FastAPI Blog Tracker Helm Chart

This Helm chart deploys the FastAPI Blog Tracker application on a Kubernetes cluster.

## Prerequisites

- Kubernetes 1.19+
- Helm 3.0+
- Nginx Ingress Controller (for ingress support)

## Installing the Chart

1. First, build and push the Docker image:
```bash
cd /path/to/fastapi_blog_tracker
docker build -t your-registry/fastapi-blog:latest .
docker push your-registry/fastapi-blog:latest
```

2. Update the `values.yaml` file with your image repository:
```yaml
image:
  repository: your-registry/fastapi-blog
  tag: latest
```

3. Install the chart:
```bash
helm install fastapi-blog ./helm/fastapi-blog
```

## Configuration

The following table lists the configurable parameters of the FastAPI Blog Tracker chart and their default values.

| Parameter | Description | Default |
|-----------|-------------|---------|
| `replicaCount` | Number of replicas | `1` |
| `image.repository` | Image repository | `fastapi-blog` |
| `image.tag` | Image tag | `latest` |
| `image.pullPolicy` | Image pull policy | `IfNotPresent` |
| `service.type` | Service type | `ClusterIP` |
| `service.port` | Service port | `8000` |
| `ingress.enabled` | Enable ingress | `true` |
| `ingress.className` | Ingress class name | `nginx` |
| `ingress.hosts` | Ingress hosts | `[{host: "fastapi-blog.local", paths: [{path: "/", pathType: "Prefix"}]}]` |
| `resources` | Pod resources | `{}` |
| `autoscaling.enabled` | Enable autoscaling | `false` |
| `autoscaling.minReplicas` | Minimum replicas | `1` |
| `autoscaling.maxReplicas` | Maximum replicas | `3` |
| `env` | Environment variables | See `values.yaml` |

## Accessing the Application

Once deployed, you can access the application through the ingress host you configured. By default, it's accessible at:

```
http://fastapi-blog.local
```

Make sure to add the domain to your hosts file or configure your DNS accordingly.

## Uninstalling the Chart

To uninstall/delete the deployment:

```bash
helm uninstall fastapi-blog
```

## Notes

- The application uses SQLite by default. For production, consider using a proper database service.
- Secrets should be managed properly in production using a secrets management solution.
- Configure resource limits and requests according to your application's needs.
- Enable and configure autoscaling based on your production requirements.

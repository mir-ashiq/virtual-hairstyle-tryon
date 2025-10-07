# Performance Optimization Guide

## Overview

This guide provides strategies for optimizing the Virtual Hairstyle Try-On application for better performance, reduced latency, and efficient resource usage.

## Optimization Strategies

### 1. Image Preprocessing

#### Resize Images Before Transfer
```python
from src.utils import ImageProcessor

processor = ImageProcessor()
face_img = processor.resize_image(face_img, max_width=1024, max_height=1024)
hair_img = processor.resize_image(hair_img, max_width=1024, max_height=1024)
```

**Benefits:**
- Reduced memory usage
- Faster processing time
- Lower GPU memory requirements

#### Batch Processing
For multiple transfers, process in batches:

```python
def process_batch(face_images, hairstyle_images):
    results = []
    for face, hair in zip(face_images, hairstyle_images):
        result, log = service.transfer_hairstyle(face, hair)
        results.append(result)
    return results
```

### 2. Model Optimization

#### One-Time Initialization
Initialize the model once and reuse:

```python
# At startup
service = HairstyleTransferService()
service.initialize()

# For each request (no re-initialization)
result, log = service.transfer_hairstyle(face, hair)
```

#### GPU Acceleration
Enable CUDA if available:

```python
import torch

if torch.cuda.is_available():
    device = torch.device('cuda')
    print(f"Using GPU: {torch.cuda.get_device_name(0)}")
else:
    device = torch.device('cpu')
    print("Using CPU")
```

### 3. Caching Strategies

#### Cache Aligned Images
Avoid re-alignment for same images:

```python
from functools import lru_cache
import hashlib

@lru_cache(maxsize=100)
def get_aligned_image(image_hash):
    # Return cached aligned image
    pass
```

#### Gallery Caching
Cache gallery metadata:

```python
class HairstyleGalleryService:
    def __init__(self):
        self._category_cache = None
        self._stats_cache = None
    
    def get_categories(self):
        if self._category_cache is None:
            self._category_cache = self._load_categories()
        return self._category_cache
```

### 4. Resource Management

#### Limit Concurrent Requests
Use queuing for multiple simultaneous requests:

```python
from queue import Queue
from threading import Thread

request_queue = Queue(maxsize=10)

def worker():
    while True:
        face, hair = request_queue.get()
        process_transfer(face, hair)
        request_queue.task_done()
```

#### Clean Up Temporary Files
Regularly clean temporary files:

```python
import os
import time

def cleanup_old_files(directory, max_age_hours=24):
    now = time.time()
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.getmtime(filepath) < now - (max_age_hours * 3600):
            os.remove(filepath)
```

### 5. Configuration Tuning

#### Optimal Settings
Adjust settings for your use case:

```python
# For faster processing (lower quality)
settings.PROCESS_TIMEOUT = 180  # 3 minutes
smoothness = 3

# For better quality (slower)
settings.PROCESS_TIMEOUT = 600  # 10 minutes
smoothness = 5
enhance = True
```

#### Memory Management
Monitor and limit memory usage:

```python
import psutil

def check_memory():
    memory = psutil.virtual_memory()
    if memory.percent > 80:
        # Clear caches or reject request
        print("Memory usage high, clearing cache")
```

### 6. Network Optimization

#### Compress Images
Compress images before upload/download:

```python
from PIL import Image

def compress_image(image, quality=85):
    buffer = io.BytesIO()
    image.save(buffer, format='JPEG', quality=quality, optimize=True)
    return Image.open(buffer)
```

#### Async Loading
Load resources asynchronously:

```python
import asyncio

async def load_gallery():
    # Load gallery items asynchronously
    pass
```

### 7. Database & Storage

#### Use Database for Metadata
Store gallery metadata in database instead of files:

```python
import sqlite3

def store_hairstyle_metadata(name, category, tags):
    conn = sqlite3.connect('gallery.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO hairstyles VALUES (?, ?, ?)",
        (name, category, json.dumps(tags))
    )
    conn.commit()
```

#### CDN for Static Assets
Use CDN for hairstyle images:

```python
CDN_URL = "https://cdn.example.com/hairstyles/"

def get_hairstyle_url(category, name):
    return f"{CDN_URL}{category}/{name}.png"
```

## Performance Metrics

### Monitoring
Track key metrics:

```python
import time

class PerformanceMonitor:
    def __init__(self):
        self.metrics = {
            'total_transfers': 0,
            'avg_time': 0,
            'success_rate': 0
        }
    
    def track_transfer(self, duration, success):
        self.metrics['total_transfers'] += 1
        # Update metrics
```

### Benchmarking
Regular benchmarking:

```python
def benchmark_transfer():
    times = []
    for _ in range(10):
        start = time.time()
        result, log = service.transfer_hairstyle(face, hair)
        times.append(time.time() - start)
    
    print(f"Average time: {sum(times)/len(times):.2f}s")
    print(f"Min time: {min(times):.2f}s")
    print(f"Max time: {max(times):.2f}s")
```

## Production Deployment

### Load Balancing
Distribute load across multiple instances:

```nginx
upstream hairstyle_app {
    server app1.example.com;
    server app2.example.com;
    server app3.example.com;
}
```

### Horizontal Scaling
Scale based on load:

```yaml
# Kubernetes autoscaling
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: hairstyle-app
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: hairstyle-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### Queue-Based Processing
Use message queues for async processing:

```python
import redis
from rq import Queue

redis_conn = redis.Redis()
queue = Queue(connection=redis_conn)

def process_async(face_img, hair_img):
    job = queue.enqueue(
        transfer_hairstyle,
        face_img,
        hair_img,
        timeout='10m'
    )
    return job.id
```

## Optimization Checklist

- [ ] Resize images to optimal size
- [ ] Initialize model once at startup
- [ ] Enable GPU if available
- [ ] Implement caching for repeated operations
- [ ] Clean up temporary files regularly
- [ ] Monitor memory and CPU usage
- [ ] Use appropriate timeout values
- [ ] Compress images for transfer
- [ ] Implement request queuing
- [ ] Set up monitoring and alerts
- [ ] Use CDN for static assets
- [ ] Enable load balancing
- [ ] Implement auto-scaling
- [ ] Use async processing for long operations

## Expected Performance

### With Optimizations

| Metric | CPU | GPU |
|--------|-----|-----|
| Transfer Time | 3-4 min | 1-2 min |
| Memory Usage | 4-6 GB | 6-8 GB |
| Concurrent Users | 2-3 | 5-10 |
| Success Rate | 95%+ | 97%+ |

### Without Optimizations

| Metric | CPU | GPU |
|--------|-----|-----|
| Transfer Time | 5-7 min | 2-3 min |
| Memory Usage | 6-10 GB | 8-12 GB |
| Concurrent Users | 1-2 | 3-5 |
| Success Rate | 90%+ | 95%+ |

## Troubleshooting

### High Memory Usage
- Reduce image sizes
- Clear caches more frequently
- Limit concurrent requests
- Use swap space

### Slow Processing
- Enable GPU acceleration
- Reduce smoothness level
- Resize images before processing
- Use faster transfer style

### Request Timeouts
- Increase timeout values
- Queue long-running requests
- Process in smaller batches
- Scale horizontally

## Tools & Monitoring

### Recommended Tools
- **Monitoring**: Prometheus, Grafana
- **Profiling**: cProfile, py-spy
- **Memory**: memory_profiler
- **Load Testing**: locust, ab
- **APM**: New Relic, DataDog

### Sample Monitoring Setup
```python
from prometheus_client import Counter, Histogram

transfer_counter = Counter('hairstyle_transfers_total', 'Total transfers')
transfer_duration = Histogram('hairstyle_transfer_duration_seconds', 'Transfer duration')

@transfer_duration.time()
def process_transfer(face, hair):
    transfer_counter.inc()
    return service.transfer_hairstyle(face, hair)
```

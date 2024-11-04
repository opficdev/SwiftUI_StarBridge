import multiprocessing

workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
wsgi_app = "api_ulti:app"
timeout = 60
loglevel = "info"
bind = "0.0.0.0:8000"  
max_requests = 1000
max_requests_jitter = 100

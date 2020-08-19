# bytesized-metrics
Prometheus exporter for bytesized appbox

# Example
docker run -d -e API="$apikey" -p 8888:8888  manofcolombia/bytesized-metrics:latest

Generate your api key here: https://bytesized-hosting.com/api_keys

We collect metrics on scrape. This is to mean the scrape interval in prometheus config determines how often metrics from the API are polled.

Recommended 600 seconds for a scrape. Seems like the API is only updated every ~30 mins.

# Screenshots

![alt text](https://github.com/manofcolombia/bytesized-metrics/blob/dev/extras/bytesized-dashboard.png?raw=true)

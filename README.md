# bytesized-metrics
Prometheus exporter for bytesized appbox

# Example
docker run -d -e API="$apikey" -e INTERVAL="$interval" -p 8888:8888  manofcolombia/bytesized-metrics:latest

Generate your api key here: https://bytesized-hosting.com/api_keys

Interval is in seconds.
Recommended interval is 600. The appbox api seems to only update between 10-30 minute intervals.
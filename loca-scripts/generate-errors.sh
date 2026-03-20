#!/bin/bash
HOST="http://julian-areiza-el-mas-crack:8080"

echo "=== Generating 401 errors (invalid API key) ==="
for i in $(seq 1 10); do
  curl -s -o /dev/null -w "%{http_code}\n" -X POST "$HOST/api/v1/items" \
    -H "Content-Type: application/json" \
    -H "X-Api-Key: wrong-key" \
    -d '{"name":"test","description":"test"}'
done

echo ""
echo "=== Generating 404 errors (item not found) ==="
for i in $(seq 1 10); do
  curl -s -o /dev/null -w "%{http_code}\n" "$HOST/api/v1/items/999"
done

echo ""
echo "=== Generating 500 errors (triggers ERROR logs) ==="
for i in $(seq 1 5); do
  curl -s -o /dev/null -w "%{http_code}\n" "$HOST/api/v1/error"
done

echo ""
echo "Done. Wait ~1 min for metrics to appear in Grafana."

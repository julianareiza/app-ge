# Tráfico normal (50% estable, 50% canary)
for i in $(seq 1 10); do curl -s http://julian-areiza-el-mas-crack:8080/version; echo; done

# Forzar canary
curl -H "X-Canary: always" http://julian-areiza-el-mas-crack:8080/version

# Forzar estable (sin header)
curl http://julian-areiza-el-mas-crack:8080/version

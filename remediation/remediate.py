import requests
import time
import subprocess
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Config
PROMETHEUS_URL = "http://localhost:9090"
AIOPS_API_URL = "http://localhost:8000"
CHECK_INTERVAL = 30  # Check every 30 seconds

def get_current_metrics():
    """Fetch current metrics from Prometheus"""
    try:
        # Get CPU usage
        cpu_response = requests.get(
            f"{PROMETHEUS_URL}/api/v1/query",
            params={"query": "100 - (avg(rate(node_cpu_seconds_total{mode='idle'}[5m])) * 100)"}
        )
        cpu_data = cpu_response.json()
        cpu_usage = float(cpu_data['data']['result'][0]['value'][1])

        # Get Memory usage
        mem_response = requests.get(
            f"{PROMETHEUS_URL}/api/v1/query",
            params={"query": "((node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes) * 100"}
        )
        mem_data = mem_response.json()
        memory_usage = float(mem_data['data']['result'][0]['value'][1])

        # Get Disk usage
        disk_response = requests.get(
            f"{PROMETHEUS_URL}/api/v1/query",
            params={"query": "((node_filesystem_size_bytes{mountpoint='/'} - node_filesystem_free_bytes{mountpoint='/'}) / node_filesystem_size_bytes{mountpoint='/'}) * 100"}
        )
        disk_data = disk_response.json()
        disk_usage = float(disk_data['data']['result'][0]['value'][1])

        return {
            "cpu_usage": round(cpu_usage, 2),
            "memory_usage": round(memory_usage, 2),
            "disk_usage": round(disk_usage, 2)
        }

    except Exception as e:
        logger.error(f"Error fetching metrics: {e}")
        return None

def check_anomaly(metrics):
    """Send metrics to AI model for anomaly detection"""
    try:
        response = requests.post(
            f"{AIOPS_API_URL}/predict",
            json=metrics
        )
        return response.json()
    except Exception as e:
        logger.error(f"Error checking anomaly: {e}")
        return None

def remediate(metrics, anomaly_result):
    """Auto remediation based on anomaly type"""
    logger.warning(f"ANOMALY DETECTED! Metrics: {metrics}")
    logger.warning(f"Anomaly Score: {anomaly_result['anomaly_score']}")

    # High CPU remediation
    if metrics['cpu_usage'] > 80:
        logger.info("High CPU detected! Clearing system cache...")
        subprocess.run(['sudo', 'sync'], capture_output=True)
        subprocess.run(['sudo', 'sh', '-c', 'echo 3 > /proc/sys/vm/drop_caches'],
                      capture_output=True)
        logger.info("Cache cleared!")

    # High Memory remediation
    if metrics['memory_usage'] > 85:
        logger.info("High Memory detected! Restarting heavy services...")
        subprocess.run(['sudo', 'systemctl', 'restart', 'docker'],
                      capture_output=True)
        logger.info("Docker restarted!")

    # High Disk remediation
    if metrics['disk_usage'] > 85:
        logger.info("High Disk usage detected! Cleaning up...")
        subprocess.run(['sudo', 'docker', 'system', 'prune', '-f'],
                      capture_output=True)
        logger.info("Docker cleanup done!")

def main():
    logger.info("AIOps Auto-Remediation System Started!")
    logger.info(f"Checking metrics every {CHECK_INTERVAL} seconds...")

    while True:
        # Get metrics
        metrics = get_current_metrics()

        if metrics:
            logger.info(f"Current Metrics → CPU: {metrics['cpu_usage']}% | Memory: {metrics['memory_usage']}% | Disk: {metrics['disk_usage']}%")

            # Check for anomaly
            anomaly_result = check_anomaly(metrics)

            if anomaly_result:
                if anomaly_result['is_anomaly']:
                    remediate(metrics, anomaly_result)
                else:
                    logger.info(f"Status: {anomaly_result['status']}")

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
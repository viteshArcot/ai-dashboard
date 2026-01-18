#!/usr/bin/env python3
"""Simple test script for the AI Dashboard API"""

import requests
import pandas as pd
import io

# Create a sample CSV for testing
sample_data = {
    'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
    'age': [25, 30, 35, 28, 32],
    'salary': [50000, 60000, 70000, 55000, 65000],
    'department': ['IT', 'HR', 'IT', 'Finance', 'IT']
}

df = pd.DataFrame(sample_data)
csv_content = df.to_csv(index=False)

def test_api():
    base_url = "http://localhost:8000"
    
    print("Testing API endpoints...")
    
    # Test health check
    try:
        response = requests.get(f"{base_url}/health")
        print(f"✓ Health check: {response.json()}")
    except Exception as e:
        print(f"✗ Health check failed: {e}")
        return
    
    # Test upload
    try:
        files = {'file': ('test_data.csv', csv_content, 'text/csv')}
        response = requests.post(f"{base_url}/api/v1/upload", files=files)
        upload_result = response.json()
        print(f"✓ Upload: {upload_result}")
        dataset_id = upload_result['dataset_id']
    except Exception as e:
        print(f"✗ Upload failed: {e}")
        return
    
    # Test analysis
    try:
        response = requests.get(f"{base_url}/api/v1/analyze/{dataset_id}")
        analysis_result = response.json()
        print(f"✓ Analysis completed in {analysis_result['processing_time']:.2f}s")
        print(f"  Charts generated: {len(analysis_result['charts'])}")
        print(f"  Summary: {analysis_result['summary'][:100]}...")
    except Exception as e:
        print(f"✗ Analysis failed: {e}")
    
    # Test history
    try:
        response = requests.get(f"{base_url}/api/v1/history")
        history = response.json()
        print(f"✓ History: {len(history['history'])} analyses")
    except Exception as e:
        print(f"✗ History failed: {e}")
    
    # Test metrics
    try:
        response = requests.get(f"{base_url}/api/v1/metrics")
        metrics = response.json()
        print(f"✓ Metrics: {metrics}")
    except Exception as e:
        print(f"✗ Metrics failed: {e}")

if __name__ == "__main__":
    test_api()
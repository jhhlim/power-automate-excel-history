"""Download files from SharePoint using provided URLs."""

import sys
import os
import requests
from pathlib import Path


def download_file(file_url: str, output_path: str) -> bool:
    """
    Download a file from a URL and save it locally.
    
    Args:
        file_url: URL to download from (e.g., SharePoint download link)
        output_path: Local path to save the file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        print(f"Downloading from: {file_url}")
        print(f"Saving to: {output_path}")
        
        # Create parent directories if they don't exist
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Download the file
        response = requests.get(file_url, timeout=30)
        response.raise_for_status()
        
        # Save to disk
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        print(f"Successfully downloaded file ({len(response.content)} bytes)")
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python download_file.py <file_url> <output_path>")
        sys.exit(1)
    
    file_url = sys.argv[1]
    output_path = sys.argv[2]
    
    success = download_file(file_url, output_path)
    sys.exit(0 if success else 1)

"""
Script to download the Online Retail dataset for Customer Segmentation.
Saves the dataset into the 'dataset' directory.
Supports fast CDN mirrors with automatic fallback and progress reporting.
"""

import os
import sys
import time
import urllib.request
from pathlib import Path

# Configuration
DATASET_DIR = Path(__file__).resolve().parent / "dataset"
DATASET_FILENAME = "Online Retail.xlsx"
TARGET_PATH = DATASET_DIR / DATASET_FILENAME

# Mirrors: 1st is fast GitHub CDN, 2nd is UCI repository archive
DATASET_MIRRORS = [
    {
        "name": "Fast GitHub Raw CDN Mirror",
        "url": "https://raw.githubusercontent.com/pplonski/datasets-for-start/refs/heads/master/online-retail/Online-Retail.xlsx"
    },
    {
        "name": "Official UCI Machine Learning Repository",
        "url": "https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx"
    }
]


def format_size(bytes_size: float) -> str:
    """Format bytes to human readable format (B, KB, MB, GB)."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} TB"


def download_from_url(url: str, output_path: Path, timeout: int = 40) -> bool:
    """Download a file with progress indicator from a given URL."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    req = urllib.request.Request(url, headers=headers)
    start_time = time.time()

    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            content_length = response.getheader("Content-Length")
            total_bytes = int(content_length) if content_length and content_length.isdigit() else None
            
            chunk_size = 1024 * 128  # 128 KB chunks
            downloaded_bytes = 0
            
            # Temporary download file
            temp_output = output_path.with_suffix(".tmp")
            
            with open(temp_output, "wb") as f:
                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded_bytes += len(chunk)
                    
                    elapsed = max(time.time() - start_time, 0.001)
                    speed = downloaded_bytes / elapsed
                    speed_str = f"{format_size(speed)}/s"

                    if total_bytes and total_bytes > 0:
                        percent = (downloaded_bytes / total_bytes) * 100
                        bar_len = 30
                        filled = int(bar_len * downloaded_bytes // total_bytes)
                        bar = "#" * filled + "-" * (bar_len - filled)
                        status = f"\r  [{bar}] {percent:5.1f}% | {format_size(downloaded_bytes)} / {format_size(total_bytes)} | {speed_str} "
                    else:
                        status = f"\r  Downloading... {format_size(downloaded_bytes)} | {speed_str} "

                    sys.stdout.write(status)
                    sys.stdout.flush()

            # Rename temp to target
            if temp_output.exists():
                if output_path.exists():
                    output_path.unlink()
                temp_output.rename(output_path)
            
            print()
            return True

    except Exception as e:
        temp_output = output_path.with_suffix(".tmp")
        if temp_output.exists():
            temp_output.unlink()
        print(f"\n  [WARN] Download from mirror failed: {e}")
        return False


def download_dataset(output_path: Path = TARGET_PATH, force: bool = False):
    """
    Downloads the dataset and verifies its presence.
    Tries multiple mirrors until successful.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if output_path.exists() and output_path.stat().st_size > 1000 and not force:
        size_str = format_size(output_path.stat().st_size)
        print("=" * 65)
        print(f"[INFO] Dataset already exists at:")
        print(f"       -> {output_path} ({size_str})")
        print("[INFO] Use --force flag if you wish to re-download.")
        print("=" * 65)
        return

    print("=" * 65)
    print("CUSTOMER SEGMENTATION - DATASET DOWNLOADER")
    print("=" * 65)
    print(f"Target Directory: {output_path.parent}")
    print(f"Target Filename : {output_path.name}")
    print("-" * 65)

    success = False
    for i, mirror in enumerate(DATASET_MIRRORS, 1):
        print(f"\nAttempting Mirror {i}/{len(DATASET_MIRRORS)}: {mirror['name']}")
        print(f"URL: {mirror['url']}")
        if download_from_url(mirror['url'], output_path):
            success = True
            break
        print("Trying next available mirror...")

    if not success:
        print("\n" + "=" * 65)
        print("[ERROR] All download attempts failed. Please check your internet connection.")
        print("=" * 65)
        sys.exit(1)

    final_size = output_path.stat().st_size
    print("-" * 65)
    print(f"[SUCCESS] Dataset successfully downloaded & saved:")
    print(f"          Path: {output_path}")
    print(f"          Size: {format_size(final_size)}")
    print("=" * 65)
    print("\nHow to load this dataset in your Jupyter Notebook:")
    print(f"     import pandas as pd")
    print(f"     df = pd.read_excel('dataset/{output_path.name}')")


if __name__ == "__main__":
    force_flag = "--force" in sys.argv
    download_dataset(force=force_flag)

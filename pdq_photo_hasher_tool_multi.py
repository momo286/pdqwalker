#!/usr/bin/env python3
import argparse
import sys
import os
import multiprocessing

# Add parent path for importing local modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from pdqhashing.hasher.pdq_hasher import PDQHasher

def hash_file(path):
    try:
        hasher = PDQHasher()
        hash_data = hasher.fromFile(path)
        hash_code = hash_data.getHash()
        return f"{hash_code},{path}"
    except Exception as e:
        return f"Error processing {path}: {e}"

def find_image_files(directory):
    supported_exts = ('.jpg', '.jpeg', '.png')
    return [
        os.path.join(root, file)
        for root, _, files in os.walk(directory)
        for file in files
        if file.lower().endswith(supported_exts)
    ]

def compute_pdq_hashes(directory, num_processes):
    image_files = find_image_files(directory)
    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.map(hash_file, image_files)
    print("\n".join(results))

def main():
    parser = argparse.ArgumentParser(description="Compute PDQ hashes for image files.")
    parser.add_argument("directory", help="Directory to recursively process.")
    parser.add_argument("--num-processes", type=int, default=multiprocessing.cpu_count(),
                        help="Number of processes to use for hashing.")
    args = parser.parse_args()

    compute_pdq_hashes(args.directory, args.num_processes)

if __name__ == "__main__":
    main()

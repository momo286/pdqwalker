#!/usr/bin/env python
import argparse
import sys
import os
import multiprocessing
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from pdqhashing.hasher.pdq_hasher import PDQHasher


def hash_file(path):
    pdq_hasher = PDQHasher()
    try:
        hash_and_quality = pdq_hasher.fromFile(path)
        hash_code = hash_and_quality.getHash()  
        result = f"{str(hash_code)},{path}"
    except IOError as e:
        result = f"Error reading {path}: {e}"
    except Exception as e:
        result = f"Error processing {path}: {e}"
    return result
 
def compute_pdq_hashes(directory, output_hashes, num_processes):
    image_files = [os.path.join(dp, f) for dp, _, filenames in os.walk(directory) for f in filenames if f.endswith(('.jpg', '.jpeg', '.png'))]
    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.map(hash_file, image_files)
    for result in results:
        print(result)

def main():
    parser = argparse.ArgumentParser(description="Compute PDQ hashes for image files.")
    parser.add_argument("directory", help="Directory to recursively process.")
    parser.add_argument("--output", type=argparse.FileType('w'), default=sys.stdout,
                        help="Output file to write the hashes to.")
    parser.add_argument("--num-processes", type=int, default=(multiprocessing.cpu_count()),
                        help="Number of processes to use for hashing.")
    args = parser.parse_args()

    dir=args.directory

    compute_pdq_hashes(args.directory, args.output, args.num_processes)

if __name__ == "__main__":
    main()

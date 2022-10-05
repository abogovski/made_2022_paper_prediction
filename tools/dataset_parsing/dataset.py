import json
import os
import re
from tqdm import tqdm


def read_dataset(path):
    bytes_read = 0
    total = os.stat(path).st_size
    with open(path, 'rb') as f, tqdm(total=total, unit_scale=True) as pbar:
        entry = []
        for line in f:
            if line.startswith(b'[') or line.startswith(b']'):
                continue

            if not line.startswith(b'}'):
                entry.append(line)
                continue

            entry.append(b'}')
            yield json.loads(re.sub(br'NumberInt\((\d*)\)', br"\1", b''.join(entry)))
            entry.clear()

            new_bytes_read = f.tell()
            pbar.update(new_bytes_read - bytes_read)
            bytes_read = new_bytes_read

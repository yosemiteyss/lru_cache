import sys
import time
from cache import Cache
from cache_entry import CacheEntry

OUTPUT_FILE = '20514332-output.txt'

# Query
QUERY_CHECK = 'Check'
QUERY_ADD = 'Add'
QUERY_DELETE = 'Delete'

# Caches
l1_cache = Cache(8)
l2_cache = Cache(16)
l3_cache = Cache(32)
storage = []

def cache_str(frm):
    return ','.join([str(data) for data in map(lambda entry: entry.data, frm.queue)])

def write_output(outfile, line):
    outfile.write(f'{line}\n')

def move_mru(frm, to):
    frm_mru = frm.get_mru()
    frm.remove(frm_mru.data)
    to.add(frm_mru)

def move_lru(frm, to):
    frm_lru = frm.detach_lru()
    to.add(frm_lru)   

def delete(outfile, data):
    if l1_cache.contains(data):
        l1_cache.remove(data)
        
        if not l2_cache.is_empty():
            # Move L2's mru entry to L1
            move_mru(l2_cache, l1_cache)

            if not l3_cache.is_empty():
                # Move L3's mru entry to L2
                move_mru(l3_cache, l2_cache)
        
        write_output(outfile, 'Deleted')
    
    elif l2_cache.contains(data):
        l2_cache.remove(data)

        if not l3_cache.is_empty():
            # Move L3's mru entry to L2
            move_mru(l3_cache, l2_cache)
        
        write_output(outfile, 'Deleted')

    elif l3_cache.contains(data):
        l3_cache.remove(data)
        write_output(outfile, 'Deleted')
        
    elif data in storage:
        storage.remove(data)
        write_output(outfile, 'Deleted')

    else:
        write_output(outfile, 'Already absent')

def add(outfile, data):
    if l1_cache.contains(data) or l2_cache.contains(data) or l3_cache.contains(data) or data in storage:
        write_output(outfile, 'Already present')
    else:
        # Add to storage, caches are left untouched
        storage.append(data)
        write_output(outfile, 'Added')
        
def check(outfile, data):
    if l1_cache.contains(data):
        # Re-add check entry to L1
        l1_cache.remove(data)
        l1_cache.add(CacheEntry(data))

        write_output(outfile, 'Found in L1')

    elif l2_cache.contains(data):
        # Remove check entry from L2
        l2_cache.remove(data)

        # Move L1's lru entry to L2
        move_lru(l1_cache, l2_cache)

        # Add check entry to L1
        l1_cache.add(CacheEntry(data))      

        write_output(outfile, 'Found in L2')         

    elif l3_cache.contains(data):
        # Remove check entry from L3
        l3_cache.remove(data)

        # Move L2's lru entry to L3
        move_lru(l2_cache, l3_cache)

        # Move L1's lru entry to L2
        move_lru(l1_cache, l2_cache)

        # Add check entry to L1
        l1_cache.add(CacheEntry(data))   

        write_output(outfile, 'Found in L3')

    elif data in storage:
        # Remove check entry from storage
        storage.remove(data)

        if l1_cache.is_full() and l2_cache.is_full() and l3_cache.is_full():
            # Move L3's lru entry back to storage
            l3_lru = l3_cache.detach_lru()
            storage.append(l3_lru.data)

            move_lru(l2_cache, l3_cache)
            move_lru(l1_cache, l2_cache)

        elif l1_cache.is_full() and l2_cache.is_full():
            move_lru(l2_cache, l3_cache)
            move_lru(l1_cache, l2_cache)

        elif l1_cache.is_full():
            move_lru(l1_cache, l2_cache)
            
        # Add check entry to L1
        l1_cache.add(CacheEntry(data))

        write_output(outfile, 'Found in storage')

    else:
        write_output(outfile, 'Not found')
    
def main(argv):
    input_file_name = argv[1]

    with open(input_file_name, 'r') as input_file, open(OUTPUT_FILE, 'a') as output_file:
        for line in input_file:
            inputs = line.split()
            query = inputs[0]
            data = int(inputs[1])

            # Execute query
            switcher = {
                QUERY_CHECK: check,
                QUERY_ADD: add,
                QUERY_DELETE: delete
            }
            switcher[query](output_file, data)

        # Print cache result
        write_output(output_file, cache_str(l1_cache))
        write_output(output_file, cache_str(l2_cache))
        write_output(output_file, cache_str(l3_cache))
            
if __name__ == "__main__":
    main(sys.argv)


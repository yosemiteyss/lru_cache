import sys
import time
from cache import Cache
from cache_entry import CacheEntry

# Query
QUERY_CHECK = 'Check'
QUERY_ADD = 'Add'
QUERY_DELETE = 'Delete'

l1_cache = Cache(8)
l2_cache = Cache(16)
l3_cache = Cache(32)

storage = []

def write_query(line):
    with open('output.txt', 'a') as output_file:
        output_file.write(line)

def write_output(line):
    l1_str = ' '.join(str(x) for x in map(lambda q: q.data, l1_cache.queue))
    l2_str = ' '.join(str(x) for x in map(lambda q: q.data, l2_cache.queue))
    l3_str = ' '.join(str(x) for x in map(lambda q: q.data, l3_cache.queue))
    storage_str = ' '.join(str(x) for x in storage)
    print(line)
    with open('output.txt', 'a') as output_file:
        #output_file.write(f'{line}\n\t\tL1: {l1_str}\n\t\tL2: {l2_str}\n\t\tL3: {l3_str}\n\t\tstorage: {storage_str}\n')
        output_file.write(f'{line}\n')

def delete(data):
    if l1_cache.contains(data):
        l1_cache.remove(data)
        #storage.append(data)
        
        if not l2_cache.is_empty():
            # Remove mru from L2
            l2_mru = l2_cache.get_mru()
            l2_cache.remove(l2_mru.data)

            # Add L2's mru to L1
            l1_cache.add(l2_mru)

            if not l3_cache.is_empty():
                 # Remove mru from L3
                l3_mru = l3_cache.get_mru()
                l3_cache.remove(l3_mru.data)

                # Add L3's mru to L2
                l2_cache.add(l3_mru)
        
        write_output('Deleted')
    
    elif l2_cache.contains(data):
        l2_cache.remove(data)
        #storage.append(data)

        if not l3_cache.is_empty():
             # Remove mru from L3
            l3_mru = l3_cache.get_mru()
            l3_cache.remove(l3_mru.data)

            # Add L3's mru to L2
            l2_cache.add(l3_mru)
        
        write_output('Deleted')

    elif l3_cache.contains(data):
        l3_cache.remove(data)
        #storage.append(data)
        write_output('Deleted')
        
    elif data in storage:
        storage.remove(data)
        write_output('Deleted')

    else:
        write_output('Already absent')

def add(data):
    if l1_cache.contains(data) or l2_cache.contains(data) or l3_cache.contains(data) or data in storage:
        write_output('Already present')
    else:
        # Add to storage, caches are left untouched
        storage.append(data)
        write_output('Added')
        
def check(data):
    if l1_cache.contains(data):
        l1_cache.remove(data)
        l1_cache.add(CacheEntry(data))

        write_output('Found in L1')

    elif l2_cache.contains(data):
        # Remove check entry from L2
        l2_cache.remove(data)

        # Add check entry to L1
        l1_last = l1_cache.detach_last()
        l1_cache.add(CacheEntry(data))      

        # Add L1's lru entry to L2
        l2_cache.add(l1_last)     

        write_output('Found in L2')         

    elif l3_cache.contains(data):
        # Remove check entry from L3
        l3_cache.remove(data)

        # Add check entry to L1
        l1_last = l1_cache.detach_last()
        l1_cache.add(CacheEntry(data))

        # Remove lru entry from L2
        l2_last = l2_cache.detach_last()
        l2_cache.add(l1_last)

        # Add L2's lru entry to L3
        l3_cache.add(l2_last)

        write_output('Found in L3')

    elif data in storage:
        # Remove check entry from storage
        storage.remove(data)

        # Add check entry to L1
        if l1_cache.is_full():
            l1_last = l1_cache.detach_last()
            l1_cache.add(CacheEntry(data))

            if l2_cache.is_full():
                l2_last = l2_cache.detach_last()
                l2_cache.add(l1_last)

                if l3_cache.is_full():
                    l3_last = l3_cache.detach_last()
                    l3_cache.add(l2_last)
                    storage.append(l3_last.data)
                else:
                    l3_cache.add(l2_last)
            
            else:
                l2_cache.add(l1_last)

        else:
            l1_cache.add(CacheEntry(data))

        write_output('Found in storage')

    else:
        write_output('Not found')
    
def main(argv):
    input_file_name = argv[1]

    # Open file
    with open(input_file_name, 'r') as input_file:
        for line in input_file:
            inputs = line.split()

            query = inputs[0]
            data = int(inputs[1])

            switcher = {
                QUERY_CHECK: check,
                QUERY_ADD: add,
                QUERY_DELETE: delete
            }

            #write_query(line)

            switcher[query](data)
            
if __name__ == "__main__":
    main(sys.argv)


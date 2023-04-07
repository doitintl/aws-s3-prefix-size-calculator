'''
                 @                               (             (                
               @@@@@                          ((((((         (((((              
               @@@@@(                          ,(((          (((((              
      @@@@@@@@@@@@@@(       @@@@@@@@           ((((          ((((((((((((       
   @@@@@@@@@@@@@@@@@(    @@@@@@@@@@@@@@       ((((((         (((((((((((((      
 @@@@@@@@   @@@@@@@@(  @@@@@@@@  @@@@@@@@     ((((((         (((((              
 @@@@@        @@@@@@( @@@@@@        @@@@@@    ((((((         (((((         (((((
 @@@@@         @@@@@  @@@@@@        @@@@@@    ((((((        ((((((         (((((
 @@@@@@@    /@@@@@@@   @@@@@@@    @@@@@@@      (((((((     (((((((((     (((((((
   @@@@@@@@@@@@@@@      @@@@@@@@@@@@@@@@        ,(((((((((((((((((((((((((((((  
      @@@@@@@@@            @@@@@@@@@@              ((((((((((     (((((((((     
                        S3 prefix size calculator
'''

import csv


def sizeof_fmt(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"


if __name__ == '__main__':
    ### Path to file ###
    file_path = '/path/to/s3-inventory-file'
    ### End of path to file ###
    output = {}
    with open(file_path, 'r') as source:
        source_csv = list(csv.reader(source, delimiter=","))
        for inventory_row in source_csv:
            storage_class = inventory_row[8]
            size_in_bytes = int(inventory_row[5])
            object_path = inventory_row[1]
            prefix_as_list = object_path.split('/')
            prefix_list_without_object_name = prefix_as_list[:-1]
            i = 0
            for path in prefix_list_without_object_name:
                i += 1
                prefix = '/'.join(prefix_list_without_object_name[:i])
                if prefix not in output:
                    output[prefix] = {}
                if storage_class not in output[prefix]:
                    output[prefix][storage_class] = {'size': 0, 'objects': 0}
                output[prefix][storage_class]['size'] += size_in_bytes
                output[prefix][storage_class]['objects'] += 1
        for folder, details in output.items():
            for output_storage_class, size_and_objects_dict in details.items():
                size = sizeof_fmt(size_and_objects_dict['size'])
                objects = size_and_objects_dict['objects']
                print(f'prefix: {folder}, objects: {objects}, storage_class: {output_storage_class}, size: {size}')

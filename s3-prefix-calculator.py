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
                        S3 prefix size calculator by Avi Keinan
                        https://github.com/doitintl/aws-s3-prefix-size-calculator
'''

import json
import csv


def get_column_position_from_manifest(key: str):
    position = manifest_json['fileSchema'].split(', ')
    try:
        return position.index(key)
    except ValueError:
        print(f'Unable to find {key} in manifest file, please check aws s3 inventory settings and make sure to include {key}.')
        print('Exiting.')
        exit(0)


def sizeof_fmt(num, suffix="B"):
    # This function was copied from: https://stackoverflow.com/a/1094933
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"


if __name__ == '__main__':
    ### Edit Path to files ###
    manifest_file_path = '/path/to/manifest/manifest.json'
    csv_files = ['/path/to/file1.csv', '/path/to/file2.csv']
    ### End of path to files ###
    output = {}
    manifest_json = json.load(open(manifest_file_path))

    # Check if file format is CSV
    if manifest_json['fileFormat'] != 'CSV':
        print('this script supports s3 inventory in CSV format')
        print('Exiting.')
        exit(0)

    for csv_file_path in csv_files:
        with open(csv_file_path, 'r') as source:
            source_csv = list(csv.reader(source, delimiter=","))
            for inventory_row in source_csv:
                storage_class = inventory_row[get_column_position_from_manifest('StorageClass')]
                size_in_bytes = int(inventory_row[get_column_position_from_manifest('Size')])
                object_path = inventory_row[get_column_position_from_manifest('Key')]
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
print('Thank you for using DoiT.com s3 prefix size calculator')

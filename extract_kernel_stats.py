import argparse
import glob
import os
import sys

from tensorboard_plugin_profile.convert import raw_to_tool_data

def read_data(path_to_tests):
    """Read all the data in the default profile directory."""
    data_files = os.path.join(path_to_tests, 'plugins/profile' ,'*', '*.xplane.pb')
    return glob.glob(data_files)


def write_kernel_stats(data, format, path):
    """Writes kernel_stats to a file and adds file type extension."""
    file_name = os.path.join(path, 'kernel_stats' + '.' + format)
    with open(file_name, "w") as f:
        f.write(data)


def export_kernel_stats(data_files):
    """Exports the kernel_stats data for each file in `data_files` and saves them as csv and json next to the corresponding *.xplane.pb"""
    for data in data_files:
        
        # using "kernal_stats^" from 'profiler/plugin/tensorboard_plugin_profile/convert/raw_to_tool_data.py'
        # other stats are possible by simply changing the string
        data_csv, _ = raw_to_tool_data.xspace_to_tool_data([data], 'kernel_stats^', {'tqx' : 'out:csv;'})
        data_json, _ = raw_to_tool_data.xspace_to_tool_data([data], 'kernel_stats^', {'tqx' : 'out:json;'})
        
        path, _ = os.path.split(data)
        write_kernel_stats(data_csv, 'csv', path)
        write_kernel_stats(data_json, 'json', path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                    prog=os.path.basename(__file__),
                    description='Extracts kernel_stats from *.xplane.pb files in <logpath>',
                    epilog='')
    
    parser.add_argument("logpath")
    args = parser.parse_args()
    
    if not os.path.exists(args.logpath):
        print("No such directory: '" + args.logpath + "'")
        sys.exit(-1)
    
    print("Starting extraction of data...")
    data = read_data(args.logpath)
    export_kernel_stats(data)
    print("Done!")

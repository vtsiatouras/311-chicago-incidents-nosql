import time

import importers

from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument('input_files', nargs='+', help='The input files to parse')

args = parser.parse_args()
start = time.time()

for input_file in args.input_files:
    print(f"Processing file {input_file}")
    if input_file.endswith('abandoned-vehicles.csv'):
        importers.import_abandoned_vehicles(input_file=input_file)
    elif input_file.endswith('alley-lights-out.csv'):
        importers.import_alley_lights_out_or_street_lights_all_out(input_file=input_file, street_lights=False)
    elif input_file.endswith('garbage-carts.csv'):
        importers.import_garbage_carts(input_file=input_file)
    elif input_file.endswith('graffiti-removal.csv'):
        importers.import_graffiti(input_file=input_file)
    elif input_file.endswith('pot-holes-reported.csv'):
        importers.import_potholes(input_file=input_file)
    elif input_file.endswith('rodent-baiting.csv'):
        importers.import_rodent_baiting(input_file=input_file)
    elif input_file.endswith('sanitation-code-complaints.csv'):
        importers.import_sanitation_complaints(input_file=input_file)
    elif input_file.endswith('tree-debris.csv'):
        importers.import_tree_debris(input_file=input_file)
    elif input_file.endswith('tree-trims.csv'):
        importers.import_tree_trims(input_file=input_file)
    elif input_file.endswith('street-lights-all-out.csv'):
        importers.import_alley_lights_out_or_street_lights_all_out(input_file=input_file, street_lights=True)
    elif input_file.endswith('street-lights-one-out.csv'):
        importers.import_street_lights_one_out(input_file=input_file)
    else:
        print(f"File '{input_file}' cannot be processed, skipping.")

end = time.time()
print(f"Finished importing datasets, took {(end - start):.2f} seconds")




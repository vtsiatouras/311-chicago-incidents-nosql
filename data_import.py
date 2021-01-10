import time

from app.import_scripts import incidents_data_import, citizens_data_import, create_indexes

from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument('input_files', nargs='+', help='The input files to parse')

args = parser.parse_args()
start = time.time()

for input_file in args.input_files:
    print(f"Processing file {input_file}")
    if input_file.endswith('abandoned-vehicles.csv'):
        incidents_data_import.import_abandoned_vehicles(input_file=input_file)
    elif input_file.endswith('alley-lights-out.csv'):
        incidents_data_import.import_alley_lights_out_or_street_lights_all_out(input_file=input_file, street_lights=False)
    elif input_file.endswith('garbage-carts.csv'):
        incidents_data_import.import_garbage_carts(input_file=input_file)
    elif input_file.endswith('graffiti-removal.csv'):
        incidents_data_import.import_graffiti(input_file=input_file)
    elif input_file.endswith('pot-holes-reported.csv'):
        incidents_data_import.import_potholes(input_file=input_file)
    elif input_file.endswith('rodent-baiting.csv'):
        incidents_data_import.import_rodent_baiting(input_file=input_file)
    elif input_file.endswith('sanitation-code-complaints.csv'):
        incidents_data_import.import_sanitation_complaints(input_file=input_file)
    elif input_file.endswith('tree-debris.csv'):
        incidents_data_import.import_tree_debris(input_file=input_file)
    elif input_file.endswith('tree-trims.csv'):
        incidents_data_import.import_tree_trims(input_file=input_file)
    elif input_file.endswith('street-lights-all-out.csv'):
        incidents_data_import.import_alley_lights_out_or_street_lights_all_out(input_file=input_file, street_lights=True)
    elif input_file.endswith('street-lights-one-out.csv'):
        incidents_data_import.import_street_lights_one_out(input_file=input_file)
    else:
        print(f"File '{input_file}' cannot be processed, skipping.")

print("Generating citizens and up-votes")
citizens_data_import.create_up_votes()

print("Creating Indexes")
create_indexes.create_indexes()

end = time.time()
print(f"Finished importing datasets, took {(end - start):.2f} seconds")




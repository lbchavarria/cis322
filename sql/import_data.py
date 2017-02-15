import csv

def import_conv():
    conv_file = open("convoy.csv")
    convoy = csv.reader(conv_file, skipinitialspace=True)
    next(convoy)
    for i in convoy:
        print("INSERT INTO convoys (request, depart_dt, arrive_dt) VALUES ('{}', '{}', '{}',);".format(i[0], i[1], i[6]))
        vehicles = i[7]strip().split(",")
        for j in range(len(vehicles)):
            print("INSERT INTO assets (asset_tag, description) VALUES ('{}', 'vehicle');".format(vehicles[j].strip()))
            print("INSERT INTO vehicles (asset_fk) SELECT asset_pk FROM assets WHERE assets.asset_tag = '{}';".format(vehicles[j].strip()))
            print("INSERT INTO used_by (convoy_fk) SELECT convoy_pk FROM convoys WHERE convoys.request = '{}';".format(i[0]))
            print("UPDATE used_by SET vehicle_fk = (SELECT vehicle_pk FROM vehicles WHERE vehicles.asset_fk = (SELECT asset_pk FROM assets WHERE assets.asset_tag = '{}')) WHERE used_by.convoy_fk = (SELECT convoy_pk FROM convoys WHERE convoys.request = '{}');".format(vehicles[j].strip(), i[0]))
    convoy_file.close()

def import_DC():
    DC_file = open("DC_inventory.csv")
    DC = csv.reader(DC_file, skipinitialspace=True)
    next(DC)
    for i in DC:
        print("INSERT INTO products (description) VALUES ('{}');".format(i[1]))
        print("INSERT INTO assets (asset_tag) VALUES ('{}');".format(i[0]))
        print("UPDATE assets SET product_fk = (SELECT product_pk FROM products WHERE products.description = '{}') WHERE assets.asset_tag = '{}';".format(i[1], i[0]))
        print("INSERT INTO asset_at (asset_fk) SELECT asset_pk FROM assets WHERE asset_tag = '{}';".format(s[0]))
        print("UPDATE asset_at SET arrive_dt = '{}' WHERE asset-fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format('January 10, 2017', i[0]))
        print("UPDATE asset_at SET facility_fk = (SELECT facility_pk FROM facilities WHERE facilities.fcode = 'DC') WHERE asset_at.asset_fk = )SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format(i[0]))
        tag = i[3].split(":")
        level = tag[1]
        compartment = tag[0]

import csv, random, pprint
from datetime import datetime

# remplacement théorique d'une tête d'impression toutes les 1300h d'utilisation (environ 3 mois)
class PrintingJobFeatures():

    MIN = 50

    # printer technical details
    zaxis_speed = 35 # cm/hour
    linear_speed = 300 # mm/sec
    nozzle_size = 1.8 #mm

    # job's product dimension
    height = 0
    width = 0
    depth = 0
    layers = 0
    layers_perimeters = []
    linear_perimeter = 0
    average_zaxis_speed = 0
    material_used = 0
    uv_temperature = 0
    average_speed = 0
    elapsed_time = 0

    def __init__(self):
        # creation des dimensions du produit (height, width, depth, layers)
        self.product_size()
        # creation de la liste des périmètres des layers
        self.set_linear_perimeter_and_speed()
        self.average_zaxis_speed()
        self.set_material_used()
        self.average_uv_temperature()
        self.create_row()


    def product_size(self):
        self.height = random.randint(self.MIN,180) # cm
        self.width = random.randint(self.MIN,145) # cm
        self.depth = random.randint(self.MIN,111) # cm
        self.product_layers()
    
    def product_layers(self):
        self.layers = round((self.height*10)/self.nozzle_size)

    def set_layers_perimeters(self):
        layers_perimeters = []
        for i in range(0, self.layers):
            layer_perimeter = (random.randint(self.MIN, self.width*10)*2)+(random.randint(self.MIN, self.depth*10)*2)
            layers_perimeters.append(layer_perimeter)
        return layers_perimeters

    def set_linear_perimeter_and_speed(self):
        speeds = []
        sum_speed = 0
        layers_perimeters = self.set_layers_perimeters()
        for layer_perimeter in layers_perimeters: 
            self.linear_perimeter += layer_perimeter
            speeds.append(round(layer_perimeter/self.linear_speed)) # mm/sec
            self.elapsed_time += round(layer_perimeter/self.linear_speed)
        for speed in speeds:
            sum_speed += speed
        self.average_speed = sum_speed/len(speeds)
        
    def average_zaxis_speed(self):
        self.average_zaxis_speed = round(self.height/self.average_speed)
            

    def set_material_used(self):
        gr_per_layer = random.randint(1,2) # gr
        self.material_used = self.layers*gr_per_layer

    def average_uv_temperature(self):
        self.uv_temperature = random.randint(70,120) # celsius

    def create_row(self):
        row = {}
        row['index'] = 0
        row['elapsed_time'] = self.elapsed_time
        row['uv_temperature'] = self.uv_temperature
        row['material_used'] = self.material_used
        row['linear_speed'] = self.linear_speed
        row['zaxis_speed'] = self.average_zaxis_speed
        row['perimeter'] = self.linear_perimeter
        row['quality'] = 100
        return row


def create_rows():
    dataset_max_size = 5000
    start = 1600779498

    total_elapsed_time = 0
    total_browsed_perimeter = 0
    total_material_used = 0
    total_uv_exposed = 0

    theorical_time_deprecation = (3000*60*60) # 3000h
    theorical_perimeter_deprecation = 400000
    theorical_material_deprecation = (19*100*1000)
    uv_over_exposed = 1000

    rows = []
    keys = []
    coeff_deprecation = 0.97

    for i in range(1,dataset_max_size+1):
        row = PrintingJobFeatures().create_row()
        row.update({'index':i})

        if i == 1 :
            row['timestamp'] = start
        else :
            row['timestamp'] = start + row['elapsed_time'] + random.randint(3600,7200)
            start = row['timestamp']
        row['datetime'] = datetime.fromtimestamp(row['timestamp'])


        total_elapsed_time += row['elapsed_time']
        total_browsed_perimeter += row['perimeter']
        total_material_used += row['material_used']
        if row['uv_temperature'] >= 100 :
            total_uv_exposed += 1

        if total_elapsed_time >= theorical_time_deprecation or total_browsed_perimeter >= theorical_perimeter_deprecation :
            if total_material_used >= theorical_material_deprecation or total_uv_exposed >= uv_over_exposed :
                print(i, total_elapsed_time, total_browsed_perimeter, total_material_used, total_uv_exposed)
                quality = round(row['quality']*coeff_deprecation) 
                row.update({'quality': quality})
                coeff_deprecation -= 0.05
                if quality <= 60 :
                    total_elapsed_time = 0
                    total_browsed_perimeter = 0
                    total_material_used = 0
                    total_uv_exposed = 0
                    coeff_deprecation = 0.99
        rows.append(row)

        if i == dataset_max_size-1 :
            keys = row.keys()

        #pprint.pprint(rows)
    return keys, rows


def create_csv(filename, columns, rows):
    # open the file in the write mode
    f = open(filename, 'w', encoding='UTF8', newline='')
    # create the csv writer
    writer = csv.DictWriter(f, fieldnames=columns)
    # write a row to the csv file
    writer.writeheader()
    writer.writerows(rows)
    # close the file
    f.close()
    print('csv file "%s" created'% filename)

columns, rows = create_rows()
filename = 'dataset_printhead_quality.csv'
create_csv(filename=filename,columns=columns, rows=rows)

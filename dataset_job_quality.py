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
        gr_per_layer = random.uniform(0.8,2.3) # gr

        layers_perimeters = self.set_layers_perimeters()

        for layer_perimeter in layers_perimeters:
            # sets total perimeter
            self.linear_perimeter += layer_perimeter
            # sets speeds per layer
            speeds.append(round(layer_perimeter/self.linear_speed)) # mm/sec
            # sets total time spent
            deceleration_coeff = random.randint(4,10)/10 # printer head changing axes between 4 and 10 times
            self.elapsed_time += round(layer_perimeter/(self.linear_speed*deceleration_coeff))
        
        # sets total material used
        self.material_used = round(self.linear_perimeter*gr_per_layer)

        for speed in speeds:
            sum_speed += speed
        self.average_speed = sum_speed/len(speeds)
        
    def average_zaxis_speed(self):
        self.average_zaxis_speed = round(self.height/self.average_speed)

    def average_uv_temperature(self):
        self.uv_temperature = random.randint(70,130) # celsius

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
    total_browsed_perimeter = 0
    total_material_used = 0
    total_uv_exposed = 0

    rows = []
    keys = []
    coeff_deprecation = 0.97
    t,p,m = 0,0,0

    for i in range(1,dataset_max_size+1):

        # creation des lignes
        row = PrintingJobFeatures().create_row()
        row.update({'index':i})

        # insertion des valeurs timestamp et datetime
        if i == 1 :
            row['timestamp'] = start
        else :
            row['timestamp'] = start + row['elapsed_time'] + random.randint(3600,7200)
            start = row['timestamp']
        row['datetime'] = datetime.fromtimestamp(row['timestamp'])

        uv_temperature = row['uv_temperature']
        uv_temperature_threshold = 99 # degrees
        if uv_temperature >= uv_temperature_threshold :
            coeff_deprecation = 1-(uv_temperature/1000)
            quality = round(row['quality']*coeff_deprecation) 
            row.update({'quality': quality})
            t += 1
        
        perimeter = row['perimeter']
        perimeter_threshold = ((100*2 + 100*2)*round((100*10)/1.8))*10 # mm
        if perimeter >= perimeter_threshold :
            coeff_deprecation = (perimeter_threshold/perimeter)
            quality = round(row['quality']*coeff_deprecation) 
            row.update({'quality': quality})
            p += 1

        material_used = row['material_used']
        material_used_threshold = perimeter_threshold*2 # gr
        if material_used >= material_used_threshold :
            coeff_deprecation = material_used_threshold/material_used
            quality = round(row['quality']*coeff_deprecation) 
            row.update({'quality': quality})
            m += 1

        rows.append(row)

        if i == dataset_max_size-1 :
            keys = row.keys()

    print(t,p,m)
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
filename = 'dataset_job_quality.csv'
create_csv(filename=filename,columns=columns, rows=rows)

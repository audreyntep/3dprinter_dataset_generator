# 3D Printer Head dataset generator

Run dataset.py to generate a dataset csv file with 6000 rows.

Columns : index, elapsed_time, uv_temperature, material_used, linear_speed, zaxis_speed, perimeter, quality, timestamp, datetime

Starting date can be change by modifying variable line 93 :

- **start** = ***1600779498*** (22/09/2020 - 14:58:18)

Quality is deprecated over time :

- **theorical_time_deprecation** = ***(3000*60*60)*** (seconds)
- **theorical_perimeter_deprecation** = ***400000*** (milimeters)
- **theorical_material_deprecation** = ***(19*100*1000)*** (grammes)
- **uv_over_exposed** = ***1000*** (reached 100 degrees more than 1000 times)

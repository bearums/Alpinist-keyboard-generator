import cadquery as cq
import os
import sys
sys.path.append('../../')
from config import read_config_from_json
from plate import make_plate
from case import make_case, get_distance_between_two_shapes

config_dict = """{
    "name": "square",
    "row_key_numbers": [
        4,
        4,
        4,
        4
    ],
    "columnSpacing": 19,
    "rowSpacing": 19,
    "plateThickness": 2,
    "screwHoleDiamater": 2.4,
    "switchHoleSize": 13.9,
    "shape": 0,
    "notched_keyhole": true,
    "caseHeight": 18,
    "caseGap": 0.6,
    "wallThickness": 2.0,
    "floorThickness": 3.0,
    "edgeFillet": 6,
    "bottomFillet": 2,
    "plateEdgeOffset":-1,
    "controller": {
        "name": "Pi Pico",
        "board_dimension_x": 51.0,
        "board_dimension_y": 21.0,
        "screw_hole_x": 47.0,
        "screw_hole_y": 11.4
    },
    "controllerYOffset": 5,
    "controllerBoxThickness": 2
}"""

config = read_config_from_json(string=config_dict)

def cut_holes_in_top_plate(top):
    top_plate_width = get_distance_between_two_shapes(top.edges('|Y and >Z'))['x']
    led_num=4
    led_spacing = 3.8

    led_posns = [(led_spacing,led_spacing),(-led_spacing,led_spacing), 
                 (led_spacing,-led_spacing), (-led_spacing,-led_spacing)]
    led_hole_dia = 5.15

    #cut holes for LEDs
    for i in range(0,led_num):
        pos = led_posns[i]
        top= (top.faces('>Z').workplane(centerOption="CenterOfBoundBox")
            .moveTo(pos[0], pos[1])
            .circle(0.5*led_hole_dia)
            .cutThruAll()
        )


    return top

def cut_aviator_connector_hole(case):

    aviator_hole_dia = 6.25
    aviator_flat_width = 5.3
    aviator_hole_height =  -1

    case = (case.faces(">Y").workplane(centerOption='CenterOfBoundBox')
                    .center(0,aviator_hole_height)
                    .moveTo(-0.5*aviator_flat_width, -((0.5*aviator_hole_dia)**2 - (0.5*aviator_flat_width)**2)**0.5)
                    .threePointArc((0, -0.5*aviator_hole_dia), (0.5*aviator_flat_width, -((0.5*aviator_hole_dia)**2 - (0.5*aviator_flat_width)**2)**0.5))
                    .lineTo(0.5*aviator_flat_width,((0.5*aviator_hole_dia)**2 - (0.5*aviator_flat_width)**2)**0.5)
                    .threePointArc((0, 0.5*aviator_hole_dia), (-0.5*aviator_flat_width, ((0.5*aviator_hole_dia)**2 - (0.5*aviator_flat_width)**2)**0.5))
                    .close()
                    .cutBlind(until='next')
                    )
    return case 


case = make_case(config,
                 modify_controller_box=cut_holes_in_top_plate,
                 cut_hole_for_connector=cut_aviator_connector_hole)

plate= make_plate(config)
assy = cq.Assembly()
assy.add(case)
assy.add(plate,loc=cq.Location(cq.Vector(0,0,18)) )

file_location = os.path.abspath(os.path.dirname(__file__))


assy.save( os.path.join(file_location, "%s.stl"% config.name))

cq.exporters.export(case, os.path.join(file_location,"%s_case.stl"% config.name))
cq.exporters.export(plate, os.path.join(file_location,"%s_plate.stl"% config.name))



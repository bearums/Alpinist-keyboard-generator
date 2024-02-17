import cadquery as cq
import sys
sys.path.append('../')
from config import read_config_from_json
from plate import make_plate
from case import make_case, get_distance_between_two_shapes

config_dict = """{
    "row_key_numbers": [
        7,
        10,
        10,
        10
    ],
    "columnSpacing": 19,
    "rowSpacing": 19,
    "plateThickness": 2,
    "screwHoleDiamater": 2.4,
    "switchHoleSize": 13.9,
    "shape": 0,
    "notched_keyhole": true,
    "caseHeight": 22,
    "caseGap": 1.0,
    "wallThickness": 1.6,
    "floorThickness": 3.0,
    "edgeFillet": 3,
    "bottomFillet": 2,
    "controller": {
        "name": "Pi Pico",
        "board_dimension_x": 51.0,
        "board_dimension_y": 21.0,
        "screw_hole_x": 47.0,
        "screw_hole_y": 11.1
    },
    "controllerYOffset": 5,
    "controllerBoxThickness": 2,
    "aviatorConnectorHoleDia": 6.25,
    "aviatorConnectorFlatWidth": 5.3
}"""

config = read_config_from_json(string=config_dict)

def cut_holes_in_top_plate(top):
    top_plate_width = get_distance_between_two_shapes(top.edges('|Y and >Z'))['x']
    led_num=3
    led_array_start_x = -6
    led_spacing = 7

    #cut holes for LEDs
    for i in range(0,led_num):
        top= (top.faces('>Z').workplane(centerOption="CenterOfBoundBox")
            .moveTo(led_array_start_x - i*led_spacing,(-0.5))
            .circle(2)
            .cutThruAll()
        )

    # add slot for potentiometer
    circle_dia = 9.1
    flat_width = 8.1
    encoder_hole_centre = (16, -1)
    top = (top.faces('>Z').workplane(centerOption="CenterOfBoundBox")
        .center(encoder_hole_centre[0],encoder_hole_centre[1])
        .moveTo(-0.5*flat_width, ((0.5*circle_dia)**2 - (0.5*flat_width)**2)**0.5)
        .threePointArc((0, 0.5*circle_dia), (0.5*flat_width, ((0.5*circle_dia)**2 - (0.5*flat_width)**2)**0.5))
        .vLine(-10)
        .hLine(-flat_width)
        .vLine(10)
        .wire()
        .cutThruAll()
    )
    return top

case = make_case(config,modify_controller_box=cut_holes_in_top_plate)

#plate= make_plate(config)
#assy = cq.Assembly()
#assy.add(case)
#assy.add(plate,loc=cq.Location(cq.Vector(0,0,18)) )

cq.exporters.export(case, "case.stl")
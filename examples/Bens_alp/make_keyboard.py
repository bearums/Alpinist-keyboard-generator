import cadquery as cq
import os
from factory.config import read_config_from_json
from factory.plate import make_plate
from factory.case import make_case, get_distance_between_two_shapes

config_dict = """{
    "name" : "Alpinist01",
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
    "switchHoleSize": 13.97,
    "notched_keyhole": true,
    "caseHeight": 22,
    "caseGap": 1.0,
    "wallThickness": 1.6,
    "floorThickness": 3.0,
    "edgeFillet": 3,
    "bottomFillet": 1,
    "controller": {
        "name": "Pi Pico",
        "board_dimension_x": 51.0,
        "board_dimension_y": 21.0,
        "screw_hole_x": 47.0,
        "screw_hole_y": 11.4
    },
    "controllerYOffset": 6,
    "controllerBoxThickness": 2
}"""

config = read_config_from_json(string=config_dict)

def cut_holes_in_top_plate(top):
    top_plate_width = get_distance_between_two_shapes(top.edges('|Y and >Z'))['x']
    led_num=3
    led_array_start_x = -6
    led_spacing = 7
    led_hole_dia = 5.15

    #cut holes for LEDs
    for i in range(0,led_num):
        top= (top.faces('>Z').workplane(centerOption="CenterOfBoundBox")
            .moveTo(led_array_start_x - i*led_spacing,(-0.5))
            .circle(0.5*led_hole_dia)
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

def cut_aviator_connector_hole(case):

    aviator_hole_dia = 6.25
    aviator_flat_width = 5.3
    aviator_hole_height =  1

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


# make keyboard case
case = make_case(config,
                 modify_controller_box=cut_holes_in_top_plate,
                 cut_hole_for_connector=cut_aviator_connector_hole)

# make keyboard plate
plate= make_plate(config)


# assemble plate and case
assy = cq.Assembly()
assy.add(case)
assy.add(plate,loc=cq.Location(cq.Vector(0,0,18)) )

# save stls
file_location = os.path.abspath(os.path.dirname(__file__))
assy.save( os.path.join(file_location, "%s.stl"% config.name))
cq.exporters.export(case, os.path.join(file_location,"%s_case.stl"% config.name))
cq.exporters.export(plate, os.path.join(file_location,"%s_plate.stl"% config.name))

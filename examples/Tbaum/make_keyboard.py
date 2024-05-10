import cadquery as cq
import os
from factory.config import read_config_from_json
from factory.plate import make_plate
from factory.case import make_case, get_distance_between_two_shapes


config_dict = """{
    "name": "Tbaum",
    "row_key_numbers": [
    2,
    8,
    6,
    3,
    1
    ],
    "columnSpacing": 19,
    "rowSpacing": 19,
    "plateThickness": 2,
    "screwHoleDiamater": 2.4,
    "switchHoleSize": 13.97,
    "notched_keyhole": true,
    "caseHeight": 20,
    "caseGap": 0.6,
    "wallThickness": 1.6,
    "floorThickness": 3.0,
    "edgeFillet": 2,
    "bottomFillet": 0,
    "controller": "None",
    "controllerYOffset": 5,
    "controllerBoxThickness": 2
}"""

config = read_config_from_json(string=config_dict)



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
                 modify_controller_box=None,
                 cut_hole_for_connector=cut_aviator_connector_hole)

# make keyboard plate
plate= make_plate(config)

# assemble plate and case
assy = cq.Assembly()
assy.add(case)
assy.add(plate,loc=cq.Location(cq.Vector(0,0,16)) )

# save stls
file_location = os.path.abspath(os.path.dirname(__file__))
assy.save( os.path.join(file_location, "%s.stl"% config.name))
cq.exporters.export(case, os.path.join(file_location,"%s_case.stl"% config.name))
cq.exporters.export(plate, os.path.join(file_location,"%s_plate.stl"% config.name))




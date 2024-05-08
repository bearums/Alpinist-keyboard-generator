import sys
sys.path.append('../factory')
#from config import read_config_from_json
#from plate import make_plate
#from case import make_case
import cadquery as cq
import os
from config import read_config_from_json


def make_kb(config_dict: str,
                  modify_controller_box: callable,
                  cut_hole_for_connector: callable):
    config = read_config_from_json(string=config_dict)

    case = make_case(config,
                 modify_controller_box=modify_controller_box,
                 cut_hole_for_connector=cut_hole_for_connector)

    plate= make_plate(config)
    assy = cq.Assembly()
    assy.add(case)
    assy.add(plate,loc=cq.Location(cq.Vector(0,0,18)) )

    file_location = os.path.abspath(os.path.dirname(__file__))


    assy.save( os.path.join(file_location, "%s.stl"% config.name))

    cq.exporters.export(case, os.path.join(file_location,"%s_case.stl"% config.name))
    cq.exporters.export(plate, os.path.join(file_location,"%s_plate.stl"% config.name))

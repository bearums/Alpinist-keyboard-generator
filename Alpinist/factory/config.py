import json
from controller import Controller, ControllerFromDict
from controller import AdafruitFeathernRF52840Express



class Config:
    row_key_numbers: list 
    "number of keys on each row. Eg. [4,4] is for a keyboard with 2 rows each with 4 keys"
    columnSpacing: float
    "center to center spacing between key columns in mm"
    rowSpacing: float
    "center to center spacing between key rows in mm"
    switchHoleSize: float
    "size of the switch hole in mm"
    plateThickness: float
    "thickness of the switch plate in mm"
    screwHoleDiameter: float
    "size of screws to fix switch plate to case in mm"
    notched_keyhole: bool
    "option for notched keyhole"
    plateEdgeOffset: float
    "amount in mm to remove from plate edge. Prevents a large gap between the case and keys on the perimeter"
    
        
    caseHeight: float 
    "case height in mm"
    caseGap: float
    "size difference between the case and the switch plate in mm"
    wallThickness: float
    "thickness of case sidewalls in mm"
    floorThickness: float
    "bottom thickness of case in mm"
    edgeFillet: float
    "fillet radius in mm of case edge"
    bottomFillet: float
    "fillet radius in mm of case bottom"
        
    controller : Controller
    "micro controller to use"
    controllerYOffset : float
    "amount to offset microcontroller screwholes in y direction in mm"
    controllerBoxThickness : float
    "thichness of controller box top in mm"


        
    def __init__(self, row_key_numbers, 
                 name = None,
                 columnSpacing = 19, rowSpacing = 19, 
                 switchHoleSize = 14.0,
                 plateThickness = 1.8,
                 screwHoleDiamater = 2.4,
                 notched_keyhole = True,
                 plateEdgeOffset = -2.0,
                 
                 caseHeight = 22,
                 caseGap = 0.5,
                 wallThickness = 1.6,
                 floorThickness = 3.0,
                 edgeFillet = 4,
                 bottomFillet = 2,
                 
                 controller = AdafruitFeathernRF52840Express(),
                 controllerYOffset = 3,
                 controllerBoxThickness = 2,

                 
                 
                ):
        self.row_key_numbers = row_key_numbers
        self.name = name
        self.columnSpacing = columnSpacing
        self.rowSpacing = rowSpacing
        self.plateThickness = plateThickness
        self.screwHoleDiamater = screwHoleDiamater
        self.switchHoleSize = switchHoleSize
        self.notched_keyhole = notched_keyhole
        self.plateEdgeOffset = plateEdgeOffset
        
        self.caseHeight = caseHeight
        self.caseGap = caseGap
        self.wallThickness = wallThickness
        self.floorThickness = floorThickness
        self.edgeFillet = edgeFillet
        self.bottomFillet = bottomFillet
        
        self.controller = controller  
        self.controllerYOffset = controllerYOffset
        self.controllerBoxThickness = controllerBoxThickness

        

    def to_json(self, file):
        dict_to_write = self.__dict__.copy()
        if self.controller is not None:
            dict_to_write['controller'] = self.controller.as_dict()
        else:
             dict_to_write['controller'] = 'None'
        with open(file, 'w') as f:
            json.dump(dict_to_write, f, indent=4 )
    

def read_config_from_json( **kwargs):
        if 'string' in kwargs.keys():
            dict = json.loads(kwargs['string'])
        else:
            with open(kwargs['file'], 'r') as f:
                dict= json.load(f)

        if dict['controller'] == 'None':
            dict['controller'] = None
        else:
            dict['controller']  = ControllerFromDict(dict['controller'] )
        return Config(**dict)


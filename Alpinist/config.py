from enum import IntEnum
from controller import Controller
from controller import AdafruitFeathernRF52840Express

class Shape(IntEnum):
    LEAN = 0
    HULL = 1
    
class Config:
    nrows : int
    row_key_num: list
    columnSpacing: float
    rowSpacing: float
    switchHoleSize: float
    plateThickness: float
    shape: Shape
    screwHoleDiameter: float
    notched_keyhole: bool
    plateFillet: float
        
    caseHeight: float
    caseGap: float
    wallThickness: float
    floorThickness: float
    edgeFillet: float
    bottomFillet: float
        
    controller : Controller
    controllerYOffset : float
    controllerBoxThickness : float

    aviatorConnectorHoleDia : float
    aviatorConnectorFlatWidth : float
        
    def __init__(self, row_key_num, 
                 cs = 19, rs = 19, 
                 switchHoleSize = 13.9,
                 plateThickness = 2,
                 shape = Shape.LEAN,
                 screwHoleDiamater = 2.4,
                 notched_keyhole = True,
                 plateFillet = 2.5,
                 
                 caseHeight = 22,
                 caseGap = 1.5,
                 wallThickness = 1.6,
                 floorThickness = 3.0,
                 edgeFillet = 4,
                 bottomFillet = 2,
                 
                 controller = AdafruitFeathernRF52840Express(),
                 controllerYOffset = 5,
                 controllerBoxThickness = 2,

                 aviatorConnectorHoleDia = 6.25,
                 aviatorConnectorFlatWidth = 5.3,
                 
                ):
        self.nrows = len(row_key_num)
        self.row_key_num = row_key_num
        self.columnSpacing = cs
        self.rowSpacing = rs
        self.plateThickness = plateThickness
        self.screwHoleDiamater = screwHoleDiamater
        self.angle = 0
        self.hOffset = 0
        self.switchHoleSize = switchHoleSize
        self.shape = shape
        self.notched_keyhole = notched_keyhole
        self.plateFillet = plateFillet
        
        self.caseHeight = caseHeight
        self.caseGap = caseGap
        self.wallThickness = wallThickness
        self.floorThickness = floorThickness
        self.edgeFillet = edgeFillet
        self.bottomFillet = bottomFillet
        
        self.controller = controller  
        self.controllerYOffset = controllerYOffset
        self.controllerBoxThickness = controllerBoxThickness

        self.aviatorConnectorHoleDia = aviatorConnectorHoleDia
        self.aviatorConnectorFlatWidth = aviatorConnectorFlatWidth
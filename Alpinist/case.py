import cadquery as cq
from enum import IntEnum

from plate import Config, Shape
from plate import make_plate, get_key_positions
def make_case(config:Config) -> cq.Sketch:
    """TODO: make separate floor thickness
            change fillet parameters
            add module for leds, encoder and aviator
            add screw holes"""
    
    # remove hard coding and put into Config!
    controllerBoxLength = 20
    controllerBoxWidth=80

    x_centre = 0.5*(min([x[0] for x in list(kp.values())])+ max([x[0] for x in list(kp.values())]))
    
    foot_x, foot_y = (config.columnSpacing / 2 + config.switchHoleSize, config.rowSpacing / 2 +
                          config.switchHoleSize) if config.shape == Shape.LEAN else (config.switchHoleSize, config.switchHoleSize)
    case = cq.Sketch()

    kp = get_key_positions(config)
    
    case = case.push(list(kp.values())+[(x_centre+20,80) ,(x_centre-20,80), (x_centre,80)])
    
    
    case = (case.rect(foot_x+(config.caseGap+wall_thickness)*2, foot_y+(config.caseGap+wall_thickness)*2)
            .faces()
            .clean()
            .offset(config.wallThickness)
            .clean())
    
    case= (cq.Workplane()
           .placeSketch(case)
           .extrude(config.caseHeight))
    
    case = (case
            .edges('>Y and <Z')
            .workplane(centerOption="CenterOfBoundBox")
            .box(controllerBoxWidth,controllerBoxLength, config.caseHeight, centered=[True,False,False])
           )

    case= (case.faces("+Z")
           .shell(-wall_thickness)
           .edges("|Z")
           .fillet(3))
    return case




if __name__ =="__main__":
    from cadquery import exporters
    
    nrows = 2
    rkn = [1,2]
    switchHoleSize= 13.9
    config=Config( rkn, shape=Shape.LEAN, 
                  caseHeight=3, plateThickness=1,  
              cs= switchHoleSize+3.4505, rs= switchHoleSize+5.508,
             switchHoleSize= switchHoleSize,
                 caseGap=1.0,
                 wallThickness=1.2,)
    pl = make_plate(config, holes=False)
    case = make_case(config)
    
    exporters.export(pl, 'plate.stl', tolerance=0.001, angularTolerance=0.05)
    exporters.export(case, 'case.stl', tolerance=0.001, angularTolerance=0.05)

    

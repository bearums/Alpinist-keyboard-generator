import cadquery as cq
from enum import IntEnum

from plate import Config, Shape
from plate import make_plate, get_key_positions, get_screw_positions

def get_basic_shape(config:Config) -> cq.Sketch:

    kp = get_key_positions(config)

    foot_x, foot_y = (config.columnSpacing / 2 + config.switchHoleSize, config.rowSpacing / 2 +
                            config.switchHoleSize) if config.shape == Shape.LEAN else (config.switchHoleSize, config.switchHoleSize)

        
    plate_recess = cq.Sketch()
    plate_recess = plate_recess.push(list(kp.values()))
    plate_recess = (plate_recess.rect(foot_x+(config.caseGap+config.wallThickness)*2, 
                      foot_y+(config.caseGap+config.wallThickness)*2)
                    .faces()
                    .clean()
                    .offset(config.wallThickness)
                    .clean())
            
        
    basic_shape= (cq.Workplane()
           .placeSketch(plate_recess)
           .extrude(config.caseHeight))
    return basic_shape

def make_case(config:Config) -> cq.Sketch:
    """TODO: add screw holes for microcontroller (check they are in right position!!)
            change fillet parameters
            add module for leds, encoder and aviator
            """
    
    # remove hard coding and put into Config!
    controller_y_offset = 5
    controllerBoxLength = config.controller.board_dimension_y - controller_y_offset
    controllerBoxWidth=config.controller.board_dimension_x + 5
        
    
    case= get_basic_shape(config)
    case.faces('<Z').tag('bottomface')

    # add box for microcontroller
    case = (case
             .edges('>Y and <Z')
             .workplane(centerOption="CenterOfBoundBox", invert=False)
             .box(controllerBoxWidth,controllerBoxLength, config.caseHeight, centered=[True,False,False],combine=False)
             .faces('<Z')
            .workplane(centerOption="CenterOfBoundBox")
            .tag("controllerBox")
            .union(case)
            )
    

    #fillet edges
    case = case.edges('|Z').fillet(3)

    case.edges('>Z').tag('outerTopEdge')


    # scoop out interior
    case= (case.faces(">Z")
            .shell(-config.wallThickness, kind='intersection')
            )
    
    # set floor thickness 
    btm = case.faces('<Z[1]').clean().wires().toPending()
    case_without_btm=(btm.extrude(config.wallThickness, combine="cut"))
    new_btm = case.faces('<Z[1]').clean().wires().toPending().extrude(-config.floorThickness, combine=False).translate([0,0,-config.wallThickness])
    case = case_without_btm.union(new_btm)
    
    #fillet bottom edge
    case = case.edges('<Z').fillet(3)

    # add plate screw holes 
    scr_hls = get_screw_positions(config)
    case=(case.faces('<Z').workplane(origin=(0,0))
          .pushPoints([(x,-y) for x,y in scr_hls])
          .cskHole(2.4, 4.8, 82, depth=None)    
          )

    # add controllerbox holes.
    # TODO - remove hardcoding on screw hole size
    case = (case.workplaneFromTagged("controllerBox")
            .rect(config.controller.screw_hole_x,
                   config.controller.screw_hole_y- config.wallThickness - controller_y_offset - (config.controller.board_dimension_y -config.controller.screw_hole_y)*0.5, 
                   forConstruction=True ,centered=[True,True,True])
            .vertices()
            .cskHole(2.4, 4.8, 82, depth=None))
    
    
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

    

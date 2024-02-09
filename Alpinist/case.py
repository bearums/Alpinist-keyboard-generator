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

def add_microcontrollerbox_(case, config):
    # remove hard coding and put into Config!
        controller_y_offset = 5
        controllerBoxLength = config.controller.board_dimension_y - controller_y_offset
        controllerBoxWidth=config.controller.board_dimension_x + 5
        
        case = (case
                .edges('>Y and <Z')
                .workplane(centerOption="CenterOfBoundBox", invert=False)
                .box(controllerBoxWidth,controllerBoxLength, config.caseHeight, centered=[True,False,False],combine=False)
                .faces('<Z')
                .workplane(centerOption="CenterOfBoundBox")
                .tag("controllerBox")
                #.faces('>Z').workplane(centerOption="CenterOfBoundBox").tag("controllerBoxTop")
                .union(case)
                )
        return case 
def add_microcontrollerbox(case, config):
        controller_y_offset = 5
        controllerBoxLength = config.controller.board_dimension_y - controller_y_offset
        controllerBoxWidth=config.controller.board_dimension_x + 5
        
        ctrBox = (case
                .edges('>Y and <Z')
                .workplane(centerOption="CenterOfBoundBox", invert=False)
                .box(controllerBoxWidth,controllerBoxLength, config.caseHeight, centered=[True,False,False],combine=False)
                )
        ctrBox.faces('<Z').tag("controllerBox")
        ctrBox.faces('>Z').tag("controllerBoxTop")

        case = case.union(ctrBox)
        return case

def make_controller_box_top_plate(case):

    controllerBoxLength =  get_distance_between_two_vertices(case.faces(tag='controllerBoxTop').vertices('<X'))['y']
    controllerBoxWidth = get_distance_between_two_vertices(case.faces(tag='controllerBoxTop').vertices('<Y'))['x']

    controller_box_top = (case
                        .faces(tag='controllerBoxTop')
                        .workplane(centerOption="CenterOfBoundBox", invert=True)
                        .move(0,config.wallThickness)
                        .box(controllerBoxWidth,controllerBoxLength, config.controllerBoxThickness, centered=[True,True,False],combine=False)
    )


    return controller_box_top

def cut_aviator_connector_hole(case, config):

    aviator_hole_dia = config.aviatorConnectorHoleDia
    aviator_flat_width = config.aviatorConnectorFlatWidth
    aviator_hole_height =  1

    case = (case.faces(">Y").workplane(centerOption='CenterOfBoundBox')
                    .center(0,aviator_hole_height)
                    .moveTo(-0.5*aviator_flat_width, -((0.5*aviator_hole_dia)**2 - (0.5*aviator_flat_width)**2)**0.5)
                    .threePointArc((0, -0.5*aviator_hole_dia), (0.5*aviator_flat_width, -((0.5*aviator_hole_dia)**2 - (0.5*aviator_flat_width)**2)**0.5))
                    .lineTo(0.5*aviator_flat_width,((0.5*aviator_hole_dia)**2 - (0.5*aviator_flat_width)**2)**0.5)
                    .threePointArc((0, 0.5*aviator_hole_dia), (-0.5*aviator_flat_width, ((0.5*aviator_hole_dia)**2 - (0.5*aviator_flat_width)**2)**0.5))
                    .close().cutBlind(until='next')
                    )
    return case 

def make_case(config:Config) -> cq.Sketch:
    """TODO: add screw holes for microcontroller (check they are in right position!!)
            change fillet parameters
            add module for leds, encoder and aviator
            """
    
    
    case= get_basic_shape(config)
    #case.faces('<Z').tag('bottomface')

    # add box for microcontroller
    if config.controller is not None:
        case = add_microcontrollerbox(case, config)
    

    #fillet edges
    case = case.edges('|Z').fillet(config.edgeFillet)
    #case.edges('>Z').tag('outerTopEdge')


    # scoop out interior
    case= (case.faces(">Z or <Z").shell(-config.wallThickness, kind='intersection'))
    
    # set floor thickness 
    case = case.faces('<Z').wires('>X and >Y').toPending().extrude(config.floorThickness)
    
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
    if config.controller is not None:
        case = (case.workplaneFromTagged("controllerBox")
                .rect(config.controller.screw_hole_x,
                        config.controller.screw_hole_y- config.wallThickness - controller_y_offset - (config.controller.board_dimension_y -config.controller.screw_hole_y)*0.5, 
                        forConstruction=True ,centered=[True,True,True])
                .vertices()
                .cskHole(2.4, 4.8, 82, depth=None))
    
    #cut hole for aviator connector 
    case = cut_aviator_connector_hole(case, config)

    return case

def get_distance_between_two_vertices(vertices):
    """calculates distances in each axis between two vertices:
    eg: get_distance_between_two_vertices(OBJECT.vertices('<Y'))"""
    assert len(vertices.vals())==2, "Must have only 2 vertices! %s, vertices selected"%(len(vertices.vals()))

    vals = [x.Center().toTuple() for x in vertices.vals()]
    distance = {'x': abs(vals[0][0]- vals[1][0]),
                'y': abs(vals[0][1]- vals[1][1]),
                'z': abs(vals[0][2]- vals[1][2])}
    return distance


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

    

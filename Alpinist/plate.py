import cadquery as cq
from config import Config, Shape


def get_keys(kp, key_shape, config):
    return cq.Workplane().pushPoints(kp.values()).placeSketch(key_shape).extrude(config.plateThickness)



def get_key_hole_shape(config) -> cq.Sketch:
    switchHoleSize = config.switchHoleSize
    if config.notched_keyhole:
        return cq.Sketch().rect(switchHoleSize, switchHoleSize)\
            .push([(0, 4.2545), (0, -4.2545)]).rect(switchHoleSize + 2 * 0.8128, 3.5001).clean()
    else:
        return cq.Sketch().rect(switchHoleSize, switchHoleSize)




def get_key_positions(config: Config) -> [(float, float)]:
    kp={}
    x_centre = max(config.row_key_numbers)* config.rowSpacing*0.5
    for col_num, row_size in enumerate((config.row_key_numbers)):
        centre = row_size* config.rowSpacing*0.5

        if centre != x_centre:
            x_trans = x_centre - centre
        else:
            x_trans = 0
       
        for row_num in range(row_size):
            kp[(col_num, row_num)] = (config.rowSpacing*row_num+x_trans,
                                        config.columnSpacing*col_num)


    return kp     



def get_base(config: Config, kp, thickness,base_fillet, window=False):

    foot_x, foot_y = (config.columnSpacing / 2 + config.switchHoleSize, config.rowSpacing / 2 +
                      config.switchHoleSize) if config.shape == Shape.LEAN else (config.switchHoleSize, config.switchHoleSize)
    base = cq.Sketch()
   

    base = base.push(kp.values())
    if config.shape == Shape.LEAN:
        base = base.rect(foot_x, foot_y)\
            .faces().clean().vertices().fillet(base_fillet).faces()\
            .wires().offset(0).clean()
    elif config.shape == Shape.HULL:
        base = base.rect(foot_x, foot_y)\
            .faces().hull().clean().wires().offset(12)

    base = cq.Workplane().placeSketch(base).extrude(thickness)


    if window:
        win = cq.Sketch().push(kp.values()).rect(config.columnSpacing / 2 +
                                                 config.switchHoleSize, config.rowSpacing / 2 + config.switchHoleSize)
        win = win.clean().faces().vertices().fillet(1)
        win = cq.Workplane().placeSketch(win).extrude(thickness).rotate((0, 0, 0), (0, 0, 1), config.angle).translate(
            (config.hOffset, 0))
        #if not config.split:
        win = win.mirror('YZ', union=True)
        base = base.cut(win)

    return base

def get_screw_positions(config: Config) -> [(float, float)]:
    sp=[]
    x_centre = max(config.row_key_numbers)* config.rowSpacing*0.5
    row_holes = config.row_key_numbers
    nrows = len(config.row_key_numbers)
    for col_num in range(0,nrows,1):    
        row_size = row_holes[col_num]
        centre = row_size* config.rowSpacing*0.5

        if centre != x_centre:
            x_trans = x_centre - centre
        else:
            x_trans = 0
            
        if row_size%2 ==0: #for rows with even key numbers
            for row_num in range(1,row_size, 2):
                hole_x_pos = config.rowSpacing*row_num+x_trans-0.5*config.rowSpacing
                hole_y_pos = config.columnSpacing*col_num+0.0*config.columnSpacing
                sp.append((hole_x_pos, hole_y_pos))
                
        else: # for rows with odd key numbers
            for row_num in range(1,row_size, 2):
                hole_x_pos = config.rowSpacing*row_num+x_trans-0.5*config.rowSpacing
                hole_y_pos = config.columnSpacing*col_num+0.0*config.columnSpacing
                sp.append((hole_x_pos, hole_y_pos))
    return sp

def make_plate(config:Config, 
               get_screw_hole_positions:callable=get_screw_positions) -> cq.Sketch:
    key_hole_shape = get_key_hole_shape(config)
    kp = get_key_positions(config)
    plate = get_base(config, kp, thickness=config.plateThickness, base_fillet=config.edgeFillet, window=False).cut(get_keys(kp, key_hole_shape, config))
    
    
    hole_psns= get_screw_hole_positions(config)
    plate= plate.faces(">Z").workplane().pushPoints(hole_psns).hole(config.screwHoleDiamater)
    return plate



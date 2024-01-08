import cadquery as cq
from enum import IntEnum
 
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
    def __init__(self, row_key_num, 
                 cs=19, rs=19, 
                 switchHoleSize=13.9,
                 plateThickness = 2,
                 shape=Shape.LEAN,
                 screwHoleDiamater= 2.4,
                 notched_keyhole=True,
                 plateFillet=2.5,
                 
                 caseHeight=22,
                 caseGap=1.5,
                 wallThickness=1.6,
                ):
        self.nrows = len(row_key_num)
        self.row_key_num = row_key_num
        self.columnSpacing = cs
        self.rowSpacing = rs
        self.plateThickness = plateThickness
        self.screwHoleDiamater = screwHoleDiamater
        self.angle = 0
        self.hOffset=0
        self.switchHoleSize = switchHoleSize
        self.shape = shape
        self.notched_keyhole = notched_keyhole
        self.plateFillet = plateFillet
        
        self.caseHeight = caseHeight
        self.caseGap = caseGap
        self.wallThickness = wallThickness
        
        


def get_keys(kp, key_shape, config):
    return cq.Workplane().pushPoints(kp.values()).placeSketch(key_shape).extrude(config.plateThickness)\
        .rotate((0, 0, 0), (0, 0, 1), config.angle).translate(
        (config.hOffset, 0))



def get_key_hole_shape(config) -> cq.Sketch:
    switchHoleSize = config.switchHoleSize
    if config.notched_keyhole:
        return cq.Sketch().rect(switchHoleSize, switchHoleSize)\
            .push([(0, 4.2545), (0, -4.2545)]).rect(switchHoleSize + 2 * 0.8128, 3.5001).clean()
    else:
        return cq.Sketch().rect(switchHoleSize, switchHoleSize)




def get_key_positions(config: Config) -> [(float, float)]:
    kp={}
    x_centre = max(config.row_key_num)* config.rowSpacing*0.5
    for col_num, row_size in enumerate(reversed(config.row_key_num)):
        centre = row_size* config.rowSpacing*0.5

        if centre != x_centre:
            x_trans = x_centre - centre
        else:
            x_trans = 0
       
        for row_num in range(row_size):
            kp[(col_num, row_num)] = (config.rowSpacing*row_num+x_trans,
                                        config.columnSpacing*col_num)


    return kp     

def get_screw_positions(config: Config) -> [(float, float)]:
    sp=[]
    x_centre = max(config.row_key_num)* config.rowSpacing*0.5
    row_holes = list(reversed( [config.row_key_num[0]]+ config.row_key_num)) 
    for col_num in range(0, config.nrows+1,2):    
        row_size = row_holes[col_num]
        centre = row_size* config.rowSpacing*0.5

        if centre != x_centre:
            x_trans = x_centre - centre
        else:
            x_trans = 0
            
        if row_size%2 ==0: #for rows with even key numbers
            for row_num in range(1,row_size+1, 2):
                sp.append((config.rowSpacing*row_num+x_trans-0.5*config.rowSpacing,
                       config.columnSpacing*col_num-0.5*config.columnSpacing))

        else: # for rows with odd key numbers
            for row_num in range(0,row_size, 2):
                sp.append((config.rowSpacing*row_num+x_trans-0.0*config.rowSpacing,
                       config.columnSpacing*col_num-0.5*config.columnSpacing))
        
        
    return sp

def get_base(config: Config, kp, thickness,base_fillet=2.5, window=False):

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

def make_plate(config:Config, holes=True) -> cq.Sketch:
    key_hole_shape = get_key_hole_shape(config)
    kp = get_key_positions(config)
    plate = get_base(config, kp, thickness=config.plateThickness, base_fillet=config.plateFillet, window=False).cut(get_keys(kp, key_hole_shape, config))
    hole_psns= get_screw_positions(config)
    if holes:
        plate= plate.faces(">Z").workplane().pushPoints(hole_psns).hole(config.screwHoleDiamater)
    return plate


if __name__ =="__main__":
    from cadquery import exporters

    nrows = 5
    rkn = [1,3,5,2,3]

    cc=Config(nrows, rkn, shape=Shape.LEAN)
    pl = make_plate(cc)
    exporters.export(pl, 'plate.stl', tolerance=0.001, angularTolerance=0.05)
    

#ncols = 4
#rkn = [7,7,7,6]

#cc=Config(ncols, rkn)
#kp = get_key_positions(cc)
#get_keys(kp, key_hole_shape, cc)


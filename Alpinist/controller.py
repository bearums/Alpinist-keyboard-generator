from abc import ABC, abstractmethod

class Controller(ABC):
    
    @property
    @abstractmethod
    def screw_hole_x(self):
        pass
    
    @property
    @abstractmethod
    def screw_hole_y(self):
        pass
    
    @property
    @abstractmethod
    def board_dimension_x(self):
        pass
    
    @property
    @abstractmethod
    def board_dimension_y(self):
        pass

    
    
    def as_dict(self):
        info_dict = {"name": self.name,
                     "board_dimension_x": self.board_dimension_x,
                     "board_dimension_y": self.board_dimension_y,
                     "screw_hole_x": self.screw_hole_x,
                     "screw_hole_y": self.screw_hole_y}
        return info_dict


    
    def __repr__(self):
        info_dict = self.as_dict()
        return str(info_dict)
    
def load_controller_from_dict( dict):
        name = dict['name']
        screw_hole_x = dict['screw_hole_x']
        screw_hole_y = dict['screw_hole_y']
        
        return Controller(**dict)
class PiPico(Controller):
    name = "Pi Pico"

    screw_hole_x = 47.0
    screw_hole_y = 11.1
    
    board_dimension_x = 51.0
    board_dimension_y = 21.0
    
    
class AdafruitFeathernRF52840Express(Controller):
    name = "AdafruitFeathernRF52840Express"

    screw_hole_x = 45.72
    screw_hole_y = 17.78
    
    board_dimension_x = 51.0
    board_dimension_y = 23.0

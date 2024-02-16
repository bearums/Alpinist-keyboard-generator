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

    
    
    def __repr__(self):
        info_dict = {"board_dimension_x": self.board_dimension_x,
                     "board_dimension_y": self.board_dimension_y,
                        "screw_hole_x": self.screw_hole_x,
                     "screw_hole_y": self.screw_hole_y}
        return str(info_dict)
    
class PiPico(Controller):
    
    screw_hole_x = 47.0
    screw_hole_y = 11.1
    
    board_dimension_x = 51.0
    board_dimension_y = 21.0
    
    
class AdafruitFeathernRF52840Express(Controller):
    screw_hole_x = 45.72
    screw_hole_y = 17.78
    
    board_dimension_x = 51.0
    board_dimension_y = 23.0

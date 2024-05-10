from abc import ABC, abstractmethod
from dataclasses import dataclass

class Controller(ABC):
    
    @property
    @abstractmethod
    def screw_hole_x(self):
        """distance in mm between screw holes on long side of the board"""
        pass
    
    @property
    @abstractmethod
    def screw_hole_y(self):
        """distance in mm between screw holes on short side of the board"""
        pass
    
    @property
    @abstractmethod
    def board_dimension_x(self):
        """length of long side of board in mm"""
        pass
    
    @property
    @abstractmethod
    def board_dimension_y(self):
        """length of short side of board in mm"""

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
    



@dataclass
class ControllerFromDict(Controller):
    
    dict : dict 
    board_dimension_x: float = None
    board_dimension_y : float = None
    screw_hole_x : float = None
    screw_hole_y : float = None
    
    def __post_init__(self):
        self.name : str =  self.dict['name']
        self.board_dimension_x: float = self.dict['board_dimension_x']
        self.board_dimension_y: float = self.dict['board_dimension_y']
        self.screw_hole_x: float = self.dict['screw_hole_x']
        self.screw_hole_y: float = self.dict['screw_hole_y']



class PiPico(Controller):
    name = "Pi Pico"

    screw_hole_x = 47.0
    screw_hole_y = 11.4
    
    board_dimension_x = 51.0
    board_dimension_y = 21.0
    
    
class AdafruitFeathernRF52840Express(Controller):
    name = "AdafruitFeathernRF52840Express"

    screw_hole_x = 45.72
    screw_hole_y = 17.78
    
    board_dimension_x = 51.0
    board_dimension_y = 23.0

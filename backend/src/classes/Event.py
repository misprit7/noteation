from typing import List

class Event(): 
    
    def __init__(self, event: dict = {}): 
        self.event = [(property, value) for property, value in event.items()]
        self.event.sort(key=lambda x: x[0])
    
    def get_properties(self) -> List[str]:
        return [prop for prop, val in self.event]
    
    def get_values(self) -> List[str]: 
        return [str(val) for prop, val in self.event]
        
        
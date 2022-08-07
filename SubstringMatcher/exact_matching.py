from .approach import Approach

 
class ExactMatcher(Approach):
    def __init__(self, text: list, query_text: str, threshold: int) -> None:
        super().__init__(text, query_text, threshold)
        
        
    def match(self, get_span = False, sort = True):
        result = [i.find(self.query_text) for i in self.text]
        self.verdicts  = [i>=0 for i in result]
        self.similarity_scores = [int(i)*100 for i in self.verdicts]
        self.error_scores = [100 - i for i in self.similarity_scores]
        
        if get_span:
            self.spans =  [ [i, i+len(self.query_text)] if i!=-1 else [-1,-1] for i in result]
            
        
        self._format_output()        
        if sort: 
            self.sort()
            
        
        
    

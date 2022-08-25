from .approach import Approach
 
class ExactMatcher(Approach):
    def __init__(self, text: list, query_text: str, threshold: int= None) -> None:
        super().__init__(text, query_text, threshold)
        
        
    def match(self, topK = None, get_span = False, sort = True):
        """performs query text matching against given searchable text list and return a list of matches

        Args:
            topK (int, optional): to return topK matches. Defaults to None.
            get_span (bool, optional): to return match spam. Defaults to False.
            sort (bool, optional): to return sorted matches. Defaults to True.

        Returns:
            list[namedtuple]: a list of namedtuple('output',['text','verdict', 'similarity', 'error', 'span'])
        """
        
        result = [i.find(self.query_text) for i in self.text]
        self.verdicts  = [i>=0 for i in result]
        self.similarity_scores = [int(i)*100 for i in self.verdicts]
        self.error_scores = [100 - i for i in self.similarity_scores]
        
        if get_span:
            self.spans =  [ [i, i+len(self.query_text)] if i!=-1 else [-1,-1] for i in result]
            
            
        self._format_output() 
        if topK:
            self.sort()
            self._get_topK(topK)
            
        else:
            if sort: self.sort()
            
        return self.outputs
        
    def _get_topK(self, topK):
        data = list(zip(self.text, self.verdicts, self.similarity_scores, self.spans, self.error_scores))
        data = data[:min(topK,len(data))]
        self.text, self.verdicts, self.similarity_scores, self.spans, self.error_scores = list(zip(*data))
        self.outputs = self.outputs[:min(topK, len(self.outputs))]
        
        
    

from fuzzywuzzy import fuzz, process
from difflib import SequenceMatcher
from collections import namedtuple
import numpy as np


class Approach:
    def __init__(self, text : list, query_text: str, threshold: int = None) -> None:
        """Initialize Matcher Class

        Args:
            text (list): A List text to be searched
            query_text (str): A query text
            threshold (int): character-level error threshold 
        """
        
        self.text = text if isinstance(text, list) else [text]
        self.query_text = query_text
        self.threshold = round((len(self.query_text ))**.75 - len(self.query_text)**.4) \
                              if threshold is None else threshold
        self.validity_check()
        self.similarity_scores = [-1]*len(self.text)
        self.error_scores = [-1]*len(self.text)
        self.spans = [[-1,-1]]*len(self.text)
        self.verdicts = [False]*len(self.text)
        self.output_format = namedtuple('output',['text','verdict', 'similarity', 'error', 'span'])
 
    def validity_check(self):
        assert len(self.text)>0, f"Text list must not be empty (-_-)\n"
        assert any(len(t)!=0 for t in self.text), f"Text should not be a empty string (-_-)\n"
        assert len(self.query_text)> 0, f"Query text must not be a empty string (-_-)\n"
        
        if any(len(t)<len(self.query_text) for t in self.text):
            print('Some Texts are smaller than query text; may yield undesirable results [-_-]')
        
    
    def match(self):
        pass
            
    def _format_output(self):
        self.outputs = [self.output_format(*op_) for op_ in zip(self.text, self.verdicts, 
                                                                self.similarity_scores, 
                                                                self.error_scores, self.spans)]
    @staticmethod   
    def _ratio(text_a, text_b):
        la = len(text_a)
        lb = len(text_b)
        return max(la/lb, lb/la)
        
    
    def sort(self):
        self.outputs = sorted(self.outputs, key = lambda x: \
            (x.similarity, - self._ratio(x.text, self.query_text)), reverse= True)
        
    
    def __getitem__(self, indices):
        if isinstance(indices, tuple):
            if not( (-1<indices[0]<len(self.outputs))  
                   or (-1<indices[1]<len(self.outputs)) 
                   or (indices[1]<indices[0])):
                raise "IndexError"
            return self.outputs[indices[0]:indices[1]]
        if isinstance(indices, int):
            if not (-1< indices<len(self.outputs)):
                raise "IndexError"
            else: return self.outputs[indices]
     
        
    
        
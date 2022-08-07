from fuzzywuzzy import fuzz, process
from difflib import SequenceMatcher
from collections import namedtuple
import numpy as np

from .approach import Approach



class FuzzyMatcher(Approach):
    def __init__(self, text, query_text, threshold) -> None:
        super().__init__(text, query_text, threshold)
        
        
    def match(self, topK = None,  get_span = False, sort = True):
        error_threshold_percentage = int(100*self.threshold/len(self.query_text))
        
        self._compute(topK, error_threshold_percentage)
             
        if get_span:
            self.spans = list(map(lambda x: self._get_span(*x), zip(self.text, [self.query_text]*len(self.text), 
                                                                self.verdicts, [self.threshold]*len(self.text))))
        
        self._format_output()
        if sort: self.sort()
        
        
    def _compute(self, topK, error_threshold_percentage):
        if topK:
            self.similarity_scores = list(process.extract(self.query_text, self.text, 
                                                          scorer= fuzz.partial_ratio, 
                                                          limit= min(topK, len(self.text))))
            self.text = [x[0] for x in self.similarity_scores]
        else:
            self.similarity_scores = list(process.extractWithoutOrder(self.query_text, self.text, scorer= fuzz.partial_ratio))
            
        self.similarity_scores = np.array([x[1] for x in self.similarity_scores])
        self.error_scores = 100 - self.similarity_scores
        self.verdicts = self.similarity_scores >= 100 - error_threshold_percentage
        
     
    def _get_span(self,text, query_text, verdict, threshold):
        
        if verdict == False: return [-1,-1] 
        
        sq = SequenceMatcher(None, text, query_text)
        longest_matching_block = sq.find_longest_match()
            
        if longest_matching_block.size >= len(query_text) - threshold:
            return (longest_matching_block.a, 
                    longest_matching_block.a + longest_matching_block.size)  
            
        matching_blocks = list(sq.get_matching_blocks())
        matched_chars = sum([block.size for block in matching_blocks])
            
        if (matched_chars >= (len(query_text) - threshold) 
                and len(matching_blocks)>1):
            
            block_distance = [0, 0]
            matched_char_so_far = matching_blocks[0].size
            span  = [matching_blocks[0].a, matching_blocks[0].a]

            for i in range(1, len(matching_blocks)-1):
                prev_block, current_block = matching_blocks[i-1], matching_blocks[i]
                
                block_distance = block_distance[0] + (current_block.a - (prev_block.a + prev_block.size)), \
                                    block_distance[1] + (current_block.b - (prev_block.b + prev_block.size))
                                
                if sum(block_distance)/2> threshold:
                    break
                
                matched_char_so_far += current_block.size
                span[1] = current_block.a + current_block.size   
                    
            return span            
        else:
            return [-1,-1]
        

  

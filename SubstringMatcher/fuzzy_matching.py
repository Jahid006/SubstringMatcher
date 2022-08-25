
from fuzzywuzzy import fuzz, process
from difflib import SequenceMatcher
from collections import namedtuple
import numpy as np


from .approach import Approach

class FuzzyMatcher(Approach):
    def __init__(self, text: list, query_text: str, threshold:int = None) -> None:
        super().__init__(text, query_text, threshold)
        
        
    def match(self, topK = None,  get_span = False, sort = True):
        """performs query text matching against given searchable text list and return a list of matches

        Args:
            topK (int, optional): to return topK matches. Defaults to None.
            get_span (bool, optional): to return match spam. Defaults to False.
            sort (bool, optional): to return sorted matches. Defaults to True.

        Returns:
            list[namedtuple]: a list of namedtuple('output',['text','verdict', 'similarity', 'error', 'span'])
        """
        error_threshold_percentage = int(100*self.threshold/len(self.query_text))
        
        self._compute(topK, error_threshold_percentage)
             
        if get_span:
            self.spans = list(map(lambda x: self._get_span(*x), zip(self.text, [self.query_text]*len(self.text), 
                                                                self.verdicts, [self.threshold]*len(self.text))))
            self.verdicts = [v if (s[0]!=-1 and s[1]!=-1) else False for v,s in zip(self.verdicts, self.spans)]
        
        self._format_output()
        if sort: self.sort()
        
        return self.outputs
        
        
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
        length_diff = np.array([len(x) for x in self.text]) - len(self.query_text)
        self.verdicts = self.similarity_scores >= 100 - error_threshold_percentage 
        self.verdicts[length_diff<-self.threshold] = False 
        
     
    def _get_span(self,text, query_text, verdict, threshold):
        
        if verdict == False: return [-1,-1] 
        sq = SequenceMatcher(None, text, query_text)
        longest_matching_block = sq.find_longest_match(0, len(text), 0, len(query_text))
        
        if longest_matching_block.size >= len(query_text) - threshold:
            return [longest_matching_block.a, 
                    longest_matching_block.a + longest_matching_block.size] 
            
        matching_blocks = list(sq.get_matching_blocks())
        matched_chars = sum([block.size for block in matching_blocks])
        
        span = [-1,-1]
        if (matched_chars >= (len(query_text) - threshold) 
                and len(matching_blocks)>1):
            matching_blocks = matching_blocks[:-1]  #last match is not necessary
            
            block_distance = [0, 0]
            matched_char_so_far = matching_blocks[0].size
            span  = [matching_blocks[0].a, matching_blocks[0].a + matching_blocks[0].size]
            
            i = 1
            while(i<len(matching_blocks)):
                prev_block, current_block = matching_blocks[i-1], matching_blocks[i]
                
                block_distance = [block_distance[0] + (current_block.a - (prev_block.a + prev_block.size)), \
                                  block_distance[1] + (current_block.b - (prev_block.b + prev_block.size))]
                                 
                                
                if ((block_distance[0]> threshold or block_distance[1]>threshold)):
                    if  span[1]-span[0]<=threshold and i <= len(matching_blocks)-1:
                        matched_char_so_far = 0
                        span = [matching_blocks[i].a, matching_blocks[i].a + matching_blocks[i].size]
                        block_distance = [0, 0]
                        i += 1
                        #                     [- (current_block.a - (prev_block.a + prev_block.size)), \
                        #                   - (current_block.b - (prev_block.b + prev_block.size))]
                        continue
                    else:
                        break

                matched_char_so_far += current_block.size
                span[1] = current_block.a + current_block.size
                
                if matched_char_so_far>= len(query_text):
                    break 
                i += 1
                
            if span[1]-span[0]>len(query_text) - threshold:       
                return span                            
        return [-1,-1]
        

  

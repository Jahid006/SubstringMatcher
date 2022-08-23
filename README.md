## SubstringMatcher
### Fuzzy Substring Matching using Fuzzywuzzy and Difflib. 


#### Usecase:
> - Fuzzy (sub)string matching with similarity score and span detection
> - User defined character-level error tolerance
> - Find TopK matches


#### Example
```python 
from SubstringMatcher import FuzzyMatcher

strings_to_be_searched_in = ['another fuzzywuzzy copycat', 'or it is better than fuzzywuzzy']
query_string = 'fazzywuzzy?'

matcher = FuzzyMatcher(text = strings_to_be_searched_in, query_text = query_string)
pprint(matcher.match(get_span=True))
```
Returns a list of NamedTuple of type namedtuple('output',['text','verdict', 'similarity', 'error', 'span'])
```
Output: 

[output(text='another fuzzywuzzy copycat', verdict=True, similarity=90, error=10, span=[10, 18]),
 output(text='or it is better than fuzzywuzzy', verdict=True, similarity=90, error=10, span=[23, 31])]
```
#### Lets find topK matches

```python
from SubstringMatcher import FuzzyMatcher

strings_to_be_searched_in = ['another fuzzywuzzy', 'fuzzybizzy', ' copycat', 'or it is better than fuzzywuzzy', 'pfzy package is better than fuzzywuzzy']
query_string = 'fazzywuzzy?'

matcher = FuzzyMatcher(text = strings_to_be_searched_in, query_text = query_string)
pprint(matcher.match(topK=3,get_span=True))
```
```
Output: 
Some Texts are smaller than query text; may yield undesirable results [-_-]

[output(text='another fuzzywuzzy', verdict=True, similarity=90, error=10, span=[10, 18]),
 output(text='or it is better than fuzzywuzzy', verdict=True, similarity=90, error=10, span=[23, 31]),
 output(text='pfzy package is better than fuzzywuzzy', verdict=True, similarity=90, error=10, span=[30, 38])]

```

#### You can do Exact Substring Matching too

```python
from SubstringMatcher import ExactMatcher

strings_to_be_searched_in = ['another fuzzywuzzy', 'fazzywuzzy?', ' copycat', 'or it is better than fuzzywuzzy', 'pfzy package is better than fuzzywuzzy']
query_string = 'fazzywuzzy?'

matcher = ExactMatcher(text = strings_to_be_searched_in, query_text = query_string)
pprint(matcher.match(topK=3,get_span=True))

```
```
Output: 

Some Texts are smaller than query text; may yield undesirable results [-_-]

[output(text='fazzywuzzy?', verdict=True, similarity=100, error=0, span=[0, 11]),
 output(text=' copycat', verdict=False, similarity=0, error=100, span=[-1, -1]),
 output(text='another fuzzywuzzy', verdict=False, similarity=0, error=100, span=[-1, -1])]

```

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
Returns a list of NamedTuple of type ```namedtuple('output',['text','verdict', 'similarity', 'error', 'span'])```
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
#### Comparison with Fuzzywuzzy and DiffLib
```
from fuzzywuzzy import fuzz, process
from difflib import SequenceMatcher
from SubstringMatcher import FuzzyMatcher, ExactMatcher
from pprint import pprint


data = [('zxxy', ['abcdzxcy']),    # Should found a match
        ('zxxy', ['zabcdxcxy']),   # Should not found a match
        ('zxxy', ['zabcdxxdy']),   # Should not found a match
        ('zxxy', ['zdddxdddxddy']),# Should not found a match
        ]


for datum in data:
    query_text, searchble_text = datum
    print(f"{'*'*10} {query_text = } || {searchble_text = } {'*'*10}\n")
    print(f"FuzzyWuzzy(No Span): {list(process.extractWithoutOrder('zxxy', ['abcdzxcy'], scorer= fuzz.partial_ratio))}\n")
    sq = SequenceMatcher(None, searchble_text[0], query_text)
    print(f"Difflib: {sq.find_longest_match(0, len(searchble_text[0]), 0, len(query_text))}\n")
    
    matcher = FuzzyMatcher(text = searchble_text, query_text = query_text, threshold=1)
    print(f"SubstringMatcher: {matcher.match(get_span=True)}")
    print('\n\n')
```
```
Outputs:
********** query_text = 'zxxy' || searchble_text = ['abcdzxcy'] **********

FuzzyWuzzy(No Span): [('abcdzxcy', 75)]

Difflib: Match(a=4, b=0, size=2)

SubstringMatcher: [output(text='abcdzxcy', verdict=True, similarity=75, error=25, span=[4, 8])]



********** query_text = 'zxxy' || searchble_text = ['zabcdxcxy'] **********

FuzzyWuzzy(No Span): [('abcdzxcy', 75)]

Difflib: Match(a=7, b=2, size=2)

SubstringMatcher: [output(text='zabcdxcxy', verdict=False, similarity=75, error=25, span=[-1, -1])]



********** query_text = 'zxxy' || searchble_text = ['zabcdxxdy'] **********

FuzzyWuzzy(No Span): [('abcdzxcy', 75)]

Difflib: Match(a=5, b=1, size=2)

SubstringMatcher: [output(text='zabcdxxdy', verdict=False, similarity=75, error=25, span=[-1, -1])]



********** query_text = 'zxxy' || searchble_text = ['zdddxdddxddy'] **********

FuzzyWuzzy(No Span): [('abcdzxcy', 75)]

Difflib: Match(a=0, b=0, size=1)

SubstringMatcher: [output(text='zdddxdddxddy', verdict=False, similarity=50, error=50, span=[-1, -1])]

```
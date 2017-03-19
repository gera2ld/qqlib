'''
Decode hieroglyphy with Python
@author Gerald <i@gerald.top>

Reference:
- http://patriciopalladino.com/files/hieroglyphy/
- https://github.com/alcuadrado/hieroglyphy

QZone uses hieroglyphy but changed `f`
'''

# Generate mappings with JavaScript:
# Run it at http://patriciopalladino.com/files/hieroglyphy/
# > 'mappings = ' + JSON.stringify('0123456789abcdeghijklmnopqrstuvwxyz'.split('').reduce((res, c) => {res[c] = hieroglyphy.hieroglyphyString(c).replace(/\+\[\]$/, ''); return res;}, {f:'(![]+[])[+[]]'}), null, 4)
# Store it to ./data.py
from .data import mappings

class CannotDecodeError(Exception): pass

def decode(text):
    remained = text
    results = []
    while remained:
        for key, val in mappings.items():
            if remained == val or remained.startswith(val + '+'):
                results.append(key)
                remained = remained[len(val) + 1:]
                break
        else:
            print(''.join(results), remained)
            raise CannotDecodeError(text)
    return ''.join(results)

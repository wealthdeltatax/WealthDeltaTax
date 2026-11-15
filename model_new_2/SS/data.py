import json
from wdt_jst import real_basis_inputs
J = json.load(open('jst_r6.json', encoding='utf-8'))
print(real_basis_inputs(J, 'GBR'))
# quick bank
A quick implementation of the ledger and entities aspects of a bank. There are no rules stopping negative balances, duplicate accounts etc. There is no security.

## why python?
I briefly got to use fastapi a while back and saw pydantic was quite a breath of fresh air in terms of declaring models in python (see entity_models). 

## core libraries
- pydantic

- pytest
- pydantic factories (really awesome library like factory girl but easier)

## running
```pip install -r requirements.txt```
```pytest```

## next steps
During the modelling phase the most interesting part was thinking about if there were multiple banks, how would you route money between parties. Implemented a simple bank system structure for this.


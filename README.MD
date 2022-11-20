# fast ledger
A quick implementation of the ledger and entities aspects of a bank. There are no rules stopping negative balances, duplicate accounts etc. There is no security.

## why python?
I briefly got to use fastapi a while back and saw pydantic was quite a breath of fresh air in terms of declaring models in python (see ledger_models). 

## core libraries
- pydantic

- pytest
- pydantic factories (really awesome library like factory girl but easier)

## running
```pip install -r requirements.txt```
```pytest```

## next steps
- More tests, a ledger should have 100% test coverage, run ```coverage report``` for more info
-- But mainly some methods in transactions and assets are missing tests
- Implement a scheduler to run update balances
- Implement reports
- Implement a quick frontend (for fun)
- Entity resolution service to prevent duplicates


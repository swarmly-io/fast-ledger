# quick bank
This is a quick go at creating a bank with a simple single currency ledger. You are able to create a bank, add entities with accounts.

The functionality of the bank is split up into commands and queries (see bank_worker and bank_query) with an additional maintainance component to demonstrate how I would do detail updates as customers often do.

## why python?
I briefly got to use fastapi a while back and saw pydantic was quite a breath of fresh air in terms of declaring models in python (see entity_models). Since I have another side project going on in python I used this opportunity to evaluate it for that (hope you don't mind)! Probably would build a bank in java or kotlin ;)

## core libraries
- pydantic

- pytest
- pydantic factories (really awesome library like factory girl but easier)

## running
```pip install -r requirements.txt```
```pytest```

## next steps
During the modelling phase the most interesting part was thinking about if there were multiple banks, how would you route money between parties. Implemented a simple bank system structure for this.


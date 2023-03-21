We accept new APIs for validation, there are few steps to add one:
- Find API endpoint that gives you information about user: his tariff and/or allowance
- Add a new file that represents this API in `APIs` directory and populate it
- Inside that new file add class named after this API and populate it with `check`, `present` and `write` methods, look for example in existing files
- (optional) If you can, add regex to `other.dictionaries.regex`, alternatively make sure to let other devs know your code doesn't have regex, and it needs to be added by someone else
- Add necessary methods to `apie.py` and `other.user.output.py`
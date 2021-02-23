class RuleBasedParserMixin:
    def rules(self):
        if not self._rules:
            self._rules = {
                attr: getattr(self, attr)
                for attr in dir(self)
                if not attr.startswith("_") and not callable(getattr(self, attr))
            }
        return self._rules

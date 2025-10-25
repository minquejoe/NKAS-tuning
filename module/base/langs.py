class LangMeta(type):
    _translations = {
        "LANUCHER_START": {"en-US": "Hello", "zh-CN": "你好", "jp": "こんにちは"},
        "LANUCHER_UPDATE": {"en-US": "Goodbye", "zh-CN": "再见", "jp": "さようなら"},
    }
    _current_lang = "zh-CN"

    def __getattr__(cls, name):
        if name in cls._translations:
            values = cls._translations[name]
            return values.get(cls._current_lang, next(iter(values.values())))
        raise AttributeError(f"{cls.__name__} has no attribute '{name}'")

    def use(cls, lang: str):
        """设置当前使用语言"""
        cls._current_lang = lang


class Langs(metaclass=LangMeta):
    pass

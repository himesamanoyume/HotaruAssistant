
class ConfigKeySubModule:
    mInstance = None

    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            cls.multi_login_accounts = 'multi_login_accounts'

        return cls.mInstance

    
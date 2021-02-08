RUNMODES = ["once", "forever", "async_once", "async_forever"]

NWORKERS = 4

LEGAL_GLOBALS = ["run_mode", "nworkers", "interval", "recovery_type"]

LEGAL_RECOVERYS = ["url_back_last", "url_back_first", "skip"]

RECOVERY_TYPE = "url_back_last"

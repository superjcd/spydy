RUNMODES = ["once", "forever", "async_once", "async_forever"]

NWORKERS = 4

LEGAL_GLOBALS = ["run_mode", "nworkers", "interval", "recovery_type"]

LEGAL_RECOVERYS = ["url_back_end", "url_back_front", "skip"]

RECOVERY_TYPE = "url_back_end"

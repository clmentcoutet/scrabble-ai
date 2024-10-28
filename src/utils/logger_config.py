import logging


def _setup_logger():
    # Créer un logger
    logger = logging.getLogger("app_logger")
    logger.setLevel(logging.DEBUG)  # Permet de capturer tous les niveaux de log

    # Format des logs
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s: \n%(message)s"
    )

    # Handler pour afficher dans la console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARN)  # Afficher tous les logs dans la console
    console_handler.setFormatter(formatter)
    # console_handler.setStream(sys.stdout)

    # Handler pour enregistrer les erreurs critiques dans un fichier
    file_handler = logging.FileHandler("logs/critical_errors.log")
    file_handler.setLevel(
        logging.CRITICAL
    )  # Enregistrer uniquement les erreurs critiques dans le fichier
    file_handler.setFormatter(formatter)

    # Ajouter les handlers au logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


def _setup_print_logger():
    logger = logging.getLogger("print_logger")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(message)s")

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.CRITICAL)
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger


logger = _setup_logger()
print_logger = _setup_print_logger()

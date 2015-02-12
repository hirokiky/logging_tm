==========
logging_tm
==========

Logging with transnaction.


.. code-block:: python

    import logging
    logger = logging.getLogger()

    import sys
    from logging_tm.datamanager import HandlerDataManager
    logger.addHandler(HandlerDataManager(lambda: sys.stdout.write))
    logger.setLevel(logging.INFO)

    import transaction
    with transaction.manager:
        logger.info("Hello world")
        logger.info("Hallo welt")
    # After transaction "Hello world\nHallo welt\n" will be outputted

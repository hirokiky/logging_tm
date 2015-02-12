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
    transaction.begin()
    logger.info("Hello world")
    logger.info("Hallo welt")
    transaction.commit()
    # After committing the transaction, "Hello world\nHallo welt\n" will be outputted

import logging
import sys

import transaction as zope_transaction
from transaction.interfaces import IDataManager, ISavepoint, ISynchronizer
from zope.interface import implementer


@implementer(IDataManager)
class HandlerDataManager(logging.Handler):
    def __init__(self, messenger_factory, exc_info=True,
                 transaction_manager=zope_transaction.manager,
                 *args, **kwargs):
        self.msgs = []
        # TODO: If messenger is str, import it and set.

        self.messenger = messenger_factory(*args, **kwargs)
        self.exc_info = exc_info
        self.transaction_manager = transaction_manager
        self.synch = HandlerSynchronizer(self)
        self.transaction_manager.registerSynch(self.synch)

        super(HandlerDataManager, self).__init__()

    def release_records(self):
        if not self.msgs:
            return

        self.messenger('\n'.join(self.msgs) + '\n')
        self.msgs = []

    # Handler methods

    def emit(self, record):
        msg = self.format(record)
        self.msgs.append(msg)

    # transaction methods

    def abort(self, transaction):
        if (self.exc_info and
                self.msgs and
                sys.exc_info() != (None, None, None)):
            if self.formatter:
                fmt = self.formatter
            else:
                fmt = logging.Formatter()
            exc_msg = fmt.formatException(sys.exc_info())
            self.msgs.append(exc_msg)
        self.release_records()

    def tpc_begin(self, transaction):
        pass

    def commit(self, transaction):
        pass

    def tpc_vote(self, transaction):
        # TODO Checking some?
        pass

    def tpc_abort(self, transaction):
        self.msgs = []

    def tpc_finish(self, transaction):
        self.release_records()

    def savepoint(self):
        return HandlerSavepoint(self)


@implementer(ISavepoint)
class HandlerSavepoint(object):
    def __init__(self, dm):
        pass

    def rollback(self):
        pass


@implementer(ISynchronizer)
class HandlerSynchronizer(object):
    def __init__(self, dm):
        self.dm = dm

    def newTransaction(self, new_txn):
        new_txn.join(self.dm)

    def beforeCompletion(self, txn):
        pass

    def afterCompletion(self, txn):
        pass

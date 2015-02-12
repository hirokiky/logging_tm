import logging
import unittest

import transaction


class TestHandlerDataManager(unittest.TestCase):
    def _makeOne(self, *args, **kwargs):
        from logging_tm.datamanager import HandlerDataManager
        dm = HandlerDataManager(*args, **kwargs)
        return dm

    def _makePortal(self):
        portal = {}

        class Messenger(object):
            def __init__(self, *args, **kwargs):
                pass

            def __call__(self, msg):
                portal['called'] = msg

        return Messenger, portal

    def test__it(self):
        messenger_class, portal = self._makePortal()
        target = self._makeOne(messenger_class)

        logger = logging.getLogger()
        logger.addHandler(target)
        logger.setLevel(logging.INFO)

        transaction.begin()

        logger.info("Test1")
        logger.info("Test2")
        logger.info("Test3")

        transaction.commit()

        self.assertEqual(portal['called'], "Test1\nTest2\nTest3\n")
        self.assertEqual(target.msgs, [])

    def test__didnt_catched(self):
        messenger_class, portal = self._makePortal()
        target = self._makeOne(messenger_class)

        logger = logging.getLogger()
        logger.addHandler(target)
        logger.setLevel(logging.INFO)

        transaction.begin()

        logger.debug("Test1")
        logger.debug("Test2")
        logger.debug("Test3")

        transaction.commit()

        self.assertNotIn('called', portal)
        self.assertEqual(target.msgs, [])

    def test__exc_info(self):
        messenger_class, portal = self._makePortal()
        target = self._makeOne(messenger_class, exc_info=True)

        transaction.begin()

        logger = logging.getLogger()
        logger.addHandler(target)
        logger.setLevel(logging.INFO)

        try:
            with transaction.manager:
                logger.info("Test1")
                raise Exception
        except Exception:
            pass

        self.assertTrue(portal['called'].startswith("Test1\nTraceback"),
                        msg="msg was: " + portal['called'])

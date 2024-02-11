'''Testing for processing.py'''

import unittest

class TestEvent(unittest.TestCase):
    '''For testing the Event class'''

    def test_import(self):
        """ Test that the Processing module can be imported. """
        import Processing
    
    def test_event_duration(self):
        '''tests response time'''
        from Processing.processing import Event
        from datetime import datetime
        event = Event(startTime=datetime.fromisoformat('2011-11-04T00:05:23Z'), endTime=datetime.fromisoformat('2011-11-04T00:05:24Z'))
        self.assertEquals(event.event_duration().seconds, 1)

if __name__ == '__main__':
    unittest.main()

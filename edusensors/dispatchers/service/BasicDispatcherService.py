#   -*- coding: utf-8 -*-
from zope.interface import Interface, implements
from twisted.application import service
from twisted.internet import defer


class IBasicDispatcherService(Interface):
    def my_func(self, value):
        """Return a deferred returning a string"""

class BasicDispatcherService(service.Service):
    implements(IBasicDispatcherService)
    
    db = 'moe'
    db_user = 'root'
    db_pass = '42'
    host = 'localhost'
    
    def my_func(self, value):
        print 'BasicDispatcherService::my_func'
        return defer.Deferred()
    
    def query(self, sqlQuery):
        import MySQLdb
        import datetime
        dbo = MySQLdb.connect(host=self.host,user=self.db_user, passwd=self.db_pass, db=self.db, charset='utf8')
        cursor = dbo.cursor()
        cursor.execute(sqlQuery)
        dataset = []
        for row in cursor.fetchall():
            record = []
            for val in row:
                if isinstance(val, datetime.datetime):
                    record.append(str(val))
                else:
                    record.append(val) 
            dataset.append(record)
        cursor.close()
        dbo.close()
        return dataset
        

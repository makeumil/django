import wx
from datetime import datetime, timedelta

'''
uri = "&q.op=eq&q.field=timestamp&q.op=gt&q.value="

currentUtcDateTime = datetime.utcnow()
timegap = timedelta(minutes=10)
queryDateTime = currentUtcDateTime - timegap


query = uri + str(queryDateTime)

print "currentUtcDateTime : " + str(currentUtcDateTime.isoformat())
print "queryUtcDateTime : " + str(queryDateTime.isoformat())

print " query : " + str(query)
'''


app = wx.App(redirect=True)

top = wx.Frame(None, title="Hello World", size=(300,200))
top.Show()

app.MainLoop()
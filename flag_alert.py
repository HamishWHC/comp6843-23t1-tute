
"""
Built on Jython 2.7.2

# https://featherbear.cc/UNSW-COMP6443
"""

from burp import IBurpExtender, IHttpListener
import re

RE = b"(COMP6443{.+?})"


class BurpExtender(IBurpExtender, IHttpListener):
    def registerExtenderCallbacks(self, callbacks):
        self.callbacks = callbacks
        self.helpers = callbacks.getHelpers()
        callbacks.setExtensionName("Flag Alert")
        callbacks.registerHttpListener(self)
        self.found = []

    def processHttpMessage(self, toolFlag, messageIsRequest, messageInfo):
        if not messageIsRequest:
            extract = re.findall(RE, bytearray(messageInfo.getResponse()))
            if extract:
                newEntry = False
                for item in extract:
                    if item not in self.found:
                        newEntry = True
                        self.found.append(item)
                        print(item)
                        self.callbacks.issueAlert(item)
                messageInfo.setHighlight('yellow')
                self.callbacks.addToSiteMap(messageInfo)
                if newEntry:
                    messageInfo.setHighlight('green')

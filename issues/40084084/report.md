# Bad cast to MouseEvent in Node::defaultEventHandler()

| Field | Value |
|-------|-------|
| **Issue ID** | [40084084](https://issues.chromium.org/issues/40084084) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | [Deleted User] |
| **Assignee** | mo...@google.com |
| **Created** | 2010-10-22 |
| **Bounty** | $500.00 |

## Description

Chrome Version : 8.0.552.11  

URLs (if applicable) : <http://co102w.col102.mail.live.com/default.aspx>

**What steps will reproduce the problem?**

1. Respond to a message in Hotmail
2. Click multiple times on a line while editing that message

**What is the expected result?**  

Line select, then deselect, then select again, just like when I am clicking like I'm crazy in this text field: the line I am clicking on gets selected/deselected/selected/deselected/...

**What happens instead?**  

Select/deselect/select/crash

**Please provide any additional information below. Attach a screenshot if**  

**possible.**  

Sometimes you have to click 1000 times, sometimes 2 times is enough.  

OS: Windows 7

## Attachments

- [Chrome-last.zip](attachments/Chrome-last.zip) (application/zip; charset=binary, 53.2 KB)

## Timeline

### [Deleted User] (2010-10-22)

If you haven't enabled crash logging, please enable it going to Wrench > Options > Under the Hood > Check "Help make Google Chrome better ..."

Restart Chrome

Reproduce the Crash

Start > Run > type eventvwr > Windows logs > Application > source==chrome

You should see a crash Id in it. Please post it here. Thanks.

Also, try disabling extensions.

### [Deleted User] (2010-10-22)

If I'm correct it should be this one:
1f34006a2c84e6e2

### [Deleted User] (2010-10-22)

Tried it again, but now the eventvwr showed "Crash not uploaded. Error=0x8004fffd."
Therefore I uploaded the dmp of the latest crash. This time no extensions were enabled

### pa...@google.com (2010-10-22)

Call Stack
-----------

0x5eabcf4d	 [chrome.dll	 - page_click_tracker.cc:107]	PageClickTracker::handleEvent(WebKit::WebDOMEvent const &)
0x5f17bd56	 [chrome.dll	 - eventlistenerwrapper.cpp:64]	WebKit::EventListenerWrapper::handleEvent(WebCore::ScriptExecutionContext *,WebCore::Event *)
0x5ef4dac7	 [chrome.dll	 - eventtarget.cpp:335]	WebCore::EventTarget::fireEventListeners(WebCore::Event *,WebCore::EventTargetData *,WTF::Vector<WebCore::RegisteredEventListener,1> &)
0x5ef4da01	 [chrome.dll	 - eventtarget.cpp:304]	WebCore::EventTarget::fireEventListeners(WebCore::Event *)
0x5ee7cf75	 [chrome.dll	 - node.cpp:2524]	WebCore::Node::handleLocalEvents(WebCore::Event *)
0x5ee7d25d	 [chrome.dll	 - node.cpp:2654]	WebCore::Node::dispatchGenericEvent(WTF::PassRefPtr<WebCore::Event>)
0x5ee7d08a	 [chrome.dll	 - node.cpp:2587]	WebCore::Node::dispatchEvent(WTF::PassRefPtr<WebCore::Event>)
0x5ef4d937	 [chrome.dll	 - eventtarget.cpp:282]	WebCore::EventTarget::dispatchEvent(WTF::PassRefPtr<WebCore::Event>,int &)
0x5f0cbc3c	 [chrome.dll	 - v8websocket.cpp:187]	WebCore::DOMApplicationCacheInternal::dispatchEventCallback
0x5f640ab6	 [chrome.dll	 - builtins.cc:983]	v8::internal::HandleApiCallHelper<0>
0x5f640daf	 [chrome.dll	 + 0x00cb0daf]	
0x25027aa9			
0x05cf7326			
0x2e8c3a24			
0x1f91140c			
0x0fc7ace6			
0x2f9e1058			
0x2f9d1421			
0x5f618901	 [chrome.dll	 - execution.cc:95]	v8::internal::Invoke
0x5ef46b7c	 [chrome.dll	 - v8isolatedcontext.h:88]	WebCore::V8IsolatedContext::getEntered()
0x5ef4927e	 [chrome.dll	 - v8proxy.cpp:515]	WebCore::V8Proxy::callFunction(v8::Handle<v8::Function>,v8::Handle<v8::Object>,int,v8::Handle<v8::Value> * const)
0x5ef47294	 [chrome.dll	 - v8domwrapper.cpp:392]	WebCore::V8DOMWrapper::convertEventTargetToV8Object(WebCore::EventTarget *)
0x5eed842f	 [chrome.dll	 - scriptcontrollerbase.cpp:41]	WebCore::ScriptController::canExecuteScripts(WebCore::ReasonForCallingCanExecuteScripts)
0x5efff509	 [chrome.dll	 - v8lazyeventlistener.cpp:69]	WebCore::V8LazyEventListener::callListenerFunction(WebCore::ScriptExecutionContext *,v8::Handle<v8::Value>,WebCore::Event *)
0x5eff8c11	 [chrome.dll	 - v8abstracteventlistener.cpp:151]	WebCore::V8AbstractEventListener::invokeEventHandler(WebCore::ScriptExecutionContext *,WebCore::Event *,v8::Handle<v8::Value>)
0x5eff8acb	 [chrome.dll	 - v8abstracteventlistener.cpp:94]	WebCore::V8AbstractEventListener::handleEvent(WebCore::ScriptExecutionContext *,WebCore::Event *)
0x5f4de7ff	 [chrome.dll	 - hashtable.h:482]	WTF::HashTable<WTF::AtomicString,std::pair<WTF::AtomicString,WTF::AtomicString>,WTF::PairFirstExtractor<std::pair<WTF::AtomicString,WTF::AtomicString> >,WTF::AtomicStringHash,WTF::PairHashTraits<WTF::HashTraits<WTF::AtomicString>,WTF::HashTraits<WTF::AtomicString> >,WTF::HashTraits<WTF::AtomicString> >::lookup<WTF::AtomicString,WTF::IdentityHashTranslator<WTF::AtomicString,std::pair<WTF::AtomicString,WTF::AtomicString>,WTF::AtomicStringHash> >(WTF::AtomicString const &)
0x5ef4dac7	 [chrome.dll	 - eventtarget.cpp:335]	WebCore::EventTarget::fireEventListeners(WebCore::Event *,WebCore::EventTargetData *,WTF::Vector<WebCore::RegisteredEventListener,1> &)
0x5ef4da01	 [chrome.dll	 - eventtarget.cpp:304]	WebCore::EventTarget::fireEventListeners(WebCore::Event *)
0x5ee7cf75	 [chrome.dll	 - node.cpp:2524]	WebCore::Node::handleLocalEvents(WebCore::Event *)
0x5ee7d25d	 [chrome.dll	 - node.cpp:2654]	WebCore::Node::dispatchGenericEvent(WTF::PassRefPtr<WebCore::Event>)

crash id: f0170e34604f0ae3
Full report @ http://crash/reportdetail?reportid=f0170e34604f0ae3

Google Chrome	8.0.552.11 (Official Build 63324)



### [Deleted User] (2010-10-22)

I was able to repro this 3 times but not consistently. It can be repro'ed but not easily. Keep clicking...

Full report @ http://crash/reportdetail?reportid=9b754c95bfe2fb4e


### [Deleted User] (2010-10-22)

[Empty comment from Monorail migration]

### ch...@gmail.com (2010-10-22)

This is a bad cast in Node::defaultEventHandler()

To trigger it you have to have the extension "mailto hotmail" installed and comment out the first DCHECK() in PageClickTracker::handleEvent(). Additionally you will need patience and a twitchy clicky finger. Keep clicking the text box until you are physically incapable of clicking it again, then have someone else click it for you. 

I believe I have a fix. I am testing it now and will file it upstream.



### ch...@gmail.com (2010-10-22)

[Empty comment from Monorail migration]

### [Deleted User] (2010-10-23)

Strange. The second time (commment 3) I had every extension disabled AFAIK, including mailto:hotmail. Or did I make a mistake and did I still have it enabled?

### sc...@gmail.com (2010-10-23)

[Empty comment from Monorail migration]

### [Deleted User] (2010-10-25)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-10-25)

this is going to v7. it is so simple type check. webkit bug filed - https://bugs.webkit.org/show_bug.cgi?id=48159

### ch...@gmail.com (2010-10-25)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-10-25)

merged to v7 in r70475, v8 in r70477.

### [Deleted User] (2010-10-27)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-10-28)

@fam.lam: congratulations! This bug provisionally qualifies for a $500 Chromium Security Reward.
Although this bug was not filed originally as a security bug, it was found to be a security bug. This report was therefore useful to us, hence the reward. We were also swayed by your helpfulness in the bug :D
We will require that future reports be filed as security bugs in order to qualify for rewards. If in doubt, feel free to file "Aw, snap" bugs a security bugs -- some fraction of "Aw, snap"s have security consequence.

----
Boilerplate text:
Please do NOT publicly disclose details until a fix has been released to all our
users. Early public disclosure may cancel the provisional reward.
Also, please be considerate about disclosure when the bug affects a core library
that may be used by other products.
Please do NOT share this information with third parties who are not directly
involved in fixing the bug. Doing so may cancel the provisional reward.
Please be honest if you have already disclosed anything publicly or to third parties.
----

### [Deleted User] (2010-10-28)

Thanks!
Also thanks to the developers who fixed this!

### sc...@gmail.com (2010-11-21)

@fam.lam: we released the fix a while back: http://googlechromereleases.blogspot.com/2010/11/stable-channel-update.html

Please e-mail me, cevans@chromium.org, and we'll get your reward paid :)

### sc...@gmail.com (2010-12-02)

Payment is in the electronic system.

### la...@chromium.org (2011-03-19)

Chrome Version : 8.0.552.11  

URLs (if applicable) : <http://co102w.col102.mail.live.com/default.aspx>

**What steps will reproduce the problem?**

1. Respond to a message in Hotmail
2. Click multiple times on a line while editing that message

**What is the expected result?**  

Line select, then deselect, then select again, just like when I am clicking like I'm crazy in this text field: the line I am clicking on gets selected/deselected/selected/deselected/...

**What happens instead?**  

Select/deselect/select/crash

**Please provide any additional information below. Attach a screenshot if**  

**possible.**  

Sometimes you have to click 1000 times, sometimes 2 times is enough.  

OS: Windows 7

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

### js...@chromium.org (2012-04-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### as...@chromium.org (2014-06-18)

ccing "chromium.cdn@gmail.com" as was not able to save 'hasTestcase' label.

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/60327?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084084)*

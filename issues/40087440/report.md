# Security: chrome.tabs.executeScript can reveal Chrome's profile path

| Field | Value |
|-------|-------|
| **Issue ID** | [40087440](https://issues.chromium.org/issues/40087440) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Platform>Extensions>API |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ng...@gmail.com |
| **Assignee** | rd...@chromium.org |
| **Created** | 2017-04-24 |
| **Bounty** | $500.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://www.chromium.org/Home>**  

**/chromium-security/security-faq**

**Please see the following link for instructions on filing security bugs:**  

**<http://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**VULNERABILITY DETAILS**

**VERSION**  

Chrome Version: 58.0.3029.81 stable, 60.0.3079.0 canary  

Operating System: Windows 7 SP1, also reproducible on macOS 10.12.4

**REPRODUCTION CASE**

1. Install the attached extension
2. Go to <http://example.com>
3. Read the error message

Expected result:  

The JavaScript error stack should only show `executed.js` or something like `chrome-extension://dogncidbhigdogloimjmnldclfogpmin/executed.js`

Actual result:  

The JavaScript error stack is revealing Chrome's profile path, which most likely contains the OS username too

```
Error  
    at file:///C:/Users/ngyikp/AppData/Local/Google/Chrome/User%20Data/Default/Extensions/dogncidbhigdogloimjmnldclfogpmin/1.0_0/executed.js:2:8  

```

Source code:  

content.js:

```
chrome.runtime.sendMessage('', function() {});  

```

background.js:

```
chrome.runtime.onMessage.addListener(function(message, sender, callback) {  
	chrome.tabs.executeScript(sender.tab.id, {file: 'executed.js'});  
});  

```

executed.js:

```
try {  
	throw new Error();  
} catch (ex) {  
	alert(ex.stack);  
}  

```

manifest.json:

```
{  
	"name": "executeScript",  
	"version": "1.0",  
  
	"background": {  
		"scripts": ["background.js"],  
		"persistent": false  
	},  
	"manifest_version": 2,  
  
	"permissions": [  
		"http://example.com/\*",  
		"https://example.com/\*",  
		"http://www.example.com/\*",  
		"https://www.example.com/\*"  
	],  
	"content_scripts": [{  
		"include_globs": [  
			"http://example.com/\*",  
			"https://example.com/\*",  
			"http://www.example.com/\*",  
			"https://www.example.com/\*"  
		],  
		"js": ["content.js"],  
		"matches": [  
			"http://example.com/\*",  
			"https://example.com/\*",  
			"http://www.example.com/\*",  
			"https://www.example.com/\*"  
		],  
		"run_at": "document_start"  
	}]  
}  

```

This bug is introduced since Chrome 32, Chrome 31 is OK

This commit seems suspect: <https://chromium.googlesource.com/chromium/src/+/a7074d1c5c07670813eefdbf286c23416e528123%5E%21/>

## Attachments

- [screenshot.png](attachments/screenshot.png) (image/png, 71.4 KB)
- [chrome31.png](attachments/chrome31.png) (image/png, 85.4 KB)
- [executescript.crx](attachments/executescript.crx) (application/octet-stream, 1.4 KB)

## Timeline

### ng...@gmail.com (2017-04-24)

Opps, forgot to attach extension

### el...@chromium.org (2017-04-24)

Thanks for the sleuthing!

[Monorail components: Platform>Extensions>API]

### me...@chromium.org (2017-04-24)

Agreed, thanks for the detailed description and the investigation!

According to the severity guidelines, this would normally qualify as a medium severity, but since we consider extension installation a mitigating factor the severity is downgraded to low.


### sh...@chromium.org (2017-04-25)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-05-04)

[Comment Deleted]

### mb...@chromium.org (2018-02-14)

Devlin, would you mind taking a look? Reassigning since this seems stale.

### mm...@chromium.org (2019-04-30)

[Empty comment from Monorail migration]

### rd...@chromium.org (2019-08-26)

Revisiting old bugs.

Karan, do you think you can take a look at this?  The best solution seems like it would be to surface the extension-relative url (i.e., chrome-extension://<id>/script.js).

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### rd...@chromium.org (2019-12-11)

I'll take this one back; I have a patch that should work.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-12-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d52ea54eab4fdedfe640c0838199548c1717b5ed

commit d52ea54eab4fdedfe640c0838199548c1717b5ed
Author: Devlin Cronin <rdevlin.cronin@chromium.org>
Date: Fri Dec 20 17:59:02 2019

[Extensions] Set tabs.executeScript() URLs to chrome-extension: scheme

Set the script URL for scripts executed via chrome.tabs.executeScript()
to use the chrome-extension: scheme, e.g.
chrome-extension://<id>/<path-to-script>, rather than the file URL.
This prevents referencing the filesystem in the URL, and is consistent
with content scripts that are statically specified in the manifest.

Add a regression test (that also tests the statically-defined content
script behavior). This entailed adding a new test utility,
WebContentsConsoleObserver, to track the messages sent to the console
for a given WebContents. This can replace ConsoleObserverDelegate in
the future.

Bug: 714617
Change-Id: I3de400e6dccf9f9a662824b4810bd52245cd4d62
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1962676
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Reviewed-by: Emily Stark <estark@chromium.org>
Commit-Queue: Devlin <rdevlin.cronin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#726842}

[modify] https://crrev.com/d52ea54eab4fdedfe640c0838199548c1717b5ed/chrome/browser/extensions/content_script_apitest.cc
[modify] https://crrev.com/d52ea54eab4fdedfe640c0838199548c1717b5ed/extensions/browser/api/execute_code_function.cc
[modify] https://crrev.com/d52ea54eab4fdedfe640c0838199548c1717b5ed/extensions/browser/api/execute_code_function.h
[modify] https://crrev.com/d52ea54eab4fdedfe640c0838199548c1717b5ed/extensions/browser/script_executor.cc
[modify] https://crrev.com/d52ea54eab4fdedfe640c0838199548c1717b5ed/extensions/browser/script_executor.h
[modify] https://crrev.com/d52ea54eab4fdedfe640c0838199548c1717b5ed/extensions/common/extension_messages.h
[modify] https://crrev.com/d52ea54eab4fdedfe640c0838199548c1717b5ed/extensions/renderer/programmatic_script_injector.cc


### rd...@chromium.org (2019-12-20)

This should be fixed with #13.

Given the low impact and duration this has been around, I don't think this is something we need to merge.

### sh...@chromium.org (2019-12-21)

[Empty comment from Monorail migration]

### na...@google.com (2020-01-06)

[Empty comment from Monorail migration]

### na...@google.com (2020-01-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-01-09)

Congrats! The Panel decided to reward $500 for this report!

### na...@google.com (2020-01-09)

[Empty comment from Monorail migration]

### ad...@google.com (2020-03-09)

ngyikp@gmail.com - when this appears in the Chrome release notes, how would you like to be credited?

### ng...@gmail.com (2020-03-09)

You can use my full name: Ng Yik Phang

### ad...@google.com (2020-03-13)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-03-13)

[Empty comment from Monorail migration]

### [Deleted User] (2020-03-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@chromium.org (2020-04-14)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/714617?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087440)*

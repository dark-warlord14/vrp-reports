# Security: Bypassing web_accessible_resources protections

| Field | Value |
|-------|-------|
| **Issue ID** | [40083949](https://issues.chromium.org/issues/40083949) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Platform>Extensions, UI>Browser>Navigation |
| **Platforms** | Mac |
| **Reporter** | ja...@gmail.com |
| **Assignee** | rd...@chromium.org |
| **Created** | 2016-03-28 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**

If a web page tries to open a Chrome extension file, without have been authorized, Chrome will throw a security error exception:

Denying load of chrome-extension://hgmloofddffdnphfgcellkdfbfbjeloo/RestClient.html. Resources must be listed in the web\_accessible\_resources manifest key in order to be loaded by pages outside the extension.

But there is some ways to bypass this protection.

**VERSION**

Chrome Version: 49.0.2623.87 (64-bit) (stable)  

Operating System: OS X 10.8.5

**REPRODUCTION CASE**

Open the HTML attached and see the different actions.  

Some actions will throw the expected security error exception, others will not.

Chrome extension used in the tests: <https://chrome.google.com/webstore/detail/advanced-rest-client/hgmloofddffdnphfgcellkdfbfbjeloo>

## Attachments

- [chrome-extension.html](attachments/chrome-extension.html) (text/plain, 1.4 KB)
- [chrome_installed_extensions.html](attachments/chrome_installed_extensions.html) (text/plain, 1.4 KB)

## Timeline

### wf...@chromium.org (2016-03-28)

meacer can you take a look at this potential extensions permission issue?

[Monorail components: Platform>Extensions]

### me...@chromium.org (2016-03-28)

jaumlucas: Thank you for the report. Going over the POC:

Case 1: Chrome treats "open link in new tab" navigations as direct, user initiated navigations. In other words, this should be identical to a user opening a new tab and pasting the URL. web_accessible_resources doesn't block direct navigations, so I believe this is working as intended.

Case 2 (and 3): This looks like a variant of a couple of existing bugs (https://crbug.com/chromium/576867, https://crbug.com/chromium/589237). That said, it doesn't seem possible to leak any information from the iframe, particularly whether it loads or not. I'll let asargent comment on this.

A minimized repro for case 2:

<a id="link" href="chrome-extension://hgmloofddffdnphfgcellkdfbfbjeloo/RestClient.html" target="iframe">Link</a>
<iframe src="chrome-extension://hgmloofddffdnphfgcellkdfbfbjeloo/RestClient.html" name="iframe" id="iframe"></iframe>
<script>
document.onclick = function() { link.click() }; // So that the user doesn't need to click specifically on the link
</script> 

Case 4, 5: These open the resource in a new window. Like Case 1, I don't think we intend to block these. Can't seem to get any useful data from these cases either.
Case 6, 7: These use form submits. I'm not sure what the expected behavior is here. asargent to the rescue.

Antony, assigning to you, please reassign or close as appropriate.

### pe...@chromium.org (2016-04-03)

Hello Antony,

Just wanting to make sure you've seen this ticket.  Please feel free to reassign, relabel, or close as appropriate.

Thanks.

### as...@chromium.org (2016-04-05)

Taking a look today. 

### ke...@chromium.org (2016-04-05)

asargent@: Do you see any information leakage to the web page? If not, then this shouldn't be flagged as a security issue.

### ke...@chromium.org (2016-04-07)

Friendly ping for the question in #5?

### as...@chromium.org (2016-04-07)

Ok, I've taken a look and I agree with Mustafa that I don't see any information leakage here to the attacker script in any of these cases, and extensions code always need to be prepared to handle XSRF kinds of attacks, so I'm marking this as Wontfix. 

To the original reporter: can you demonstrate any attack where the script determines that the extension is installed even if it has no web_accessible_resources? We can reopen this bug if so. 




### ja...@gmail.com (2016-04-08)

asargent@:

Sir, yes sir.
:)

http://dotfivelabs.com.br/teste-BB32FE5A/css/chrome_vuln.html

### as...@chromium.org (2016-04-08)

[Empty comment from Monorail migration]

### ke...@chromium.org (2016-04-08)

[Empty comment from Monorail migration]

### as...@chromium.org (2016-04-11)

Ok, I can confirm that the information leak does occur. It doesn't reproduce if you use a file url (eg downloading the html file from https://crbug.com/chromium/598265#c8 and loading the page from the filesystem), but does seem to work if you run it from an http(s) page. I went back to an old chrome version (31.0.1635.0) and verified that the bug didn't used to happen - I'm going to try and bisect to find where this started breaking. 

### as...@chromium.org (2016-04-13)

The bisect shows that this broke a while back - here's the relevant output:

"
You are probably looking for a change made after 287191 (known good), but no later than 287209 (first known bad).

CHANGELOG URL:
  https://chromium.googlesource.com/chromium/src/+log/0b97fd59fe09f6c911b9d32e6c
47841450d88508..cc9b29fbc3533e2bacf950ea23b6d6f0cd265bb5
"


I looked at the set of changes in that changelog, and then did a local build using source around that time, and have verified that the change which seems to have broken this was:

https://codereview.chromium.org/378743002 
(855d7d572fb4d4aaf97464771661c6805e0347a5 rev 287192)


+cc creis, nasko

nasko - this is the bug I mentioned in our recent chat. I'll be working on creating a browser test for this as well as the semi-related https://crbug.com/chromium/598265. 


### na...@chromium.org (2016-04-15)

If this is caused by the navigation transitions CL and this experiment was cancelled, can we just revert the changes?

### as...@chromium.org (2016-04-15)

Seems reasonable to me - looking at https://crbug.com/chromium/370696, it looks like a bunch of other pieces of the feature have been getting removed. 

I'm not all that familiar with this area of code - nasko, are you able to take this on? If not I can spend some more time to get up to speed on how things work. 


### as...@chromium.org (2016-04-19)

BTW, here's the test I wrote a few days ago that demonstrates this problem:

https://codereview.chromium.org/1888873003/


### na...@chromium.org (2016-04-20)

I've been poking at this and there are two pieces involved:

1. We have a difference in behavior depending whether an extension is installed or not. This allows other side effects to be used to determine if an extension is present or not. ChromeExtensionsRendererClient::ShouldFork behaves differently in - when an extension is installed and navigated to from a regular web process, the return value from ShouldFork is true and we end up sending the navigation to be performed by the browser process. If there is no such extension installed, normal resource request is made, which fails with ERR_FAILED.

2. On the browser side, ChromeContentBrowserClientExtensionsPart::ShouldAllowOpenURL allows the navigation to continue if an extension is not installed or enabled. Is there a reason for allowing this to proceed? I need to think through whether this can be abused for information leakage or not.
Furthermore, when ShoulAllowOpenURL returns false, meaning that the navigation should not be performed, the code in NavigatorImpl::RequestOpenURL (which calls it) rewrites the URL to "about:blank". The changes in https://codereview.chromium.org/378743002 made is such that a browser-side navigation to "about:blank" is treated as same-site navigation. This is in general the correct behavior, as navigating any frame to "about:blank" should put the new document in the origin of the document that initiated the navigation - in this case the attacker's page.

The combination of 1 and 2 leads to the information leakage, as for existing extension, we would send the navigation to the browser process, which will fail the ShouldAllowOpenURL and navigate it to about:blank. This allows the script to use origin checks to deduce whether the extension is installed or not.


To eliminate the info leak, we need to ensure we have consistent behavior regardless of whether an extension is installed or not. 
asargent@, why do we have a difference in behavior in ShouldFork? If we make it to only return true when we know the URL we want to navigate to is web_accessible_resource, I think we should be fine, since it will keep the navigation in the renderer and it will result in a ERR_FAILED regardless. Also, in the case of the URL being web_accessible_resource, we know on the browser side we will allow the navigation to succeed.

### ja...@gmail.com (2016-05-21)

Hey,

Do you have an update about this one?

Thanks.

Cheers,
João Lucas Melo Brasio.

### as...@chromium.org (2016-06-08)

Quick update - there have been some similar bug reports around web_accessible_resources and a fix landed for one of them, but I just checked and that doesn't fix this one. There are one or two other higher priority security bugs I'm looking at; then I'll be circling back to this one. 

### ja...@gmail.com (2016-06-17)

asargent@

Thanks for the feedback.

### ja...@gmail.com (2016-08-15)

asargent@

Do you have an update about this one?

### as...@chromium.org (2016-08-17)

I'm now circling back to have a look. 

### ja...@gmail.com (2016-08-19)

Ok. Thanks.
=)

### ji...@chromium.org (2016-08-19)

[Empty comment from Monorail migration]

### ja...@gmail.com (2016-09-16)

asargent@

Do you have an update about this bug?

### ja...@gmail.com (2016-09-28)

asargent@

Do you have an update about this bug?

### as...@chromium.org (2016-09-28)

I've been looking into some approaches for a fix - one that seems promising is checking web_accessible_resources in the ShouldFork method, returning false if the URL isn't listed. But that currently breaks two extensions tests:

ExtensionResourceRequestPolicyTest.LinkToWebAccessibleResources
ExtensionBrowserTest.WindowOpenNoPrivileges

The WindowOpenNoPrivileges essentially does the following: open the NTP, and call window.open to open some chrome-extension:// url. In conversation with Devlin and Nasko it sounds like in an ideal world we'd actually want to disallow such navigations if the url in question isn't listed in web_accessible_resources, but I need to look more into the history of that test and possibly gather some more data about how widely used this is to make sure we wouldn't cause a lot of breakage. I also need to look more into why the LinkToWebAccessibleResources test fails. 


### as...@chromium.org (2016-09-28)

Quick update:

-The ExtensionResourceRequestPolicyTest.LinkToWebAccessibleResources failure I had observed was likely a flake, since I haven't been able to reproduce it. 

-The ExtensionBrowserTest.WindowOpenNoPrivileges test was added a long time ago in r25329 (https://codereview.chromium.org/172120), before we even had the concept of web_accessible_resources (which was added in r115401 http://codereview.chromium.org/8849010). 

So we likely can just adjust the WindowOpenNoPrivileges test to make the resource being opened web_accessible. That still leaves open the question of how many existing uses of window.open(<non-web-accessible-url>) we might break. I'm going to look into getting some data on that. 
 

### ja...@gmail.com (2017-01-12)

Any news?

### ja...@gmail.com (2017-05-04)

[Comment Deleted]

### ja...@gmail.com (2017-05-04)

[Comment Deleted]

### ja...@gmail.com (2017-05-04)

Can I disclose the bug?

### as...@chromium.org (2017-05-04)

I'm no longer working on chrome, reassigning to Devlin for triage. 


### ja...@gmail.com (2017-06-28)

Update?

### rd...@chromium.org (2017-06-28)

This bug clearly slipped through the cracks.  I'll see if I can reprioritize.  That said, you have patiently waited for a *long* time, so I think you should be allowed to disclose this - but please wait for confirmation from nasko@ or creis@.

nasko@, creis@, what do you think?

### ja...@gmail.com (2017-06-28)

Thanks, Devlin.

Is this issue valid for the bug bounty program?

### na...@chromium.org (2017-06-28)

We have been given more than enough time to act on this bug. It is unfortunate it did slip through, but that should not impact the decision to disclose or not. 

As to the rules of the VRP program, I'm not certain, so adding awhalley@ to help answer whether disclosure of the bug will disqualify it.

### ja...@gmail.com (2017-06-29)

nasko@,

Thanks.
;-)

### cr...@chromium.org (2017-06-29)

+alexmos@ and nick@, who have looked at some web accessible resources issues as well and may have thoughts on how to fix.

[Monorail components: UI>Browser>Navigation]

### ja...@gmail.com (2017-07-27)

Hello,

Do you have any update?

### ja...@gmail.com (2017-08-04)

Hello,

Can you guys submit this bug to the VRP panel since I waited for a long time?

Thanks.

### aw...@chromium.org (2017-08-07)

Hello! I'm afraid that we only consider bugs for reward once they have been fixed. Also, fair warning that we tend not to reward low severity bugs often, but I'll make sure this goes in front of the panel when it is fixed and ensure there's a second look at the severity rating.

### rd...@chromium.org (2017-08-09)

@awhalley Even when it's us that's clearly dropped the ball?  In this particular case, the reporter filed the bug >1 year ago, and it's been unaddressed to a combination of lower priority, other P0s, and shifting people - but it's unfortunate that the holes in our process cause more issues...

@jaumlucas, sincerest apologies on this.  I'm bumping priority on this and going to try to push a fix this week so that we can get this through to panel.  Sorry again for all the (extremely!) long delays, and thanks so much for your patience.

### ja...@gmail.com (2017-08-09)

@rdevlin

I appreciate the increase in the priority but don't worry.

Since 2011 I have sent hundreds of security bugs to Google (Web, Android, Chrome, Apps, etc.), and you guys are awesome every time, I have no complaints at all.

I understand that this is a low severity bug and it unintentionally slipped through the cracks. Sometimes it happens.

Many thanks for your consideration and hard work.

Please let me know once this bug is fixed.

### aw...@chromium.org (2017-08-09)

jaumlucas@ - thanks for your understanding!

### bu...@chromium.org (2017-08-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f1afce25b3f94d8bddec69b08ffbc29b989ad844

commit f1afce25b3f94d8bddec69b08ffbc29b989ad844
Author: Devlin Cronin <rdevlin.cronin@chromium.org>
Date: Sat Aug 19 01:21:48 2017

[Extensions] Update navigations across hypothetical extension extents

Update code to treat navigations across hypothetical extension extents
(e.g. for nonexistent extensions) the same as we do for navigations
crossing installed extension extents.

Bug: 598265

Change-Id: Ibdf2f563ce1fd108ead279077901020a24de732b
Reviewed-on: https://chromium-review.googlesource.com/617180
Commit-Queue: Devlin <rdevlin.cronin@chromium.org>
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Reviewed-by: Nasko Oskov <nasko@chromium.org>
Cr-Commit-Position: refs/heads/master@{#495779}
[modify] https://crrev.com/f1afce25b3f94d8bddec69b08ffbc29b989ad844/chrome/browser/extensions/app_process_apitest.cc
[modify] https://crrev.com/f1afce25b3f94d8bddec69b08ffbc29b989ad844/chrome/browser/extensions/chrome_content_browser_client_extensions_part.cc
[modify] https://crrev.com/f1afce25b3f94d8bddec69b08ffbc29b989ad844/chrome/browser/extensions/extension_browsertest.cc
[modify] https://crrev.com/f1afce25b3f94d8bddec69b08ffbc29b989ad844/chrome/browser/extensions/extension_browsertest.h
[modify] https://crrev.com/f1afce25b3f94d8bddec69b08ffbc29b989ad844/chrome/browser/extensions/isolated_app_browsertest.cc
[modify] https://crrev.com/f1afce25b3f94d8bddec69b08ffbc29b989ad844/chrome/browser/extensions/process_management_browsertest.cc
[modify] https://crrev.com/f1afce25b3f94d8bddec69b08ffbc29b989ad844/chrome/browser/extensions/window_open_apitest.cc
[modify] https://crrev.com/f1afce25b3f94d8bddec69b08ffbc29b989ad844/chrome/common/extensions/extension_process_policy.cc
[add] https://crrev.com/f1afce25b3f94d8bddec69b08ffbc29b989ad844/chrome/common/extensions/extension_process_policy_unittest.cc
[modify] https://crrev.com/f1afce25b3f94d8bddec69b08ffbc29b989ad844/chrome/test/BUILD.gn


### ja...@gmail.com (2017-08-28)

Thanks @rdevlin.

### rd...@chromium.org (2017-08-28)

This should be fixed, I think.  Given we're close to stable cut for M61, it's probably not worth merging back, but could be - I'll let some security folks weigh in.

I'm also pretty sure there are going to be other similar situations to this - we have a bunch of different places we check for web accessible resources + installed extensions, etc, so there are probably other edge cases.  We should really coalesce them if we can.

### aw...@chromium.org (2017-08-28)

[Empty comment from Monorail migration]

### na...@chromium.org (2017-08-28)

IMHO, this doesn't warrant merge to M61, given we are very close to branch point and the severity is low.

### aw...@google.com (2017-08-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-08-29)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-09-01)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2017-09-01)

The VRP panel decided to award $500 for this bug.  Many thanks!  Also, when this bug is included in release notes, how would you like to be credited?

### ja...@gmail.com (2017-09-01)

Hey awhalley@,

Thank you very much.

Credit: João Lucas Melo Brasio (https://www.whitehathackers.com.br).

### aw...@chromium.org (2017-09-01)

[Empty comment from Monorail migration]

### rd...@chromium.org (2017-09-08)

[Empty comment from Monorail migration]

### aw...@google.com (2017-10-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-10-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-06)

This issue was migrated from crbug.com/chromium/598265?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Platform>Extensions, UI>Browser>Navigation]
[Monorail mergedwith: crbug.com/chromium/746567]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083949)*

# Security: Any extension can debug any other extension (e.g. crosh)

| Field | Value |
|-------|-------|
| **Issue ID** | [40079440](https://issues.chromium.org/issues/40079440) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions, Platform>Extensions>API |
| **Reporter** | is...@gmail.com |
| **Assignee** | rd...@chromium.org |
| **Created** | 2014-04-27 |
| **Bounty** | $1,500.00 |

## Description

Steps to reproduce the vulnerability:

1. From the context of a Chrome extension with privileges ["tabs","debugger","downloads"] installed on any version of Chrome OS since version 18:

2. Create a window with a location in the domain of the crosh console, such as <chrome-extension://pnhechapfaindjhompbnflcldabbghjo/html/nassh_google_relay.html> (loads faster) or crosh.html. You can make this very small and place it behind current windows defocused or off-screen in order to hide it from the user.

3. Attach a debugger to the crosh tab with chrome.debugger.attach(crosh_tab, "1.0", function()).

4. Wait for the tab to load if you go to crosh.html. I polled chrome.tabs.get(crosh_tab.tabId, function(tab)) for tab.status every 30ms.

5. Execute code in the crosh tab with chrome.debugger.sendCommand(crosh_tab, "Runtime.evaluate", {expression: code}, function(result)).
   Your payload can either be in the form of term_.command.sendString_() (if you loaded crosh.html) or by interfacing with chrome.terminalPrivate (if you loaded any page under chrome-extension://pnhechapfaindjhompbnflcldabbghjo/html/).

    5a. window.addEventListener("onload", function() {
            // if you loaded crosh.html you may need to set a timeout of ~2500ms (on haswell chromebooks) before running this
            window.onbeforeunload = null; // get rid of the closing confirmation
            // payload here
            window.close();
        });

On Chrome OS 34, whether the user is in developer mode or not (which gives them root access to the "shell" command in the crosh shell), there is quite a lot of harm that can be caused. 

Using stable channel software on official hardware[1] (Dell Chromebook 11) not in developer mode, I have quite a lot of access in crosh looking at help_advanced. Specifically, by using the "downloads" permission in conjunction with network_diag, network_logging, wpa_debug, and ff_debug it should be possible to snoop on a lot of private user data.

I can wiretap the user's microphone with the "download" permission in conjection with sound record <seconds>.

Various other harmful things I can do are: disable the touchpad (with tpcontrol), mess with wifi and cellular hardware, general DoS of the Chrome OS device, invoking a powerwash of the user's device (using the rollback command). Chaps (Chrome's PKCS #11 implementation) can be put into debug logging mode with chaps_debug start.

If you have physical proximity to the user, you can configure the cellular hardware to connect to a malicious APN and MitM user's connections. I'm not sure if you can confiure the wifi hardware, but if you can, the same physical proximity constraints apply.

As soon as the user enters developer mode (e.g. to install an Ubuntu chroot with crouton), an extension using this exploit can immediately get root access (and do anything it wants!--complete bypass of all Chrome security), unless the user sets a developer mode password (using sudo chromeos-setdevpasswd) before installing the extension.


In what Browser/OS/Platform/Version?

Since Chrome OS 18. The later the Chrome version the more I can do in the non-root crosh shell. No matter what version since Chrome OS 18, I can do anything at all if the user is in developer mode, as I can get root from crosh with the "shell" command.

Additional details:

[1]: Version 34.0.1847.134
     Platform 5500.130.0 (Official Build) stable-channel wolf
     Firmware Google_Wolf.4389.24.53

The "tabs" permission is not necessary for the vulnerability but it helps me exploit it faster.
The "downloads" permission extends on the first vulnerability by allowing me to wiretap the user's microphone and networking from crosh commands that save said information to ~/Downloads.

## Timeline

### is...@gmail.com (2014-04-27)

s/onload/load/

### is...@gmail.com (2014-04-28)

To clarify on crosh_tab, i'm just referring to what you get with when using chrome.windows.create:

chrome.windows.create({
   url: "chrome-extension://pnhechapfaindjhompbnflcldabbghjo/html/nassh_google_relay.html",
   type: "popup",
   width: 1,
   height: 1/*
   etc.
*/}, function(crosh_window) {
    var crosh_tab = {tabId: crosh_window.tabs[0].id};
});

### is...@gmail.com (2014-04-28)

Also, when I refer to the cellular MitM stuff, I'm obviously not referring to the Dell Chromebook 11 (which has no cellular modems afaik), but these still apply on all of the cellular enabled Chromebooks such as the 3G Samsung ARM Chromebook I tested this on.

### is...@gmail.com (2014-04-28)

I noticed that if the Secure Shell extension (https://chrome.google.com/webstore/detail/secure-shell/pnhechapfaindjhompbnflcldabbghjo) isn't installed, chrome.window.create()ing those URLs crashes Chrome. Instead replace every instance of pnhechapfaindjhompbnflcldabbghjo in this bug report with nkoccljplnhpfnfiajclkommnmllphnl, which is the extension ID for the built-in crosh app which all Chrome OS installs have by default. You should no longer experience crashes while attempting to reproduce this vulnerability if you were before.

### wa...@chromium.org (2014-04-28)

Thanks for the report!

We'll need to go through it more closely to figure out exactly what is expected/not expected with 'debugger' permissions + crosh, as well as what makes sense for users.

### is...@gmail.com (2014-04-29)

Whatever happens, please understand that if you make /all extensions/ undebuggable (through chrome.debugger), a fully-featured Chrome IDE that runs in Chrome will no longer be able to assist with or automate debugging (which is pretty essential for an IDE).

The solution should probably be to make crosh accessible from a chrome:// WebUI URL (like chrome://shell or chrome://crosh) instead of chrome-extension://, since it's built-in anyways.

### ke...@chromium.org (2014-05-01)

[Empty comment from Monorail migration]

### ke...@chromium.org (2014-05-01)

[Empty comment from Monorail migration]

### is...@gmail.com (2014-06-04)

Nevermind @ not making all extensions undebuggable. Thai Duong expressed to me that this is a security vulnerability when I asked about https://code.google.com/p/end-to-end/, which says "Chrome’s design means that extensions should be safe against other extensions".

I'd like to broaden the scope of this vulnerability to that of "extensions are able to debug other extensions".

This vulnerability can be used to to steal private keys from End-to-End, following mostly the same process as above. Thai told me in an email regarding End-to-End that leaking End-to-End's private keys to other extensions is a critical vulnerability.

I guess the best course of action is to make extensions undebuggable by other extensions (without user input). I hope that you will consider making it possible with user input, where the user has to agree to a permission dialog when an extension attempts to debug another extension, so that a Chrome extension IDE extension is still possible.

### is...@gmail.com (2014-06-04)

Can you change OS to All?

### is...@gmail.com (2014-06-05)

Also, for some reason I didn't notice this at first, but the packet_capture command (regarding the crosh exploit) is ripe for abuse with this vuln as well.

### fe...@chromium.org (2014-06-05)

Do you have any special flags enabled for this to work?

### va...@chromium.org (2014-06-05)

[Empty comment from Monorail migration]

### me...@chromium.org (2014-06-05)

> Any extension can debug any other extension

Is this correct? Crosh is only available on Chrome OS, and on other platforms you need to set silent-extension-debugging-api flag to debug another extension.

### jo...@chromium.org (2014-06-05)

Step one of the original report:

"1. From the context of a Chrome extension with privileges ["tabs","debugger","downloads"] installed on any version of Chrome OS since version 18:"

Which is obviously expected. Mustafa, does the "debugger" permission not work without that flag?

### is...@gmail.com (2014-06-05)

@meacer: Silent debugging is for things like background pages, where you will never see the infobar that says that the tab is being debugged by [extension name]. For this exploit, you will want to use the chrome.windows.create API as detailed in https://crbug.com/chromium/367567#c2.

### pa...@chromium.org (2014-06-05)

Low because the precondition is that the victim must install a malicious extension.

### me...@chromium.org (2014-06-18)

> does the "debugger" permission not work without that flag?

debugger permission by itself doesn't allow debugging other extensions' background pages, but it allows debugging other unprivileged chrome-extension:// pages. Unprivileged pages can still pass messages to the background pages though, so this is not good. IMO this can be medium severity too.

@iSephr:
>   Your payload can either be in the form of term_.command.sendString_() (if you loaded crosh.html) or by interfacing with chrome.terminalPrivate (if you loaded any page under chrome-extension://pnhechapfaindjhompbnflcldabbghjo/html/).

Can you explain the terminalPrivate part? The debugged chrome-extension:// page shouldn't have access to that API, do you mean accessing that API by using term_.command.sendString() and passing messages to crosh background page?

@kalman: We should block all chrome-extension:// pages (not only background pages) from being debugged without a command line flag, otherwise it's still possible to interface with the background scripts by passing messages. This will probably be a breaking change.

### is...@gmail.com (2014-06-18)

> Can you explain the terminalPrivate part? The debugged chrome-extension:// page shouldn't have access to that API, do you mean accessing that API by using term_.command.sendString() and passing messages to crosh background page?

term_.command.sendString() is just one of hterm's interfaces with chrome.terminalPrivate. I didn't delve that deep into the chrome.terminalPrivate API, and my local PoC loads crosh.html instead of nassh_google_relay.html, as I'd rather not learn how to directly interface with it when term_.command.sendString is adequate.

chrome.terminalPrivate is an interface available on any page under chrome-extension://nkoccljplnhpfnfiajclkommnmllphnl/ and is used by crosh.

### me...@chromium.org (2014-06-19)

> chrome.terminalPrivate is an interface available on any page under chrome-extension://nkoccljplnhpfnfiajclkommnmllphnl/ and is used by crosh.

Thanks for the clarification, that indeed seems to be true (any non-background page has access to all APIs). The command line flag should definitely apply to all chrome-extension:// pages in this case.

### [Deleted User] (2014-06-19)

Coming to this bug late - it seems pretty severe. If you can chrome.app.window create a page under the chrome-extension:// origin then it will create a privileged context. My read is that this effectively gives an extension with the "debugger" permission effective access to the union of all other installed extensions' permissions regardless of command line flag?

### jo...@chromium.org (2014-06-19)

That sounds correct, but Mustafa can confirm.

### is...@gmail.com (2014-06-19)

That is correct.

### js...@chromium.org (2014-06-20)

kalman@ I'm not sure if this is the same root issue as what's being hit in 386988, but for the moment I'm gong to assume it is and set it as a blocker.

### js...@chromium.org (2014-06-20)

[Empty comment from Monorail migration]

### [Deleted User] (2014-06-20)

@24 - it looks related.

note that the bug also mentions chrome.downloads, you should file a separate bug for that.

### jo...@chromium.org (2014-06-20)

Hi Ben,

How big of a fix do you think this issue needs? We've got two reports for this bug now.

Thanks!

### jo...@chromium.org (2014-06-20)

Ben as Owner so that he can assign to the appropriate person.

### [Deleted User] (2014-06-20)

Far out. The API is so blatantly wrong. Codesearch isn't finding the file for some reason, but it's here:

http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/extensions/api/debugger/debugger_api.cc?revision=HEAD&view=markup

line ~600.

The only protection is "if there is nowhere to attach an infobar" which covers neither extension options pages nor chrome:// URLs.

We should at least guard behind a CanExecuteScriptOnPage call, which automatically blacklists such URLs. There is a separate command line flag for allowing extension APIs on chrome URLs (kExtensionsOnChromeURLs). Maybe that should cover chrome-extension:// URLs as well.

Devlin or Yoyo can one of you take this?

### me...@chromium.org (2014-06-21)

^ Those should also cover urls like view-source:chrome://settings-frame/settings and about:settings-frame/settings.

### rd...@chromium.org (2014-06-21)

I'll take it on and see if I can't get a patch up on Monday.

### jo...@chromium.org (2014-06-25)

Hey Devlin, any updates on this?

### rd...@chromium.org (2014-06-25)

In review now.  https://codereview.chromium.org/352523003/ if you want to follow.

### bu...@chromium.org (2014-06-27)

------------------------------------------------------------------
r280354 | rdevlin.cronin@chromium.org | 2014-06-27T17:14:50.180894Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/extensions/api/debugger/debugger_api_constants.cc?r1=280354&r2=280353&pathrev=280354
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/extensions/api/debugger/debugger_extension_apitest.cc?r1=280354&r2=280353&pathrev=280354
   M http://src.chromium.org/viewvc/chrome/trunk/src/extensions/common/permissions/permissions_data_unittest.cc?r1=280354&r2=280353&pathrev=280354
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/test/data/extensions/api_test/debugger/background.js?r1=280354&r2=280353&pathrev=280354
   M http://src.chromium.org/viewvc/chrome/trunk/src/extensions/common/permissions/permissions_data.cc?r1=280354&r2=280353&pathrev=280354
   M http://src.chromium.org/viewvc/chrome/trunk/src/extensions/common/url_pattern.cc?r1=280354&r2=280353&pathrev=280354
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/extensions/api/debugger/debugger_api_constants.h?r1=280354&r2=280353&pathrev=280354
   M http://src.chromium.org/viewvc/chrome/trunk/src/extensions/common/permissions/permissions_data.h?r1=280354&r2=280353&pathrev=280354
   M http://src.chromium.org/viewvc/chrome/trunk/src/extensions/common/url_pattern.h?r1=280354&r2=280353&pathrev=280354
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/extensions/api/debugger/debugger_api.cc?r1=280354&r2=280353&pathrev=280354
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/extensions/api/debugger/debugger_apitest.cc?r1=280354&r2=280353&pathrev=280354

Have the Debugger extension api check that it has access to the tab

Check PermissionsData::CanAccessTab() prior to attaching the debugger.

BUG=367567

Review URL: https://codereview.chromium.org/352523003
-----------------------------------------------------------------

### bu...@chromium.org (2014-06-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/684a212a93141908bcc10f4bc57f3edb53d2d21f

commit 684a212a93141908bcc10f4bc57f3edb53d2d21f
Author: rdevlin.cronin@chromium.org <rdevlin.cronin@chromium.org@0039d316-1c4b-4281-b951-d872f2087c98>
Date: Fri Jun 27 17:14:50 2014

Have the Debugger extension api check that it has access to the tab

Check PermissionsData::CanAccessTab() prior to attaching the debugger.

BUG=367567

Review URL: https://codereview.chromium.org/352523003

git-svn-id: svn://svn.chromium.org/chrome/trunk/src@280354 0039d316-1c4b-4281-b951-d872f2087c98



### rd...@chromium.org (2014-06-30)

Change submitted and seems sticky.  Marking as fixed.

### cl...@chromium.org (2014-06-30)

[Empty comment from Monorail migration]

### jo...@chromium.org (2014-06-30)

c#21 and c#29 seem to suggest there were several checks missing here, maybe this warrants Sec-Sev-Medium.

### is...@gmail.com (2014-06-30)

The fix looks good :)

My only concern is that I would like the severity to be reconsidered in the context of crosh on Chrome OS. It's quite severe in that situation, and a full root exploit in developer mode. In my opinion, this should warrant medium severity, also taking into account the need to install an extension.

I talked with jorgelo privately on IRC regarding this and he voiced support and told me to go here to bring up my concern. meacer also brought up how this can be medium in https://crbug.com/chromium/367567#c18.

Do any of you feel the same?

### rd...@chromium.org (2014-06-30)

I have no objections to sec-sev-medium, but I leave it up to the security team to have final say.

### ti...@chromium.org (2014-07-07)

Bumping up sec severity based on prior comments.

### ti...@chromium.org (2014-07-07)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-07-08)

amineer@ - Merge-Requested for M37 (branch 2062)

### am...@chromium.org (2014-07-15)

inferno@, can we ship m37 without this change?  The CL is more extensive than I would like to approve at this point.  If you feel strongly though, given it's been on canary for > 2 weeks, we may be able to accommodate.

### am...@chromium.org (2014-07-15)

Merge approved for M37 branch 2062.

### in...@chromium.org (2014-08-02)

 rdevlin.cronin@, please merge to m37 soon.

### bu...@chromium.org (2014-08-04)

------------------------------------------------------------------
r287394 | kalman@chromium.org | 2014-08-04T19:39:52.863071Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/2062/src/chrome/browser/extensions/api/debugger/debugger_api_constants.cc?r1=287394&r2=287393&pathrev=287394
   M http://src.chromium.org/viewvc/chrome/branches/2062/src/chrome/browser/extensions/api/debugger/debugger_extension_apitest.cc?r1=287394&r2=287393&pathrev=287394
   M http://src.chromium.org/viewvc/chrome/branches/2062/src/extensions/common/permissions/permissions_data_unittest.cc?r1=287394&r2=287393&pathrev=287394
   M http://src.chromium.org/viewvc/chrome/branches/2062/src/chrome/test/data/extensions/api_test/debugger/background.js?r1=287394&r2=287393&pathrev=287394
   M http://src.chromium.org/viewvc/chrome/branches/2062/src/extensions/common/permissions/permissions_data.cc?r1=287394&r2=287393&pathrev=287394
   M http://src.chromium.org/viewvc/chrome/branches/2062/src/extensions/common/url_pattern.cc?r1=287394&r2=287393&pathrev=287394
   M http://src.chromium.org/viewvc/chrome/branches/2062/src/chrome/browser/extensions/api/debugger/debugger_api_constants.h?r1=287394&r2=287393&pathrev=287394
   M http://src.chromium.org/viewvc/chrome/branches/2062/src/extensions/common/permissions/permissions_data.h?r1=287394&r2=287393&pathrev=287394
   M http://src.chromium.org/viewvc/chrome/branches/2062/src/extensions/common/url_pattern.h?r1=287394&r2=287393&pathrev=287394
   M http://src.chromium.org/viewvc/chrome/branches/2062/src/chrome/browser/extensions/api/debugger/debugger_api.cc?r1=287394&r2=287393&pathrev=287394
   M http://src.chromium.org/viewvc/chrome/branches/2062/src/chrome/browser/extensions/api/debugger/debugger_apitest.cc?r1=287394&r2=287393&pathrev=287394

Merge 280354 "Have the Debugger extension api check that it has ..."

> Have the Debugger extension api check that it has access to the tab
> 
> Check PermissionsData::CanAccessTab() prior to attaching the debugger.
> 
> BUG=367567
> 
> Review URL: https://codereview.chromium.org/352523003

TBR=rdevlin.cronin@chromium.org

Review URL: https://codereview.chromium.org/439843002
-----------------------------------------------------------------

### bu...@chromium.org (2014-08-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6bc5985086b44b73590ae17ded63a08434762613

commit 6bc5985086b44b73590ae17ded63a08434762613
Author: kalman@chromium.org <kalman@chromium.org@0039d316-1c4b-4281-b951-d872f2087c98>
Date: Mon Aug 04 19:39:52 2014

Merge 280354 "Have the Debugger extension api check that it has ..."

> Have the Debugger extension api check that it has access to the tab
> 
> Check PermissionsData::CanAccessTab() prior to attaching the debugger.
> 
> BUG=367567
> 
> Review URL: https://codereview.chromium.org/352523003

TBR=rdevlin.cronin@chromium.org

Review URL: https://codereview.chromium.org/439843002

git-svn-id: svn://svn.chromium.org/chrome/branches/2062/src@287394 0039d316-1c4b-4281-b951-d872f2087c98



### in...@chromium.org (2014-08-06)

[Empty comment from Monorail migration]

### mb...@chromium.org (2014-08-19)

[Empty comment from Monorail migration]

### mb...@chromium.org (2014-08-22)

Thanks for the report! This qualifies for a $1500 reward. Someone should be reaching out to you soon with additional details.

How would you like to be credited when we mention this bug in our release notes?

### is...@gmail.com (2014-08-22)

I'd like to be credited with my name, Eli Grey, linked to either my Twitter or my website (@sephr or http://eligrey.com, and yeah I know that my website is down atm). Thanks for the reward :)

### is...@gmail.com (2014-08-26)

[Comment Deleted]

### is...@gmail.com (2014-08-26)

[Comment Deleted]

### ti...@chromium.org (2014-09-18)

Hey Eli,

You should be hear from the finance team next week. If you don't hear from them, please contact me directly or update this bug. Bolierplate text below for your reading pleasure:

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### is...@gmail.com (2014-09-19)

Alright, sounds good.

### cl...@chromium.org (2014-10-06)

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

This issue was migrated from crbug.com/chromium/367567?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Platform>Extensions, Platform>Extensions>API]
[Monorail blocking: crbug.com/chromium/386988]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40079440)*

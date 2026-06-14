# Security: macOS: the option to "Allow JavaScript From Apple Events" can easily be activated by malicious apps.

| Field | Value |
|-------|-------|
| **Issue ID** | [40092604](https://issues.chromium.org/issues/40092604) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>PlatformIntegration |
| **Platforms** | Mac |
| **Reporter** | an...@hegenberg.me |
| **Assignee** | rs...@chromium.org |
| **Created** | 2018-10-03 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

Google Chrome has recently disabled triggering JavaScript using Apple Events on macOS by default - which was a very good idea. As a user I expected this to protect me from attacks based on malicious apps that send Apple Events. However it turns out that it is pretty easy to bypass because the setting can be enabled by malicious apps easily.

There are at least two different situations:  

\* If the attacking app has access to the macOS Accessibility API enabled it can just enable the setting in Google Chrome by triggering the menubar item View => Developer => Allow JavaScript from Apple Events.

\* If the attacking app doesn’t have access to the macOS Accessibility API it can just assign a keyboard shortcut (using the functionality provided in System Preferences => Keyboard => Shortcuts => App Shortcuts) to the Google Chrome menubar item View => Developer => "Allow JavaScript from Apple Events" using two commands that were completely unsecured until macOS Mojave:   

defaults write -g NSUserKeyEquivalents -dict-add "Allow JavaScript from Apple Events" "@~^x"  

 defaults write com.apple.universalaccess "com.apple.custommenu.apps" -array-add NSGlobalDomain

This shortcut can then be triggered using Apple Events easily. On macOS Mojave this doesn’t work anymore because com.apple.universalaccess is now secured. However even on Mojave this works if the user has added any other shortcut globally in System Preferences => Keyboard => Shortcuts => App Shortcuts before. It is easy for an attacker to achieve this by tricking the user to add a shortcut there.

I think there may also be another way to trigger the menu item on Mojave, but I will need to do some more testing to verify this.

In general I think this menu item should be secured by an extra (secured) alert (like in Safari) or be moved to the Chrome settings page instead.

**VERSION**  

Chrome Version: Tested on Version 70.0.3538.35 (beta) and on 69.0.3497.100 (stable release)

Operating System: tested on macOS 10.13.6 and macOS 10.14.0

**REPRODUCTION CASE**  

See the attached Apple Scripts. They can be executed using the Apple Script Editor for testing.

The script „ExecuteJavaScriptUsingKeyboardShortcut\_Source“ assigns a keyboard shortcut to the Chrome menu item „Allow JavaScript from Apple Events“. Then it triggers the keyboard shortcut to enable JavaScript execution. It works without any permissions until (including) macOS High Sierra.

The script “ExecuteJavascriptUsingAccessibility\_Source“ directly triggers the menubar item using Apple Script, but it requires Accessibility access for the executing app. This works on Mojave too.

## Attachments

- [ExecuteJavaScriptUsingKeyboardShortcut_Source.applescript](attachments/ExecuteJavaScriptUsingKeyboardShortcut_Source.applescript) (application/octet-stream, 821 B)
- [ExecuteJavascriptUsingAccessibility_Source.applescript](attachments/ExecuteJavascriptUsingAccessibility_Source.applescript) (application/octet-stream, 519 B)

## Timeline

### me...@chromium.org (2018-10-04)

Thanks for the report.

> * If the attacking app has access to the macOS Accessibility API enabled it can just enable the setting in Google Chrome by triggering the menubar item View => Developer => Allow JavaScript from Apple Events.

Please note that local attacks are outside of our threat modal. Chrome cannot defend against a malicious app that can use OS APIs to control Chrome's settings.

My understanding is that this was intended as a hardening measure and not an outright ban. 

markchang: Can you please decide what to do here (wontfix or not)?

### an...@hegenberg.me (2018-10-04)

But Chrome does a lot to prevent local attacks already. (E.g. not allowing automatic installation of extensions). Allowing arbitrary Java Script execution defeats the purpose of almost all other local security measures you have taken.

The problem is that a completely unprivileged app, running just with user permissions, can run arbitrary Java Script on any website when using the "keyboard shortcut based approach" I described. Pre Mojave there is no notification to the user at all about something running Java Script on a website when doing this.

I understand that if the user gives Accessibility permissions to an app, it's already too late. But a unprivileged app should not be able to do this. 

Safaris approach is to show at least an alert before enabling this, that alert can not be confirmed using programmatically created events.


### me...@chromium.org (2018-10-05)

We take measures to prevent local attacks, but we can't fully defend Chrome from a malicious user or software running on the same machine. https://chromium.googlesource.com/chromium/src/+/lkgr/docs/security/faq.md#Why-arent-physically_local-attacks-in-Chromes-threat-model gives more details on this.

In this example, the app is no longer unprivileged if it's granted Accessibility permission, though. That said, the Safari approach sounds simple and we could try something like that.

palmer, rsesek: Any thoughts on this?

[Monorail components: Internals>PlatformIntegration]

### pa...@chromium.org (2018-10-05)

Booping this to kerrnel, who is our macOS expert.

### an...@hegenberg.me (2018-10-05)

Only the first described approach requires accessibility. The other approach works without any privileges before Mojave and even on Mojave under the described circumstances. The only requirement is that the app is not sandboxed.

I believe this is a pretty big security issue because Chrome for many users is the main app and handles a lot of sensitive data.
The problem is not that Chrome can't protect from local attacks in general but that the ability to run
 Java Script from unpriviledged apps destroys the operating systems security measures. It would allow to install keyloggers and steal private data in a very sensitive context.

### ke...@chromium.org (2018-10-05)

rsesek@, you were involved in the Apple Events restrictions, right? WDYT?

### ke...@chromium.org (2018-10-05)

Also doesn't macOS mojave require users to go into settings manually to allow the accessibility permission?

### sh...@chromium.org (2018-10-06)

[Empty comment from Monorail migration]

### ma...@chromium.org (2018-10-08)

I read the attack vector being mostly about pre-mojave, since the a11y API is not protected.



### an...@hegenberg.me (2018-10-08)

The problem is that any unpriviledged app can assign a keyboard shortcut to any menu item in macOS. This includes the Chrome menu item which enables Java Script execution via Apple Script. It can then trigger the shortcut using Apple Script/Apple events and then execute arbitrary JavaScript in Chrome. See the ExecuteUsingKeyboardShortcut script I attached in the initial post.

The other example I posted (which was using Accessibility) was just meant for clarification. Accessibility permissions are NOT necessary to execute JavaScript in Chrome.

(on Mojave it got a bit harder to assign a keyboard shortcut to the menu item, but it is still possible)

### an...@hegenberg.me (2018-10-08)

But I definitely agree it is mostly pre-Mojave because there the user won't notice anything (Especially because sending keystrokes on Mojave got harder).

Still, I think a significant number of users will continue to use Chrome on older macOS versions.

### an...@hegenberg.me (2018-10-08)

Sorry one more comment:
I just noticed that (pre-Mojave) executing Java Script is also possible by having an app "type" the Java Script into the address bar. Even if the "Allow Apple Events From Java Script" option is disabled.
If that's the desired behavior it doesn't make sense to fix the issue because any app that could use the Apple Events could also type text into the address bar (pre-Mojave).

Just note that Safari has much better security in this area. It doesn't allow Java Script from the address bar by default and it doesn't allow Java Script from Apple Events by default. In Safari both must explicitly be enabled and can not be enabled using programatically generated events.






### rs...@chromium.org (2018-10-30)

Catching up on email post-OOO.

Assigning a keyboard shortcut to the menu item and then invoking it is pretty novel - we should try to defend against that because it shouldn't be hard to do. I was wondering if the setting were to move into chrome://settings if that would be sufficient, but I suspect that a script could navigate to chrome://settings and then simulate clicks/tab key navigation to enable it.

I think we can partially protect the menu item by doing a few things:

- Checking the CGEventGetIntegerValueField(…, kCGEventSourceUnixProcessID) of the event when handling the menu item action
- Blocking the action if there's a key equivalent associated with the menu item (or somehow determining that it was a synthetic key event)

C.f. https://objective-see.com/talks/Wardle_SyScan2018.pdf

However, https://crbug.com/chromium/891697#c12 about typing in javascript navigations by sending the key events to the Omnibox would indeed bypass this altogether. That sounds like a different issue, though. Could you file a new bug for that?

### bu...@chromium.org (2018-10-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0328261c41b1b7495e1d4d4cf958f41a08aff38b

commit 0328261c41b1b7495e1d4d4cf958f41a08aff38b
Author: Robert Sesek <rsesek@chromium.org>
Date: Wed Oct 31 15:48:06 2018

mac: Do not let synthetic events toggle "Allow JavaScript From AppleEvents"

Bug: 891697
Change-Id: I49eb77963515637df739c9d2ce83530d4e21cf15
Reviewed-on: https://chromium-review.googlesource.com/c/1308771
Reviewed-by: Elly Fong-Jones <ellyjones@chromium.org>
Commit-Queue: Robert Sesek <rsesek@chromium.org>
Cr-Commit-Position: refs/heads/master@{#604268}
[modify] https://crrev.com/0328261c41b1b7495e1d4d4cf958f41a08aff38b/chrome/browser/ui/BUILD.gn
[modify] https://crrev.com/0328261c41b1b7495e1d4d4cf958f41a08aff38b/chrome/browser/ui/browser_command_controller.cc
[delete] https://crrev.com/623a610238aef2021e5230c2069d3793c117fcc8/chrome/browser/ui/browser_commands_mac.cc
[modify] https://crrev.com/0328261c41b1b7495e1d4d4cf958f41a08aff38b/chrome/browser/ui/browser_commands_mac.h
[add] https://crrev.com/0328261c41b1b7495e1d4d4cf958f41a08aff38b/chrome/browser/ui/browser_commands_mac.mm


### rs...@chromium.org (2018-10-31)

I split out the report in #12 to https://crbug.com/chromium/900654 (so no need to file a separate bug as I asked in #13).

The original report should be fixed by #14 though.

### sh...@chromium.org (2018-11-01)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-11-05)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-11-12)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-11-12)

Hi andreas@, the Chrome VRP panel decided top award $500 for this bug, thanks! A member of our finance team will be in touch to arrange payment. Also, how would you like to be credited in Chrome release notes?

### an...@hegenberg.me (2018-11-12)

Oh that is very nice, thank you!
If you want to credit me you can use: "Andreas Hegenberg (folivora.AI GmbH)"


### aw...@google.com (2018-12-03)

Noted, thanks!

### aw...@google.com (2018-12-03)

[Empty comment from Monorail migration]

### aw...@google.com (2019-01-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-01-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2019-02-19)

[Empty comment from Monorail migration]

### is...@google.com (2019-02-19)

This issue was migrated from crbug.com/chromium/891697?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092604)*

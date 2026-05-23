# Guessing the URL a cross-origin iframe was redirected to by listening to the load event

| Field | Value |
|-------|-------|
| **Issue ID** | [40057223](https://issues.chromium.org/issues/40057223) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Sandbox>SiteIsolation, UI>Browser>Navigation |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2021-09-10 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

It is possible to try to guess the URL that a cross-origin iframe was redirected to by listening to the load event of the iframe and then redirecting it to the URL you are trying to guess appended by a random hash.

After that, there are two possible outcomes:

1. If you redirect the iframe to the correct URL the iframe was redirected to, no load event will be triggered.
2. If you redirect the iframe to a different URL the iframe was redirected to, the load event will be triggered.

An attacker then would be able to infer the URL of a cross-origin iframe and thus leak sensitive information that shouldn't be available to the attacker.

This likely happens because a navigation to the current URL is treated as a soft reload and it doesn't trigger the load event (unlike a normal navigation).

This issue is similar to <https://crbug.com/chromium/1208614> but instead, it leverages and exploits the load event rather than the changes in history.length.

**VERSION**  

Chrome Version: 93.0.4577.63 (Official Build) (64-bit)  

Chrome Version: 95.0.4638.0 (Official Build) (64-bit)  

Operating System: Windows 10

**REPRODUCTION CASE**

1. Download both "me.php" and "victimName.php" and host the files in a PHP server (this is needed to simulate the server a victim is accessing).
2. Download "attack.html" (you don't need to host it on a server).
3. In the "attack.html" file you will need to change the domains in the URLs located in the "tryToGuessURL" function calls so that they match the correct domain of your server. By default, the attack is assuming the files can be found on "<http://localhost/victimName.php>" and "<http://localhost/me.php>".
4. Open the "attack.html" file and after a few seconds two alert dialogs will show up saying whether you correctly guessed the URL that the iframe was redirected or not.

**CREDIT INFORMATION**  

Reporter credit: Luan Herrera (@lbherrera\_)

## Attachments

- [me.php](attachments/me.php) (text/plain, 224 B)
- [victimName.php](attachments/victimName.php) (text/plain, 66 B)
- [attack.html](attachments/attack.html) (text/plain, 1.0 KB)

## Timeline

### [Deleted User] (2021-09-10)

[Empty comment from Monorail migration]

### ad...@google.com (2021-09-10)

This reproduction case works for me on Ubuntu (Redshell). Packages I needed to install (some of which probably weren't necessary)
sudo apt-get install php7.2-mysql php-db php7.2-mbstring php7.2-curl php7.2-zip php7.2-gd php7.2-intl apache2 php libapache2-mod-php
then put the two files in /var/www/html, chmod a+r and it works just as described. I used ASAN 902206, which is ~M93.

So I think this is a valid cross-origin leak. Cross-origin data leaks are high severity. I think this may well be mitigated down to Medium severity by the need for the attacker to guess specific URIs, but I'll leave the site isolation team to modify the severity if they think so. (Medium would also better match https://bugs.chromium.org/p/chromium/issues/detail?id=1208614#c36).

lukasza@, would you mind taking a look here and trying to route this to the right person?

[Monorail components: Internals>Sandbox>SiteIsolation]

### ad...@google.com (2021-09-10)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-10)

[Empty comment from Monorail migration]

### lu...@chromium.org (2021-09-10)

+domenic@ since it seems that this aspect of navigation behavior is web visible and therefore changes here should probably affect specs and/or other browsers

[Monorail components: UI>Browser>Navigation]

### lu...@chromium.org (2021-09-10)

Let me tentatively assign to japhet@ who has kindly worked on fixing the earlier https://crbug.com/chromium/1208614.  I wonder if a similar fix (never treating cross-origin-initiated navigations as same-doc or soft reload) might be possible here.

### cr...@chromium.org (2021-09-10)

https://crbug.com/chromium/1248444#c2: I think I agree this sounds like Medium severity, based on your note and issue https://bugs.chromium.org/p/chromium/issues/detail?id=1208614#c36.  Happy to correct it if it turns out to be worse than that.

### [Deleted User] (2021-09-11)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-09-24)

japhet: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ja...@chromium.org (2021-09-29)

If I'm reading the repro correctly and observing existing behavior, what's happening is that we don't fire onload for cross-origin *same-document* navigations. If the cross-origin initiator provides the exact url of its victim, a soft-reload happens, and because that counts as a cross-document naivgation (i.e., there is a new document object), we fire onload. But when only the fragment changes, we reuse the same document, and we don't fire onload in that case (for either inner window or the iframe element).

I'll see what breaks if we always fire iframe onload for cross-origin-initiated same-document navigations.

### ja...@chromium.org (2021-09-30)

[Empty comment from Monorail migration]

### ra...@chromium.org (2021-10-07)

Interesting! I think we should go by "is direct parent cross-origin or not" instead of "is initiator cross origin or not", which is a bit different than the history.length bug (crbug.com/1208614). With the history.length bug, it's possible for any frame to observe history.length, so it makes sense to use initiator. With the iframe load event, I think only the direct parent (the one who actually embeds the iframe) can observe the event, and a same-origin parent might have more assumptions about the timing of the load events of its same-origin child frame (so firing load events in more occasions might break some of those assumptions).



### gi...@appspot.gserviceaccount.com (2021-10-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5f8ddef5a678553c9bb1491cd5710788e6d571b3

commit 5f8ddef5a678553c9bb1491cd5710788e6d571b3
Author: Nate Chapin <japhet@chromium.org>
Date: Thu Oct 14 20:24:32 2021

Fire iframe onload for cross-origin-initiated same-document navigations

A cross-origin initiator can check whether or not onload fired to
guess the url of a target frame. Always firing onload makes it
appear to be a cross-document navigation, even when it wasn't.

Bug: 1248444
Change-Id: I79249cb441f61ac6cab65ab9e5dd4a44b291bc4a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3193885
Commit-Queue: Nate Chapin <japhet@chromium.org>
Reviewed-by: Rakina Zata Amni <rakina@chromium.org>
Cr-Commit-Position: refs/heads/main@{#931681}

[modify] https://crrev.com/5f8ddef5a678553c9bb1491cd5710788e6d571b3/third_party/blink/web_tests/http/tests/navigation/same-origin-fragment-navigation-is-sync-expected.txt
[modify] https://crrev.com/5f8ddef5a678553c9bb1491cd5710788e6d571b3/third_party/blink/web_tests/http/tests/navigation/same-origin-fragment-navigation-is-sync.html
[modify] https://crrev.com/5f8ddef5a678553c9bb1491cd5710788e6d571b3/third_party/blink/web_tests/http/tests/navigation/cross-origin-fragment-navigation-is-async-expected.txt
[modify] https://crrev.com/5f8ddef5a678553c9bb1491cd5710788e6d571b3/third_party/blink/web_tests/http/tests/navigation/cross-origin-fragment-navigation-is-async.html
[modify] https://crrev.com/5f8ddef5a678553c9bb1491cd5710788e6d571b3/third_party/blink/renderer/core/loader/document_loader.cc


### [Deleted User] (2021-10-15)

japhet: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-10-26)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ja...@chromium.org (2021-10-27)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-29)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-29)

[Empty comment from Monorail migration]

### am...@google.com (2021-11-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-11-03)

Congratulations, Luan! The VRP panel has decided to award you $5000 for this report! Thanks for this report and nice work! 

### am...@google.com (2021-11-04)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-01-04)

[Empty comment from Monorail migration]

### am...@google.com (2022-01-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1248444?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>Sandbox>SiteIsolation, UI>Browser>Navigation]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057223)*

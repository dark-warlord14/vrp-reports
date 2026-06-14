# Bypass extension manifest permission

| Field | Value |
|-------|-------|
| **Issue ID** | [40089159](https://issues.chromium.org/issues/40089159) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals, Platform>Extensions |
| **Reporter** | ku...@gmail.com |
| **Assignee** | aa...@chromium.org |
| **Created** | 2011-03-22 |
| **Bounty** | $1,337.00 |

## Description

Test chrome 11.0.696.16 dev windows xp sp3

from https://crbug.com/chromium/76666



## Attachments

- deleted (application/octet-stream, 0 B)
- [testcase.zip](attachments/testcase.zip) (application/zip; charset=binary, 1.7 KB)
- deleted (application/octet-stream, 0 B)
- [access chrome.google.com.crx](attachments/access chrome.google.com.crx) (application/octet-stream; charset=binary, 971 B)
- deleted (application/octet-stream, 0 B)
- [access file.crx](attachments/access file.crx) (application/octet-stream; charset=binary, 933 B)

## Timeline

### in...@chromium.org (2011-03-22)

Kuzzcc, can you please provide a description of what the problem, which manifest permission is being bypassed, how, etc.

### ku...@gmail.com (2011-03-23)

manifest.json 
====
"permissions": ["tabs", "http://www.google.cn/*"]

this extension only can access  http://www.google.cn/*

when use chrome.tabs.update(tabid, {url: 'javascript:alert(document.domain)'})
/* tabid is http://www.baidu.com */
user will get 'Error during tabs.update: Cannot access contents of url "http://www.baidu.com/". Extension manifest must request permission to access this host.'

when a page is spoofed, extension can bypass this permission 


### ku...@gmail.com (2011-03-23)

Blocker pick up domain from address bar not document.domain
popup blocker got same issue


### js...@chromium.org (2011-03-23)

I get it. You're spoofing with https://crbug.com/chromium/76666 and using that to access a different origin. Even if after https://crbug.com/chromium/76666 is fixed, it seems like the way we're checking could be vulnerable to a race between the document state and the information in the tab.

Adding in the extension devs to take a closer look. Assigning medium severity for now.

### ku...@gmail.com (2011-03-25)

access local files && chrome.google.com :)


### ku...@gmail.com (2011-03-25)

This two with no spoof

### aa...@chromium.org (2011-03-29)

jschuh: do you have any more details about where you think there is a race?

### js...@chromium.org (2011-03-29)

No, I was mostly just being cautious and don't have the time at the moment to investigate further. The fix for https://crbug.com/chromium/76666 should eliminate this particular case, and if you're comfortable there's no chance of a bypass otherwise then please close this bug out.


### sc...@gmail.com (2011-04-01)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-04-01)

[Empty comment from Monorail migration]

### aa...@chromium.org (2011-04-01)

CL is here: http://codereview.chromium.org/6771062/

### ka...@google.com (2011-04-06)

aaron, just checking in since this is a blocker.

### aa...@chromium.org (2011-04-07)

I just realized this is marked blocking mstone-11. Because of the refactoring work that has been going on in trunk, a change to fix this on trunk would be difficult to merge to older branches.

I will try and do something small on the 11 branch quickly.

### sc...@gmail.com (2011-04-07)

We can punt to M12 if you think it's risky or overly onerous.

But if it's low risk / easy, go for it! Thanks!

### aa...@chromium.org (2011-04-07)

Not really low-risk/easy.

### sc...@gmail.com (2011-04-11)

Thanks Aaron!
http://src.chromium.org/viewvc/chrome?view=rev&revision=80826

### sc...@gmail.com (2011-04-14)

@kuzzcc: congratulations! This is a really cool bug. The panel was particularly impressed with the way you demonstrated how nasty this can be with http://code.google.com/p/chromium/issues/detail?id=77349, where you used the JS injection to go after DOM UI functions -- even to the extent of finding a use-after-free.
Because the whole chain of bugs to get to the use-after-free is very clever, we're rewarding at the $1337 level. Nice work :D

Note - the fix will roll out with Chrome 12; hope you don't mind waiting a bit.

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

### ku...@gmail.com (2011-04-14)

Thank you :)
I'll keep on working hard.

### [Deleted User] (2011-05-18)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-06-03)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-06-09)

Invoice finalized; payment is in e-payment system; it can take a couple of weeks.

Congrats on your first $1337 reward, welcome to an exclusive club :)

### js...@chromium.org (2011-10-05)

Batch update.

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

### js...@chromium.org (2012-04-18)

[Empty comment from Monorail migration]

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

This issue was migrated from crbug.com/chromium/77026?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals, Platform>Extensions]
[Monorail mergedwith: crbug.com/chromium/78119]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089159)*

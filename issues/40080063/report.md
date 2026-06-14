# crash with form tag

| Field | Value |
|-------|-------|
| **Issue ID** | [40080063](https://issues.chromium.org/issues/40080063) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | ku...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2010-03-26 |
| **Bounty** | $500.00 |

## Description

<form><form>

like this 

## Timeline

### ku...@gmail.com (2010-03-26)

save it as 1.xhtml

### sc...@gmail.com (2010-03-29)

Great bug, kuzzcc! Don't forget to file these as "Security" or we may not see them.

My initial analysis is that this would appear to be serious.


### sc...@gmail.com (2010-03-29)

Refreshing simply this XHTML seems to do it, too:
<html>
<form></form>
<form></form>
</html>

Looks like the password form detection code is assuming that any node with its tag 
named "form" can be cast to an HTMLFormElement -- which does not seem to be the case!

### sc...@gmail.com (2010-03-29)

[Empty comment from Monorail migration]

### ku...@gmail.com (2010-03-29)

Yes .When i post it i found forget select the Template .Defect report from user is 
default,I think you should give reporter permission to change the Template from "Defect 
report from user" to "Security"

### sc...@gmail.com (2010-03-30)

Fixed on trunk with WebKit r55346 and r56098... merging to 249 branch.

### sc...@gmail.com (2010-03-30)

Committed Chromium r43027 and r43028.... syncing and testing 249 branch.

### sc...@gmail.com (2010-03-30)

[Empty comment from Monorail migration]

### sk...@chromium.org (2010-03-30)

I've changed my HTML fuzzer to use "application/xhtml+xml" and "text/html" mime types. 
That should make sure I find similar issues in the future.

### ku...@gmail.com (2010-03-30)

yes i fuzz it out some days ago and report it 

### sc...@gmail.com (2010-03-30)

Congrats - subject to responsible disclosure, this bug qualifies for a $500 reward! We 
will get the fix out shortly and credit you appropriately.

### sc...@gmail.com (2010-03-31)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-03-31)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-05-19)

Was fixed in 4.1.249.1059

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### [Deleted User] (2011-03-22)


Google Chrome	11.0.696.11 (Official Build 77963)

### js...@chromium.org (2011-10-05)

Batch update.

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-11)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/39443?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/39832, crbug.com/chromium/39920]

### pe...@google.com (2024-02-04)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080063)*

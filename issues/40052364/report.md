# Heap-buffer-overflow in WebCore::Font::codePath

| Field | Value |
|-------|-------|
| **Issue ID** | [40052364](https://issues.chromium.org/issues/40052364) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | to...@chromium.org |
| **Created** | 2011-12-22 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**

buffer overflow with text and flexbox  

**VERSION**  

Chrome Version:

Chromium 18.0.980.0 (Developer Build 115549)  

OS Linux  

WebKit 535.14 (@103399)  

JavaScript V8 3.8.2.1

Operating System: linux 64bit

**REPRODUCTION CASE**  

attached

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer  

Crash State:

READ of size 2 at 0x7fffeab381b4 thread T0  

#0 0x5555599a3d47 in WebCore::Font::codePath(WebCore::TextRun const&) const ???:0  

0x7fffeab381b4 is located 0 bytes to the right of 16692-byte region [0x7fffeab34080,0x7fffeab381b4)  

allocated by thread T0 here:  

#0 0x55555ce519d4 in malloc ??:0  

#1 0x55555905d346 in WTF::fastMalloc(unsigned long) ???:0

---

Invalid read of size 2  

at 0x183AF90: void WTF::Vector<unsigned short, 0ul>::append<unsigned short>(unsigned short const\*, unsigned long) (in chromium/chrome-linux/chromium-browser)  

by 0x183E9DD: WebKit::frameContentAsPlainText(unsigned long, WebCore::Frame\*, WTF::Vector<unsigned short, 0ul>\*) (in chromium/chrome-linux/chromium-browser)  

by 0x1840CD4: WebKit::WebFrameImpl::contentAsText(unsigned long) const (in chromium/chrome-linux/chromium-browser)  

by 0xF1E1BF: ChromeRenderViewObserver::CaptureText(WebKit::WebFrame\*, std::basic\_string<unsigned short, base::string16\_char\_traits, std::allocator<unsigned short> >\*) (in chromium/chrome-linux/chromium-browser)  

by 0xF22BA3: ChromeRenderViewObserver::CapturePageInfo(int, bool) (in chromium/chrome-linux/chromium-browser)  

by 0x101DC45: MessageLoop::RunTask(base::PendingTask const&) (in chromium/chrome-linux/chromium-browser)  

by 0x101E377: MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) (in chromium/chrome-linux/chromium-browser)

Address 0x13136152 is 0 bytes after a block of size 34 alloc'd  

at 0x50BD90F: malloc (vg\_replace\_malloc.c:1072)  

by 0x18A1619: WTF::fastMalloc(unsigned long) (in chromium/chrome-linux/chromium-browser)  

by 0x18AC732: WTF::StringImpl::createUninitialized(unsigned int, unsigned short\*&) (in chromium/chrome-linux/chromium-browser)  

by 0x18B2F7F: WTF::String::remove(unsigned int, int) (in chromium/chrome-linux/chromium-browser)  

by 0x1A3D4D8: WebCore::CharacterData::deleteData(unsigned int, unsigned int, int&) (in chromium/chrome-linux/chromium-browser)

## Attachments

- [second.html](attachments/second.html) (text/html; charset=us-ascii, 920 B)
- [firstb.html](attachments/firstb.html) (text/html; charset=us-ascii, 1006 B)
- [first.html](attachments/first.html) (text/html; charset=us-ascii, 1.1 KB)
- [second-asan.txt](attachments/second-asan.txt) (text/plain; charset=us-ascii, 1.6 KB)
- [secondb-asan.txt](attachments/secondb-asan.txt) (text/plain; charset=us-ascii, 1.6 KB)
- [firstb-asan.txt](attachments/firstb-asan.txt) (text/plain; charset=us-ascii, 1.6 KB)
- [secondb.html](attachments/secondb.html) (text/html; charset=us-ascii, 823 B)
- [first-asan.txt](attachments/first-asan.txt) (text/plain; charset=us-ascii, 1.6 KB)

## Timeline

### in...@chromium.org (2011-12-22)

Adding the repros to clusterfuzz now.

### in...@chromium.org (2011-12-23)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=9306646

Uploader: inferno@chromium.org

Crash Type: Heap-buffer-overflow READ 2
Crash Address: 0x7f244657571e
Crash State:
  - crash stack -
  WebCore::Font::codePath
  WebCore::Font::selectionRectForText
  WebCore::InlineTextBox::positionForOffset
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=110080:110106

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94gIxj3rwijRyw1Um_-kI8t-vh_iQGurPKvuhS-0kQjFxk5wRRT7xt7YxzWEgB3Iz-yDj6DyDVSy-773csWjpWLH5UEkJbogAqdVtYtk5VX64AX7cqm0GFNveyNR17BAzeuWbjh7EDz1MuOpVHVYBDtttMSyw

### in...@chromium.org (2011-12-23)

This is an issue with the new flexbox, can you please take a look.

### in...@chromium.org (2011-12-26)

Upstreamed - https://bugs.webkit.org/show_bug.cgi?id=75213

### in...@chromium.org (2011-12-29)

Awesome Tony has a patch upstream :)

### to...@chromium.org (2012-01-11)

http://trac.webkit.org/changeset/104645 should fix the bug.

### js...@chromium.org (2012-01-11)

Needs to be merged to beta.

### to...@chromium.org (2012-01-13)

Is it safe for me to merge to the 963 branch now?

### in...@chromium.org (2012-01-14)

Yes, m17 is ok to merge anytime.

### to...@chromium.org (2012-01-17)

Merged in http://trac.webkit.org/changeset/105165

### in...@chromium.org (2012-01-17)

Thanks a lot Tony.

### sc...@gmail.com (2012-02-06)

@miaubiz: seems like we never sent this past the rewards panel.
Although we try to be diligent, I do worry that we might forget the "reward-topanel" label sometimes -- especially on bugs that get tangled up with existing bugs or forked into new bugs. Feel free to keep an eye out and harass us if the reward-topanel never appears :D

### sc...@gmail.com (2012-02-07)

@miaubiz: goes wrong in the text handling, so maybe the OOB content might appear in the page and be recoverable? :)
$500, thanks for catching it ahead of time.

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

### mi...@gmail.com (2012-02-07)

fwiw I am seeing this exact stack trace with another repro. but it's a (reliable) 223 line recursive unminimizable repro :|

### in...@chromium.org (2012-02-07)

please file a new bug, it might be a dup of http://code.google.com/p/chromium/issues/detail?id=112317

### sc...@gmail.com (2012-02-15)

[Empty comment from Monorail migration]

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-06-13)

ClusterFuzz has detected this issue as fixed in range 117116:117171.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=9306646

Uploader: inferno@chromium.org

Crash Type: Heap-buffer-overflow READ 2
Crash Address: 0x7f244657571e
Crash State:
  - crash stack -
  WebCore::Font::codePath
  WebCore::Font::selectionRectForText
  WebCore::InlineTextBox::positionForOffset
  
Fixed: https://cluster-fuzz.appspot.com/revisions?range=117116:117171

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94gIxj3rwijRyw1Um_-kI8t-vh_iQGurPKvuhS-0kQjFxk5wRRT7xt7YxzWEgB3Iz-yDj6DyDVSy-773csWjpWLH5UEkJbogAqdVtYtk5VX64AX7cqm0GFNveyNR17BAzeuWbjh7EDz1MuOpVHVYBDtttMSyw

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/108476?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052364)*

# Heap-buffer-overflow in ConvertWOFF2ToTTF

| Field | Value |
|-------|-------|
| **Issue ID** | [40083621](https://issues.chromium.org/issues/40083621) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>WebFonts |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ks...@chromium.org |
| **Created** | 2016-02-03 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Heap buffer overflow exists in ConvertWOFF2ToTTF method of woff2\_dec.cc file.  

Code:  

if (PREDICT\_FALSE(!Read255UShort(&file, &table\_idx))) {  

return FONT\_COMPRESSION\_FAILURE();  

}  

ttc\_font.table\_indices[j] = table\_idx;  

const Table& table = tables[table\_idx];

Code does not validate whether table\_idx is less than the size of tables vector.

**VERSION**  

Chrome Version: [49.0.2623.28 (64-bit)] + [beta]  

[50.0.2639.0 (64-bit)] + [trunk build]  

Operating System: [Ubuntu 14.04, Windows 10]

**REPRODUCTION CASE**

1. Download and save corruptFont.woff2 and testfont.html in same folder.
2. Open chrome built with address sanitizer and open testfont.html.
3. Sometimes tab does not crash. Please reload the page several times if tab does not crash.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [tab]  

Crash State: Address Sanitizer output  

==13485==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x60400010e2d8 at pc 0x55e014527ae4 bp 0x7ffee7735330 sp 0x7ffee7735328  

READ of size 4 at 0x60400010e2d8 thread T0 (chrome)  

#0 0x55e014527ae3 in ConvertWOFF2ToTTF third\_party/woff2/src/woff2\_dec.cc:892:19  

#1 0x55e014495709 in ProcessWOFF2 third\_party/ots/src/ots.cc:482:8  

#2 0x55e014495709 in Process third\_party/ots/src/ots.cc:896:0  

#3 0x55e01421eb6b in sanitize third\_party/WebKit/Source/platform/fonts/opentype/OpenTypeSanitizer.cpp:88:15  

#4 0x55e0141ef68c in create third\_party/WebKit/Source/platform/fonts/FontCustomPlatformData.cpp:92:44  

#5 0x55e00c93a678 in ensureCustomFontData third\_party/WebKit/Source/core/fetch/FontResource.cpp:143:26  

...

\* Address Sanitizer reports this same bug as a use after free sometimes.  

I think it happens when overflow reaches memory of another freed object.

==13865==ERROR: AddressSanitizer: heap-use-after-free on address 0x6040000ea518 at pc 0x55902c85fae4 bp 0x7ffc2b3f6e30 sp 0x7ffc2b3f6e28  

READ of size 4 at 0x6040000ea518 thread T0 (chrome)  

#0 0x55902c85fae3 in ConvertWOFF2ToTTF third\_party/woff2/src/woff2\_dec.cc:892:19  

#1 0x55902c7cd709 in ProcessWOFF2 third\_party/ots/src/ots.cc:482:8  

#2 0x55902c7cd709 in Process third\_party/ots/src/ots.cc:896:0  

#3 0x55902c556b6b in sanitize third\_party/WebKit/Source/platform/fonts/opentype/OpenTypeSanitizer.cpp:88:15  

#4 0x55902c52768c in create third\_party/WebKit/Source/platform/fonts/FontCustomPlatformData.cpp:92:44  

#5 0x559024c72678 in ensureCustomFontData third\_party/WebKit/Source/core/fetch/FontResource.cpp:143:26  

#6 0x5590254625df in fontLoaded third\_party/WebKit/Source/core/css/RemoteFontFaceSource.cpp:96:5  

#7 0x559024c72db8 in checkNotify third\_party/WebKit/Source/core/fetch/FontResource.cpp:200:9  

#8 0x559024c98ddd in finish  

.....

0x6040000ea518 is located 8 bytes inside of 48-byte region [0x6040000ea510,0x6040000ea540)  

freed by thread T0 (chrome) here:  

#0 0x55901e1699bb in operator delete(void\*) ??:?  

#1 0x559020c25565 in ~ResourceResponseInfo content/public/common/resource\_response\_info.cc:29:1  

#2 0x559028e0d746 in ~TupleLeaf base/tuple.h:174:8  

#3 0x559028e0d746 in ~TupleBaseImpl base/tuple.h:167:0  

#4 0x559028e0d746 in Dispatch<content::ResourceDispatcher, content::ResourceDispatcher, void, void (content::ResourceDispatcher::\*)(int, const content::ResourceResponseHead &)> content/common/resource\_messages.h:313:0  

#5 0x559028e0d746 in DispatchMessage content/child/resource\_dispatcher.cc:567:0  

.......

previously allocated by thread T0 (chrome) here:  

#0 0x55901e1693fb in operator new(unsigned long) ??:?  

#1 0x7fc9c148fd12 in \_\_allocate buildtools/third\_party/libc++/trunk/include/new:168:10  

#2 0x7fc9c148fd12 in allocate buildtools/third\_party/libc++/trunk/include/memory:1729:0  

#3 0x7fc9c148fd12 in allocate buildtools/third\_party/libc++/trunk/include/memory:1488:0  

#4 0x7fc9c148fd12 in \_\_grow\_by\_and\_replace buildtools/third\_party/libc++/trunk/include/string:2325:0  

#5 0x7fc9c148edbb in assign buildtools/third\_party/libc++/trunk/include/string:2392:9  

#6 0x55901eea530e in ReadString base/pickle.cc:153:3  

#7 0x559020d1c82c in Read ipc/ipc\_message\_utils.h:285:12  

#8 0x559020d1c82c in ReadParam<std::\_\_1::basic\_string<char> > ipc/ipc\_message\_utils.h:112:0  

#9 0x559020d1c82c in Read content/common/resource\_messages.h:118:0  

#10 0x559020cb8075 in Read content/common/resource\_messages.h:102:1  

#11 0x559020cb8075 in ReadParam[content::ResourceResponseHead](javascript:void(0);) ipc/ipc\_message\_utils.h:112:0  

#12 0x559020cb8075 in Read ipc/ipc\_message\_utils.h:630:0  

#13 0x559020cb8075 in ReadParam<base::Tuple<int, content::ResourceResponseHead> > ipc/ipc\_message\_utils.h:112:0  

........

## Attachments

- [corruptFont.woff2](attachments/corruptFont.woff2) (application/octet-stream, 64 B)
- [testfont.html](attachments/testfont.html) (text/html, 158 B)

## Timeline

### ke...@chromium.org (2016-02-03)

I reproduced this on an M50 ASAN build. I do not see the bug in the M48 source but please verify.

### cl...@chromium.org (2016-02-03)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5579385660243968

### cl...@chromium.org (2016-02-03)

[Empty comment from Monorail migration]

### ks...@chromium.org (2016-02-04)

Confirmed.
This is a bug of TTC support code which is introduced in M49.

### ks...@chromium.org (2016-02-04)

[Empty comment from Monorail migration]

### ks...@chromium.org (2016-02-04)

[Empty comment from Monorail migration]

### ks...@chromium.org (2016-02-05)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-02-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e36c7f206423cd6e5b6b7695c7b5e228c653eb31

commit e36c7f206423cd6e5b6b7695c7b5e228c653eb31
Author: ksakamoto <ksakamoto@chromium.org>
Date: Fri Feb 05 04:06:12 2016

Cherry-pick woff2 revision d1efde9

d1efde9: Update woff2_dec.cc range checking

BUG=583563

Review URL: https://codereview.chromium.org/1667413003

Cr-Commit-Position: refs/heads/master@{#373741}

[modify] http://crrev.com/e36c7f206423cd6e5b6b7695c7b5e228c653eb31/third_party/woff2/README.chromium
[modify] http://crrev.com/e36c7f206423cd6e5b6b7695c7b5e228c653eb31/third_party/woff2/src/woff2_dec.cc


### ks...@chromium.org (2016-02-05)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-02-05)

[Empty comment from Monorail migration]

### ti...@google.com (2016-02-06)

Your change meets the bar and is auto-approved for M49 (branch: 2623)

### bu...@chromium.org (2016-02-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/3832a64d099fce5cff582f4b95f48dd38feb8402

commit 3832a64d099fce5cff582f4b95f48dd38feb8402
Author: Kunihiko Sakamoto <ksakamoto@chromium.org>
Date: Mon Feb 08 01:20:55 2016

Cherry-pick woff2 revision d1efde9

d1efde9: Update woff2_dec.cc range checking

BUG=583563

Review URL: https://codereview.chromium.org/1667413003

Cr-Commit-Position: refs/heads/master@{#373741}
(cherry picked from commit e36c7f206423cd6e5b6b7695c7b5e228c653eb31)

Review URL: https://codereview.chromium.org/1681433002 .

Cr-Commit-Position: refs/branch-heads/2623@{#291}
Cr-Branched-From: 92d77538a86529ca35f9220bd3cd512cbea1f086-refs/heads/master@{#369907}

[modify] http://crrev.com/3832a64d099fce5cff582f4b95f48dd38feb8402/third_party/woff2/README.chromium
[modify] http://crrev.com/3832a64d099fce5cff582f4b95f48dd38feb8402/third_party/woff2/src/woff2_dec.cc


### bu...@chromium.org (2016-02-08)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/bling/chromium.git/+/3832a64d099fce5cff582f4b95f48dd38feb8402

commit 3832a64d099fce5cff582f4b95f48dd38feb8402
Author: Kunihiko Sakamoto <ksakamoto@chromium.org>
Date: Mon Feb 08 01:20:55 2016


### oc...@chromium.org (2016-02-09)

Fixing the severity, since it's a buffer overflow read in the renderer process.

### oc...@chromium.org (2016-02-09)

[Empty comment from Monorail migration]

### ch...@gmail.com (2016-02-13)

Firefox also started using woff2 library on 2016-02-05.
https://bugzilla.mozilla.org/show_bug.cgi?id=1227058.

Fix for this bug is not yet merged for firefox source code.
https://hg.mozilla.org/mozilla-central/log/tip/modules/woff2/src/woff2_dec.cc
So this bug reproduces in firefox nightly 47.0a1 (2016-02-12).

Can you please disclose this bug to firefox?

### ti...@google.com (2016-02-29)

#16: It's best if you disclose this bug to Mozilla as you found it. It won't affect your bug bounty to let Mozilla know that they have the same issue.

### ch...@gmail.com (2016-03-01)

I reported this bug to mozilla today.

### ti...@google.com (2016-04-22)

Congrats - $1000 for this report! I'll start the payment process today.

### ch...@gmail.com (2016-04-22)

Thanks a lot for the reward. I have to disclose that I reported this bug to firefox too after reporting this bug to chrome. I also accepted a reward from them and before accepting their reward I informed them I reported this bug to chrome too.

### ti...@google.com (2016-04-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-05-13)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/583563?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083621)*

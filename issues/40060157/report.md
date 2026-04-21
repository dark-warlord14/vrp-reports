# Typeconfuse in blink::LayoutTableRow::AddChild layout_table_row.cc:193

| Field | Value |
|-------|-------|
| **Issue ID** | [40060157](https://issues.chromium.org/issues/40060157) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>CSS |
| **Platforms** | Linux, Windows |
| **Reporter** | m....@gmail.com |
| **Assignee** | ko...@chromium.org |
| **Created** | 2022-07-04 |
| **Bounty** | $5,000.00 |

## Description

**Steps to reproduce the problem:**  

#TestOn  

asan-win32-release\_x64-1020473

#Reproduce

1. chrome --no-sandbox --user-data-dir=test poc.html

**Problem Description:**  

#Type of crash  

render tab

**Additional Comments:**  

[1984:8480:0704/151735.420:FATAL:casting.h(126)] Security DCHECK failed: IsA<Derived>(from).  

Backtrace:  

base::debug::CollectStackTrace [0x00007FF8EC877452+18] (C:\b\s\w\ir\cache\builder\src\base\debug\stack\_trace\_win.cc:329)  

base::debug::StackTrace::StackTrace [0x00007FF8EC68A87A+26] (C:\b\s\w\ir\cache\builder\src\base\debug\stack\_trace.cc:218)  

logging::LogMessage::~LogMessage [0x00007FF8EC6C2F33+659] (C:\b\s\w\ir\cache\builder\src\base\logging.cc:670)  

blink::LayoutTableRow::AddChild [0x00007FF8F905A6A9+2073] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\layout\_table\_row.cc:193)  

blink::LayoutTableSection::AddChild [0x00007FF8F906428B+3499] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\layout\_table\_section.cc:206)  

blink::LayoutTable::AddChild [0x00007FF8F85782CF+3039] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\layout\_table.cc:249)  

blink::LayoutObject::AddChild [0x00007FF8F493ED7B+875] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\layout\_object.cc:574)  

blink::LayoutBlockFlow::AddChild [0x00007FF8F4EE5DCF+1343] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\layout\_block\_flow.cc:2905)  

blink::Element::AttachLayoutTree [0x00007FF8F1B44CDD+1309] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\element.cc:3431)  

blink::Node::ReattachLayoutTree [0x00007FF8F1C45A42+370] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\node.cc:1587)  

blink::Element::RebuildLayoutTree [0x00007FF8F1B57968+968] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\element.cc:4326)  

blink::ContainerNode::RebuildLayoutTreeForChild [0x00007FF8F1EEB03C+1020] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\container\_node.cc:1404)  

blink::ContainerNode::RebuildChildrenLayoutTrees [0x00007FF8F1EEB22A+138] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\container\_node.cc:1425)  

blink::Element::RebuildLayoutTree [0x00007FF8F1B57DD9+2105] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\element.cc:4360)  

blink::StyleEngine::RebuildLayoutTree [0x00007FF8F1E01C73+787] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\style\_engine.cc:2876)  

blink::StyleEngine::UpdateStyleAndLayoutTree [0x00007FF8F1E03906+1558] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\style\_engine.cc:2944)  

blink::Document::UpdateStyle [0x00007FF8F17E0310+672] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\document.cc:2253)  

blink::Document::UpdateStyleAndLayoutTreeForThisDocument [0x00007FF8F17DDCE4+1908] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\document.cc:2202)  

blink::LocalFrameView::UpdateStyleAndLayoutInternal [0x00007FF8F171BCCB+443] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:3247)  

blink::LocalFrameView::UpdateStyleAndLayout [0x00007FF8F16FC257+695] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:3199)  

blink::Document::UpdateStyleAndLayout [0x00007FF8F17DE963+739] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\document.cc:2580)  

blink::TimerBase::RunInternal [0x00007FF8EEEDEF9B+187] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\timer.cc:159)  

base::TaskAnnotator::RunTaskImpl [0x00007FF8EC7DE9C5+917] (C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:135)  

base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl [0x00007FF8EF50E032+2274] (C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:406)  

base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork [0x00007FF8EF50D20F+415] (C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:284)  

base::MessagePumpDefault::Run [0x00007FF8EF4EB93B+491] (C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_default.cc:39)  

base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run [0x00007FF8EF50FC3B+1019] (C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:551)  

base::RunLoop::Run [0x00007FF8EC752650+1328] (C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:143)  

content::RendererMain [0x00007FF8EEFD208E+2910] (C:\b\s\w\ir\cache\builder\src\content\renderer\renderer\_main.cc:290)  

content::RunOtherNamedProcessTypeMain [0x00007FF8EC30B75F+1244] (C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:720)  

content::ContentMainRunnerImpl::Run [0x00007FF8EC30D6F4+1742] (C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1063)  

content::RunContentProcess [0x00007FF8EC309DCC+3355] (C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:407)  

content::ContentMain [0x00007FF8EC30A536+403] (C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:435)  

ChromeMain [0x00007FF8E0D414AD+937] (C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:182)  

MainDllLoader::Launch [0x00007FF63B6D56FF+2047] (C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:162)  

main [0x00007FF63B6D2AE5+6775] (C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:395)  

\_\_scrt\_common\_main\_seh [0x00007FF63BADA1E0+268] (d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288)  

BaseThreadInitThunk [0x00007FF96A187034+20]  

RtlUserThreadStart [0x00007FF96B3C2651+33]

\*\*Chrome version: \*\* 103.0.5060.53 \*\*Channel: \*\* Not sure

**OS:** Windows

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 6.6 KB)
- [poc.html](attachments/poc.html) (text/plain, 1.8 KB)
- [testharness.js](attachments/testharness.js) (text/plain, 155.7 KB)

## Timeline

### [Deleted User] (2022-07-04)

[Empty comment from Monorail migration]

### da...@chromium.org (2022-07-05)

[Empty comment from Monorail migration]

[Monorail components: Blink>Layout]

### cl...@chromium.org (2022-07-05)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4688708469194752.

### da...@chromium.org (2022-07-05)

Interesting. IsTableCell() must be true given: https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/layout/layout_table_row.cc;l=153;drc=88dc73df4a5b0c5588e2085f1859285258497c4b

But it's not a `LayoutTableCell`. So IsTableCell() must include other types? Looks like LayoutNGTableCell?

### da...@chromium.org (2022-07-05)

Is LayoutNG recently enabled? Or tables as part of it? Maybe clusterfuzz will find us a bisect.

### da...@chromium.org (2022-07-05)

Looks like LayoutNG tables have been on long before M102. So probably FoundIn-102, but we can wait to see.

### [Deleted User] (2022-07-05)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2022-07-05)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-07-05)

This crash occurs very frequently on linux platform and is likely preventing the fuzzer None from making much progress. Fixing this will allow more bugs to be found.

Marking this bug as a blocker for next Beta release.

If this is incorrect, please add the ClusterFuzz-Wrong label and remove the ReleaseBlock-Beta label.

### sz...@chromium.org (2022-07-06)

I'm OOO until next week, assigning to ikilpatrick@ for triage.

### da...@chromium.org (2022-07-06)

Clusterfuzz just seems to have found crashpad is crashing on that bot.

### da...@chromium.org (2022-07-06)

https://bugs.chromium.org/p/chromium/issues/detail?id=1342206 for the clusterfuzz failure

### da...@chromium.org (2022-07-06)

[Empty comment from Monorail migration]

### ik...@chromium.org (2022-07-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-07-06)

ClusterFuzz testcase 4688708469194752 appears to be flaky, updating reproducibility label.

### m....@gmail.com (2022-07-07)

@ping Anyone take a look at this issue?

### da...@chromium.org (2022-07-07)

Why was this bug moved to unowned?

### ik...@chromium.org (2022-07-07)

I'm OOO - kojii@ can triage.

### da...@chromium.org (2022-07-07)

[Empty comment from Monorail migration]

### ko...@chromium.org (2022-07-07)

Bisected.

You are probably looking for a change made after 1014849 (known good), but no later than 1014869 (first known bad).
CHANGELOG URL:
  https://chromium.googlesource.com/chromium/src/+log/d9e7efb98161fa32b30fa3061dca7ee0e0b00978..6889f49d0f31d22c8c101e58310b22f3f99ab832

Suspects: [@container] Enable CSSContainerQueries for "stable"
https://chromium.googlesource.com/chromium/src/+/ed08a64b71e627016a044f2d4899dcf07c7d0509

But Rune is OOO until Jul 25th, I'll take a look.

[Monorail components: -Blink>Layout Blink>CSS]

### ko...@chromium.org (2022-07-07)

Verified it does not reproduce with `--disable-blink-features=CSSContainerQueries`.

### ko...@chromium.org (2022-07-07)

I'll turn this to a normal crash, and see how much it can occur in the real world.

While using `To<>` for incorrect type causes a `SECURITY_DCHECK`, it is for engineers to look into it further. Because it crashes the browser, in this case, I don't see any possible security issues.

### gi...@appspot.gserviceaccount.com (2022-07-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/cd7e5cf71523a7f037b1cd3d174807b94c98c1d9

commit cd7e5cf71523a7f037b1cd3d174807b94c98c1d9
Author: Koji Ishii <kojii@chromium.org>
Date: Thu Jul 07 23:33:18 2022

Turn a SECURITY_DCHECK in |LayoutTableRow::AddChild| to CHECK

When the |child| of the |LayoutTableRow::AddChild| is a
|LayoutNGTableCell|, |child->IsTableCell()| is |true|, but
|To<LayoutTableCell>(child)| causes a SECURITY_DCHECK. This
patch turns it to a normal crash.

This happens when:
1. CSS Container Query crbug.com/1145970 is enabled.
2. A table cell is added to a multi-column container, which
   creates a legacy anonymous table.
3. Then turn off the multi-column, causing reattach.

When the CSS Container Query is enabled, the table cell will
be |LayoutNGTableCell|, but the legacy anonymous table is not
removed. |LayoutObject::AddChild| tries to add the
|LayoutNGTableCell| to the legacy anonymous table, resulting
this failure.

Fixed: 1341619
Change-Id: Ic935b8fbd88be5ccbcea2eb5cc926247064b2934
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3750720
Commit-Queue: Koji Ishii <kojii@chromium.org>
Commit-Queue: Xiaocheng Hu <xiaochengh@chromium.org>
Reviewed-by: Xiaocheng Hu <xiaochengh@chromium.org>
Auto-Submit: Koji Ishii <kojii@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1021919}

[modify] https://crrev.com/cd7e5cf71523a7f037b1cd3d174807b94c98c1d9/third_party/blink/renderer/core/layout/layout_table_row.cc


### [Deleted User] (2022-07-08)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-08)

[Empty comment from Monorail migration]

### da...@chromium.org (2022-07-12)

SECURITY_DCHECK does not crash the browser on users machines, unfortunately. So proceeding past one tends to be a security vulnerability (not entirely unlike other DCHECKs)

https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/wtf/assertions.h;l=46-67?ss=chromium%2Fchromium%2Fsrc&q=SECURITY_DCHECK

### am...@google.com (2022-07-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-07-13)

Congratulations! The VRP Panel has decided to award you $5,000 for this report. Thank you for your efforts and nice work! 

### am...@google.com (2022-07-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-10-14)

This issue was migrated from crbug.com/chromium/1341619?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocking: crbug.com/chromium/1145970]
[Monorail components added to Component Tags custom field.]

### ti...@chromium.org (2024-06-27)

Adding `ClusterFuzz-Ignore` hotlist to all `ClusterFuzz-Wrong` issues per crbug.com/40285975.

### ti...@chromium.org (2024-06-27)

Adding `ClusterFuzz-Ignore` hotlist to all `ClusterFuzz-Wrong` issues per crbug.com/40285975.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060157)*

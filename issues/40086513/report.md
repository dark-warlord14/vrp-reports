# Security: Heap-use-after-free in CPWL_Wnd::GetWindowMatrix

| Field | Value |
|-------|-------|
| **Issue ID** | [40086513](https://issues.chromium.org/issues/40086513) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Mac |
| **Reporter** | ne...@gmail.com |
| **Assignee** | ds...@chromium.org |
| **Created** | 2017-01-15 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

The attached poc.pdf contains two widgets on two pages (tf0 and tf1 respectively). When the first page's widget's OnFormat JS contains `this.getField("tf1").setFocus();` and the Document JS (on load) contains `this.getField("tf1").setFocus();`, a use after free occurs when the PDF is opened in Chrome.

I tested this on the latest dev version on my machine, and the ASAN trace is from `asan-mac-release-442831`.

**VERSION**  

Chrome Version: 57.0.2979.0 (dev)  

Operating System: macOS 10.12.2

**REPRODUCTION CASE**  

See attached file.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: PDF plugin process  

Crash State: See attached asan\_log

## Attachments

- [poc.pdf](attachments/poc.pdf) (application/pdf, 2.5 KB)
- [asan_output](attachments/asan_output) (text/plain, 24.3 KB)
- [register-control.pdf](attachments/register-control.pdf) (application/pdf, 2.2 KB)
- [traceback](attachments/traceback) (text/plain, 3.6 KB)

## Timeline

### ne...@gmail.com (2017-01-15)

This didn't repro on Chrome stable (55.0.xxx) on my Windows and Mac machines, but it did repro in the beta (56.0.2924.59).

### do...@chromium.org (2017-01-17)

tsepez: can you take a look? I think the crash happens in fpdfsdk/pdfwindow/PWL_Wnd.cpp

[Monorail components: Internals>Plugins>PDF]

### do...@chromium.org (2017-01-17)

[Empty comment from Monorail migration]

### do...@chromium.org (2017-01-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-17)

[Empty comment from Monorail migration]

### ne...@gmail.com (2017-01-17)

If it helps, it looks like this file reenters `void CPWL_Wnd::InvalidateRect(CFX_FloatRect* pRect)` in InvalidateRect. I was setting breakpoints on OnFormat:

Here we break at OnFormat normally, called by JS:
* thread #1: tid = 0x19401, 0x000000029489d01c Chromium Framework`::OnFormat() + 60 at cpdfsdk_interform.cpp:274, name = 'CrPPAPIMain', queue = 'com.apple.main-thread', stop reason = breakpoint 2.1
  * frame #0: 0x000000029489d01c Chromium Framework`::OnFormat() + 60 at cpdfsdk_interform.cpp:274
    frame #1: 0x00000002948daed1 Chromium Framework`::OnFormat() + 241 at cpdfsdk_widget.cpp:796
    frame #2: 0x00000002948e5c2a Chromium Framework`::OnLoad() + 954 at cpdfsdk_widgethandler.cpp:233
    frame #3: 0x0000000294846bb1 Chromium Framework`::Annot_OnLoad() + 273 at cpdfsdk_annothandlermgr.cpp:74
    frame #4: 0x00000002948b7ea4 Chromium Framework`::LoadFXAnnots() + 3380 at cpdfsdk_pageview.cpp:436
    frame #5: 0x000000029488beae Chromium Framework`::GetPageView() + 3134 at cpdfsdk_formfillenvironment.cpp:586
    frame #6: 0x000000029494b602 Chromium Framework`::FormHandleToPageView() + 210 at fpdfformfill.cpp:58
    frame #7: 0x000000029494d5d0 Chromium Framework`::FORM_OnAfterLoadPage() + 80 at fpdfformfill.cpp:658
    frame #8: 0x00000002948168d7 Chromium Framework`::GetPage() + 1303 at pdfium_page.cc:128
    frame #9: 0x00000002947e1f6b Chromium Framework`::GetVisiblePageIndex() + 1995 at pdfium_engine.cc:3380
    frame #10: 0x00000002947773ad Chromium Framework`::Form_Invalidate() + 605 at pdfium_engine.cc:3609
    frame #11: 0x000000029488850c Chromium Framework`::Invalidate() + 668 at cpdfsdk_formfillenvironment.cpp:241
    frame #12: 0x000000029484024e Chromium Framework`::InvalidateRect() + 2622 at cfx_systemhandler.cpp:60
    frame #13: 0x0000000295af1ef8 Chromium Framework`::InvalidateRect() + 3128 at PWL_Wnd.cpp:403
    frame #14: 0x0000000295a5118f Chromium Framework`::IOnInvalidateRect() + 191 at PWL_EditCtrl.cpp:564
    frame #15: 0x00000002954c9c5c Chromium Framework`::Refresh() + 1228 at fxet_edit.cpp:1631
    frame #16: 0x00000002954c4d0b Chromium Framework`::Paint() + 251 at fxet_edit.cpp:1362
    frame #17: 0x00000002954ccd91 Chromium Framework`::SetText() + 481 at fxet_edit.cpp:1274
    frame #18: 0x0000000295a35b4a Chromium Framework`::SetText() + 1370 at PWL_Edit.cpp:76
    frame #19: 0x0000000294ac1222 Chromium Framework`::NewPDFWindow() + 850 at cffl_textfield.cpp:104
    frame #20: 0x0000000294a8d5ee Chromium Framework`::GetPDFWindow() + 4654 at cffl_formfiller.cpp:372
    frame #21: 0x0000000294a938fe Chromium Framework`::SetFocusForAnnot() + 494 at cffl_formfiller.cpp:248
    frame #22: 0x0000000294aad35a Chromium Framework`::OnSetFocus() + 2922 at cffl_interactiveformfiller.cpp:411
    frame #23: 0x00000002948e5f62 Chromium Framework`::OnSetFocus() + 466 at cpdfsdk_widgethandler.cpp:251
    frame #24: 0x000000029484865a Chromium Framework`::Annot_OnSetFocus() + 298 at cpdfsdk_annothandlermgr.cpp:230
    frame #25: 0x0000000294890c1a Chromium Framework`::SetFocusAnnot() + 746 at cpdfsdk_formfillenvironment.cpp:717
    frame #26: 0x00000002957ee2e1 Chromium Framework`::setFocus() + 1729 at Field.cpp:3214
    frame #27: 0x0000000295856289 Chromium Framework`::JSMethod<Field, &Field::setFocus>() + 5017 at JS_Define.h:153

Then we encounter the crash when we get an InvalidateRect callback from the browser:

* thread #1: tid = 0x19401, 0x00007fffcb56cdd6 libsystem_kernel.dylib`__pthread_kill + 10, name = 'CrPPAPIMain', queue = 'com.apple.main-thread', stop reason = signal SIGABRT
  * frame #0: 0x00007fffcb56cdd6 libsystem_kernel.dylib`__pthread_kill + 10
    frame #1: 0x00007fffcb658787 libsystem_pthread.dylib`pthread_kill + 90
    frame #2: 0x00007fffcb4d2420 libsystem_c.dylib`abort + 129
    frame #3: 0x0000000105939ff1 libclang_rt.asan_osx_dynamic.dylib`___lldb_unnamed_symbol986$$libclang_rt.asan_osx_dynamic.dylib + 65
    frame #4: 0x00000001059357f5 libclang_rt.asan_osx_dynamic.dylib`___lldb_unnamed_symbol917$$libclang_rt.asan_osx_dynamic.dylib + 117
    frame #5: 0x000000010591e972 libclang_rt.asan_osx_dynamic.dylib`___lldb_unnamed_symbol484$$libclang_rt.asan_osx_dynamic.dylib + 290
    frame #6: 0x000000010591e408 libclang_rt.asan_osx_dynamic.dylib`___lldb_unnamed_symbol482$$libclang_rt.asan_osx_dynamic.dylib + 344
    frame #7: 0x000000010591f1db libclang_rt.asan_osx_dynamic.dylib`__asan_report_load8 + 43
    frame #8: 0x0000000295b0f9ea Chromium Framework`::GetWindowMatrix() + 442 at PWL_Wnd.cpp:847
    frame #9: 0x0000000295af21a3 Chromium Framework`::PWLtoWnd() + 435 at PWL_Wnd.cpp:864
    frame #10: 0x0000000295af1888 Chromium Framework`::InvalidateRect() + 1480 at PWL_Wnd.cpp:395
    frame #11: 0x0000000295a28098 Chromium Framework`::InvalidateRect() + 1128 at PWL_Caret.cpp:146
    frame #12: 0x0000000295a275aa Chromium Framework`::TimerProc() + 634 at PWL_Caret.cpp:99

I'm not 100% sure that's what's going on though.

### ts...@chromium.org (2017-01-17)

Repro'd on linux 64, note the window has to be small enough so that the second page isn't visible.

### ts...@chromium.org (2017-01-18)

bisects to c5267c54ea3 at https://codereview.chromium.org/2473103003

### ts...@chromium.org (2017-01-18)

Reverting c5267c resovled the issue, but not sure what breaks.  Over to Dan.

### ds...@chromium.org (2017-01-19)

[Empty comment from Monorail migration]

### ds...@chromium.org (2017-01-19)

Two CLs out for review:
  - pdfium: https://pdfium-review.googlesource.com/c/2270/
  - chromium: https://codereview.chromium.org/2641163002/

Fixing the issue on the PDFium side triggered a DCHECK in the chrome side.

### bu...@chromium.org (2017-01-19)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium.git/+/bc8dcc3ede286fbcaac3f741c379297cffff0eea

commit bc8dcc3ede286fbcaac3f741c379297cffff0eea
Author: Dan Sinclair <dsinclair@chromium.org>
Date: Thu Jan 19 18:53:02 2017

Add ObservedPtrs to PWL_CREATEPARAM

It's possible for both the provider and attached widget to be destroyed before
the PWL_CREATEPARAM objects which point to them. This causes issues when those
widgets access their attached widget or provider.

This CL wraps the pAttachedWidget and pProvider into ObservedPtrs so we will
know if the underlying pointer has gone away.

BUG=chromium:681351

Change-Id: Ib40445be9487dc3e89a66bb7407abdeed7d2c946
Reviewed-on: https://pdfium-review.googlesource.com/2270
Reviewed-by: Nicolás Peña <npm@chromium.org>
Reviewed-by: Tom Sepez <tsepez@chromium.org>
Commit-Queue: dsinclair <dsinclair@chromium.org>

[modify] https://crrev.com/bc8dcc3ede286fbcaac3f741c379297cffff0eea/BUILD.gn
[modify] https://crrev.com/bc8dcc3ede286fbcaac3f741c379297cffff0eea/fpdfsdk/cpdfsdk_widget.h
[modify] https://crrev.com/bc8dcc3ede286fbcaac3f741c379297cffff0eea/fpdfsdk/formfiller/cffl_formfiller.cpp
[modify] https://crrev.com/bc8dcc3ede286fbcaac3f741c379297cffff0eea/fpdfsdk/pdfwindow/PWL_Wnd.cpp
[modify] https://crrev.com/bc8dcc3ede286fbcaac3f741c379297cffff0eea/fpdfsdk/pdfwindow/PWL_Wnd.h
[add] https://crrev.com/bc8dcc3ede286fbcaac3f741c379297cffff0eea/fpdfsdk/pdfwindow/cpwl_color.h


### bu...@chromium.org (2017-01-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/1eccd2632893e632be32bc50c92b1c78df7150b2

commit 1eccd2632893e632be32bc50c92b1c78df7150b2
Author: pdfium-deps-roller <pdfium-deps-roller@chromium.org>
Date: Thu Jan 19 22:58:17 2017

Roll src/third_party/pdfium/ 341b5c2c1..bc8dcc3ed (2 commits).

https://pdfium.googlesource.com/pdfium.git/+log/341b5c2c1cbd..bc8dcc3ede28

$ git log 341b5c2c1..bc8dcc3ed --date=short --no-merges --format='%ad %ae %s'
2017-01-19 dsinclair Add ObservedPtrs to PWL_CREATEPARAM
2017-01-18 npm Fix leak in PixarLogSetupDecode

BUG=681351,681301

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, see:
http://www.chromium.org/developers/tree-sheriffs/sheriff-details-chromium#TOC-Failures-due-to-DEPS-rolls

TBR=dsinclair@chromium.org

Review-Url: https://codereview.chromium.org/2645953003
Cr-Commit-Position: refs/heads/master@{#444875}

[modify] https://crrev.com/1eccd2632893e632be32bc50c92b1c78df7150b2/DEPS


### ne...@gmail.com (2017-01-22)

I was able to get EIP control using this bug on a local build of Chrome.

Register control repros on Version 57.0.2986.0 dev (Ubuntu 16.04 64-bit) - you can see I've reclaimed the memory that was backed by the freed FormFiller.

The key step to making this work is realizing that the two frees are scheduled as callbacks to take place once all the JS is done running; they're not performed immediately when the setFocus calls are happening. To reclaim the freed memory, it's sufficient to schedule a JS callback myself after the first free is scheduled, so when the second free is scheduled we end up with the following callbacks queued:

1. unregister form
2. arbitrary js to reclaim form
3. unregister form

Please see the attached test case and traceback from my machine (using pwndbg, kudos to Googler zachriggle!)

### ds...@chromium.org (2017-01-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-24)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-01-24)

This bug requires manual review: DEPS changes referenced in bugdroid comments.
Please contact the milestone owner if you have questions.
Owners: amineer@(clank), cmasso@(bling), ketakid@(cros), govind@(desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2017-01-24)

+awhalley@ (Security TPM) for M57 merge review.

### bu...@chromium.org (2017-01-24)

Per offline discussion approving for merge in M56

### ds...@chromium.org (2017-01-24)

This has been merged into M56 [1]. Please let me know if/when I should merge into M57.


1- https://pdfium.googlesource.com/pdfium/+/75c2af49705f99267ef74e742d536c7327aeb452

### aw...@chromium.org (2017-01-24)

Thanks!  And yep, good to merge to M57.

### ds...@chromium.org (2017-01-24)

Which branch is the M57 merge? I don't see a 2987 in the list of branches in PDFium?

### ds...@chromium.org (2017-01-24)

Ah, there it is, merging to 2987 now ....

### ds...@chromium.org (2017-01-24)

Actually, nm, this is already in 2987. Was the last commit before branch.

### aw...@chromium.org (2017-01-24)

oopse, should I have spotted that.  Thanks for checking!

### aw...@chromium.org (2017-01-24)

*I should have :-)

### go...@chromium.org (2017-01-24)

M57 merge is already in per https://crbug.com/chromium/681351#c25. Hence, removing "Merge-Review-57" label.

### sh...@chromium.org (2017-01-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-30)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-02-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-02-06)

Congrats! The panel awarded $5,000 for this report!

### aw...@chromium.org (2017-02-06)

[Empty comment from Monorail migration]

### ne...@gmail.com (2017-02-07)

Thank you! Glad we caught this before it made it to stable.

### sh...@chromium.org (2017-05-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2017-05-03)

This issue was migrated from crbug.com/chromium/681351?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086513)*

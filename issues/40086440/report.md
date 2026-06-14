# Desktop web payments crash when closing a tab

| Field | Value |
|-------|-------|
| **Issue ID** | [40086440](https://issues.chromium.org/issues/40086440) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Payments |
| **Platforms** | Windows |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ma...@chromium.org |
| **Created** | 2017-01-09 |
| **Bounty** | $500.00 |

## Description

**VERSION**  

Chrome Version: 57.0.2977.0 (64-bit)  

Operating System: Windows 7

**REPRODUCTION CASE**

1. Run chromium with --enable-experimental-web-platform-features flag.
2. Visit <https://rsolomakhin.github.io/pr/iframe/>
3. Click on "Buy" button which is inside the first frame and reload the page.
4. Open a new tab and close the original >> Crash.

# Backtrace: media::WebMediaPlayerImpl::`vcall'{16}' [0x1ACB9D7F+19] base::internal::Invoker<base::internal::BindState<void (blink::PaymentRequest::\*)(payments::mojom::PaymentErrorReason) **attribute**((thiscall)),blink::WeakPers istent[blink::PaymentRequest](javascript:void(0);),payments::mojom::PaymentErrorReason>,void ()>::Run [0x1898D103+113] mojo::InterfaceEndpointClient::NotifyError [0x12EF0A8E+510] base::MessageLoop::~MessageLoop [0x12D5626B+939] base::MessageLoop::~MessageLoop [0x12D539EB+11] content::RenderThreadImpl::Shutdown [0x19013760+2636] content::ChildProcess::~ChildProcess [0x152680BB+123] content::RendererMain [0x18FC51BC+1332] (C:\b\c\b\win\_asan\_release\src\content\renderer\renderer\_main.cc:210) content::RunNamedProcessTypeMain [0x12BE0FA4+486] (C:\b\c\b\win\_asan\_release\src\content\app\content\_main\_runner.cc:416) content::ContentMainRunnerImpl::Run [0x12BE2641+587] (C:\b\c\b\win\_asan\_release\src\content\app\content\_main\_runner.cc:793) content::ContentMain [0x12BE0B7D+117] (C:\b\c\b\win\_asan\_release\src\content\app\content\_main.cc:20) ChromeMain [0x0F7F11FF+511] (C:\b\c\b\win\_asan\_release\src\chrome\app\chrome\_main.cc:112) MainDllLoader::Launch [0x00C57B78+702] (C:\b\c\b\win\_asan\_release\src\chrome\app\main\_dll\_loader\_win.cc:173) main [0x00C51944+2372] (C:\b\c\b\win\_asan\_release\src\chrome\app\chrome\_exe\_main\_win.cc:262) \_\_scrt\_common\_main\_seh [0x00E660DE+249] (f:\dd\vctools\crt\vcstartup\src\startup\exe\_common.inl:253) BaseThreadInitThunk [0x77023677+18] RtlInitializeExceptionChain [0x77549D72+99] RtlInitializeExceptionChain [0x77549D45+54]

==4652==ERROR: AddressSanitizer: access-violation on unknown address 0x52210054 (pc 0x1acb9d7f bp 0x0045e4b8 sp 0x0045e4b4 T0)  

==4652==The signal is caused by a READ memory access.  

==4652==\*\*\* WARNING: Failed to initialize DbgHelp! \*\*\*  

==4652==\*\*\* Most likely this means that the app is already \*\*\*  

==4652==\*\*\* using DbgHelp, possibly with incompatible flags. \*\*\*  

==4652==\*\*\* Due to technical reasons, symbolization might crash \*\*\*  

==4652==\*\*\* or produce wrong results. \*\*\*  

#0 0x1acb9d7e (C:\Users\admin\Desktop\asan-win32-release-440681\chrome\_child.dll+0x1b4c9d7e)  

#1 0x1898d102 (C:\Users\admin\Desktop\asan-win32-release-440681\chrome\_child.dll+0x1919d102)  

#2 0x12ef0a8d (C:\Users\admin\Desktop\asan-win32-release-440681\chrome\_child.dll+0x13700a8d)  

#3 0x12d5626a (C:\Users\admin\Desktop\asan-win32-release-440681\chrome\_child.dll+0x1356626a)  

#4 0x12d539ea (C:\Users\admin\Desktop\asan-win32-release-440681\chrome\_child.dll+0x135639ea)  

#5 0x1901375f (C:\Users\admin\Desktop\asan-win32-release-440681\chrome\_child.dll+0x1982375f)  

#6 0x152680ba (C:\Users\admin\Desktop\asan-win32-release-440681\chrome\_child.dll+0x15a780ba)  

#7 0x18fc51bb (C:\Users\admin\Desktop\asan-win32-release-440681\chrome\_child.dll+0x197d51bb)  

#8 0x12be0fa3 (C:\Users\admin\Desktop\asan-win32-release-440681\chrome\_child.dll+0x133f0fa3)  

#9 0x12be2640 (C:\Users\admin\Desktop\asan-win32-release-440681\chrome\_child.dll+0x133f2640)  

#10 0x12be0b7c (C:\Users\admin\Desktop\asan-win32-release-440681\chrome\_child.dll+0x133f0b7c)  

#11 0xf7f11fe (C:\Users\admin\Desktop\asan-win32-release-440681\chrome\_child.dll+0x100011fe)  

#12 0xc57b77 (C:\Users\admin\Desktop\asan-win32-release-440681\chrome.exe+0x407b77)  

#13 0xc51943 (C:\Users\admin\Desktop\asan-win32-release-440681\chrome.exe+0x401943)  

#14 0xe660dd (C:\Users\admin\Desktop\asan-win32-release-440681\chrome.exe+0x6160dd)  

#15 0x77023676 (C:\Windows\syswow64\kernel32.dll+0x7dd73676)  

#16 0x77549d71 (C:\Windows\SysWOW64\ntdll.dll+0x7dea9d71)  

#17 0x77549d44 (C:\Windows\SysWOW64\ntdll.dll+0x7dea9d44)

## Attachments

- deleted (application/octet-stream, 0 B)
- [testcase.html](attachments/testcase.html) (text/plain, 5.9 KB)
- [heap-use-after-free_ASan.txt](attachments/heap-use-after-free_ASan.txt) (text/plain, 10.3 KB)

## Timeline

### ch...@gmail.com (2017-01-09)

[Comment Deleted]

### mm...@chromium.org (2017-01-09)

Doesn't crash for me on 57.0.2972.0

Could you please provide a testcase that works without user interaction? It should be easy to automate button-clicking Thanks!

### ch...@gmail.com (2017-01-09)

[Comment Deleted]

### ch...@gmail.com (2017-01-11)

mmoroz@, And now I can repro this easly without user interaction.

### ch...@gmail.com (2017-01-11)

This seems like a use-after-free vulnerability. Sorry I cannot get the ASan trace symbolized on Windows.

### ke...@chromium.org (2017-01-17)

I reproduced the crash. Over to a media/ owner to take a look. I find it weird that the crashes ends in the WebMediaPlayer when this is a payments request. Is that really expected or did the stack get corrupted? Does this affect stable or just head?

[Monorail components: Blink>Media]

### sh...@chromium.org (2017-01-17)

This issue is a security regression. If you are not able to fix this quickly, please revert the change that introduced it.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@gmail.com (2017-01-17)

Doesn't repro on stable.

### jr...@chromium.org (2017-01-17)

I doubt this has anything to do with media::WebMediaPlayerImpl, since there appears to be no media player involved. I was able to get my local build to crash as well (crash/3ca010fa80000000, SIGSEGV @ 0x00000000), and using objdump this is what I see:

SF0 (chrome + 0x047f8e21)       payments::PaymentRequest::Cancel()	
SF1 (chrome + 0x041f37fc)       payments::PaymentRequestDialog::Cancel()
SF2 (libviews.so + 0x002f92c2)  views::DialogDelegate::Close()
SF3 (libviews.so + 0x002f6dc9)  views::DialogClientView::CanClose()
SF4 (libviews.so + 0x002fb81f)  views::NonClientView::CanClose()
SF5 (libviews.so + 0x002dda0e)  views::Widget::Close()
SF6 (chrome + 0x05d9c0d1)       constrained_window::NativeWebContentsModalDialogManagerViews::Close()
SF7 (chrome + 0x03907499)       web_modal::WebContentsModalDialogManager::DidNavigateMainFrame()
SF8 (chrome + 0x03907714)       web_modal::WebContentsModalDialogManager::WebContentsDestroyed()

Looks like a problem with payments, which makes sense since that is what the repro is testing. Assigning to mathp@ who added the cancel code a few days ago. My guess is that the mojo pipe is already closed when Cancel() tries to use it.

I will note that my crash followed the steps in the initial bug, not the test case in #4. My crash callstack has 100+ entries (on Linux, not Windows), but I only listed the first 9 above.


[Monorail components: -Blink>Media Blink>Payments]

### ch...@gmail.com (2017-01-22)

Any updates on this bug?

### go...@chromium.org (2017-01-23)


A friendly reminder that M57 Beta launch is coming soon on February 2nd! Your bug is labelled as Beta ReleaseBlock, pls make sure to land the fix and get it merged into the release branch (2987) ASAP so it gets enough baking time in Dev (before Beta promotion). Thank you!

### ro...@chromium.org (2017-01-23)

Since you had to enable --enable-experimental-web-platform-feature flag, this does not affect regular users, so it's not a release blocker.

Desktop implementation of web payments is highly experimental, unreleased, and hidden behind a command-line flag. I appreciate you giving it a go, but please don't be alarmed if it does not work quite right yet.

We're working on a similar issue in http://crbug.com/683731 with a patch in code review at http://crrev.com/2649683002.

[Monorail components: UI>Browser>Autofill>Payments]

### ro...@chromium.org (2017-01-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-23)

mathp: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-01-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-23)

This issue is a security regression. If you are not able to fix this quickly, please revert the change that introduced it.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ro...@chromium.org (2017-01-23)

[Empty comment from Monorail migration]

### ma...@chromium.org (2017-01-23)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-01-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f4bc50e24731fad2ef8ac320f6347aa60fe70532

commit f4bc50e24731fad2ef8ac320f6347aa60fe70532
Author: mathp <mathp@chromium.org>
Date: Tue Jan 24 05:17:50 2017

[Payments] Improve the closing of the PR dialog.

Various changes around the dialog's disappearance.
* The PaymentRequest object, through its delegate, can now close the
  dialog. This will need to happen if the Mojo pipe is closed by the
  renderer (can happen on failure or success of the PR logic).
* Similarly, when the user closes the dialog through an explicit
  action, the PaymentRequest object will inform the renderer and
  subsequently self destruct (this is not new but is improved)
* Some logic is added to avoid cycles: if the dialog is closing and it
  informs PaymentRequest, PaymentRequest will not ask to close it again
  (and vice versa). This is done through closing the bindings.
* abort() is implemented, it currently simply returns onAbort(true) to
  the caller (to be improved).
* As a result of the Mojo connection closing on navigation, reload,
  etc, the dialog will now close too.
* PaymentRequestDialog is renamed PaymentRequestDialogView and
  implements a new interface, PaymentRequestDialog.
* The tests are now a WidgetObserver to be warned of all possible
  closures of the dialog.

BUG=683731, 679245
TEST=PaymentRequest interactive_ui_tests

Review-Url: https://codereview.chromium.org/2649683002
Cr-Commit-Position: refs/heads/master@{#445652}

[modify] https://crrev.com/f4bc50e24731fad2ef8ac320f6347aa60fe70532/chrome/browser/payments/chrome_payment_request_delegate.cc
[modify] https://crrev.com/f4bc50e24731fad2ef8ac320f6347aa60fe70532/chrome/browser/payments/chrome_payment_request_delegate.h
[modify] https://crrev.com/f4bc50e24731fad2ef8ac320f6347aa60fe70532/chrome/browser/ui/BUILD.gn
[modify] https://crrev.com/f4bc50e24731fad2ef8ac320f6347aa60fe70532/chrome/browser/ui/browser_dialogs.h
[modify] https://crrev.com/f4bc50e24731fad2ef8ac320f6347aa60fe70532/chrome/browser/ui/views/payments/order_summary_view_controller.cc
[modify] https://crrev.com/f4bc50e24731fad2ef8ac320f6347aa60fe70532/chrome/browser/ui/views/payments/order_summary_view_controller.h
[modify] https://crrev.com/f4bc50e24731fad2ef8ac320f6347aa60fe70532/chrome/browser/ui/views/payments/payment_method_view_controller.cc
[modify] https://crrev.com/f4bc50e24731fad2ef8ac320f6347aa60fe70532/chrome/browser/ui/views/payments/payment_method_view_controller.h
[rename] https://crrev.com/f4bc50e24731fad2ef8ac320f6347aa60fe70532/chrome/browser/ui/views/payments/payment_request_dialog_view.cc
[rename] https://crrev.com/f4bc50e24731fad2ef8ac320f6347aa60fe70532/chrome/browser/ui/views/payments/payment_request_dialog_view.h
[modify] https://crrev.com/f4bc50e24731fad2ef8ac320f6347aa60fe70532/chrome/browser/ui/views/payments/payment_request_interactive_uitest.cc
[modify] https://crrev.com/f4bc50e24731fad2ef8ac320f6347aa60fe70532/chrome/browser/ui/views/payments/payment_request_interactive_uitest_base.cc
[modify] https://crrev.com/f4bc50e24731fad2ef8ac320f6347aa60fe70532/chrome/browser/ui/views/payments/payment_request_interactive_uitest_base.h
[modify] https://crrev.com/f4bc50e24731fad2ef8ac320f6347aa60fe70532/chrome/browser/ui/views/payments/payment_request_sheet_controller.h
[modify] https://crrev.com/f4bc50e24731fad2ef8ac320f6347aa60fe70532/chrome/browser/ui/views/payments/payment_sheet_view_controller.cc
[modify] https://crrev.com/f4bc50e24731fad2ef8ac320f6347aa60fe70532/chrome/browser/ui/views/payments/payment_sheet_view_controller.h
[modify] https://crrev.com/f4bc50e24731fad2ef8ac320f6347aa60fe70532/chrome/browser/ui/views/payments/test_chrome_payment_request_delegate.cc
[modify] https://crrev.com/f4bc50e24731fad2ef8ac320f6347aa60fe70532/chrome/browser/ui/views/payments/test_chrome_payment_request_delegate.h
[modify] https://crrev.com/f4bc50e24731fad2ef8ac320f6347aa60fe70532/components/payments/BUILD.gn
[modify] https://crrev.com/f4bc50e24731fad2ef8ac320f6347aa60fe70532/components/payments/payment_request.cc
[modify] https://crrev.com/f4bc50e24731fad2ef8ac320f6347aa60fe70532/components/payments/payment_request.h
[modify] https://crrev.com/f4bc50e24731fad2ef8ac320f6347aa60fe70532/components/payments/payment_request_delegate.h
[add] https://crrev.com/f4bc50e24731fad2ef8ac320f6347aa60fe70532/components/payments/payment_request_dialog.h


### sh...@chromium.org (2017-01-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-24)

This issue is a security regression. If you are not able to fix this quickly, please revert the change that introduced it.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@chromium.org (2017-01-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-25)

[Empty comment from Monorail migration]

### ch...@gmail.com (2017-01-27)

Since this bug needs to enable --enable-experimental-web-platform-features flag, is it qualified for a chromium security reward? Thanks.

### ro...@chromium.org (2017-01-27)

I don't think so, but let me loop in some more people to offer their opinion as well. +Zach.

### zk...@chromium.org (2017-01-27)

I'm not familiar with the chrome security award procedures, so adding awhalley, but I suspect this won't qualify as it's behind an experimental flag.

### aw...@chromium.org (2017-01-27)

If the report caused us to fix a security bug that would have affected stable when we ship the feature then it should be up for consideration. (Unless we're totally sure we would have found it ourselves before shipping).  Adding reward-topanel

### mb...@chromium.org (2017-02-01)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-02-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-02-06)

Thanks for the report! The panel noted the limited use this bug would be to an attacker, but decided to award $500.

### aw...@chromium.org (2017-02-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-05-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### la...@chromium.org (2017-06-27)

[Empty comment from Monorail migration]

[Monorail components: -UI>Browser>Autofill>Payments UI>Browser>Payments]

### is...@google.com (2017-06-27)

This issue was migrated from crbug.com/chromium/679245?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086440)*

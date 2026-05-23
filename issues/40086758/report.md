# Security: Heap-use-after-free in ShareServiceImpl::OnPickerClosed

| Field | Value |
|-------|-------|
| **Issue ID** | [40086758](https://issues.chromium.org/issues/40086758) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebShare |
| **Platforms** | Linux, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | mg...@chromium.org |
| **Created** | 2017-02-10 |
| **Bounty** | $3,000.00 |

## Description

Chrome Version: 58.0.3007.0 canary  

Operating System: Windows 7

**REPRODUCTION CASE**  

1.) Run chrome with --enable-experimental-web-platform-features flag.  

2.) Open a tab to any page.  

3.) Open the testcase and click on "Click here" and wait til the page closes.  

4.) Click on "Share" which is on the request.

00000000`0017dab0 000007fe`df8c4d11 chrome\_7fedddf0000!ShareServiceImpl::OnPickerClosed+0x424 [c:\b\build\slave\win64-pgo\build\src\chrome\browser\webshare\share\_service\_impl.cc @ 186]  

00000000`0017dca0 000007fe`dfffade1 chrome\_7fedddf0000!base::internal::Invoker<base::internal::BindState<void (\_\_cdecl ShareServiceImpl::\*)(std::basic\_string<char,std::char\_traits<char>,std::allocator<char> > const & \_\_ptr64,std::basic\_string<char,std::char\_traits<char>,std::allocator<char> > const & \_\_ptr64,GURL const & \_\_ptr64,base::Callback<void \_\_cdecl(base::Optional<std::basic\_string<char,std::char\_traits<char>,std::allocator<char> > > const & \_\_ptr64),1,1> const & \_\_ptr64,base::Optional<std::basic\_string<char,std::char\_traits<char>,std::allocator<char> > >) \_\_ptr64,base::internal::UnretainedWrapper<ShareServiceImpl>,std::basic\_string<char,std::char\_traits<char>,std::allocator<char> >,std::basic\_string<char,std::char\_traits<char>,std::allocator<char> >,GURL,base::Callback<void \_\_cdecl(base::Optional<std::basic\_string<char,std::char\_traits<char>,std::allocator<char> > > const & \_\_ptr64),1,1> >,void \_\_cdecl(base::Optional<std::basic\_string<char,std::char\_traits<char>,std::allocator<char> > >)>::Run+0x7d [c:\b\build\slave\win64-pgo\build\src\base\bind\_internal.h @ 343]  

00000000`0017dd20 000007fe`dfad20ec chrome\_7fedddf0000!WebShareTargetPickerView::Accept+0xa5 [c:\b\build\slave\win64-pgo\build\src\chrome\browser\ui\views\webshare\webshare\_target\_picker\_view.cc @ 137]  

00000000`0017dd80 000007fe`dfad6ed5 chrome\_7fedddf0000!views::DialogClientView::AcceptWindow+0x24 [c:\b\build\slave\win64-pgo\build\src\ui\views\window\dialog\_client\_view.cc @ 94]  

00000000`0017ddb0 000007fe`dfab7495 chrome\_7fedddf0000!views::TableView::OnMousePressed+0x99 [c:\b\build\slave\win64-pgo\build\src\ui\views\controls\table\table\_view.cc @ 410]  

00000000`0017de00 000007fe`dfab50dd chrome\_7fedddf0000!views::View::ProcessMousePressed+0xc1 [c:\b\build\slave\win64-pgo\build\src\ui\views\view.cc @ 2314]  

00000000`0017de50 000007fe`deea3e6f chrome\_7fedddf0000!views::View::OnMouseEvent+0x169 [c:\b\build\slave\win64-pgo\build\src\ui\views\view.cc @ 1103]  

00000000`0017de80 000007fe`deea4500 chrome\_7fedddf0000!ui::EventHandler::OnEvent+0x14b [c:\b\build\slave\win64-pgo\build\src\ui\events\event\_handler.cc @ 36]  

00000000`0017deb0 000007fe`deea407b chrome\_7fedddf0000!ui::EventDispatcher::DispatchEvent+0x58 [c:\b\build\slave\win64-pgo\build\src\ui\events\event\_dispatcher.cc @ 192]  

00000000`0017dee0 000007fe`deea3f08 chrome\_7fedddf0000!ui::EventDispatcherDelegate::DispatchEventToTarget+0x123 [c:\b\build\slave\win64-pgo\build\src\ui\events\event\_dispatcher.cc @ 86]  

00000000`0017df80 000007fe`dfae68a1 chrome\_7fedddf0000!ui::EventDispatcherDelegate::DispatchEvent+0x60 [c:\b\build\slave\win64-pgo\build\src\ui\events\event\_dispatcher.cc @ 58]  

00000000`0017dfd0 000007fe`dfaaeaba chrome\_7fedddf0000!views::internal::RootView::OnMousePressed+0x1ad [c:\b\build\slave\win64-pgo\build\src\ui\views\widget\root\_view.cc @ 379]  

00000000`0017e390 000007fe`deea3e6f chrome\_7fedddf0000!views::Widget::OnMouseEvent+0x23e [c:\b\build\slave\win64-pgo\build\src\ui\views\widget\widget.cc @ 1182]  

00000000`0017e3e0 000007fe`deea4500 chrome\_7fedddf0000!ui::EventHandler::OnEvent+0x14b [c:\b\build\slave\win64-pgo\build\src\ui\events\event\_handler.cc @ 36]  

00000000`0017e410 000007fe`deea407b chrome\_7fedddf0000!ui::EventDispatcher::DispatchEvent+0x58 [c:\b\build\slave\win64-pgo\build\src\ui\events\event\_dispatcher.cc @ 192]  

00000000`0017e440 000007fe`deea3f08 chrome\_7fedddf0000!ui::EventDispatcherDelegate::DispatchEventToTarget+0x123 [c:\b\build\slave\win64-pgo\build\src\ui\events\event\_dispatcher.cc @ 86]  

00000000`0017e4e0 000007fe`dfba95ca chrome\_7fedddf0000!ui::EventDispatcherDelegate::DispatchEvent+0x60 [c:\b\build\slave\win64-pgo\build\src\ui\events\event\_dispatcher.cc @ 58]  

00000000`0017e530 000007fe`dfba97cc chrome\_7fedddf0000!ui::EventProcessor::OnEventFromSource+0xf2 [c:\b\build\slave\win64-pgo\build\src\ui\events\event\_processor.cc @ 35]  

00000000`0017e5a0 000007fe`dfaef105 chrome\_7fedddf0000!ui::EventSource::SendEventToProcessor+0xc0 [c:\b\build\slave\win64-pgo\build\src\ui\events\event\_source.cc @ 52]  

00000000`0017e610 000007fe`dfb0dc71 chrome\_7fedddf0000!views::DesktopWindowTreeHostWin::HandleMouseEvent+0x1d [c:\b\build\slave\win64-pgo\build\src\ui\views\widget\desktop\_aura\desktop\_window\_tree\_host\_win.cc @ 831]

## Attachments

- heap-use-after-free on address 0x0fa232b0 (text/plain, 11.9 KB)
- testcase.html (text/plain, 151 B)
- [Recording.mp4](attachments/Recording.mp4) (video/mp4, 390.4 KB)

## Timeline

### ch...@gmail.com (2017-02-10)

Crash/74a8c9d580000000

### ji...@chromium.org (2017-02-10)

9 crash with the same magic signature.

https://crash.corp.google.com/browse?q=custom_data.ChromeCrashProto.magic_signature_1.name%3D%27ShareServiceImpl%3A%3AOnPickerClosed%27%20OMIT%20RECORD%20IF%20SUM(CrashedStackTrace.StackFrame.FunctionName%3D%27ShareServiceImpl%3A%3AOnPickerClosed(std%3A%3Abasic_string%3Cchar%2Cstd%3A%3Achar_traits%3Cchar%3E%2Cstd%3A%3Aallocator%3Cchar%3E%20%3E%20const%20%26%2Cstd%3A%3Abasic_string%3Cchar%2Cstd%3A%3Achar_traits%3Cchar%3E%2Cstd%3A%3Aallocator%3Cchar%3E%20%3E%20const%20%26%2CGURL%20const%20%26%2Cbase%3A%3ACallback%3Cvoid%20%2C1%2C1%3E%20const%20%26%2Cbase%3A%3AOptional%3Cstd%3A%3Abasic_string%3Cchar%2Cstd%3A%3Achar_traits%3Cchar%3E%2Cstd%3A%3Aallocator%3Cchar%3E%20%3E%20%3E)%27)%20%3D%200&ignore_case=false&enable_rewrite=true&omit_field_name=CrashedStackTrace.StackFrame.FunctionName&omit_field_value=ShareServiceImpl%3A%3AOnPickerClosed(std%3A%3Abasic_string%3Cchar%2Cstd%3A%3Achar_traits%3Cchar%3E%2Cstd%3A%3Aallocator%3Cchar%3E%20%3E%20const%20%26%2Cstd%3A%3Abasic_string%3Cchar%2Cstd%3A%3Achar_traits%3Cchar%3E%2Cstd%3A%3Aallocator%3Cchar%3E%20%3E%20const%20%26%2CGURL%20const%20%26%2Cbase%3A%3ACallback%3Cvoid%20%2C1%2C1%3E%20const%20%26%2Cbase%3A%3AOptional%3Cstd%3A%3Abasic_string%3Cchar%2Cstd%3A%3Achar_traits%3Cchar%3E%2Cstd%3A%3Aallocator%3Cchar%3E%20%3E%20%3E)&omit_field_opt=%3D&stbtiq=&reportid=&index=0#4

constantina@, could you take a look? Seems you have been actively working on ShareServiceImpl. Thanks!

[Monorail components: Blink>WebShare]

### ji...@chromium.org (2017-02-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-02-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-02-11)

This issue is a security regression. If you are not able to fix this quickly, please revert the change that introduced it.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mg...@chromium.org (2017-02-12)

I will look at this tomorrow.

May be the same as https://crbug.com/chromium/689805 which has already been fixed.

### mg...@chromium.org (2017-02-13)

The version in question (r449855) is after the fix for https://crbug.com/chromium/689805, so this is separate. Looking now.

### mg...@chromium.org (2017-02-13)

Confirmed: the ShareServiceImpl object is being deleted by window.close(), then OnPickerClosed is called on it from WebShareTargetPickerView.

It's actually a bit harder to reproduce than the above steps suggest, because window.close() requires that your tab has no history; otherwise you get "Scripts may close only the windows that were opened by it." [1] So you need to open the test case via a middle-clicked link, or from the command line (not via a navigation from the New Tab Page).

The exact line of the crash is Line 186:

  OpenTargetURL(target_url);

which just happens to be the first reference to |this| from ShareServiceImpl::OnPickerClosed (OpenTargetURL is a virtual method).

This bug goes back to the introduction of WebShareTargetPickerView in r447187. There are too many CLs landed on top to revert, so I will try to land a fix soon.

[1] http://stackoverflow.com/a/19768082

### mg...@chromium.org (2017-02-14)

+sammc who I've assigned on the code review.

### bu...@chromium.org (2017-02-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/bd4b24d3cb10b535d47005567c3d5589125585fe

commit bd4b24d3cb10b535d47005567c3d5589125585fe
Author: mgiuca <mgiuca@chromium.org>
Date: Fri Feb 17 01:40:57 2017

Fixed crash if tab closes while WebShare picker dialog is open.

Now, in this case, the picker dialog will do nothing (it has a weak
pointer to the share service which is invalidated if the tab closes).

Significantly reworked unit test to make testing this case possible:
instead of synchronously closing the picker in ShowPickerDialog, it now
stores the callback and exits the run-loop, allowing the individual
tests to call the callback as they wish. The new test
ShareServiceDeletion deletes the share service before calling the
callback, which would have crashed before this fix.

BUG=690775

Review-Url: https://codereview.chromium.org/2688413006
Cr-Commit-Position: refs/heads/master@{#451169}

[modify] https://crrev.com/bd4b24d3cb10b535d47005567c3d5589125585fe/chrome/browser/webshare/share_service_impl.cc
[modify] https://crrev.com/bd4b24d3cb10b535d47005567c3d5589125585fe/chrome/browser/webshare/share_service_impl.h
[modify] https://crrev.com/bd4b24d3cb10b535d47005567c3d5589125585fe/chrome/browser/webshare/share_service_impl_unittest.cc


### mg...@chromium.org (2017-02-17)

This should now be fixed and no merge is required.

### sh...@chromium.org (2017-02-17)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-02-20)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-02-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-02-28)

Congratulations! The panel decided to award $3,000 for this bug!  We also raised the severity to High since it's a sandbox escape, though they did note that exploiting this would be very tricky.  Thanks for the report!

### ch...@gmail.com (2017-02-28)

Oh nice I didn't expect that! :)

### aw...@chromium.org (2017-02-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-05-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2017-05-26)

This issue was migrated from crbug.com/chromium/690775?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086758)*

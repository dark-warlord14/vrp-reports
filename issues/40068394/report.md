# Uaf in OmniboxPopupPresenter::WaitForHandler

| Field | Value |
|-------|-------|
| **Issue ID** | [40068394](https://issues.chromium.org/issues/40068394) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Omnibox |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | tt...@gmail.com |
| **Assignee** | or...@chromium.org |
| **Created** | 2023-07-31 |
| **Bounty** | $2,000.00 |

## Description

**Steps to reproduce the problem:**

1. apply the patch and compile Chromium with ASAN
2. start a server for poc.html
3. `./Chromium --enable-features=WebUIOmniboxPopup --user-data-dir=./tmp http://127.0.0.1:8080/poc.html`
4. click the address bar and input anything, then press `tab` on the keyboard to focus on one of the Popup results, finally close the browser, and you'll see the crash.

**Problem Description:**  

`OmniboxPopupPresenter::WaitForHandler` uses an `Unretained(this)` in callback and then passes it into a ThreadPool. We could free `this` before the callback running is done on ThreadPool, which will cause Uaf.

<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/omnibox/omnibox_popup_presenter.cc;l=146>

```
void OmniboxPopupPresenter::WaitForHandler() {  
  bool ready = IsHandlerReady();  
  base::UmaHistogramBoolean("Omnibox.WebUI.HandlerReady", ready);  
  if (!ready) {  
    SCOPED_UMA_HISTOGRAM_TIMER("Omnibox.WebUI.HandlerWait");  
    base::RunLoop loop;  
    auto quit = loop.QuitClosure();  
    auto runner = base::ThreadPool::CreateTaskRunner(base::TaskTraits());  
    runner->PostTask(FROM_HERE,  
                     base::BindOnce(  
                         [](OmniboxPopupPresenter\* presenter,  
                            base::RepeatingClosure\* closure) {  
                           while (!presenter->IsHandlerReady()) {  
                             base::PlatformThread::Sleep(base::Milliseconds(1));  
                           }  
                           closure->Run();  
                         },  
                         base::Unretained(this), &quit));  
    // base::Unretained is safe here because this is not currently destructing  
    // and we are blocking until quit closure is run.  
    loop.Run();  
    CHECK(IsHandlerReady());  
  }  
}  

```

I wrote a simple patch to make this Uaf more easier to trigger. It adds a sleep to ThreadPool to let us have more time to free this. It also patches the `if(!ready)` to `if(ready)`, which makes the target PostTask code easier to trigger.

This problem is introduced in <https://chromium-review.googlesource.com/c/chromium/src/+/4706090>  

It affects Chrome Dev 117.0.5911.2

**Additional Comments:**

\*\*Chrome version: \*\* 117 \*\*Channel: \*\* Not sure

**OS:** Mac OS

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 77 B)
- [patch.diff](attachments/patch.diff) (text/plain, 1.1 KB)
- [movie.mov](attachments/movie.mov) (video/quicktime, 4.3 MB)
- [asan.txt](attachments/asan.txt) (text/plain, 19.8 KB)

## Timeline

### [Deleted User] (2023-07-31)

[Empty comment from Monorail migration]

### th...@chromium.org (2023-07-31)

I can reproduce this on M117 with the patch. The patch seems valid to me, because PostTask does not guarantee it will run immediately. I agree with the culprit CL described in the description, so setting FoundIn to 117. Setting severity to high because this is a UAF in the browser process but only occurs during shutdown. It could possibly be downgraded to medium due to the specific user interaction required to reproduce this. Also setting Security_Impact-None since this is behind WebUIOmniboxPopup, whose field trial configuration has not been turned on.

orinj@: Could you PTAL? Also, if you think the patch is invalid, please say so.

[Monorail components: UI>Browser>Omnibox]

### or...@chromium.org (2023-07-31)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-07-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/080eac227f0de92a92f7869c2c5d7267d413a580

commit 080eac227f0de92a92f7869c2c5d7267d413a580
Author: Orin Jaworski <orinj@google.com>
Date: Mon Jul 31 22:19:46 2023

[omnibox][webui] Use WeakPtr instead of Unretained to not crash on exit

Fixed: 1468886
Change-Id: Id07c9b4102036ff133f3a8aef20cf625e8622434
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4735073
Reviewed-by: Moe Ahmadi <mahmadi@chromium.org>
Commit-Queue: Orin Jaworski <orinj@chromium.org>
Code-Coverage: Findit <findit-for-me@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1177510}

[modify] https://crrev.com/080eac227f0de92a92f7869c2c5d7267d413a580/chrome/browser/ui/views/omnibox/omnibox_popup_presenter.cc
[modify] https://crrev.com/080eac227f0de92a92f7869c2c5d7267d413a580/chrome/browser/ui/views/omnibox/omnibox_popup_presenter.h


### or...@chromium.org (2023-08-01)

The special .html isn't necessary; just opening the omnibox, pressing down arrow to select a suggestion, and closing chrome were enough to repro -- but *only with the patch*. I am not sure it's possible to repro without changing the logic or adding sleeps, but I updated with WeakPtr just in case. For sure I can say that "ready" becomes true once on startup and then stays true, and it's only possible to interact with the omnibox after it has become true. So with ordinary user interaction, this bug might never happen in the wild, but I don't have data to be sure of this yet...because the webui omnibox code is still in the prototyping phase.

### [Deleted User] (2023-08-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-01)

[Empty comment from Monorail migration]

### or...@chromium.org (2023-08-01)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-08-09)

Congratulations! The VRP Panel has decided to award you $2,000 for this report of a security issue significantly mitigated by UI interaction, race condition, and shutdown. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-08-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-11-07)

This issue was migrated from crbug.com/chromium/1468886?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40068394)*

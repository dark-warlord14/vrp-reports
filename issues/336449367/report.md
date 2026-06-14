# UAF in ModelManagerImpl::CanCreateGenericSession

| Field | Value |
|-------|-------|
| **Issue ID** | [336449367](https://issues.chromium.org/issues/336449367) |
| **Status** | Accepted |
| **Severity** | S4-Minimal |
| **Priority** | P3 |
| **Component** | Unknown |
| **Reporter** | zh...@gmail.com |
| **Assignee** | le...@chromium.org |
| **Created** | 2024-04-23 |
| **Bounty** | $3,000.00 |

## Description

#### VULNERABILITY DETAILS

Bitset: <https://chromium-review.googlesource.com/c/chromium/src/+/5446465>

While studying the implementation of the JS model execution API, I discovered that repeatedly calling `window.model.canCreateGenericSession()` within an iframe and subsequently removing the iframe may lead to a UAF issue in the Chrome browser process.

In the `ModelManagerImpl::CanCreateGenericSession` function, the reference to the current render frame host is bound to the callback after the completion of ModelManagerImpl::IsModelPathValid in the thread pool. If IsModelPathValid returns false, the reference is used to invoke rfh.AddMessageToConsole. However, since the render frame host may have been freed, this becomes a Use-After-Free vulnerability.

```
void ModelManagerImpl::CanCreateGenericSession(
    CanCreateGenericSessionCallback callback) {

  // redacted ...

  // This needs to be done in a task runner with `MayBlock` trait.
  base::ThreadPool::PostTaskAndReplyWithResult(
      FROM_HERE, {base::MayBlock()},
      base::BindOnce(&ModelManagerImpl::IsModelPathValid,
                     base::Unretained(this), model_path.value()),
      base::BindOnce(
          [](CanCreateGenericSessionCallback callback,
             content::RenderFrameHost& rfh, const std::string& model_path,
             bool is_valid_path) {
            if (!is_valid_path) {
              rfh.AddMessageToConsole(                           // <-- UAF here, render frame host may be freed
                  blink::mojom::ConsoleMessageLevel::kWarning,
                  base::StringPrintf("Unable to create generic session because "
                                     "the model path ('%s') is invalid.",
                                     model_path.c_str()));
            }
            std::move(callback).Run(is_valid_path);
          },
          std::move(callback), std::ref(render_frame_host()),
          model_path.value()));
}

```

<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/model_execution/model_manager_impl.cc;l=82-101;drc=050b5f225e98d132a97d05816bf94319f003398d>

#### VERSION

- Chrome Version: HEAD
- Operating System: Linux, Windows, Mac

According to <https://chromiumdash.appspot.com/commit/050b5f225e98d132a97d05816bf94319f003398d> in Linux, the latest release is Dev 126.0.6423.2.

#### REPRODUCTION CASE

```
# Host poc.html and frame.html on an HTTP server.
$ python -m http.server 8000

$ ./out/Default/chrome --optimization-guide-ondevice-model-execution-override=/invalid-path  http://127.0.0.1:8000/poc.html

```
#### FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION

Type of crash: browser

Crash log: see asan.txt

#### CREDIT INFORMATION

Reporter credit: Chaobin Zhang

## Attachments

- [model_manager_uaf.mp4](attachments/model_manager_uaf.mp4) (video/mp4, 4.3 MB)
- [asan.txt](attachments/asan.txt) (text/plain, 24.6 KB)
- [frame.html](attachments/frame.html) (text/html, 186 B)
- [poc.html](attachments/poc.html) (text/html, 353 B)

## Timeline

### zh...@gmail.com (2024-04-23)

Here is my proposed fix: <https://chromium-review.googlesource.com/c/chromium/src/+/5472551>, hope it help.

### sr...@google.com (2024-04-23)

Thanks for the report! I'm marking this as severity 3 since it looks like this path can only be triggered with a command line argument pointing to an invalid path. Please let me know if that assumption is wrong.

### pe...@google.com (2024-04-23)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ap...@google.com (2024-05-09)

Project: chromium/src
Branch: main

commit ed033048039d37beb182cafac0bae67e06701fb1
Author: ChaobinZhang <zhchbin@gmail.com>
Date:   Thu May 09 07:58:25 2024

    Bundz: fix UAF in ModelManagerImpl::CanCreateGenericSession
    
    1. Transfer ModelManagerImpl::IsModelPathValid to an anonymous
    namespace to prevent accessing member variables.
    2. Use weak pointer to prevent executing the callback when the
    render frame host has been destroyed.
    
    Bug: 336449367
    Change-Id: I3bb7e88fc5262697dd3d5c6fe603ea453851b5da
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5472551
    Reviewed-by: Fergal Daly <fergal@chromium.org>
    Commit-Queue: Mingyu Lei <leimy@chromium.org>
    Reviewed-by: Mingyu Lei <leimy@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1298551}

M       chrome/browser/model_execution/model_manager_impl.cc
M       chrome/browser/model_execution/model_manager_impl.h
A       chrome/browser/model_execution/model_manager_impl_unittest.cc
M       chrome/test/BUILD.gn

https://chromium-review.googlesource.com/5472551


### zh...@gmail.com (2024-05-13)

Maybe we can mark this as fixed?

### zh...@gmail.com (2024-06-10)

@leimy @fergal @sroettger

Hey there! Just wanted to check in on this – can we go ahead and mark it as fixed now since the patch landed on May 9th?

Thanks!

### le...@chromium.org (2024-06-12)

Thanks for fixing this, let me mark it as fixed.

### sp...@google.com (2024-06-28)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
$1,000 for report of highly mitigated memory corruption in a non-sandboxed process + $1,000 bisect bonus + $1,000 patch bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-06-28)

Thank you for you efforts and providing and committing a patch for this issue, Chaobin! 

### zh...@gmail.com (2024-06-28)

Thank you very much. I'm very glad I could help.

### pe...@google.com (2024-09-19)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/336449367)*

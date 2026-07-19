# Unlocked MetafilePlayer access in OOP SpoolDocument leads to heap-use-after-free in the browser process

| Field | Value |
|-------|-------|
| **Issue ID** | [494764371](https://issues.chromium.org/issues/494764371) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Printing |
| **Platforms** | Linux, Mac, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2026-03-21 |
| **Bounty** | $1,000.00 |

## Description

# Unlocked MetafilePlayer access in OOP SpoolDocument leads to heap-use-after-free in the browser process

## Summary

On Linux and macOS, where out-of-process (OOP) printing is enabled by default, the browser-process worker thread in `PrintJobWorkerOop::SpoolDocument` reads a `MetafilePlayer` pointer from `PrintedDocument` without holding the required lock. A concurrent call to `SetDocument` on the UI thread can replace and destroy that `MetafilePlayer` while the worker thread is still using it, resulting in a heap-use-after-free. A compromised renderer can trigger this race by sending a `DidPrintDocument` Mojo message during the window between `GetMetafile` and the subsequent dereference. The crash occurs in the browser process.

## Bisect

Introducing Commit: `311052a7201fcffe5b820f950b5446fe1dee1235`

- Date: 2022-04-08
- Author: Alan Screen
- Review: <https://chromium-review.googlesource.com/q/311052a7201fcffe5b820f950b5446fe1dee1235>

## Root Cause

`PrintedDocument` guards its mutable state with a lock and documents this requirement in the header:

```
// printing/printed_document.h:73-75
// Retrieves the metafile with the data to print. Lock must be held when
// calling this function
const MetafilePlayer* GetMetafile();

```

The implementation of `GetMetafile` returns the raw pointer without any locking of its own:

```
// printing/printed_document.cc:185-187
const MetafilePlayer* PrintedDocument::GetMetafile() {
  return mutable_.metafile_.get();
}

```

`SetDocument` replaces the metafile under the lock, destroying the previous one:

```
// printing/printed_document.cc:172-176
void PrintedDocument::SetDocument(std::unique_ptr<MetafilePlayer> metafile) {
  {
    base::AutoLock lock(lock_);
    mutable_.metafile_ = std::move(metafile);
  }
  ...
}

```

The OOP printing worker violates the locking contract. `PrintJobWorkerOop::SpoolDocument` runs on a dedicated `Printing_Worker` thread and calls `GetMetafile` without holding the lock, then proceeds to call virtual methods on the returned pointer:

```
// chrome/browser/printing/print_job_worker_oop.cc:285-296
bool PrintJobWorkerOop::SpoolDocument() {
  DCHECK(task_runner()->RunsTasksInCurrentSequence());

  const MetafilePlayer* metafile = document()->GetMetafile();
  DCHECK(metafile);
  base::MappedReadOnlyRegion region_mapping =
      metafile->GetDataAsSharedMemoryRegion();
  ...
}

```

Between the call to `GetMetafile` and the dereference of the returned pointer, the UI thread is free to process an incoming `DidPrintDocument` Mojo message from the renderer. That handler reaches `PrintDocument`, which calls `SetDocument` with a new metafile. `SetDocument` acquires the lock and moves a new `unique_ptr` into `mutable_.metafile_`, destroying the old `MetafilePlayer` that the worker thread still references.

```
// chrome/browser/printing/print_view_manager_base.cc:295-300
std::unique_ptr<MetafileSkia> metafile = std::make_unique<MetafileSkia>();
CHECK(metafile->InitFromData(*print_data));

PrintedDocument* document = print_job_->document();
document->SetDocument(std::move(metafile));

```

The `DidPrintDocument` handler does not enforce single-use semantics. It only checks that the document cookie matches the active print job:

```
// chrome/browser/printing/print_view_manager_base.cc:590-596
void PrintViewManagerBase::DidPrintDocument(
    mojom::DidPrintDocumentParamsPtr params,
    DidPrintDocumentCallback callback) {
  if (!PrintJobHasDocument(params->document_cookie)) {
    OnDidPrintDocument(std::move(callback), /*succeeded=*/false);
    return;
  }
  ...

```

A compromised renderer can therefore call `DidPrintDocument` repeatedly with a matching cookie, each call replacing the metafile. OOP printing is enabled by default on Linux and macOS via the `kEnableOopPrintDrivers` feature flag.

## Reproduce

Note: this is a race condition that requires source patches and a configured CUPS printer to reproduce. Please do not use ClusterFuzz for validation; follow the manual steps below instead. Testing is recommended on Linux, where OOP printing and CUPS integration are most mature. On macOS the code path appears structurally identical, but we were unable to trigger the race despite the same patches and printer configuration.

Tested at commit `7c89d33808e551aed6122c1f324864784011c158` on Linux x86\_64 with an ASAN build (`is_asan = true`, `is_debug = false`). A CUPS printer must be configured; here we use a `cups-pdf` virtual printer for verification (`sudo apt install cups-pdf`).

Apply the attached `patch.diff`. The patch inserts a `Sleep(1s)` on the browser side between `GetMetafile` and the dereference to stabilize the race timing. The renderer side repeatedly sends `DidPrintDocument` every 500ms starting from when the print-ready document is finalized.

```
cd ~/chromium/src
git apply issue_metafile_toctou/patch.diff
autoninja -C out/asan-release chrome

```

Launch:

```
ASAN_OPTIONS=detect_odr_violation=0 out/asan-release/chrome \
  --kiosk-printing \
  --user-data-dir=/tmp/poc-$(date +%s) \
  file://$(pwd)/issue_metafile_toctou/poc.html

```

The page calls `window.print()` after two seconds. The `--kiosk-printing` flag makes the print preview auto-accept without user interaction; it is not required for the vulnerability itself and can be omitted, in which case the user must manually select a system printer and click Print in the preview dialog. The browser process crashes with a heap-use-after-free within roughly ten seconds.

```
==4164388==ERROR: AddressSanitizer: heap-use-after-free on address 0x7cb1217e6c40 at pc 0x55fdefce502b bp 0x7b70f2bd4210 sp 0x7b70f2bd4208
READ of size 8 at 0x7cb1217e6c40 thread T35 (Printing_Worker)
    #0 0x55fdefce502a in printing::PrintJobWorkerOop::SpoolDocument() chrome/browser/printing/print_job_worker_oop.cc:293:17
    #1 0x55fdefc9591a in printing::PrintJobWorker::OnNewPage() chrome/browser/printing/print_job_worker.cc:180:10
    #2 0x55fdefce6694 in base::internal::Invoker<...>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #3 0x7f71a2560622 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    ...

0x7cb1217e6c40 is located 0 bytes inside of 408-byte region [0x7cb1217e6c40,0x7cb1217e6dd8)
freed by thread T0 (chrome) here:
    #0 0x55fde7c9c062 in operator delete(void*, unsigned long)
    #1 0x7f71765ec634 in printing::PrintedDocument::SetDocument(std::__Cr::unique_ptr<printing::MetafilePlayer, std::__Cr::default_delete<printing::MetafilePlayer>>) gen/third_party/libc++/src/include/__memory/unique_ptr.h:74:5
    #2 0x55fdefcf8962 in printing::PrintViewManagerBase::PrintDocument(scoped_refptr<base::RefCountedMemory>, gfx::Size const&, gfx::Rect const&, gfx::Point const&) chrome/browser/printing/print_view_manager_base.cc:300:13
    #3 0x55fdefcfc219 in printing::PrintViewManagerBase::OnComposePdfDoneImpl(...) chrome/browser/printing/print_view_manager_base.cc:562:3
    #4 0x55fdefcfc4fa in printing::PrintViewManagerBase::OnComposeDocumentDone(...) chrome/browser/printing/print_view_manager_base.cc:577:7
    ...

previously allocated by thread T0 (chrome) here:
    #0 0x55fde7c9b45d in operator new(unsigned long)
    #1 0x55fdefcf885d in printing::PrintViewManagerBase::PrintDocument(...) gen/third_party/libc++/src/include/__memory/unique_ptr.h:756:26
    ...

SUMMARY: AddressSanitizer: heap-use-after-free chrome/browser/printing/print_job_worker_oop.cc:293:17 in printing::PrintJobWorkerOop::SpoolDocument()

```

The complete ASAN log is in `issue_metafile_toctou/asan.log`.

## Credit

Please use c6eed09fc8b174b0f3eebedcceb1e792 as the credit for this vulnerability. Thank you.

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 26.3 KB)
- [patch.diff](attachments/patch.diff) (text/x-diff, 3.9 KB)
- [poc.html](attachments/poc.html) (text/html, 437 B)

## Timeline

### ch...@google.com (2026-03-25)

Setting Priority to P3 to match Severity s3. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### th...@chromium.org (2026-03-25)

I'll take a look and try to confirm this, but just to nitpick, <https://chromium-review.googlesource.com/q/311052a7201fcffe5b820f950b5446fe1dee1235> cannot be the cause of this issue since all it did was rename some variables / functions.

### th...@chromium.org (2026-03-28)

I can reproduce the issue locally with the sleep call patched in, but I wonder how likely the malicious renderer will win the race without the sleep call. I tried the same PoC without the sleep call many times, and can't get it to repro.

### th...@chromium.org (2026-03-28)

With the current PoC, since the content is a webpage and OOPPD is enabled, it's a race between:

1. PrintJobWorkerOop::SpoolDocument() getting a pointer and immediately accessing it on a worker thread.

vs.

2. The UI thread making an IPC to the Print Compositor process, and then handling the reply.

The worker thread has to get extremely unlucky to lose the race.

### je...@gmail.com (2026-03-29)

re [#comment3](https://issues.chromium.org/issues/494764371#comment3):
This should be the correct entry point where the SpoolJob() function is introduced, with document()->GetMetafile() being called on the worker thread without holding a lock.

```
  Introducing Commit: 7be09ce93d171b94306dd0ee019c0eba23e6a2f8
  - Date: 2022-04-08
  - Author: Alan Screen
  - CL: https://chromium-review.googlesource.com/c/chromium/src/+/3565046
  - Title: "Add service-based usage to render printed document"

```

### dx...@google.com (2026-03-31)

Project: chromium/src  

Branch:  main  

Author:  Lei Zhang [thestig@chromium.org](mailto:thestig@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7709456>

Printing: Fix locking in PrintedDocument

---


Expand for full commit details
```
     
    The PrintedDocument class has a `lock_` to guard the `mutable_` field, 
    but it is not used consistently. Add GUARDED_BY() to annotate `mutable_` 
    and get the compiler to check for cases where it is not guarded. Based 
    on its findings, the unsafe issues are: 
     
    1. Trying to post a task to run DebugDumpTask() on another thread later 
       without a lock. To fix this, just run the task on the current thread 
       while holding the lock. This has the potential to do I/O on the UI 
       thread, but only when the browser has a debugging command line 
       switch, which is very rare. So make an exception for this and let the 
       debug-only function use base::ScopedAllowBlocking. 
     
       Tidy the code slightly and rename it to DumpMetafileIfDebugEnabled(). 
     
    2. Exposing GetMetafile() as a public method, which requires locking, 
       but the callers do not have a way to acquire the lock. To fix this, 
       get rid of this getter with an impossible locking requirement, and 
       replace it with HasDocument() and GetDocumentData(), which are 
       tailored to the two external callers. These new methods acquire the 
       lock properly. For the internal GetMetafile() caller, just access the 
       underlying `mutable_` field directly. 
     
    Bug: 494764371 
    Change-Id: I3a6ae714e01955bde474ae146416bc8ff92b4e41 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7709456 
    Auto-Submit: Lei Zhang <thestig@chromium.org> 
    Commit-Queue: Rebekah Potter <rbpotter@chromium.org> 
    Reviewed-by: Rebekah Potter <rbpotter@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1607530}

```

---

Files:

- M `base/threading/thread_restrictions.h`
- M `chrome/browser/printing/print_job_worker.cc`
- M `chrome/browser/printing/print_job_worker_oop.cc`
- M `printing/printed_document.cc`
- M `printing/printed_document.h`

---

Hash: [3ac886fd67262e99f07b0107cd93d16f379a78b2](https://chromiumdash.appspot.com/commit/3ac886fd67262e99f07b0107cd93d16f379a78b2)  

Date: Tue Mar 31 01:13:10 2026


---

### sp...@google.com (2026-05-16)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
Heavily mitigated. Browser process UAF


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-14)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/494764371)*

# UAF in  blink::ImageBitmapFactories::ImageBitmapLoader::DecodeImageOnDecoderThread

| Field | Value |
|-------|-------|
| **Issue ID** | [40095808](https://issues.chromium.org/issues/40095808) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>Canvas, Blink>Workers, Internals>Images>Codecs |
| **Platforms** | Linux |
| **Reporter** | cd...@gmail.com |
| **Assignee** | ju...@chromium.org |
| **Created** | 2019-07-23 |
| **Bounty** | $7,500.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36

Steps to reproduce the problem:
1. Download and release asan-linux-release-679905 version of chrome.
2. Build a webserver and run chrome poc.html

What is the expected behavior?

What went wrong?

Can get UAF crash  stably.

When calls createImageBitmap,if the parameter is a blob, the ImageBitmapFactories will read from blob and take use of the 
result.

At third_party/blink/renderer/core/imagebitmap/image_bitmap_factories.cc:300

void ImageBitmapFactories::ImageBitmapLoader::DidFinishLoading() {
  DOMArrayBuffer* array_buffer = loader_->ArrayBufferResult(); <---take the raw_pointer
  loader_.reset();                                             <---reset loader and the persistent member
  if (!array_buffer) {
    RejectPromise(kAllocationFailureImageBitmapRejectionReason);
    return;
  }
  ScheduleAsyncImageBitmapDecoding(array_buffer);
}

When all blob was read, the callback above would take a raw ponter,free it's persistent reference and passed the pointer to worker_pool.

Although the DOMArrayBuffer pointer was warpped by CrossThreadPersistent,  the received function take it as a raw pointer again.
At third_party/blink/renderer/core/imagebitmap/image_bitmap_factories.cc:327
void ImageBitmapFactories::ImageBitmapLoader::DecodeImageOnDecoderThread(
    scoped_refptr<base::SingleThreadTaskRunner> task_runner,
    DOMArrayBuffer* array_buffer,                      <---use it as raw pointer again
    const String& premultiply_alpha_option,
    const String& color_space_conversion_option)

The loader was reseted, so if GC takes place while DecodeImageOnDecoderThread is using the array_buffer, UAF happened.

The poc is simple: new a worker that calls createImageBitmap.Construct a image and trans it to blob then pass it to worker.Terminate the worker and make a GC.

The decode() is a override function, so the crash stacktrace may be different according to different type of image.
To watch this, please change the second parameter in canvas.toblob, such as "image/png","image/jpeg","image/webp".
And the more time decode uses, the more stably uaf happens. So we can pass a large size canvas data.

Im not sure it caused by whether the reason above or wrong processing the persistent object in multi-thread GC.But there is another code that has the same logic as this one.
At third_party/blink/renderer/modules/clipboard/clipboard_writer.cc:146
void ClipboardWriter::DidFinishLoading() {
  DCHECK_CALLED_ON_VALID_SEQUENCE(sequence_checker_);
  DOMArrayBuffer* array_buffer = file_reader_->ArrayBufferResult();
  DCHECK(array_buffer);
  file_reader_.reset();  <---reset loader

  worker_pool::PostTask(
      FROM_HERE,
      CrossThreadBindOnce(&ClipboardWriter::DecodeOnBackgroundThread,
                          /* This unretained is safe because the ClipboardWriter
                             will wait for Decode to finish and return back to
                             this thread before deallocating. */
                          CrossThreadUnretained(this), clipboard_task_runner_,
                          WrapCrossThreadPersistent(array_buffer)));
}

The ClipboardWriter handle writing  in same logic: Reset loader and pass the raw pointer to another thread.

Did this work before? N/A 

Chrome version: 77.0.3862.0  Channel: n/a
OS Version: 16.04
Flash Version:

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### cl...@chromium.org (2019-07-24)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5199262839603200.

### cl...@chromium.org (2019-07-24)

Detailed report: https://clusterfuzz.com/testcase?key=5199262839603200

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x6340000b6943
Crash State:
  Cr_z_inflate_fast_chunk_
  Cr_z_inflate
  cr_png_process_IDAT_data
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5199262839603200

Additional requirements: Requires HTTP

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### oc...@google.com (2019-07-25)

fserb,zakerinasab, could you please take a look at this as OWNERS? 

[Monorail components: Blink>Canvas Blink>Workers]

### sh...@chromium.org (2019-07-25)

Setting milestone and target because of Security_Impact=Head and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-07-25)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-07-25)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### fs...@chromium.org (2019-07-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-25)

[Empty comment from Monorail migration]

### aa...@chromium.org (2019-07-25)

Hey cblume@, scroggo@ sent me your way. We have a use-after-free in the png image decoder. I can repro on ToT and on beta linux. The address being used is NOT the png_, frame or decoder. Any suspicions?

### cl...@chromium.org (2019-07-26)

Detailed report: https://clusterfuzz.com/testcase?key=5199262839603200

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x6340000b6943
Crash State:
  Cr_z_inflate_fast_chunk_
  Cr_z_inflate
  cr_png_process_IDAT_data
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5199262839603200

Additional requirements: Requires HTTP

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

### cl...@chromium.org (2019-07-27)

Detailed report: https://clusterfuzz.com/testcase?key=5199262839603200

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x6340000b6943
Crash State:
  Cr_z_inflate_fast_chunk_
  Cr_z_inflate
  cr_png_process_IDAT_data
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=649091:649092

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5199262839603200

Additional requirements: Requires HTTP

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

### cl...@chromium.org (2019-07-27)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Internals>Images>Codecs]

### sh...@chromium.org (2019-07-31)

[Empty comment from Monorail migration]

### ju...@chromium.org (2019-07-31)

[Empty comment from Monorail migration]

### ju...@chromium.org (2019-07-31)

[Empty comment from Monorail migration]

### ju...@chromium.org (2019-07-31)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-07-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0081ca8b4b0d7a87058ea64a3c650b9935ad8e0c

commit 0081ca8b4b0d7a87058ea64a3c650b9935ad8e0c
Author: Juanmi Huertas <juanmihd@chromium.org>
Date: Wed Jul 31 21:30:41 2019

Ensuring the arrayBuffer is not deleted by copying it

Improving the DCHECKS to control that we are being on the correct thread
and copying the buffer if we are not coming from mainthread.

Bug: 986792
Change-Id: I45436b2a778c72586719f88aa579ad3e24cc48cf
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1721790
Commit-Queue: Juanmi Huertas <juanmihd@chromium.org>
Reviewed-by: Fernando Serboncini <fserb@chromium.org>
Cr-Commit-Position: refs/heads/master@{#682931}

[modify] https://crrev.com/0081ca8b4b0d7a87058ea64a3c650b9935ad8e0c/third_party/blink/renderer/core/imagebitmap/image_bitmap_factories.cc
[modify] https://crrev.com/0081ca8b4b0d7a87058ea64a3c650b9935ad8e0c/third_party/blink/renderer/core/imagebitmap/image_bitmap_factories.h


### cl...@chromium.org (2019-08-01)

ClusterFuzz testcase 5199262839603200 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=682930:682931

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### bu...@chromium.org (2019-08-01)

[Auto-generated comment by a script] We noticed that this issue is targeted for M-77; it appears the fix may have landed after branch point, meaning a merge might be required. The owner of this bug should confirm if a merge is required here. If so, add Merge-Request-77 label and indicate which commits/CLs are to be merged. Otherwise, remove Merge-TBD label. Thanks.

### sh...@chromium.org (2019-08-02)

[Empty comment from Monorail migration]

### ju...@chromium.org (2019-08-02)

https://chromium-review.googlesource.com/c/chromium/src/+/1721790 This CL should be merged.

### cl...@chromium.org (2019-08-02)

Detailed report: https://clusterfuzz.com/testcase?key=5199262839603200

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x6340000b6943
Crash State:
  Cr_z_inflate_fast_chunk_
  Cr_z_inflate
  cr_png_process_IDAT_data
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=649091:649092

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5199262839603200

Additional requirements: Requires HTTP

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

### cl...@chromium.org (2019-08-02)

Detailed report: https://clusterfuzz.com/testcase?key=5199262839603200

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x6340000b460b
Crash State:
  Cr_z_inflate_fast_chunk_
  Cr_z_inflate
  cr_png_process_IDAT_data
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=649091:649092

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5199262839603200

Additional requirements: Requires HTTP

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

### sm...@chromium.org (2019-08-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-08-03)

Your change meets the bar and is auto-approved for M77. Please go ahead and merge the CL to branch 3865 (refs/branch-heads/3865) manually. Please contact milestone owner if you have questions.
Merge instructions: https://www.chromium.org/developers/how-tos/drover
Owners: benmason@(Android), kariahda@(iOS), dgagnon@(ChromeOS), lakpamarthy@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-08-06)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-08-12)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2019-08-12)

[Empty comment from Monorail migration]

### na...@google.com (2019-08-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-08-14)

Congrats! The Panel decided to reward $7,500 for this report!

### na...@google.com (2019-08-14)

[Empty comment from Monorail migration]

### la...@google.com (2019-09-03)

This request for M77 merge is already approved. Please land your changes into M77 branch (3865) today. We are one week away from Stable and doing the final Beta tomorrow.

### la...@google.com (2019-09-03)

[Empty comment from Monorail migration]

### ju...@chromium.org (2019-09-04)

There was a new fix that addresses this issue in the CL:
https://chromium-review.googlesource.com/c/chromium/src/+/1738629

According to gerrit it is merged.

### la...@google.com (2019-09-04)

The change has landed into M77 branch

### sh...@chromium.org (2019-11-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/986792?no_tracker_redirect=1

[Multiple monorail components: Blink>Canvas, Blink>Workers, Internals>Images>Codecs]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095808)*

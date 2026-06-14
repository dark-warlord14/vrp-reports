# Security: Stack Buffer Overflow in QuicClientPromisedInfo::OnPromiseHeaders

| Field | Value |
|-------|-------|
| **Issue ID** | [40089392](https://issues.chromium.org/issues/40089392) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Internals>Network>QUIC |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ne...@gmail.com |
| **Assignee** | rc...@chromium.org |
| **Created** | 2017-10-24 |
| **Bounty** | $10,500.00 |

## Description

VULNERABILITY DETAILS
The QUIC Protocol has a feature called "Server Push", where a server
can push resources to a client before they are explicitly requested,
to prevent unneeded round-trips. When handling push headers,
QuicClientPromisedInfo::OnPromiseHeaders assumes that the `:method`
header is present when receiving a server push, but it may not be.

from net/quic/core/quic_client_promised_info.cc:
```
void QuicClientPromisedInfo::OnPromiseHeaders(const SpdyHeaderBlock& headers) {
  // RFC7540, Section 8.2, requests MUST be safe [RFC7231], Section
  // 4.2.1.  GET and HEAD are the methods that are safe and required.
  SpdyHeaderBlock::const_iterator it = headers.find(kHttp2MethodHeader);
  DCHECK(it != headers.end());
  if (!(it->second == "GET" || it->second == "HEAD")) {
    QUIC_DVLOG(1) << "Promise for stream " << id_ << " has invalid method "
                  << it->second;
    Reset(QUIC_INVALID_PROMISE_METHOD);
    return;
  }
```

Here, if the `kHttp2MethodHeader` was not found, it will point to
the end of the headers map, which is allocated on the stack in
net/quic/chromium/quic_chromium_client_stream.cc in function
QuicChromiumClientStream::OnPromiseHeaderList.

The function goes on to dereference the OOB `it->second`.

SpdyHeaderBlock::const_iterator has a custom `operator->()`
which calls `SpdyHeaderBlock::HeaderValue::as_pair()`, performing
an OOB write. On Linux's libcxx, the underlying std::list::end is
on the stack, and on Windows, it is in the heap. I've observed
the following PoC repro attempting to dereference ASCII from the
heap as the linked list next/prev pointers, so exploitation seems
easier on Windows in the current stable build; on the current Linux
stable I believe it always crashes memcpy'ing off the end of the heap.

I've attached a patch that fixes the vulnerability.

VERSION
Chrome Version: Chrome 62 Stable
Operating System: All

REPRODUCTION CASE
Apply the attached server.patch so the sample QUIC server will send empty PUSH_PROMISE headers.

Setup and run quic_server using the guide at https://www.chromium.org/quic/playing-with-quic,
substituting my attached sources files from `www.example.org.tar`:
`out/Default/quic_server --quic_response_cache_dir=/path/to/attached/www.example.org
--certificate_file=net/tools/quic/certs/out/leaf_cert.pem
--key_file=net/tools/quic/certs/out/leaf_cert.pkcs8 --v=3`

Launch Chrome 62 with `--no-proxy-server --origin-to-force-quic-on=www.example.org:443 --host-resolver-rules='MAP www.example.org:443 127.0.0.1:6121' https://www.example.org`.
I used `asan-linux-stable-62.0.3202.62` to generate the asan.log output.

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: Browser
Crash State: See attached asan.log

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 10.3 KB)
- deleted (application/octet-stream, 0 B)
- [server.patch](attachments/server.patch) (application/octet-stream, 1.3 KB)
- [www.example.org.tar](attachments/www.example.org.tar) (application/octet-stream, 8.5 KB)
- [fix.patch](attachments/fix.patch) (application/octet-stream, 1.9 KB)

## Timeline

### ne...@gmail.com (2017-10-24)

My previous fix still had an OOB access in debug mode when logging the error. I went ahead and added an explicit case instead. These iterator bugs are pernicious!

### el...@chromium.org (2017-10-24)

Thanks for the report!

[Monorail components: Internals>Network>QUIC]

### mb...@chromium.org (2017-10-24)

Haven't had a chance to verify this quite yet, but will update with severity and impact soon.

rch: Would you mind taking a look at this?

### pa...@chromium.org (2017-10-31)

As far as I can tell, this is an OOB read, not write, and it doesn't seem to enable any kind of exfiltration of the OOB content:

void QuicClientPromisedInfo::OnPromiseHeaders(const SpdyHeaderBlock& headers) {
  // RFC7540, Section 8.2, requests MUST be safe [RFC7231], Section
  // 4.2.1.  GET and HEAD are the methods that are safe and required.
  SpdyHeaderBlock::const_iterator it = headers.find(kHttp2MethodHeader);
  DCHECK(it != headers.end());
  if (!(it->second == "GET" || it->second == "HEAD")) {
    QUIC_DVLOG(1) << "Promise for stream " << id_ << " has invalid method "
                  << it->second;
    Reset(QUIC_INVALID_PROMISE_METHOD);
    return;
  }
  if (!SpdyUtils::UrlIsValid(headers)) {
    QUIC_DVLOG(1) << "Promise for stream " << id_ << " has invalid URL "
                  << url_;
    Reset(QUIC_INVALID_PROMISE_URL);
    return;
  }
  if (!session_->IsAuthorized(SpdyUtils::GetHostNameFromHeaderBlock(headers))) {
    Reset(QUIC_UNAUTHORIZED_PROMISE_URL);
    return;
  }
  request_headers_.reset(new SpdyHeaderBlock(headers.Clone()));
}

So, I'd call this a browser process DoS. We don't consider such bugs to be security vulnerabilities (https://chromium.googlesource.com/chromium/src/+/master/docs/security/faq.md#Are-denial-of-service-issues-considered-security-bugs).

However, it might be that there's something I'm missing — I'm not an expert in this area. I'll defer to rch and nharper on that. But, if you agree, please feel free to change the Type to Bug, and remove the view restriction.

### ne...@gmail.com (2017-10-31)

I agree that when I first found this, it appeared to be a useless OOB read. But weeks later when I went to report it, I was stunned to find that `headers.find` returns a completely custom iterator that allows OOB write. Note that in the asan.log a few lines up from the first read (when ASAN aborts immediately) the read value goes on to be assigned here:

```
const std::pair<SpdyStringPiece, SpdyStringPiece>&
SpdyHeaderBlock::HeaderValue::as_pair() const {
  pair_.second = ConsolidatedValue();
  return pair_;
}
```

What makes this particularly bad IMO is that ConsolidatedValue has side effects (joining the string within the object), all of this taking place out of bounds on the stack. As I mentioned, I did repro this on a fresh Chrome 62 install with a read/write on corrupted registers.

I'll give a shot at heap spraying on Windows to better demonstrate the severity, hopefully by the end of the week.

### pa...@chromium.org (2017-10-31)

#5: Yeah, see, I was afraid something like that might happen. :) OOB write would make this a Critical, I believe. To prove that, you don't necessarily need to build a working proof of concept, just show that the vulnerable snippet you pasted above is reachable.

### ne...@gmail.com (2017-10-31)

I have some repro instructions in the initial report. To prove it reaches that as_pair code snippet, I actually just kept applying `__attribute__((no_sanitize_address))` at each crashing function to see how far it would go. It led to a write then a memcpy (!). Whoever owns the fix here should be able to verify that. Cheers!

### ab...@chromium.org (2017-10-31)

Marking M-62

### ab...@chromium.org (2017-11-01)

[Empty comment from Monorail migration]

### ab...@chromium.org (2017-11-01)

[Empty comment from Monorail migration]

### cb...@chromium.org (2017-11-01)

[Empty comment from Monorail migration]

### rc...@chromium.org (2017-11-01)

I'll get a fix landed ASAP.

### aw...@chromium.org (2017-11-01)

[Empty comment from Monorail migration]

### rc...@chromium.org (2017-11-01)

[Empty comment from Monorail migration]

### rc...@chromium.org (2017-11-01)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-11-01)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-11-01)

[Empty comment from Monorail migration]

### rc...@chromium.org (2017-11-01)

https://chromium-review.googlesource.com/c/chromium/src/+/748425 should be landing soon.

### bu...@chromium.org (2017-11-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/7a6484fa7b7f86ea06749bfc9d10bb67b145140b

commit 7a6484fa7b7f86ea06749bfc9d10bb67b145140b
Author: Ryan Hamilton <rch@chromium.org>
Date: Wed Nov 01 11:35:00 2017

Fix Stack Buffer Overflow in QuicClientPromisedInfo::OnPromiseHeaders

BUG=777728

Cq-Include-Trybots: master.tryserver.chromium.android:android_cronet_tester;master.tryserver.chromium.mac:ios-simulator-cronet
Change-Id: I6a80db88aafdf20c7abd3847404b818565681310
Reviewed-on: https://chromium-review.googlesource.com/748425
Reviewed-by: Zhongyi Shi <zhongyi@chromium.org>
Commit-Queue: Ryan Hamilton <rch@chromium.org>
Cr-Commit-Position: refs/heads/master@{#513105}
[modify] https://crrev.com/7a6484fa7b7f86ea06749bfc9d10bb67b145140b/net/quic/core/quic_client_promised_info.cc
[modify] https://crrev.com/7a6484fa7b7f86ea06749bfc9d10bb67b145140b/net/quic/core/quic_client_promised_info_test.cc


### sh...@chromium.org (2017-11-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-11-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f31b7c4c2e2aab26ffef3a0a3dc852439a3ac9dd

commit f31b7c4c2e2aab26ffef3a0a3dc852439a3ac9dd
Author: Ryan Hamilton <rch@chromium.org>
Date: Wed Nov 01 18:09:11 2017

Fix Stack Buffer Overflow in QuicClientPromisedInfo::OnPromiseHeaders

BUG=777728

Cq-Include-Trybots: master.tryserver.chromium.android:android_cronet_tester;master.tryserver.chromium.mac:ios-simulator-cronet
Change-Id: I6a80db88aafdf20c7abd3847404b818565681310
Reviewed-on: https://chromium-review.googlesource.com/748425
Reviewed-by: Zhongyi Shi <zhongyi@chromium.org>
Commit-Queue: Ryan Hamilton <rch@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#513105}(cherry picked from commit 7a6484fa7b7f86ea06749bfc9d10bb67b145140b)
Reviewed-on: https://chromium-review.googlesource.com/748828
Reviewed-by: Claude Masso <cmasso@chromium.org>
Cr-Commit-Position: refs/branch-heads/3255@{#2}
Cr-Branched-From: fc2679dfa73c1dc102d86832ef049359f433c314-refs/heads/master@{#513029}
[modify] https://crrev.com/f31b7c4c2e2aab26ffef3a0a3dc852439a3ac9dd/net/quic/core/quic_client_promised_info.cc
[modify] https://crrev.com/f31b7c4c2e2aab26ffef3a0a3dc852439a3ac9dd/net/quic/core/quic_client_promised_info_test.cc


### rc...@chromium.org (2017-11-01)

This also needs to merged to M63, right? Shall I do that now?

### rc...@chromium.org (2017-11-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-11-01)

This bug requires manual review: M63 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), gkihumba@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@chromium.org (2017-11-01)

Approving merge to both M62 and M63. 
M62 branch: 3202
M63 branch: 3239

Priority should be to merge to M62 first, and then M63. 



### bu...@chromium.org (2017-11-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/159a410566da34aa646806111397b1afe73d538b

commit 159a410566da34aa646806111397b1afe73d538b
Author: Ryan Hamilton <rch@chromium.org>
Date: Wed Nov 01 22:36:01 2017

[m62 merge] Fix Stack Buffer Overflow in QuicClientPromisedInfo::OnPromiseHeaders

BUG=777728
TBR=rch@chromium.org

(cherry picked from commit 7a6484fa7b7f86ea06749bfc9d10bb67b145140b)

Cq-Include-Trybots: master.tryserver.chromium.android:android_cronet_tester;master.tryserver.chromium.mac:ios-simulator-cronet
Change-Id: I6a80db88aafdf20c7abd3847404b818565681310
Reviewed-on: https://chromium-review.googlesource.com/748425
Reviewed-by: Zhongyi Shi <zhongyi@chromium.org>
Commit-Queue: Ryan Hamilton <rch@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#513105}
Reviewed-on: https://chromium-review.googlesource.com/750063
Reviewed-by: Ryan Hamilton <rch@chromium.org>
Cr-Commit-Position: refs/branch-heads/3202@{#767}
Cr-Branched-From: fa6a5d87adff761bc16afc5498c3f5944c1daa68-refs/heads/master@{#499098}
[modify] https://crrev.com/159a410566da34aa646806111397b1afe73d538b/net/quic/core/quic_client_promised_info.cc
[modify] https://crrev.com/159a410566da34aa646806111397b1afe73d538b/net/quic/core/quic_client_promised_info_test.cc


### bu...@chromium.org (2017-11-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d36a49798c97641cd6c48c3e8f730ad44cc67bb0

commit d36a49798c97641cd6c48c3e8f730ad44cc67bb0
Author: Ryan Hamilton <rch@chromium.org>
Date: Wed Nov 01 22:42:37 2017

Fix Stack Buffer Overflow in QuicClientPromisedInfo::OnPromiseHeaders

BUG=777728
TBR=rch@chromium.org

(cherry picked from commit 7a6484fa7b7f86ea06749bfc9d10bb67b145140b)

Cq-Include-Trybots: master.tryserver.chromium.android:android_cronet_tester;master.tryserver.chromium.mac:ios-simulator-cronet
Change-Id: I6a80db88aafdf20c7abd3847404b818565681310
Reviewed-on: https://chromium-review.googlesource.com/748425
Reviewed-by: Zhongyi Shi <zhongyi@chromium.org>
Commit-Queue: Ryan Hamilton <rch@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#513105}
Reviewed-on: https://chromium-review.googlesource.com/750065
Reviewed-by: Ryan Hamilton <rch@chromium.org>
Cr-Commit-Position: refs/branch-heads/3239@{#337}
Cr-Branched-From: adb61db19020ed8ecee5e91b1a0ea4c924ae2988-refs/heads/master@{#508578}
[modify] https://crrev.com/d36a49798c97641cd6c48c3e8f730ad44cc67bb0/net/quic/core/quic_client_promised_info.cc
[modify] https://crrev.com/d36a49798c97641cd6c48c3e8f730ad44cc67bb0/net/quic/core/quic_client_promised_info_test.cc


### ab...@chromium.org (2017-11-01)

rch@ - for Enterprise, we provide N-1 version support (specifically for Enterprises that have this signed in their contract). We've agreed to merge critical security patches into N-1 version. Can you please merge this to M61 as well for that purpose? This won't be released unless a customer specifically requests an M61 copy. 

Branch:3163


### rc...@chromium.org (2017-11-01)

Will do!

### bu...@chromium.org (2017-11-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/34ae85f6bc596af851096f028aded7c09a44ead5

commit 34ae85f6bc596af851096f028aded7c09a44ead5
Author: Ryan Hamilton <rch@chromium.org>
Date: Thu Nov 02 00:12:43 2017

[m61 merge] Fix Stack Buffer Overflow in QuicClientPromisedInfo::OnPromiseHeaders

BUG=777728
TBR=rch@chromium.org

(cherry picked from commit 7a6484fa7b7f86ea06749bfc9d10bb67b145140b)

Cq-Include-Trybots: master.tryserver.chromium.android:android_cronet_tester;master.tryserver.chromium.mac:ios-simulator-cronet
Change-Id: I6a80db88aafdf20c7abd3847404b818565681310
Reviewed-on: https://chromium-review.googlesource.com/748425
Reviewed-by: Zhongyi Shi <zhongyi@chromium.org>
Commit-Queue: Ryan Hamilton <rch@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#513105}
Reviewed-on: https://chromium-review.googlesource.com/749923
Reviewed-by: Ryan Hamilton <rch@chromium.org>
Cr-Commit-Position: refs/branch-heads/3163@{#1323}
Cr-Branched-From: ff259bab28b35d242e10186cd63af7ed404fae0d-refs/heads/master@{#488528}
[modify] https://crrev.com/34ae85f6bc596af851096f028aded7c09a44ead5/net/quic/core/quic_client_promised_info.cc
[modify] https://crrev.com/34ae85f6bc596af851096f028aded7c09a44ead5/net/quic/core/quic_client_promised_info_test.cc


### sh...@chromium.org (2017-11-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-11-02)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2017-11-02)

[Empty comment from Monorail migration]

### rc...@chromium.org (2017-11-02)

[Empty comment from Monorail migration]

### ab...@chromium.org (2017-11-02)

[Empty comment from Monorail migration]

### gk...@google.com (2017-11-03)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-11-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-11-03)

[Empty comment from Monorail migration]

### rc...@chromium.org (2017-11-03)

[Empty comment from Monorail migration]

### rc...@chromium.org (2017-11-03)

[Empty comment from Monorail migration]

### rc...@chromium.org (2017-11-03)

[Empty comment from Monorail migration]

### pa...@chromium.org (2017-11-03)

[Empty comment from Monorail migration]

### rc...@chromium.org (2017-11-03)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-11-06)

[Empty comment from Monorail migration]

### rc...@chromium.org (2017-11-07)

[Empty comment from Monorail migration]

### ne...@gmail.com (2017-11-07)

This bug was found with libFuzzer.

I'm contributing my fuzz target to the fuzzer program for those that are curious how I went about finding this: https://chromium-review.googlesource.com/c/chromium/src/+/753006

I should note that auditing could have easily found this bug, but I was trying to find bugs in many areas of code and fuzzing brings the cost of fully auditing a module down dramatically.

### aw...@chromium.org (2017-11-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2017-11-09)

The VRP Panel awarded $10,500 for this bug, and mentioned that we'd be happy to look again if you submit a functional export for it.  Cheers!

### el...@chromium.org (2017-11-09)

Re #48: I believe "functional export" was meant to be "functional exploit"-- that is to say, a demonstration that results in the execution of arbitrary code in the browser process. https://www.google.com/about/appsecurity/chrome-rewards/index.html

### aw...@chromium.org (2017-11-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-01-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-02-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-03-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-19)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-05)

[Empty comment from Monorail migration]

### aw...@google.com (2018-10-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-31)

[Empty comment from Monorail migration]

### ad...@google.com (2019-08-13)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-04)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-05)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/777728?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089392)*

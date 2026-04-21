# Security: Container Overflow in UDPSocket::OnLeaveGroupCompleted

| Field | Value |
|-------|-------|
| **Issue ID** | [40062153](https://issues.chromium.org/issues/40062153) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Apps>API |
| **Platforms** | ChromeOS |
| **Reporter** | ss...@gmail.com |
| **Assignee** | re...@chromium.org |
| **Created** | 2022-12-09 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**  

In `UDPSocket::OnLeaveGroupCompleted`, there is a container `erase` operation on `multicast_groups_` without checking the legality of the iterator.

```
void UDPSocket::OnLeaveGroupCompleted(net::CompletionOnceCallback callback,  
                                      const std::string& normalized_address,  
                                      int result) {  
  if (result == net::OK) {  
    auto find_result =  
        base::ranges::find(multicast_groups_, normalized_address);  
    multicast_groups_.erase(find_result); // may erase multicast_groups_.end()  
  }  
  
  std::move(callback).Run(result);  
}  

```

The IP address is removed from `multicast_groups_` when we disconnect the multicast connection or the UDP socket leaves the multicast group.

The former case can be reached by [chrome.socket.leaveGroup](https://developer.chrome.com/docs/extensions/reference/socket/#method-leaveGroup) API and finally get into [UDPSocket::LeaveGroup](https://source.chromium.org/chromium/chromium/src/+/main:extensions/browser/api/socket/udp_socket.cc;drc=38321ee39cd73ac2d9d4400c56b90613dee5fe29;l=337), then the `UDPSocket::OnLeaveGroupCompleted` is set as the response callback.

The later case can be reached by [chrome.socket.disconnect](https://developer.chrome.com/docs/extensions/reference/socket/#method-disconnect) API and will clear the `multicast_groups_` synchronously.

So there is a race between the `chrome.socket.leaveGroup` and `chrome.socket.disconnect`, which will result in container overflow if `UDPSocket::OnLeaveGroupCompleted` is invoked after the `multicast_groups_` got cleared.

**VERSION**  

Operating System: Ubuntu 22.04  

Commit Id: [dev] 4f40d66e66edb1c1c7dd00d83e09ff7ab89081cf

**REPRODUCTION CASE**  

To reproduce:

1. download `background.js` and `manifest.json`
2. ./chrome --load-extension=/path/to/ext

Note that chromium has enabled the safe libc++ feature by default on Linux, to get the `asan.log`, you should disable it while compiling the chromium.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see `asan.log`

**CREDIT INFORMATION**  

Reporter credit: avaue at S.S.L.

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 37.3 KB)
- [background.js](attachments/background.js) (text/plain, 573 B)
- [manifest.json](attachments/manifest.json) (text/plain, 397 B)
- [asan-read.log](attachments/asan-read.log) (text/plain, 35.8 KB)
- [asan-write.log](attachments/asan-write.log) (text/plain, 35.9 KB)

## Timeline

### [Deleted User] (2022-12-09)

[Empty comment from Monorail migration]

### ad...@google.com (2022-12-10)

[Empty comment from Monorail migration]

### ad...@google.com (2022-12-12)

Reproduced on asan-linux-release-1058931 (equivalent to M108). It does indeed merely say "Trace/breakpoint trap (core dumped)" due to libc++ hardening.

Per https://bugs.chromium.org/p/chromium/issues/detail?id=1335422#c140 and chatting with ayzhao@, only ChromeOS still doesn't use hardened C++, so setting OS=Chrome.

As a browser process OOB read, requiring an extension, rating this as Medium severity. (If it can trigger an OOB write, we should bump it up to High).

Sending towards owners of extensions/browser/api/socket

[Monorail components: Internals>Services>Network]

### [Deleted User] (2022-12-12)

[Empty comment from Monorail migration]

### re...@chromium.org (2022-12-12)

Fix out for review: https://chromium-review.googlesource.com/c/chromium/src/+/4098365

[Monorail components: -Internals>Services>Network Platform>Apps>API]

### gi...@appspot.gserviceaccount.com (2022-12-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5158dfea6671200202e99d8e85d87ddbaaee2247

commit 5158dfea6671200202e99d8e85d87ddbaaee2247
Author: Reilly Grant <reillyg@chromium.org>
Date: Mon Dec 12 22:25:45 2022

Fix race between UDPSocket::LeaveGroup() and Disconnect()

Since LeaveGroup() is asynchronous Disconnect() can be invoked before
OnLeaveGroupCompleted() is called, which will clear multicast_groups_
and so erase() would be called with an invalid iterator.

This change switches to using base::Erase(), which tolerates the value
being removed not being in the container.

Fixed: 1399904
Change-Id: I6319ad54bd2f7815c1ccf81f8206ce306926e665
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4098365
Auto-Submit: Reilly Grant <reillyg@chromium.org>
Reviewed-by: Istiaque Ahmed <lazyboy@chromium.org>
Commit-Queue: Reilly Grant <reillyg@chromium.org>
Commit-Queue: Istiaque Ahmed <lazyboy@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1082065}

[modify] https://crrev.com/5158dfea6671200202e99d8e85d87ddbaaee2247/extensions/browser/api/socket/udp_socket.cc
[modify] https://crrev.com/5158dfea6671200202e99d8e85d87ddbaaee2247/chrome/test/data/extensions/api_test/socket/api/multicast.js


### ss...@gmail.com (2022-12-13)

Re #3> "As a browser process OOB read, requiring an extension, rating this as Medium severity. (If it can trigger an OOB write, we should bump it up to High)."

Hi, the erase operation on `std::vector<std::string>` will hit an OOB write while invoking the move constructor of `std::string` with `std::vector<std::string>::end()`.

I tested the POC above with safe libc++ disabled and `ASAN_OPTIONS=detect_container_overflow=0,halt_on_error=0 ./chrome --load-extension=/path/to/ext`

Both OOB read[1] and write[2] were detected in [void basic_string<_CharT, _Traits, _Allocator>::__move_assign(basic_string& __str, true_type);](https://source.chromium.org/chromium/chromium/src/+/main:buildtools/third_party/libc++/trunk/include/string;drc=267afcfc476453b3902edc43620cfac35c25b9f8;l=2557)

```
template <class _CharT, class _Traits, class _Allocator>
inline _LIBCPP_CONSTEXPR_SINCE_CXX20
void
basic_string<_CharT, _Traits, _Allocator>::__move_assign(basic_string& __str, true_type)
#if _LIBCPP_STD_VER > 14
    _NOEXCEPT
#else
    _NOEXCEPT_(is_nothrow_move_assignable<allocator_type>::value)
#endif
{
  if (__is_long()) {
    __alloc_traits::deallocate(__alloc(), __get_long_pointer(),
                               __get_long_cap());
#if _LIBCPP_STD_VER <= 14
    if (!is_nothrow_move_assignable<allocator_type>::value) {
      __set_short_size(0);
      traits_type::assign(__get_short_pointer()[0], value_type());
    }
#endif
  }
  __move_assign_alloc(__str);
  __r_.first() = __str.__r_.first(); # [1] oob read, __str.__r
  if (__libcpp_is_constant_evaluated()) {
    __str.__default_init();
  } else {
    __str.__set_short_size(0); # [2] oob write
    traits_type::assign(__str.__get_short_pointer()[0], value_type());
  }
}
```

Would you please consider bumping the severity to high?


### [Deleted User] (2022-12-13)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-13)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-13)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-13)

Requesting merge to beta M109 because latest trunk commit (1082065) appears to be after beta branch point (1070088).

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-13)

Merge review required: M109 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), eakpobaro (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### re...@chromium.org (2022-12-13)

1. Why does your merge fit within the merge criteria for these milestones?

Yes, this is a security issue.

2. What changes specifically would you like to merge? Please link to Gerrit.

https://chromium-review.googlesource.com/c/chromium/src/+/4098365

3. Have the changes been released and tested on canary?

The issue is covered by new automated tests.

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

No.

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents

N/A

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

No.

### ma...@google.com (2022-12-14)

Approved, M109.

Security fix

### gi...@appspot.gserviceaccount.com (2022-12-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7fddb7d95518663f220073a11ce078ffe78c5d77

commit 7fddb7d95518663f220073a11ce078ffe78c5d77
Author: Reilly Grant <reillyg@chromium.org>
Date: Wed Dec 14 19:32:07 2022

[M-109] Fix race between UDPSocket::LeaveGroup() and Disconnect()

Since LeaveGroup() is asynchronous Disconnect() can be invoked before
OnLeaveGroupCompleted() is called, which will clear multicast_groups_
and so erase() would be called with an invalid iterator.

This change switches to using base::Erase(), which tolerates the value
being removed not being in the container.

(cherry picked from commit 5158dfea6671200202e99d8e85d87ddbaaee2247)

Fixed: 1399904
Change-Id: I6319ad54bd2f7815c1ccf81f8206ce306926e665
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4098365
Auto-Submit: Reilly Grant <reillyg@chromium.org>
Reviewed-by: Istiaque Ahmed <lazyboy@chromium.org>
Commit-Queue: Reilly Grant <reillyg@chromium.org>
Commit-Queue: Istiaque Ahmed <lazyboy@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1082065}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4107549
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5414@{#730}
Cr-Branched-From: 4417ee59d7bf6df7a9c9ea28f7722d2ee6203413-refs/heads/main@{#1070088}

[modify] https://crrev.com/7fddb7d95518663f220073a11ce078ffe78c5d77/extensions/browser/api/socket/udp_socket.cc
[modify] https://crrev.com/7fddb7d95518663f220073a11ce078ffe78c5d77/chrome/test/data/extensions/api_test/socket/api/multicast.js


### ro...@google.com (2023-01-04)

Opened b/264420866 to check on build hardening

### ch...@google.com (2023-01-09)

[Empty comment from Monorail migration]

### am...@google.com (2023-01-10)

[Empty comment from Monorail migration]

### pg...@google.com (2023-01-10)

[Empty comment from Monorail migration]

### am...@google.com (2023-01-12)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-01-12)

Congratulations avaue! The VRP Panel has decided to award you $10,000 for this report of a mildly mitigated security bug. Thank you for your efforts in discovering and reporting this issue to us -- nice work! 

### am...@google.com (2023-01-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1399904?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062153)*

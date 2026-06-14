# Heap-use-after-free in WebCore::SubresourceLoader::didFail

| Field | Value |
|-------|-------|
| **Issue ID** | [40051431](https://issues.chromium.org/issues/40051431) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | si...@chromium.org |
| **Created** | 2011-11-19 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

loading the same nonexistent with multiple workers, leads to a use-after-free condition

**VERSION**  

Chrome Version: dev channel only

## Chromium 17.0.944.0 (Developer Build 110836) OS Linux WebKit 535.10 (trunk@100785) JavaScript V8 3.7.8

Chromium 17.0.944.0 (Developer Build 110835)  

OS Linux  

WebKit 535.10 (@100825)  

JavaScript V8 3.7.8

Operating System: 64bit ubuntu

**REPRODUCTION CASE**  

http schema required.

<script>
var worker = new Worker("a")
worker.onerror = function() {
window.stop()
}
new Worker("a")
</script>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: worker (renderer)  

Crash State:

==19729== ERROR: AddressSanitizer heap-use-after-free on address 0x7fffe30043d4 at pc 0x7ffff30973d9 bp 0x7fffffff95e0 sp 0x7fffffff95d8  

READ of size 4 at 0x7fffe30043d4 thread T0  

#0 0x7ffff30973d9 in WebCore::CachedResource::finish() ???:0  

#1 0x7ffff3071ddc in WebCore::SubresourceLoader::didFinishLoading(double) ???:0

0x7fffe30043d4 is located 852 bytes inside of 944-byte region [0x7fffe3004080,0x7fffe3004430)  

freed by thread T0 here:  

#0 0x7ffff5cf5096 in free /tmp/address-sanitizer/asan/asan\_malloc\_linux.cc:37  

#1 0x7ffff309ac8a in WebCore::CachedResource::unregisterHandle(WebCore::CachedResourceHandleBase\*) ???:0  

#2 0x7ffff3093932 in WebCore::CachedRawResource::data(WTF::PassRefPtr[WebCore::SharedBuffer](javascript:void(0);), bool) ???:0

## Attachments

- [asan-worker-error.txt](attachments/asan-worker-error.txt) (text/x-c; charset=us-ascii, 9.3 KB)
- [worker-error.html](attachments/worker-error.html) (text/plain; charset=us-ascii, 114 B)
- [valgrind-worker-error.txt](attachments/valgrind-worker-error.txt) (text/x-c; charset=us-ascii, 5.6 KB)

## Timeline

### [Deleted User] (2011-11-21)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-11-21)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=660047

Uploader: aarya@google.com [2011-11-21 21:29:23]

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x7fb4dcb563d0
Crash State:
  - crash stack -
  WebCore::SubresourceLoader::didFail
  WebCore::ResourceHandleInternal::didFail
  - free stack -
  WebCore::CachedResource::unregisterHandle
  WebCore::DocumentThreadableLoader::~DocumentThreadableLoader
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=110350:110431

Minimized Testcase (0.11 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv950N9t1G4C_NMMTlvqFlMOcebKHtgEyj7BD5Fdo6JSJ1BnVtdt42_ADpI7K4gScFREzRaIgVP4TxefAyswqsudqSq69nMu3PWnv8q445tNMB2NAu1UZ7CkyifnqhfhbIpk6-fAFoMx6wjYICBn_Ec7qeRfEKA
<script>
var worker = new Worker("a")
worker.onerror = function() {
    window.stop()
}
new Worker("a")
</script>

### in...@chromium.org (2011-11-21)

This probably got broken in 
[100503]: Source/WebCore: Fix incorrect multipart handling in r100311. ...
Source/WebCore: Fix incorrect multipart handling in r100311. SubresourceLoader::didReceiveData() is getting called twice, which has unintended side effects. https://bugs.webkit.org/show_bug.cgi?id=72436 Reviewed by Adam Barth. http/tests ...
By japhet@chromium.org — 11/16/2011 14:10:53
[100311]: Source/WebCore: CachedResourceRequest is now the only ...
Source/WebCore: CachedResourceRequest is now the only SubresourceLoaderClient Merge CachedResourceRequest into SubresourceLoader and delete the SubresourceLoaderClient interface. A few items were moved to CachedResource instead of Subresou ...
By japhet@chromium.org — 11/15/2011 12:40:12

Nate, can you please help to take a look.

### in...@chromium.org (2011-11-21)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-11-21)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-11-22)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-11-22)

Upstreamed - https://bugs.webkit.org/show_bug.cgi?id=72979

### sc...@gmail.com (2011-11-23)

Security regression => this is a release blocker for M17.

### in...@chromium.org (2011-11-23)

James found it first under valgrind on Nov 18. We will use this upstream tracking bug - https://bugs.webkit.org/show_bug.cgi?id=72787

### in...@chromium.org (2011-11-23)

Just noticed James's comment on https://crbug.com/chromium/72979, we will keep both the bugs open until we determine that they are dupes.

### mi...@gmail.com (2011-11-24)

irlol. there is a comment by a different James on crbug 72979. and it's a bug that I was already familiar with, so it took me longer to realize it was the wrong bug. that comment by James W. Noord is quite psychedelic, especially in this context.

### ke...@google.com (2011-11-25)

[Empty comment from Monorail migration]

### ke...@chromium.org (2011-11-25)

Another repro from Aki. I don't know if it will help but we should test it against the eventual fix:

<script type="text/javascript">
var foo = function() {
        bar.open("GET", "http://localhost:0", true);
        bar.send();
}
var bar = new XMLHttpRequest;
bar.onerror = foo;
foo();
</script>

### in...@chromium.org (2011-11-29)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-11-30)

http://trac.webkit.org/changeset/101543

### in...@chromium.org (2011-12-15)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-12-21)

@miaubiz: nice regression catch, and we've determined it as distinct from another very similar issue we found internally. Hence a $1000 Chromium Security Reward :)

### sc...@gmail.com (2012-02-15)

[Empty comment from Monorail migration]

### ke...@chromium.org (2012-07-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### la...@google.com (2013-01-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-06-13)

ClusterFuzz has detected this issue as fixed in range 112559:112644.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=660047

Uploader: aarya@google.com [2011-11-21 21:29:23]

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x7fb4dcb563d0
Crash State:
  - crash stack -
  WebCore::SubresourceLoader::didFail
  WebCore::ResourceHandleInternal::didFail
  - free stack -
  WebCore::CachedResource::unregisterHandle
  WebCore::DocumentThreadableLoader::~DocumentThreadableLoader
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=110350:110431
Fixed: https://cluster-fuzz.appspot.com/revisions?range=112559:112644

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95J3BYtIMVDa7hfanbQaB95_4wqRkzDvGQhO_YI0nVi4Q3RCDx-SG-yxOj-Z1mTFVuILv-v_OiG54nN4X9jm9PcUMKB9H888XZfPsSgXmQtnGiXXVVgdXBJtrTzxf8u1LhrJsQBMj_TRYqqVhRWRKSYEiDlpQ

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sh...@chromium.org (2016-06-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/104863?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/105398, crbug.com/chromium/105774]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051431)*

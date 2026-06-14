# Security: race condition with workers and sync xmlhttprequests

| Field | Value |
|-------|-------|
| **Issue ID** | [40061166](https://issues.chromium.org/issues/40061166) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | mi...@chromium.org |
| **Created** | 2012-07-11 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

race condition with workers and sync xmlhttprequests

**VERSION**  

Chrome Version: trunk  

Chromium 22.0.1199.0 (Developer Build 145612)  

OS Mac OS X  

WebKit 537.1 (trunk@121126)  

JavaScript V8 3.12.9

Operating System: osx lion + 64bit precise

**REPRODUCTION CASE**

<script>
new Worker('m.js')
setTimeout("location.reload()", 200)
</script>

m.js:  

for (var i=0; i<100; i++) {  

req = new XMLHttpRequest  

req.open("GET", "A", false)  

req.send()  

}

http schema required

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: asan + tab  

Crash State:

==18424== ERROR: AddressSanitizer heap-use-after-free on address 0x7fffdd307f80 at pc 0x55555941a6a5 bp 0x7fffe7b8b4d0 sp 0x7fffe7b8b4c8  

READ of size 4 at 0x7fffdd307f80 thread T98  

#0 0x55555941a6a5 in WebCore::ResourceResponse::~ResourceResponse() ???:0  

#1 0x55555aa9f52b in WebCore::XMLHttpRequest::~XMLHttpRequest() ???:0  

#2 0x55555aa9eefe in WebCore::XMLHttpRequest::~XMLHttpRequest() ???:0

0x7fffdd307f80 is located 0 bytes inside of 50-byte region [0x7fffdd307f80,0x7fffdd307fb2)  

freed by thread T0 here:  

#0 0x55555e8cd452 in free ??:0  

#1 0x55555941a4d1 in WebCore::ResourceResponse::~ResourceResponse() ???:0  

#2 0x55555a8cc361 in WebCore::CachedResource::~CachedResource() ???:0  

#3 0x55555ae50c0e in WebCore::CachedRawResource::~CachedRawResource() ???:0

osx:

==21806== ERROR: AddressSanitizer heap-use-after-free on address 0x1b9ad080 at pc 0x44a0020 bp 0xb129e778 sp 0xb129e774  

READ of size 4 at 0x1b9ad080 thread T20  

#0 0x44a0020 in WebCore::ResourceResponse::~ResourceResponse() (in Chromium Framework) + 976  

#1 0x308739d in WebCore::XMLHttpRequest::~XMLHttpRequest() (in Chromium Framework) + 1341  

#2 0x3086de1 in WebCore::XMLHttpRequest::~XMLHttpRequest() (in Chromium Framework) + 17  

#3 0x23d4755 in WebCore::DOMData::derefObject(WebCore::WrapperTypeInfo\*, void\*) (in Chromium Framework) + 53

0x1b9ad080 is located 0 bytes inside of 40-byte region [0x1b9ad080,0x1b9ad0a8)  

freed by thread T0 here:  

#0 0xdc760 in (anonymous namespace)::mz\_free(\_malloc\_zone\_t\*, void\*) (in Chromium Helper) + 80  

#1 0xdc113 in wrap\_free (in Chromium Helper) + 83  

#2 0x449fe45 in WebCore::ResourceResponse::~ResourceResponse() (in Chromium Framework) + 501  

#3 0x2e758e4 in WebCore::CachedResource::~CachedResource() (in Chromium Framework) + 692  

#4 0x2e74831 in WebCore::CachedRawResource::~CachedRawResource() (in Chromium Framework) + 17

## Attachments

- [worker.html](attachments/worker.html) (text/plain; charset=us-ascii, 79 B)
- [m.js](attachments/m.js) (text/plain; charset=us-ascii, 106 B)
- [linux.txt](attachments/linux.txt) (text/x-c; charset=us-ascii, 11.5 KB)
- [osx.txt](attachments/osx.txt) (text/x-c; charset=us-ascii, 15.1 KB)

## Timeline

### in...@chromium.org (2012-07-11)

Michael, can you please take a look or help with an owner.

Miaubiz, this is an extremely flaky repro. if it produces reliably on your box, can you check if it impacts stable ?

### mi...@chromium.org (2012-07-11)

Is this a newly introduced bug or are you just now are noticing something that's been around for a while?

### in...@chromium.org (2012-07-11)

I think miaubiz can comment on that based on reproducibility on his machine. for me, the repro reproduces 1 in like 50 times, so neither me nor ClusterFuzz can't tell whether it affects stable or not.

### mi...@gmail.com (2012-07-12)

stable is affected also (on my box :|)

### in...@chromium.org (2012-07-12)

Thanks miaubiz.

### in...@chromium.org (2012-08-01)

[Empty comment from Monorail migration]

### mi...@chromium.org (2012-08-01)

gah... i had lost track of this one!

### in...@chromium.org (2012-08-02)

Please do read Mark's email titled "Code Yellow: Security Bug Backlog" on chrome-team mailing list.

### mi...@chromium.org (2012-08-02)

cc'ing nate on this one too since he knows something about 'the loader' and how it plays with cached resources and such

### mi...@chromium.org (2012-08-02)

... and cc'ing levin who knows something about ThreadableLoaders and CrossThreadCopier and such

ASAN is complaining about ResponseResponse being accessed (deleted) on the worker thread after it's been deleted on the main thread, but the ResourceResponse in question is an inline data member of the XHR class which is very much a worker-thread-only sort of object... and the ResourceResponse poked at on the worker is a CrossThreadCopier produced thing (maybe we missed copying some response data members properly in there??)

But most curiously... ~XHRHttpRequest is on the stack twice... wassup with that.. that may be closer to the real problem?

    #0 0x44a0020 in WebCore::ResourceResponse::~ResourceResponse() (in Chromium Framework) + 976
    #1 0x308739d in WebCore::XMLHttpRequest::~XMLHttpRequest() (in Chromium Framework) + 1341
    #2 0x3086de1 in WebCore::XMLHttpRequest::~XMLHttpRequest() (in Chromium Framework) + 17

### mi...@chromium.org (2012-08-03)

David found it... we're not cross-thread-copying the String m_remoteIPAddress ResourceResponse data member.

Thank you!

I'll make a patch for this.

### mi...@chromium.org (2012-08-03)

Patch out for review in webkit-land...
https://bugs.webkit.org/show_bug.cgi?id=93158

### mi...@chromium.org (2012-08-03)

I guess we'll want to patch that in to the release branch after its committed.

### in...@chromium.org (2012-08-04)

http://trac.webkit.org/changeset/124682

### mi...@chromium.org (2012-08-07)

per a chat with inferno, leaving any merging to be done to others 

### sc...@gmail.com (2012-08-16)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-08-20)

Thanks miaubiz. Race condition => $500

### sc...@gmail.com (2012-08-24)

M21: http://trac.webkit.org/changeset/126646

### sc...@gmail.com (2012-08-29)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-09-12)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-14)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### js...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-01-18)

Restrict-View-EditIssue is preferred since it allows anyone who can edit an issue (committers and contributors) to view the bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-14)

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

### sh...@chromium.org (2016-06-14)

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

This issue was migrated from crbug.com/chromium/136881?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061166)*

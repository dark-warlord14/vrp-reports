# CSP: `*.x.y` must match a host that ends with `.x.y` (4.2.2 step 4.6)

| Field | Value |
|-------|-------|
| **Issue ID** | [40082901](https://issues.chromium.org/issues/40082901) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>SecurityFeature |
| **CVE IDs** | CVE-2015-6785 |
| **Reporter** | m....@shapesecurity.com |
| **Assignee** | jw...@chromium.org |
| **Created** | 2015-09-21 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**

Given a CSP header of `script-src \*.a.localhost`, the script `<script src="//a.localhost/script.js"></script>` should not be loaded. CSP spec section 4.2.2 step 4.6 states "If the first character of the source expression’s host-part is an U+002A ASTERISK character (\*) and the remaining characters, including the leading U+002E FULL STOP character (.), are not a case insensitive match for the rightmost characters of url-host, then return does not match". Scripts such as `<script src="//b.a.localhost/script.js"></script>` should be allowed by this policy.

**VERSION**  

Chrome Version: 45.0.2454.85  

Operating System: Darwin c101.local 14.5.0 Darwin Kernel Version 14.5.0: Wed Jul 29 02:26:53 PDT 2015; root:xnu-2782.40.9~1/RELEASE\_X86\_64 x86\_64 i386 MacBookPro11,3 Darwin

**REPRODUCTION CASE**

See VULNERABILITY DETAILS section above.

## Timeline

### jw...@chromium.org (2015-09-22)

[Empty comment from Monorail migration]

### mk...@chromium.org (2015-09-22)

Hrm. What does Firefox do here? I'm not sure the specced behavior is intentional. :)

### m....@shapesecurity.com (2015-09-22)

The wording of the spec makes it seem very intentional: "... the remaining characters, including the leading U+002E FULL STOP character (.), are not ...". Firefox blocks this request. Here's a simple repro case for you:

```
var http = require("http");
var express = require("express");

var app = express();

app.use(express.static("static"));

// BUG:: *.x.y must match a host that ends with `.x.y` (4.2.2 step 4.6)
app.get("/", function (req, res) {
  res.set('Content-Security-Policy', "script-src *.a.localhost");
  res.send('Hello, world! <script src="//a.localhost/script.js"></script>');
});

var server = app.listen(80, function () {
  var host = server.address().address;
  var port = server.address().port;
  console.log('Listening at http://%s:%s', host, port);
});
```

### mk...@chromium.org (2015-09-22)

I agree 100% that the text is intentionally there, I just don't remember making that decision. :)

That makes sense, as it's apparently been there since CSP1. So I blame Adam. If Firefox matches the spec, then we should do the same. Joel, are you ok to take this?

### jw...@chromium.org (2015-09-22)

Yup, happy to clean up abarth's mess ;-)

### bu...@chromium.org (2015-09-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6282934a62f7b1416b677acad89a2880f2de201c

commit 6282934a62f7b1416b677acad89a2880f2de201c
Author: jww <jww@chromium.org>
Date: Thu Sep 24 19:52:29 2015

CSP source *.x.y should not match host x.y

This fixes a minor CSP bug where a source in a source list with a
wildcard was matching more liberally than it should have. It was
matching a source of the form *.x.y to host x.y when, in fact, it should
only be matching subdomains.

BUG=534542
TBR=mkwst@chromium.org

Review URL: https://codereview.chromium.org/1367933003

Cr-Commit-Position: refs/heads/master@{#350629}

[delete] http://crrev.com/b614c7445fef05edaafcb8e80f2ea4e685c43a17/third_party/WebKit/LayoutTests/http/tests/security/contentSecurityPolicy/image-full-host-wildcard-allowed-expected.txt
[add] http://crrev.com/6282934a62f7b1416b677acad89a2880f2de201c/third_party/WebKit/LayoutTests/http/tests/security/contentSecurityPolicy/image-full-host-wildcard-fails-expected.txt
[rename] http://crrev.com/6282934a62f7b1416b677acad89a2880f2de201c/third_party/WebKit/LayoutTests/http/tests/security/contentSecurityPolicy/image-full-host-wildcard-fails.html
[add] http://crrev.com/6282934a62f7b1416b677acad89a2880f2de201c/third_party/WebKit/LayoutTests/http/tests/security/contentSecurityPolicy/source-list-parsing-11.html
[modify] http://crrev.com/6282934a62f7b1416b677acad89a2880f2de201c/third_party/WebKit/Source/core/frame/UseCounter.h
[modify] http://crrev.com/6282934a62f7b1416b677acad89a2880f2de201c/third_party/WebKit/Source/core/frame/csp/CSPSource.cpp
[modify] http://crrev.com/6282934a62f7b1416b677acad89a2880f2de201c/third_party/WebKit/Source/core/frame/csp/CSPSourceListTest.cpp
[modify] http://crrev.com/6282934a62f7b1416b677acad89a2880f2de201c/third_party/WebKit/Source/core/frame/csp/CSPSourceTest.cpp
[modify] http://crrev.com/6282934a62f7b1416b677acad89a2880f2de201c/third_party/WebKit/Source/core/frame/csp/ContentSecurityPolicy.cpp
[modify] http://crrev.com/6282934a62f7b1416b677acad89a2880f2de201c/third_party/WebKit/Source/core/frame/csp/ContentSecurityPolicy.h
[modify] http://crrev.com/6282934a62f7b1416b677acad89a2880f2de201c/tools/metrics/histograms/histograms.xml


### jw...@chromium.org (2015-09-24)

[Empty comment from Monorail migration]

### m....@shapesecurity.com (2015-09-24)

Being a security bug that affects all users of Chromium, does this bug qualify for the Chrome Reward Program (https://www.google.com/about/appsecurity/chrome-rewards/)?

### jw...@chromium.org (2015-09-24)

It will be reviewed and the rewards panel will get back to you on this.

### m....@shapesecurity.com (2015-09-24)

Thank you.

### cl...@chromium.org (2015-09-24)

[Empty comment from Monorail migration]

### ti...@google.com (2015-11-28)

#10: Sorry for the reward delay - this fell off my radar due to missing some labels I use to track rewards. I've fixed the issue and shall get this taken care of in short order.



### ti...@google.com (2015-12-01)

As an update for #12, our reward panel decided to award you $500 for taking the time and effort to report this to us - congratulations!

We'll list you in our release notes as "mficarra@shapesecurity.com". If you would prefer to use another name for credit, please update this bug and I can update the release notes. I'll also provide you with a CVE ID in a few hours for your reference.

A member of our finance team should reach out within a week to arrange payment. If you don't hear from someone in the next week, please either update this bug or reach out to me directly at timwillis@.

Thanks again for your report!

### ti...@google.com (2015-12-01)

CVE-2015-6785

### m....@shapesecurity.com (2015-12-01)

Thanks. Please list me as "Michael Ficarra / Shape Security".

### ti...@google.com (2015-12-02)

Done: googlechromereleases.blogspot.com/2015/12/stable-channel-update.html

### ti...@google.com (2015-12-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-12-31)

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

This issue was migrated from crbug.com/chromium/534542?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082901)*

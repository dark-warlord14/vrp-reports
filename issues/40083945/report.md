# Cross-Origin CSS Attack with Service Worker

| Field | Value |
|-------|-------|
| **Issue ID** | [40083945](https://issues.chromium.org/issues/40083945) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>SecurityFeature, Blink>ServiceWorker |
| **CVE IDs** | CVE-2016-1692 |
| **Reporter** | [Deleted User] |
| **Assignee** | ho...@chromium.org |
| **Created** | 2016-03-25 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2687.0 Safari/537.36

Steps to reproduce the problem:
1. Download the attached file and unzip it.
2. Setup a web server for the two directories at localhost:8000 and localhost:8001.
3. Access localhost:8000/index.html and reload it once.

What is the expected behavior?
localhost:8000/index.html loads localhost:8001/secret.html as css via service worker:

-- localhost:8000/index.html --
<script> navigator.serviceWorker.register('serviceworker.js'); </script>
<link rel="stylesheet" href="style.css">

-- localhost:8000/serviceworker.js --
self.addEventListener('fetch', event => {
  if (!event.request.url.endsWith('style.css'))
    return;
  cssUrl = 'http://localhost:8001/secret.html';
  request = new Request(cssUrl, { mode: 'no-cors' });
  event.respondWith(fetch(request));
});

-- localhost:8001/secret.html --
html {
 background: green;
}

Normally, loading a css file with a content-type other than text/css should only succeed if it is same origin.
This is not the case so localhost:8000/index.html should not be able to load localhost:8001/secret.html as css.

What went wrong?
The site at localhost:8000/index.html loads style.css which should be on the same domain.
The service worker routes this request to a file on localhost:8001, however this is not considered when checking the origin of style.css.

Did this work before? N/A 

Chrome version: 51.0.2687.0  Channel: dev
OS Version: Kubuntu 15.10
Flash Version: Shockwave Flash 21.0 r0

The attack itself and an analysis of exploitability can be found here:
http://scarybeastsecurity.blogspot.de/2009/12/generic-cross-browser-cross-domain.html
https://www.linshunghuang.com/papers/css.pdf

## Attachments

- [sw.zip](attachments/sw.zip) (application/octet-stream, 1.1 KB)

## Timeline

### wf...@chromium.org (2016-03-26)

[Empty comment from Monorail migration]

[Monorail components: Blink>SecurityFeature Blink>ServiceWorker]

### wf...@chromium.org (2016-03-27)

Thanks for your report, I wonder if you could check in response headers what content type localhost:8001/secret.html is being returned at?

### [Deleted User] (2016-03-27)

The file is correctly served with content-type text/html. When loaded over service worker it also shows the following warning but interprets it regardless because it is seen as same origin:

Resource interpreted as Stylesheet but transferred with MIME type text/html: "http://localhost:8000/style.css".

### pe...@chromium.org (2016-03-29)

CC a few recommended experts to help confirm and triage (thank you).

### jw...@chromium.org (2016-03-31)

This is a very interesting one. I am able to repro, and I'm really unsure how we should be handling this case. Basically, what's happening is that because the original *request* was same origin (to style.css), the MIME type check passes even though it's *response* is cross-origin. Overall, this seems like incorrect behavior to me, but it's hard to tell.

Really, this seems like an extension of the problem in https://crbug.com/chromium/553535. Because of that, I'm assigning to falken@. falken@ and slightlyoff@, what do you think about this behavior?

### fa...@chromium.org (2016-04-01)

It does seem the same as https://crbug.com/chromium/553535 (and https://crbug.com/chromium/435446) which is blocked on the spec issue https://github.com/slightlyoff/ServiceWorker/issues/787.

Interestingly, Firefox, which seems to have a bug open for the same issue <https://bugzilla.mozilla.org/show_bug.cgi?id=1222008> disallows the CSS load:

The stylesheet http://localhost:8001/secret.html was not loaded because its MIME type, "text/html", is not "text/css".

horo@ what is your take on this?

### ke...@chromium.org (2016-04-05)

Can we resolve this specific issue by similarly blocking based on MIME type, to address this sooner?

### ja...@chromium.org (2016-04-06)

Agree that checking the mime-type should happen if the response url is cross-origin, regardless of request url.

### ho...@chromium.org (2016-04-06)

There is the same potential attack as https://crbug.com/chromium/419383.
So I think the priority of this issue should be 1.

I'll start work on this.

### ho...@chromium.org (2016-04-06)

[Empty comment from Monorail migration]

### jw...@chromium.org (2016-04-06)

Thanks, horo@.

Re: #7 and #8: Certainly that's what needs to happen, but my point has long been that we're going to keep seeing these types of issues until https://crbug.com/chromium/435446 is resolved, and fixing https://crbug.com/chromium/435446 is the generalized solution to this problem.

In short, request origins/URLs are basically not meaningful anymore for security checks, in a world with SWs.

### bu...@chromium.org (2016-04-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/3d9fa8719b092361eb0a6baec91d378599e74b75

commit 3d9fa8719b092361eb0a6baec91d378599e74b75
Author: horo <horo@chromium.org>
Date: Wed Apr 06 12:06:06 2016

Check the mime type of cross-origin CSS fetched via the Service Worker.

BUG=598077

Review URL: https://codereview.chromium.org/1861243002

Cr-Commit-Position: refs/heads/master@{#385441}

[add] https://crrev.com/3d9fa8719b092361eb0a6baec91d378599e74b75/third_party/WebKit/LayoutTests/http/tests/serviceworker/fetch-request-css-cross-origin-mime-check.html
[add] https://crrev.com/3d9fa8719b092361eb0a6baec91d378599e74b75/third_party/WebKit/LayoutTests/http/tests/serviceworker/resources/fetch-request-css-cross-origin-mime-check-cross.css
[add] https://crrev.com/3d9fa8719b092361eb0a6baec91d378599e74b75/third_party/WebKit/LayoutTests/http/tests/serviceworker/resources/fetch-request-css-cross-origin-mime-check-cross.html
[add] https://crrev.com/3d9fa8719b092361eb0a6baec91d378599e74b75/third_party/WebKit/LayoutTests/http/tests/serviceworker/resources/fetch-request-css-cross-origin-mime-check-iframe.html
[add] https://crrev.com/3d9fa8719b092361eb0a6baec91d378599e74b75/third_party/WebKit/LayoutTests/http/tests/serviceworker/resources/fetch-request-css-cross-origin-mime-check-same.css
[add] https://crrev.com/3d9fa8719b092361eb0a6baec91d378599e74b75/third_party/WebKit/LayoutTests/http/tests/serviceworker/resources/fetch-request-css-cross-origin-mime-check-same.html
[add] https://crrev.com/3d9fa8719b092361eb0a6baec91d378599e74b75/third_party/WebKit/LayoutTests/http/tests/serviceworker/resources/fetch-request-css-cross-origin-mime-check-worker.js
[modify] https://crrev.com/3d9fa8719b092361eb0a6baec91d378599e74b75/third_party/WebKit/Source/core/css/StyleSheetContents.cpp


### ho...@chromium.org (2016-04-12)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-04-12)

[Empty comment from Monorail migration]

### ti...@google.com (2016-05-24)

[Empty comment from Monorail migration]

### ti...@google.com (2016-05-26)

Our reward panel decided on $500 for this report - congratulations!

We've listed you in our release notes: http://googlechromereleases.blogspot.com/2016/05/stable-channel-update_25.html

Let me know if you want to donate the reward again, otherwise we can be in touch with details for payment.

CVE-ID is CVE-2016-1692

### [Deleted User] (2016-05-26)

Thanks! Please donate the reward to EWB USA as last time.

### aw...@chromium.org (2016-06-08)

Updating as $1,000 was paid to #17 in Til Jasper Ullrich's honor. Many thanks for the report and the donation!


### sh...@chromium.org (2016-07-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-14)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/598077?no_tracker_redirect=1

[Multiple monorail components: Blink>SecurityFeature, Blink>ServiceWorker]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083945)*

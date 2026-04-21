# upgrade-insecure-requests does not also upgrade navigational requests 

| Field | Value |
|-------|-------|
| **Issue ID** | [40084938](https://issues.chromium.org/issues/40084938) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>SecurityFeature, Blink>SecurityFeature>ContentSecurityPolicy |
| **Platforms** | Mac |
| **Reporter** | ia...@iancarrico.com |
| **Assignee** | ct...@chromium.org |
| **Created** | 2016-07-25 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36

Steps to reproduce the problem:
1. Create a webpage at a sample domain, served over HTTPS with the header "Content-Security-Policy: upgrade-insecure-requests"
2. Create links on the webpage to other locations on the same FQDN, but without https (e.g. http://example.com/subpage) 
3. Click on links to non-secure site

What is the expected behavior?
When you click a link to a non-secure site— it should upgrade the request to go to the https version. As per the W3 spec: https://www.w3.org/TR/upgrade-insecure-requests/#example-navigation

What went wrong?
The links are not upgraded, and the user is taken away from the https-secure site. 

Did this work before? N/A 

Chrome version: 51.0.2704.103  Channel: canary
OS Version: OS X 10.11.6
Flash Version: Shockwave Flash 22.0 r0

## Timeline

### ke...@chromium.org (2016-07-25)

Can you please provide a sample test case so that we know exactly what input seems to cause the behavior? Thanks. Will re-open if I get a test case that reproduces this.

### ia...@iancarrico.com (2016-07-25)

The exact behavior that would cause is a secure page with insecure hyperlinks to the same domain. With the "upgrade-insecure-requests" headers, it should upgrade those links. 

As to why this is important, and use case for this— is exactly what is in the spec. We have a site that has insecure content, and a lot of legacy links that we cannot manually update. This will keep users on the secure version of the site, even if there are legacy links that are http. 

### ke...@chromium.org (2016-07-25)

mkwst, can you take a look?

If the reporter's steps are correct, this sounds like a bug. However, note that
per the spec (https://www.w3.org/TR/upgrade-insecure-requests/#example-navigation), this upgrade does not apply to third party navigation links.

Ian, if you have a public website that reproduces this, that would be a big help.

### ia...@iancarrico.com (2016-07-25)

I do not have a public site right now— but I can make one and toss it somewhere in the morning. Currently using some private sandboxes to test the issue, I can share the link privately for some testing until then. 

### mk...@chromium.org (2016-07-26)

I'm OOO today, but I can take a look at this tomorrow. It would surprise me a bit if we'd regressed this behavior, but anything's possible!

Ian, what version of the browser are you testing in? The description says 51 and "canary", which don't match up at all. :)

### ia...@iancarrico.com (2016-07-26)

I tested in both 51 (the one I used to make the issue) and in Canary. 


### ri...@chromium.org (2016-07-26)

[Empty comment from Monorail migration]

[Monorail components: Blink>SecurityFeature]

### ri...@chromium.org (2016-07-26)

[Empty comment from Monorail migration]

### ia...@iancarrico.com (2016-08-04)

Howdy! A little late, but I did make a branch off of the Google Chrome samples page, and tossed it up on S3 to provide a test. Should all be there: 


https://s3.amazonaws.com/share.sbndev.net/csp/csp-upgrade-insecure-requests-navigation/index.html

### el...@chromium.org (2017-08-16)

The repro shared in https://crbug.com/chromium/631174#c9 shows that navigational requests are not upgraded in Chrome 62.3187 or Firefox 56b2.

Sending the Content-Security-Policy directive as a HTTP response header instead of a META did not help. Disabling Chrome's PlzNavigate feature didn't help.

### mk...@chromium.org (2017-08-24)

[Empty comment from Monorail migration]

[Monorail components: Blink>SecurityFeature>ContentSecurityPolicy]

### es...@chromium.org (2017-11-10)

[Empty comment from Monorail migration]

### es...@chromium.org (2018-02-18)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-04-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-02-05)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-09)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-20)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-16)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-26)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-07)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### ad...@google.com (2023-02-16)

(auto-cc on security bug)

### [Deleted User] (2023-04-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-31)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-10)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-11)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-11)

This issue was migrated from crbug.com/chromium/631174?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>SecurityFeature, Blink>SecurityFeature>ContentSecurityPolicy]
[Monorail components added to Component Tags custom field.]

### ct...@chromium.org (2025-02-27)

I'm having trouble reproducing this.

Here are my repro attempt steps:

0. Open DevTools network tab to be able to inspect requests and responses
1. Go to <https://http-me.glitch.me/html?header=Content-Security-Policy:upgrade-insecure-requests>
2. Verify in Network tab that the response includes the correct UIR header
3. Inspect the page content and add a link to <http://http-me.glitch.me/>
4. Click the link
5. See that the request goes directly to https:// (without an internal redirect as would happen if this was being upgraded by HTTPS-Upgrades)

### am...@chromium.org (2025-02-27)

this is not fixed, having to temporarily close as fixed; will reopen momentarily

### sp...@google.com (2025-02-27)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
report of lower impact exploitation mitigation bypass


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-02-27)

Hello! We are going through some of our oldest issues tracked as security bugs.
We're unsure when we'll come to a resolution on this one, but given the time and past discussions, we've earmarked this one for public disclosure. There is low potential for user harm from this issue and we feel it's reasonable to open this up despite not being resolved. Given this issue is related to a web spec we're not following, opening this issue for disclosure will also provide anyone from the Chromium community, such other Chromium browsers, Chromium embedders, or other contributors, to remark on or contribute to this discussion of a way forward related to UIR.

Since after all this time we remain unsure of when this will be resolved, we are going ahead and issuing a Chrome VRP reward for this report.
Thank you for your efforts and reporting this issue to us, as well as your patience while it remains on our backlog.

Cheers!

### ct...@chromium.org (2025-02-28)

WPTs were added for this case in [crrev.com/c/848836](https://crrev.com/c/848836), which if this had not been fixed yet may have incidentally fixed this issue as well. Those tests are passing (see [wpt.fyi](https://wpt.fyi/results/upgrade-insecure-requests/link-upgrade.sub.https.html?label=master&label=experimental&aligned&q=upgrade-insecure-requests%2F)) so I think we can close this bug as Fixed.

## Bounty Award

> report of lower impact exploitation mitigation bypass

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084938)*

# SameSite cookie bypass via source map

| Field | Value |
|-------|-------|
| **Issue ID** | [40091074](https://issues.chromium.org/issues/40091074) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>SecurityFeature, Internals>Network>Cookies, Internals>Sandbox>SiteIsolation, Platform>DevTools>Sources |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | s....@gmail.com |
| **Assignee** | sz...@google.com |
| **Created** | 2018-04-11 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36

Steps to reproduce the problem:
1. Register SameSite Strict cookie to your site.
2. Host attached file somewhere and change your-site to the site where you registered SameSite Cookie
3. Open hosted page
4. Open devtool

What is the expected behavior?
SameSite cookie not sent

What went wrong?
JS and CSS source map will send SameSite cookie when devtool is opened

Did this work before? N/A 

Chrome version: 65.0.3325.181  Channel: stable
OS Version: Windows 10 RS3
Flash Version:

## Attachments

- [bypass.html](attachments/bypass.html) (text/plain, 123 B)

## Timeline

### el...@chromium.org (2018-04-11)

Opening the Developer Tools on an attacker site isn't a common user-interaction (roughly on par with middle-clicking a link, also a SameSite-bypass), but it certainly seems reasonable to suppress SameSite cookies for sourcemaps, especially if the markup in which they appear is not same-origin to the sourcemap URL.

### s....@gmail.com (2018-04-12)

[Comment Deleted]

### s....@gmail.com (2018-04-12)

It happened to me once that I haven't opened devtools and source maps are requested. But I can't repro it constantly. It might be easier to get info from dev that when source maps are requested. If there's a way to make source map request without opening a devtool, then that would send a cookie.

### ca...@chromium.org (2018-04-13)

[Empty comment from Monorail migration]

[Monorail components: Blink>SecurityFeature Internals>Network>Cookies]

### ca...@chromium.org (2018-04-13)

[Empty comment from Monorail migration]

### mk...@chromium.org (2018-04-24)

pfeldman@: Handing this to you just for a question: is there a way to cause a sourcemap request that doesn't involve opening devtools? It's not at all clear to me where these requests are initiated, pointers would be helpful. :)

### pf...@chromium.org (2018-04-24)

DevTools needs to be open to issue a sourcemap request.

Front-end side request: https://cs.chromium.org/chromium/src/third_party/blink/renderer/devtools/front_end/sdk/SourceMap.js?q=SourceMap.js&sq=package:chromium&dr&l=224

Actual fetch: https://cs.chromium.org/chromium/src/chrome/browser/devtools/devtools_ui_bindings.cc?type=cs&q=devtools_ui_bindings&sq=package:chromium&l=748

### ts...@chromium.org (2018-05-02)

[Empty comment from Monorail migration]

### mk...@chromium.org (2018-10-04)

(Unassigning myself, marking untriaged in preparation to retriage with folks who will do a better job taking care of cookies than I've been able to)

### mk...@chromium.org (2019-02-12)

CCing some folks who might have bandwidth.

### lu...@chromium.org (2019-05-23)

Most likely this is also a Sec-Fetch-Site bypass (since AFAIK both SameSite cookies and Sec-Fetch-Site both rely on network::ResourceRequest::request_initiator).

[Monorail components: Internals>Sandbox>SiteIsolation]

### lu...@chromium.org (2019-06-11)

pfeldman@, is it possible for DevToolsUIBindings::LoadNetworkResource to know the origin that specified the |url| argument and set that as network::ResourceRequest::request_initiator?

By "the origin that specified the |url| argument" I mean:
1. The origin that responded with X-SourceMap or SourceMap header [1]
     or the origin of the javascript file that had a "//# sourceMappingURL=..." https://crbug.com/chromium/831731#c2. The origin of the sourcemap that triggered additional fetches via "sourceRoot" or "sources" [2]

By "know the origin" I mean knowing the origin based on trustworthy data (e.g. browser-side data is trustworthy and data from a renderer process hosting a web page is less trustworthy;  I know very little of how DevTools works - i.e. whether some pieces are hosted in the same renderer process as a webpage being debugged).

[1] https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/SourceMap
[2] https://docs.google.com/document/d/1U1RGAehQwRypUTovF1KRlpiOFze0b-_2gc6fAH0KY0k/edit#heading=h.75yo6yoyk7x5

### lu...@chromium.org (2019-06-11)

I think DevTools (e.g. DevToolsUIBindings::LoadNetworkResource) needs to properly set/propagate network::ResourceRequest - therefore I hope it is okay if now I assign the bug to pfeldman@.

[Monorail components: Platform>DevTools]

### na...@chromium.org (2019-06-14)

Adding caseq@, since I don't think pfeldman@ works actively on Chrome anymore.

### ca...@chromium.org (2019-06-14)

Well, I guess this one would have got routed to me even if he were here ;-)

### ca...@chromium.org (2019-06-14)

[Empty comment from Monorail migration]

### lu...@chromium.org (2019-06-27)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-07-01)

[Empty comment from Monorail migration]

### lu...@chromium.org (2019-07-02)

This bug feels like a Security_Severity-Medium:
1) This is a CSRF-enabling bug (e.g. a web app should be able to rely on Chrome securely implementing web security features like SameSite cookies and/or Sec-Fetch-Site)
2) Other similar bugs (https://crbug.com/chromium/966507 and https://crbug.com/chromium/831761) are already marked as Security_Severity-Medium.

### lu...@chromium.org (2019-07-02)

Hmmm... palmer@ points ouyt that if the attack only works if the victim opens dev tools, that bumps it down 1 level of severity...

### mk...@chromium.org (2019-07-17)

Since it's fetch metadata hackit day, I'll try to figure out how any of this works. :)

### lu...@chromium.org (2019-07-17)

[Empty comment from Monorail migration]

### ca...@chromium.org (2019-07-18)

[Empty comment from Monorail migration]

### ca...@chromium.org (2019-08-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### lu...@chromium.org (2020-01-15)

I think mkwst@ is not actively working on this bug.  Let me reassign to caseq@ for finding an owner from the DevTools team.  Also adding sigurds@ who asked about expected |request_initiator| behavior VS source maps.

### lu...@chromium.org (2020-01-15)

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

### bd...@chromium.org (2020-10-15)

@caseq, are there any updates to this bug or anyone that can be assigned this? (friendly marshal)

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-20)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-11)

[Empty comment from Monorail migration]

### fs...@chromium.org (2021-09-14)

Is this still a thing?
It seems it has been publicly disclosed for a while now: https://weizman.github.io/?javascript-anti-debugging-some-next-level-shit-part-1
And the article has been recently picked up by some aggregators.

### lu...@chromium.org (2021-09-15)

sigurds@, can you PTAL?  Is this still a problem after your on work on https://crbug.com/chromium/1069378?  (i.e. does DevTools now correctly propagate request_initiator for source map requests and other similar requests?)

### pf...@chromium.org (2021-09-16)

dsv@, can you take a look?

### [Deleted User] (2021-09-22)

[Empty comment from Monorail migration]

### ds...@chromium.org (2021-10-14)

[Empty comment from Monorail migration]

### ds...@chromium.org (2021-10-14)

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

### ad...@chromium.org (2022-11-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### bm...@chromium.org (2022-12-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### ad...@google.com (2023-02-16)

(auto-cc on security bug)

### [Deleted User] (2023-04-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-31)

[Empty comment from Monorail migration]

### bm...@chromium.org (2023-06-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-27)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

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

This issue was migrated from crbug.com/chromium/831731?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>SecurityFeature, Internals>Network>Cookies, Internals>Sandbox>SiteIsolation, Platform>DevTools]
[Monorail blocking: crbug.com/chromium/786673, crbug.com/chromium/843478, crbug.com/chromium/979231]
[Monorail mergedwith: crbug.com/chromium/988267]
[Monorail components added to Component Tags custom field.]

### na...@chromium.org (2025-01-08)

Assigning to bmeurer@, as we are moving all security bugs to be owned by someone. Feel free to reassign to a more appropriate owner.

### sz...@google.com (2025-01-13)

This has been fixed (probably) with <https://crrev.com/c/1399515> and no longer reproduces (tested with 134.0.6953.0 (Official Build) (64-bit))

### sp...@google.com (2025-01-23)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
report of lower impact exploitation mitigation bypass


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-01-23)

Thanks for your past efforts and reporting this issue to us, Jun!

### s....@gmail.com (2025-01-23)

Happy to help! :) Thanks for the ~~spot bonus~~ reward!

### ch...@google.com (2025-04-22)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091074)*

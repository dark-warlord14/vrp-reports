# iOS QR code spoof: embedded backslashes

| Field | Value |
|-------|-------|
| **Issue ID** | [379818904](https://issues.chromium.org/issues/379818904) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Mobile |
| **Platforms** | iOS |
| **Reporter** | ze...@gmail.com |
| **Assignee** | am...@google.com |
| **Created** | 2024-11-19 |
| **Bounty** | $1,000.00 |

## Description

VULNERABILITY DETAILS

We are currently investigating QR code issues across various browsers and have discovered that Chrome on iOS may be susceptible to certain phishing attacks when handling QR codes.

When Chrome scans a QR code on iOS, it attempts to truncate the full URL based on the backslash somehow, trying to display only the SLD in the pop-up. However, when users click the pop-up, Chrome may truncate certain characters in the URL during navigation, potentially redirecting users to a different, misleading website.

VERSION

Chrome Version: 131.0.6778.73

Operating System: iOS 18.1

REPRODUCTION CASE

1. Create a QR code which contains `http://msdn.com\\@long.long.evil.com`. You can use the first attached picture.
2. Open chrome on iOS then use the build-in camera to scan this QR code.
3. Seeing the second attached picture, user may think it is `msdn.com` and it is a safe link.
4. After clicking the pop-up, user will be directed to `long.long.evil.com`.

CREDIT INFORMATION Reporter credit: Zeddy in CUHK

## Attachments

- [446.png](attachments/446.png) (image/png, 1.4 KB)
- [IMG_1645.jpeg](attachments/IMG_1645.jpeg) (image/jpeg, 1.8 MB)

## Timeline

### nh...@chromium.org (2024-11-19)

mahmadi: Can you find an owner for this bug?

### pe...@google.com (2024-11-20)

Setting milestone because of s2 severity.

### pe...@google.com (2024-11-20)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### pe...@google.com (2024-12-06)

itslawrence: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ze...@gmail.com (2024-12-12)

Any updates here?

### it...@google.com (2024-12-17)

It appears the URL truncation logic is handled outside on the server side: <http://google3/lens/common/barcode_utils.h;l=15;rcl=453628821>, <http://google3/vision/visualsearch/server/lens/mixer/gleam_metadata_extractor.cc;l=26;rcl=453628821>

Looking for the right person to investigate this issue and the other ones.

### pe...@google.com (2024-12-31)

itslawrence: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ze...@gmail.com (2025-02-21)

any updates?

### it...@google.com (2025-02-21)

Hi! Apologies, haven't had the bandwidth lately to look into this further. I haven't been able to repro this on the Lens side (iGA, Lens standalone), which seems to be WAI: <https://screencast.googleplex.com/cast/NjEyODY5MjQzNzcxMjg5Nnw3ZmU2YmVkZi02MQ>. While the truncation behavior is the same (msdn.com), the link that is opened in Lens is indeed msdn.com, not evil.com. In fact, entering this URL directly into the browser header on Chrome routes me to the expected website, msdn.com. I assume Chrome uses the QR code detection/display logic from Lens, and it seems like the underlying browser does handle the link in the same way as iGA, so not sure why the Chrome QR code flow is handling this URL differently. @cm...@google.com any ideas on why this might be happening?

### ze...@gmail.com (2025-02-24)

yes. That's true. We tested different apps that use the Google Lens, including Google Chrome(Android), Google Lens(Android), Google Chrome(iOS) and Google App(iOS)(as no Google Lens provided on iOS). So far we only found that Google Chrome on iOS has this unique behavior, which may put users under phishing attacks.

As we don't have the source code, we assume there is somewhere in Chrome iOS that may santinize the URL differently than other apps.

### el...@chromium.org (2025-02-25)

Security shepherd: -> rohitrao@ for iOS triage, since this seems not to be a Lens bug but rather specific to iOS Chrome.

### ro...@google.com (2025-02-27)

Over to Mark for Fundamentals triage.

### fe...@google.com (2025-02-27)

I confirm I'm able to reproduce this issue on iOS. I will investigate code to find the root cause, will keep you posted.

### st...@google.com (2025-02-27)

The link preview is in Lens Viewfinder, which is an internal component. Charles, please take a look!

### fe...@google.com (2025-02-27)

Hello Charles, this vulnerability seems to be a real issue. Can we prioritize its resolution ASAP?

### cm...@google.com (2025-02-27)

Printed the URLs that are passed up to the Host App

- Bling: `http://msdn.com%5C@long.long.evil.com`
- iGA: `http://msdn.com/@long.long.evil.com`

### no...@google.com (2025-02-28)

Maybe a useful resource: When Chrome displays an URL in the UI, it uses a fairly complex set of rules to potentially elide parts of it if the space is too small. Those have stand the test of time, maybe a good inspiration?

<https://crsrc.org/c/components/url_formatter/elide_url.h>

### cm...@google.com (2025-03-03)

Update, we've identified potential fixes on the Lens side and are in discussion about which one to apply.

### ch...@google.com (2025-03-18)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Some CLs listed in the “Fixed By Code Changes” field are invalid and have been removed. Please provide an appropriate Gerrit url that matches the pattern: `https://<host>-review.googlesource.com/c/<repo>/+/<change_number>` or use the value 'NA' and re-mark this bug as fixed. If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### no...@google.com (2025-03-19)

Can you add a link to the CL that actually fixes the issue? The current linked CL just adds a flag. Thanks.

### ch...@google.com (2025-03-19)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M135. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [135].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### cm...@google.com (2025-03-19)

1. Which CLs should be backmerged? (Please include Gerrit links.)

The bot removed all the relevant CLs. Please consider updating the bot!

Fix (in google3):

- <https://critique.corp.google.com/cl/736209497>
- <https://critique.corp.google.com/cl/736653638>

Lens Feature flag wiring/bridging to potentially turn off fix (not strictly required, but nice to have?):

- <https://chromium-review.googlesource.com/c/chromium/src/+/6353941>
- <https://chrome-internal-review.googlesource.com/c/chrome/ios_internal/+/8103766>

2. Has this fix been verified on Canary to not pose any stability regressions?
   yes.
3. Does this fix pose any potential non-verifiable stability risks?
   no.
4. Does this fix pose any known compatibility risks?
   no.
5. Does it require manual verification by the test team? If so, please describe required testing.
   no.

### am...@chromium.org (2025-03-20)

The bot is specifically designed to reject non-public / non-Chromium CL links as the function of this field and automation is specifically related to security automation and and visibility of security changes in Chromium.
Security merge review here is only related to the Chromium side of the fixes. Since this is a bug in Lens rather than in Chrome itself, security merge for Chromium isn't really relevant here.

This probably should have been reported to Google rather than Chrome, given the root source in Lens, however, given the manifestation in Chrome, it's understood why it was reported here, there's just no security merge review relevant since the security fix changes are not on the Chromium side.

### am...@chromium.org (2025-03-21)

deleted

### ch...@google.com (2025-03-22)

The older reward-topanel [issue 379805718](https://issues.chromium.org/issues/379805718) has been merged into this one. Please manually review this issue to see if the duplicate is potentially eligible for a reward.

### ch...@google.com (2025-03-22)

The older reward-topanel [issue 379764831](https://issues.chromium.org/issues/379764831) has been merged into this one. Please manually review this issue to see if the duplicate is potentially eligible for a reward.

### ze...@gmail.com (2025-03-25)

May I know the root cause and the patch? I don't think it is fair to just merge these reports into this one because one patch works for three payloads and the patch is not public. And the paylods in the other two reports can make slightly different attack effects. Open to discussing this and hearing your perspective.

### am...@chromium.org (2025-03-25)

Hello, your three separate POCs and bug reports are variations on the same root cause -- lack of appropriate application level barcode parsing and allowing for URL spoofing in QR codes on iOS. This was solved by a single code change to enable specific barcode parsing capabilities. The other CLs are related to introducing the feature flag so that it can be enabled or disabled.
We can't provide the visibility to that code change here, because unlike Chromium, Lens is a Google feature used in Chrome, but is not open source code.

Multiple reports and POCs that are a variation of an issue but are the result of a specific, shared root cause (and resolution) are considered to be a one issue, with the duplicate reports merged into the canonical report accordingly.

### ze...@gmail.com (2025-03-26)

btw, may I know the release plan?

### am...@chromium.org (2025-03-26)

The fix will be shipped in the first M136 Stable channel release of Chrome

### am...@chromium.org (2025-03-26)

[comment #30](https://issues.chromium.org/issues/379818904#comment30) made me realize I didn't update this bug with the off-bug conversations
The fix in Lens was rolled into Chromium as part of Lens auto-roll, which happens twice per day. There is, however, no Canary build for iOS.
In tandem, this issue -- while a security issue -- has a lower potential impact for exploitability and harm and I've reduced the severity to reflect that. Based on both these considerations, it was decided not to backmerge the fix or flag changes to support it.

The fix will be released with the first release of M136 Stable channel.

### sp...@google.com (2025-03-26)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
report of lower impact security UI spoof


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-03-26)

Congratulations Zeddy! Thank you for your efforts and reporting this issue to us.

### ze...@gmail.com (2025-04-10)

btw, will this have a CVE number?

### am...@chromium.org (2025-04-10)

CVEs are assigned at the time the fix ships in a Stable channel update of Chrome. [1]

[1] <https://chromium.googlesource.com/chromium/src/+/main/docs/security/vrp-faq.md#will-i-receive-a-cve-for-my-bug>

### ze...@gmail.com (2025-05-26)

I think the patch works on the latest stable Chrome on iOS but I checked the change logs from March to now and didn't see some logs about this issue and didn't see any CVEs related to this. Is there anything I missed?

### am...@chromium.org (2025-05-27)

Thanks for reaching out. 
The fix did ship in the M136 Stable milestone release, but it looks like our automation didn't pick this one up for the advisory / release notes and CVE. 
I've added the appropriate tags so that it can be picked up in our clean-up processes. 
(cc: pgrace@) 

### ch...@google.com (2025-06-28)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ze...@gmail.com (2026-01-20)

Still no CVE assigned? Or it will not be assigned?

## Bounty Award

> report of lower impact security UI spoof

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/379818904)*

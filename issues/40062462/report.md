# Security: Possible to include mixed content in an about:blank popup opened by a https page

| Field | Value |
|-------|-------|
| **Issue ID** | [40062462](https://issues.chromium.org/issues/40062462) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>SecurityFeature |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | fa...@gmail.com |
| **Assignee** | ca...@chromium.org |
| **Created** | 2023-01-02 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Typically, a https site can't use or access resources from a http site. The browser will block attempts by a https site to include a http resources.

this vulnerability is similar to <https://bugs.chromium.org/p/chromium/issues/detail?id=957002>

**REPRODUCTION CASE**

1. Load a https site example: <https://www.google.com>
2. Use console to open popup tab using:

w = open("about:blank");

3. Try to load http hosted image using:

w.document.write('<img src="http://www.clascertification.com/\_img/\_public/actualites/medium\_52-Cap\_Sici.jpg">');

in the above case the system will warn about mixed content and upgrades the link to https (<http://www.clascertification.com/_img/_public/actualites/medium_52-Cap_Sici.jpg>).

4. Try to load again using data uri inside iframe using:

w.document.write('<iframe src="data:text/html,<img src=http://www.clascertification.com/\_img/\_public/actualites/medium\_52-Cap\_Sici.jpg>"></iframe>');

Here the system also warns about mixed content but fails to upgrade the link to https.

In Case of Step 3:  

Mixed Content: The page at '<https://www.google.com/>' was loaded over HTTPS, but requested an insecure element '<http://www.clascertification.com/_img/_public/actualites/medium_52-Cap_Sici.jpg>'. This request was automatically upgraded to HTTPS, For more information see <https://blog.chromium.org/2019/10/no-more-mixed-messages-about-https.html>

In Case of Step 4:  

Mixed Content: The page at '<https://www.google.com/>' was loaded over HTTPS, but requested an insecure image '<http://www.clascertification.com/_img/_public/actualites/medium_52-Cap_Sici.jpg>'. This content should also be served over HTTPS.

First one upgrades while second one fails to upgrade but warns with (This content should also be served over HTTPS).

## Attachments

- deleted (application/octet-stream, 0 B)
- [poc.mp4](attachments/poc.mp4) (video/mp4, 4.4 MB)
- [Screenshot 2025-03-19 220238.png](attachments/Screenshot 2025-03-19 220238.png) (image/png, 294.2 KB)
- [no-upgrade-vuln.png](attachments/no-upgrade-vuln.png) (image/png, 13.9 KB)
- [omnibox-icon-change-no-upgrade.png](attachments/omnibox-icon-change-no-upgrade.png) (image/png, 132.0 KB)

## Timeline

### [Deleted User] (2023-01-02)

[Empty comment from Monorail migration]

### fa...@gmail.com (2023-01-04)

VERSION
108.0.5359.125 (Official Build) (64-bit) (cohort: Stable) 


### da...@chromium.org (2023-01-04)

Per https://bugs.chromium.org/p/chromium/issues/detail?id=957002: This should fail, given that the window that was opened is same-origin with the original https page. However, it doesn't and the iframe is loaded successfully.

This reproduces in stable M108.

Copying labels from https://bugs.chromium.org/p/chromium/issues/detail?id=957002

[Monorail components: Blink>SecurityFeature]

### da...@chromium.org (2023-01-04)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-04)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-04)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### fa...@gmail.com (2023-01-09)

friendly ping.

### fa...@gmail.com (2023-01-25)

I wanted to check in and make sure that there has been progress on this open issue. Could you please provide an update on the current status and let me know when it will be resolved?

### fa...@gmail.com (2023-02-06)

This vulnerability enables an attacker to initiate Insecure HTTP requests on an HTTPS site, making it vulnerable to man-in-the-middle attacks.

### ca...@chromium.org (2023-02-16)

Sorry about the delay. Looks like the issue here is that the FetchClientSettingsObject (https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/loader/mixed_content_checker.cc;drc=7cc3323e070b7271e8c801775475260249e5b9eb;l=770) used to check whether or not something is mixed content is set to the data URL in the case that fails, so it is not detected as a secure URL, and thus doesn't trigger the upgrade.

I'm trying to figure out how why we are using the data url here instead of the security origin

### ca...@chromium.org (2023-02-16)

Taking a closer look, looks like the check is indeed done with GetSecurityOrigin, but that returns null for the data url case

### ad...@google.com (2023-02-16)

(auto-cc on security bug)

### fa...@gmail.com (2023-04-03)

Friendly ping 

### fa...@gmail.com (2023-05-02)

[Comment Deleted]

### fa...@gmail.com (2023-06-08)

It has been more than 4 months since I reported this bug, and there has been no discussion or update regarding this issue. Team, could you please provide any updates on this matter?

### fa...@gmail.com (2023-10-29)

Friendly ping

### is...@google.com (2023-10-29)

This issue was migrated from crbug.com/chromium/1404470?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### fa...@gmail.com (2024-02-20)

Friendly ping.

### fa...@gmail.com (2024-05-21)

Hi, friendly ping.

### fa...@gmail.com (2024-07-09)

The site I used here for testing is currently outdated (<http://www.clascertification.com/_img/_public/actualites/medium_52-Cap_Sici.jpg>). We could use <http://aogarantiza.com/google_logo.png> instead.

### am...@chromium.org (2024-07-13)

Hi Shaheen, the correct team is tracking this issue. This is a low-severity issue, so there is no SLO here. Such issues come only after prioritized work and critical tasks are in order.
Thank you for your patience in the meantime.

### fa...@gmail.com (2025-03-19)

I have made a commit <https://chromium-review.googlesource.com/c/chromium/src/+/6367881> to address this issue.

- Test:
  
  ```
  w = window.open("about:blank");
  w.document.write('<iframe src="data:text/html,<img src=http://aogarantiza.com/google_logo.png>"></iframe>');
  
  ```
  
  The new changes block any embedding of HTTP content inside an HTTPS page when using `data:` URLs.
- Verified normal behavior:
  
  ```
  w.document.write('<iframe src="data:text/html,<img src=https://www.google.com/logos/2024/moon/moon_march-rc2/cta.png>"></iframe>');
  
  ```
  
  Embedding HTTPS content works without any issues.

These changes ensure improved mixed content blocking while maintaining expected functionality.

### fa...@gmail.com (2025-03-19)

I haven't disclosed the main security issue in the commit as it requires an iframed `data:` URL to bypass mixed content. However, the fix ensures that content inside framed `data:` URLs is blocked. Thanks.

### to...@chromium.org (2025-03-21)

I have 2 questions here.

Is this a mixed content problem among a page and windows opened from the page, rather than in a single page issue?
I am not an expert in the mixed content problem, and an not sure how our policy about this case on mixed content is.
Let me invite Mile West here to discuss the problem with professional views.

Another question is on the direction to resolve this problem.
IIUC, you are trying to resolve this by disallowing using data urls for subframes, right? If so, I think this has a very big impact, and could cause a breakage in many sites.
Can we check the opener page's scheme instead?

### fa...@gmail.com (2025-03-21)

> Is this a mixed content problem among a page and windows opened from the page, rather than in a single page issue?

It's a single-page issue as well. We don't need to open about:blank as a new tab here (See the attached image for this weird behavior). Also, a similar issue was fixed in the past for reference regarding security issues: Chromium [Issue 40094750](https://issues.chromium.org/issues/40094750).

Basically, in this issue, a secured framed data URL with insecure content is neither upgraded nor blocked. Instead, a warning is shown, but no action is taken.

> Another question is on the direction to resolve this problem.

Yes, we could try different methods, but usually, it’s either upgrading the insecure scheme or blocking it. However, no **data URLs** are blocked in the process. As I have shown in the screenshot in **[comment #23](https://issues.chromium.org/issues/40062462#comment23)**, **data URLs** work as expected, and even secure content can function within them.

If the **data URL** is inside a secure page and an insecure resource is introduced within an iframe inside that **data URL**, we should be blocking it (or at least upgrading it to HTTPS), which is the root cause of this issue.

As for the fix, I am trying to solve this by reusing the already implemented blocking feature for mixed content, specifically for iframes with **data URLs** (`frame->GetDocument()->Url().ProtocolIsData()`). In this case, blocking is preventing any insecure content (HTTP) from loading within a secure (HTTPS) parent page—so only HTTP content would be blocked if it is inside an HTTPS parent (**Mixed Content**).

```
// For data: URLs, treat Mixed Content as blockable
      if (frame->GetDocument()->Url().ProtocolIsData()) {
        allowed = false;
        break;
      }

```

`allowed = false` may seem like we are completely blocking the **data URL**, but I believe this value is meant to prevent mixed content by blocking the **insecure resource** inside the **data URL** when the parent page is secure.

### fa...@gmail.com (2025-03-21)

See also [comment #4](https://issues.chromium.org/issues/40062462#comment4) and [comment #11](https://issues.chromium.org/issues/40062462#comment11) for context. [Comment #11](https://issues.chromium.org/issues/40062462#comment11) also helped me look into mixed\_content\_checker.cc, where I made this simple fix. Maybe a more complex fix is needed, but this seems to work building with this change.

Regarding the screenshot attached in **[comment #23](https://issues.chromium.org/issues/40062462#comment23)**, to avoid confusion:

- The **first browser window** shows the fix blocking the mixed content.
- The **second browser window** shows the behavior without the fix, where mixed content is present, and the browser appears to show a warning.

However, if we check the **network section**(second browser window), the resource (image) is still being loaded over **HTTP** and hasn't actually been upgraded/blocked.

### to...@google.com (2025-03-24)

changed as Googlers' visible.
I will ping security experts in the internal chat so that someone from the team can take a look.

### ca...@chromium.org (2025-03-24)

Thanks for the proposed fix! While that does fix this case, I suspect there will be other opaque origin cases where this issue will continue, since it does not address the root cause.

I believe a full fix for the root cause would be to make ShouldAutoupgrade use the same check that IsMixedContent already uses, which takes opaque origins into account (https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/loader/mixed_content_checker.cc;drc=8d201f296ea4efda4529e69fd9509be8abd63156;l=293). I put together a CL with this change (crrev.com/c/6388538), but I still need to fix some tests before it's ready.

### dx...@google.com (2025-05-08)

Project: chromium/src  

Branch: main  

Author: Carlos IL [carlosil@chromium.org](mailto:carlosil@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6388538>

Mixed Content: Use the same check for ShouldAutoUpgrade and IsMixedContent

---


Expand for full commit details
```
     
    Currently IsMixedContent determines whether mixed content is restricted 
    in a particular context by checking if its security origin or precursor 
    if opaque is https (https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/loader/mixed_content_checker.cc;drc=8d201f296ea4efda4529e69fd9509be8abd63156;l=293), whereas ShouldAutoupgrade only checks the 
    security origin, which is null if opaque (https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/loader/mixed_content_checker.cc;drc=8d201f296ea4efda4529e69fd9509be8abd63156;l=867). 
     
    This can lead to some requests not being autoupgraded when they should be. 
     
    Bug: 40062462 
    Change-Id: I10c381e407a0693ae262533027fad9e2c37fa365 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6388538 
    Auto-Submit: Carlos IL <carlosil@chromium.org> 
    Commit-Queue: Carlos IL <carlosil@chromium.org> 
    Reviewed-by: Takashi Toyoshima <toyoshim@chromium.org> 
    Reviewed-by: Emily Stark <estark@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1457364}

```

---

Files:

- M `third_party/blink/renderer/core/frame/remote_frame.cc`
- M `third_party/blink/renderer/core/loader/frame_loader.cc`
- M `third_party/blink/renderer/core/loader/mixed_content_checker.cc`
- M `third_party/blink/renderer/core/loader/mixed_content_checker.h`
- M `third_party/blink/renderer/core/loader/mixed_content_checker_test.cc`
- M `third_party/blink/renderer/core/loader/worker_fetch_context.cc`

---

Hash: 3e9801630f7a3697936eb90d31185542abd8f60c  

Date:  Thu May 8 01:32:19 2025


---

### fa...@gmail.com (2025-05-13)

Hi Carlos, thank you for the CL. Could you please close this issue as fixed/resolved? (With Gerrit link to the CL that resolved the issue in the 'Fixed by code changes' field.)

### dx...@google.com (2025-05-16)

Project: chromium/src  

Branch: main  

Author: Carlos IL [carlosil@chromium.org](mailto:carlosil@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6525688>

Add killswitch for mixed content autoupgrade using IsMixedContentRestrictedInFrame

---


Expand for full commit details
```
     
    This behavior change was added in crrev.com/c/6388538 as a fix for 
    crbug.com/40062462. This adds a (default on) feature flag as a 
    killswitch in case the fix results in any breakage. 
     
    Fixed: 40062462 
    Change-Id: I76b197576fe698e8f2f302c22b6b48c0eae46a58 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6525688 
    Commit-Queue: Carlos IL <carlosil@chromium.org> 
    Reviewed-by: Takashi Toyoshima <toyoshim@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1461677}

```

---

Files:

- M `third_party/blink/renderer/core/loader/mixed_content_checker.cc`
- M `third_party/blink/renderer/platform/runtime_enabled_features.json5`

---

Hash: aa485810fe8a130244e4b86367d89726a3d8e572  

Date:  Fri May 16 23:46:00 2025


---

### ch...@google.com (2025-05-16)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### sp...@google.com (2025-05-21)

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

### am...@chromium.org (2025-05-22)

Thank you for your efforts and reporting this issue to us!

### fa...@gmail.com (2025-05-22)

Thankyou 😊.

### ch...@google.com (2025-08-24)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062462)*

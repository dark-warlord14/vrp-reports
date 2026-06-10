# Security: Guess a cross-origin iframe URL by firing multiple navigations

| Field | Value |
|-------|-------|
| **Issue ID** | [41485206](https://issues.chromium.org/issues/41485206) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Navigation |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | re...@gmail.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2023-12-18 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

This is a bypass for <https://crbug.com/chromium/1248444>.

It is possible to figure out whether a cross-origin iframe is on a specific URL by firing multiple hash-navigations at the same time, and then counting the onload events fired. If the URL you're navigating to fires more than one load event, it was previously on the same URL.

Eg if the iframe is on `example.org/foo` and you navigate to `example.org/foo#a`, `example.org/foo#b`, and `example.org/foo#c`, you will get three onload events, but if the iframe starts off on `example.org/bar` you will only get one.

**VERSION**  

Chrome Version: 122.0.6182.0 Dev + Stable  

Operating System: Windows, Linux, macOS

**REPRODUCTION CASE**  

In this example I am using [www.chromium.org](http://www.chromium.org) because it redirects to [www.chromium.org/chromium-projects/](http://www.chromium.org/chromium-projects/), which we will detect.

1. Download the `poc.html` file and open it.
2. Write "<https://www.chromium.org/>" in both inputs.
3. Click "Set URL" and wait for the page to load.
4. Click "Check URL". The URL in the iframe should NOT match.
5. Repeat 2-4, but write "<https://www.chromium.org/chromium-projects/>" in the bottom input. This time the iframe URL should match.

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Lyra Rebane (rebane2001)

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 1.1 KB)
- [demo.mov](attachments/demo.mov) (video/quicktime, 2.6 MB)

## Timeline

### [Deleted User] (2023-12-18)

[Empty comment from Monorail migration]

### me...@chromium.org (2023-12-18)

Thanks for the report. I can repro on stable. japhet, could you PTAL?

[Monorail components: Internals>Sandbox>SiteIsolation UI>Browser>Navigation]

### [Deleted User] (2023-12-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-19)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2024-01-01)

japhet: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### cr...@chromium.org (2024-01-12)

japhet@: Any thoughts on this one?

My guess is that a bit of a race is involved, between a cross-document navigation committing and the next navigation starting.  The PoC does this:

  for (let i = 0; i < 5; i++)
    iframe.src = `${url}#` + Math.random();

There's no waiting between the navigations, so the difference between correct and incorrect guesses is that same-document navigations commit synchronously and cannot be interrupted by the next navigation, but cross-document navigations would kick off a network request and might get canceled if the next navigation request arrives before commit.

It's a little more subtle than that because the victim frame will often be in a different process, but that doesn't change the outcome.  If process A sends 5 consecutive IPCs telling process B to navigate to a URL, then process B will either generate 5 consecutive DispatchLoad event IPCs to make their way back to process A (if it's same document and the DispatchLoad / commit happen synchronously) or it will keep canceling the previous cross-document navigation when receiving the next IPC, only sending one DispatchLoad event IPC to process A at the end.

If that's true, then in theory more DispatchLoads could happen if there's enough time between the IPCs for each navigation to commit.  I think I verified that by setting a breakpoint in the main frame process in RemoteFrame::Navigate to give time between the navigations, and then the page reports a match when the URL is incorrect.

Cross-document navigations will usually fail that race in practice, though, so I'm not sure what to suggest here.  Maybe change the fix from r931681 to start a timer to do the DispatchLoad, such that any subsequent navigations cancel the timer rather than firing extra DispatchLoads?  Other thoughts?

CC'ing rakina@ from https://crbug.com/chromium/1248444 and clamy@ for general XSLeaks advice.  This is also more XSLeaks than Site Isolation, so updating the component/hotlist.

[Monorail components: -Internals>Sandbox>SiteIsolation]

### [Deleted User] (2024-01-15)

japhet: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2024-01-25)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2024-01-25)

This issue was migrated from crbug.com/chromium/1512629?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### ps...@google.com (2024-02-15)

Hello japhet@,

Is there any updates for this bug? Has the suggestion at #8 been investigated or confirmed?

[Secondary security shepherd]


### ja...@chromium.org (2024-10-08)

Sorry for sitting on this so long, it dropped off my radar.

The analysis in comment #8 matches my understanding. A little bit of experimentation indicates that it requires a relatively lightweight and fast-loading site to trigger the same-url detection, but it might be worth trying queueing the load timer to make these attacks less reliable.

### pe...@google.com (2024-10-26)

japhet: Uh oh! This issue still open and hasn't been updated in the last 17 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2024-11-10)

japhet: Uh oh! This issue still open and hasn't been updated in the last 32 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ja...@chromium.org (2025-02-06)

[secondary shepherd]

Hi japhet@, are you going to follow up on your recommendation from [comment#13](https://issues.chromium.org/issues/41485206#comment13)? Are you still a good owner for this bug? If not, can you reassign it to someone who can implement the change you recommended?

### dx...@google.com (2026-02-24)

Project: chromium/src  

Branch:  main  

Author:  Nate Chapin [japhet@chromium.org](mailto:japhet@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7560041>

Fire load event for same-document nav initiated by cross-origin parent on a delayed timer

---


Expand for full commit details
```
     
    Fixed: 41485206 
    Change-Id: I905e09a080d5bd715becf00c99375f3bc144240e 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7560041 
    Reviewed-by: Charlie Reis <creis@chromium.org> 
    Commit-Queue: Nate Chapin <japhet@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1589055}

```

---

Files:

- M `third_party/blink/renderer/core/loader/document_loader.cc`
- M `third_party/blink/renderer/core/loader/document_loader.h`
- M `third_party/blink/web_tests/http/tests/navigation/cross-origin-fragment-navigation-is-async-expected.txt`
- M `third_party/blink/web_tests/http/tests/navigation/cross-origin-fragment-navigation-is-async.html`

---

Hash: [9a4f5dc8779d4e11b96c043fb54a2977b89664a1](https://chromiumdash.appspot.com/commit/9a4f5dc8779d4e11b96c043fb54a2977b89664a1)  

Date: Tue Feb 24 01:08:34 2026


---

### sp...@google.com (2026-03-11)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Baseline. User information disclosure


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-03)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41485206)*

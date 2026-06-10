# Tricking a user into a same-page drag-and-drop can disclose data to cross-origin frames

| Field | Value |
|-------|-------|
| **Issue ID** | [409972635](https://issues.chromium.org/issues/409972635) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>DataTransfer, Blink>FencedFrames, Blink>Portals, UI>Browser>Navigation>MPArch |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | lu...@chromium.org |
| **Assignee** | dt...@chromium.org |
| **Created** | 2025-04-11 |
| **Bounty** | $1,000.00 |

## Description

# Steps to reproduce the problem

1. Clone <https://github.com/KallynGowdy/chrome-iframe-bug> or use the attached .zip file
2. Serve index.html and iframe.html on port <http://localhost:8081>.
3. Go to <http://localhost:8081> and open the console.
4. Drag a file into the window.
5. Observe that MAIN WINDOW ENTER is logged to the console.
6. Go to <http://127.0.0.1:8081> and open the console.
7. Drag a file into the window.
8. Observe that IFRAME WINDOW ENTER is logged to the console.

# Problem Description

System Info:
135.0.7049.85 (Official Build) (arm64)
macOS Version 15.3.1 (Build 24D70)
JavaScript V8 13.5.212.10
User Agent Mozilla/5.0 (Macintosh; Intel Mac OS X 10\_15\_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36
Command Line /Applications/Google Chrome.app/Contents/MacOS/Google Chrome --restart --flag-switches-begin --flag-switches-end

For some reason, the iframe captures the dragenter and dragleave events when it is loaded from a different domain, but doesn't when loaded from the same domain.
Other event types might be affected, but I've only tested dragenter and dragleave.

Additionally, I tested the following combinations of origins:

- site -> iframe: result
- localhost:8081 -> localhost:8081: correct
- 127.0.0.1:8081 -> localhost:8081: incorrect
- localhost:8081 -> 127.0.0.1:8081: incorrect
- localhost:8081 -> localhost:8082: correct
- localhost:8081 -> mac.localhost:8081: incorrect

So, at least from my testing, differing only in origin (by port number) is not enough to trigger the bug. It has to be a different domain.

I've tested MacOS and Windows, and so far the bug only happens on MacOS. Additionally, this behavior is not present in other web browsers (e.g. Safari).

# Additional Comments

Google Chrome 135.0.7049.85 (Official Build) (arm64)
Revision 1e112499da812a1dde62101ed601dcb93024aaff-refs/branch-heads/7049@{#1779}
OS macOS Version 15.3.1 (Build 24D70)
JavaScript V8 13.5.212.10
User Agent Mozilla/5.0 (Macintosh; Intel Mac OS X 10\_15\_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36
Command Line /Applications/Google Chrome.app/Contents/MacOS/Google Chrome --restart --flag-switches-begin --flag-switches-end
Executable Path /Applications/Google Chrome.app/Contents/MacOS/Google Chrome
Profile Path /Users/kallyngowdy/Library/Application Support/Google/Chrome/Profile 3
Linker lld

# Summary

Cross-origin iframe captures dragenter, dragleave, events when behind other elements

# Custom Questions

#### Reporter credit:

Kallyn Gowdy

# Additional Data

Category: Security   

Chrome Channel: Stable   

Regression: N/A

## Attachments

- [drag-bug.zip](attachments/drag-bug.zip) (application/zip, 31.4 KB)
- [variations.txt](attachments/variations.txt) (text/plain, 54.0 KB)
- [Chrome Iframe Drag Bug.mov](attachments/Chrome Iframe Drag Bug.mov) (video/quicktime, 59.9 MB)

## Timeline

### ka...@yeticgi.com (2025-04-11)

I actually uploaded a version that sets the iframe to 300x300px, so to actually reproduce the bug with the uploaded version you will need to drag the file over where the iframe is and not just into the window. If you set the iframe to 100%x100% then that will also demonstrate the bug.

### fl...@google.com (2025-04-15)

Can you include a video so I can see what exactly your setup is / what's being dragged/dropped? I wasn't able to reproduce this locally.

Furthermore, I don't think this is a security bug. It might be a bug in how events are handled via iframes but I don't think any security boundaries are being violated here.

That being said I may be able to reassign this to someone more familiar with iframe behavior if I'm able to reproduce. Thanks!

### ka...@yeticgi.com (2025-04-15)

Hi, here's a video that demonstrates the issue. In short, make sure that the iframe is set to 100% width and 100% height (the bug still exists when the iframe is sized differently, but it is easier to reproduce when it covers the entire window) and drag a file from the file explorer into the window.

And I reported this as a security bug because it is a potential data disclosure bug (similar to clickjacking), where a malicious iframe could capture the contents of a file that a user is trying to drag into a trusted site. 

### dt...@chromium.org (2025-04-15)

Can repro. Agree that this seems different based on the process renderers the iframe is placed in. Charlie is this a duplicate of anything open?

### ka...@yeticgi.com (2025-06-11)

Are there any updates on this?

On Tue, Apr 15, 2025, 3:07 PM <buganizer-system@google.com> wrote:

> Replying to this email means your email address will be shared with the
> team that works on this product.
> https://issues.chromium.org/issues/409972635
>
> *Changed*
>
> *dt...@chromium.org <dt...@chromium.org> added comment #5
> <https://issues.chromium.org/issues/409972635#comment5>:*
> Can repro. Agree that this seems different based on the process renderers
> the iframe is placed in. Charlie is this a duplicate of anything open?
> _______________________________
>
> *Reference Info: 409972635 Cross-origin iframe captures dragenter,
> dragleave, events when behind other elements*
> component:  Public Trackers > 1362134 > Chromium > Internals > Sandbox >
> SiteIsolation <https://issues.chromium.org/components/1456652>
> status:  New
> reporter:  kallyn.gowdy@yeticgi.com
> cc:  cr...@chromium.org, fl...@google.com, kallyn.gowdy@yeticgi.com
> collaborators:  se...@chromium.org
> type:  Bug
> access level:  Limited visibility
> priority:  P4
> severity:  S4
> hotlist:  external_security_report
> <https://issues.chromium.org/hotlists/5433527>, Unconfirmed
> <https://issues.chromium.org/hotlists/5437934>
> retention:  Component default
> BuildNumber:  135.0.0.0
> Component Ancestor Tags:  Internals, Internals>Sandbox,
> Internals>Sandbox>SiteIsolation
> Component Tags:  Internals>Sandbox>SiteIsolation
> OS:  Mac
>
>
> Generated by Google IssueTracker notification system.
>
> You're receiving this email because you are subscribed to updates on
> Google IssueTracker issue 409972635
> <https://issues.chromium.org/issues/409972635> where you have the roles:
> cc, reporter
> Unsubscribe from this issue.
> <https://issues.chromium.org/issues/409972635?unsubscribe=true>
>


### fl...@google.com (2025-06-11)

(Assigning, in case you missed this earlier~)

### cr...@chromium.org (2025-06-11)

Sorry for missing this before. dcheng@ may be the right one to take a first look, and maybe it can go to input event folks if it isn't specific to drag and drop. (The closest I can think of is past issues with drags within the same page like [issue 40057823](https://issues.chromium.org/issues/40057823), but this is a drag of a file into a page, which is different.)

### dc...@chromium.org (2025-06-13)

I wasn't able to reproduce the exact scenario, but I definitely did see some weirdness.

Mac implementation is backed by <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/web_contents/web_drag_dest_mac.mm;l=321;drc=46e0a7fb3fd7c4951efd982ae2caf138e20d2a95>

Other platforms are implemented using <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/web_contents/web_contents_view_aura.cc;l=1517;drc=46e0a7fb3fd7c4951efd982ae2caf138e20d2a95>

Notably, we're not using the same function to look up the target RWH, and I suspect that's the root cause of the weirdness we're seeing here. I'm guessing the right fix is to port <https://chromium-review.googlesource.com/c/chromium/src/+/1693442> to Mac as well... but the author (and reviewer) of that CL are gone. I'll have to ask around to see who can help own this on the Mac side.

### ka...@yeticgi.com (2025-08-08)

Just checking on the status of this again. Is there anything new to note?

### dc...@chromium.org (2025-12-08)

(Making sure this gets re-triaged; I don't really work on drag-and-drop anymore but I do help consult still from time to time)

### ro...@microsoft.com (2025-12-23)

This should be fixed with - chromium-review.googlesource.com/c/chromium/src/+/7255554

### ch...@google.com (2025-12-23)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2026-05-14)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### sp...@google.com (2026-05-27)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
Baseline. User information disclosure


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

## Bounty Award

> Baseline. User information disclosure

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/409972635)*

# Sandbox escape: bypass allow-popups-to-escape-sandbox

| Field | Value |
|-------|-------|
| **Issue ID** | [40057525](https://issues.chromium.org/issues/40057525) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature>IFrameSandbox |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | nd...@protonmail.com |
| **Assignee** | ar...@chromium.org |
| **Created** | 2021-10-05 |
| **Bounty** | $2,500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36

Steps to reproduce the problem:
Go to the following with the popup blocker disabled.
https://terjanq.me/xss.php?html=%3Ciframe%20sandbox=%22allow-popups%20allow-same-origin%20allow-scripts%22%20src=%22//a.terjanq.me/xss.php?html=%3Ciframe%20name=b%3E%3C/iframe%3E%3Cscript%3Eb.open(%27//c.terjanq.me/xss.php?js=alert()%27)%3C/script%3E%22%3E

What is the expected behavior?
Sandbox inheritance to be enforced,
So window.origin === "null"

What went wrong?
When a website uses the sandbox attribute with "allow-same-origin allow-scripts allow-popups" in a crossorigin iframe,
Its still possible to create a popup thats escaped from the sandbox. Bypassing the need for "allow-popups-to-escape-sandbox"

Did this work before? N/A 

Chrome version: 94.0.4606.71  Channel: stable
OS Version: 10.0

This works because a blank iframe without src srcdoc.
Does not apply the normal policy to window.open();

## Timeline

### [Deleted User] (2021-10-05)

[Empty comment from Monorail migration]

### xi...@chromium.org (2021-10-05)

Thanks for the report. Triaging it following the previous iframe sandbox escape bug (https://crbug.com/1014371).

+mkwst@ to take a look. Thanks!

[Monorail components: Blink>SecurityFeature>IFrameSandbox]

### [Deleted User] (2021-10-05)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-07)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-10-07)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aa...@google.com (2021-10-12)

[Empty comment from Monorail migration]

### nd...@protonmail.com (2021-10-12)

Sandbox also does not seem to get applied based of its opener before sending the initial request.
So while the origin changes later cookies still get sent with the first request ideally a sandbox would never be send cookies unless allow-same-origin is used.

### mk...@chromium.org (2021-10-13)

Assigning to Arthur, who knows things about sandbox.

That said, I'm not sure I understand the PoC. If you're specifying `allow-same-origin`, why would you expect `window.origin` to be null?

### te...@google.com (2021-10-13)

The origin shouldn't be null, though the bypass is valid. 

"allow-same-origin allow-popups allow-scripts" shouldn't allow for modals, even in popups, if "allow-popups-escape-sandbox" is not set. The PoC executes alert() triggered from a sandboxed iframe. 

The bug seems to lie in empty iframe that doesn't inherit sandbox, hence with "allow-same-origin" it's possible to do something like empty_iframe.contentWindow.open('') and the new popup escaped the sandbox. It's also possible to achieve the same in devtools without "allow-same-origin" token, but then accessing empty frame is tough because of the 'null' origin, and when srcdoc or src is set seems to not escape the sandbox but maybe this could still be somehow bypassed.


### ar...@chromium.org (2021-10-13)

Thanks for reporting this bug!

I agree the bypass is valid too. I tried sending a form from the popup and I wasn't blocked.

The initial empty document is a special case, it is tested and expected it to be properly handled:
See related design and patch about this edge case:
- https://docs.google.com/document/d/1KY0DCaoKjUPbOX28N9KWvBjbnAfQEIRTaLbZUq9EkK8/edit#heading=h.d4a6nk89y2i9
- https://chromium-review.googlesource.com/c/chromium/src/+/2741587

I will take a look soon, once I am no more busy with Android sherrifing.

### nd...@protonmail.com (2021-10-13)

The reason I put window.origin === "null" was a mistake the use of allow-same-origin was only used in the proof of concept, originally it was found with devtools.
https://crbug.com/chromium/1256822#c7 is a separate "issue".

### ar...@chromium.org (2021-10-15)

New regression tests:
https://chromium-review.googlesource.com/c/chromium/src/+/3225890

(now investigating)

### ar...@chromium.org (2021-10-15)

Bisection:

```
./tools/bisect-builds.py --good=76.0.3809.111 --bad=94.0.4606.81 --archive=linux64 --use-local-cache
Scanning from 665002 to 911515 (246513 revisions).
Downloading list of known revisions... 
Loaded revisions 41523-931993 from /home/arthursonzogni/chromium/src/tools/.bisect-builds-cache.json
Downloading revision 758380...
Received 131588932 of 131588932 bytes, 100.00%
Bisecting range [665006 (good), 911494 (bad)], roughly 16 steps left.
Trying revision 758380...
Revision 758380 is [(g)ood/(b)ad/(r)etry/(u)nknown/(s)tdout/(q)uit]: g
Downloading revision 821235...
Bisecting range [758380 (good), 911494 (bad)], roughly 15 steps left.
Trying revision 821235...
Revision 821235 is [(g)ood/(b)ad/(r)etry/(u)nknown/(s)tdout/(q)uit]: g
Downloading revision 854124...
Bisecting range [821235 (good), 911494 (bad)], roughly 14 steps left.
Trying revision 854124...
Revision 854124 is [(g)ood/(b)ad/(r)etry/(u)nknown/(s)tdout/(q)uit]: g
Downloading revision 873704...
Bisecting range [854124 (good), 911494 (bad)], roughly 13 steps left.
Trying revision 873704...
Revision 873704 is [(g)ood/(b)ad/(r)etry/(u)nknown/(s)tdout/(q)uit]: b
Downloading revision 864180...
Bisecting range [854124 (good), 873704 (bad)], roughly 12 steps left.
Trying revision 864180...
Revision 864180 is [(g)ood/(b)ad/(r)etry/(u)nknown/(s)tdout/(q)uit]: b
*Downloading revision 859391...
Bisecting range [854124 (good), 864180 (bad)], roughly 11 steps left.
Trying revision 859391...
Revision 859391 is [(g)ood/(b)ad/(r)etry/(u)nknown/(s)tdout/(q)uit]: g
Revision 859391 is [(g)ood/(b)ad/(r)etry/(u)nknown/(s)tdout/(q)uit]: g
Downloading revision 861638...
Bisecting range [859391 (good), 864180 (bad)], roughly 10 steps left.
Trying revision 861638...
Revision 861638 is [(g)ood/(b)ad/(r)etry/(u)nknown/(s)tdout/(q)uit]: g
Downloading revision 862756...
Bisecting range [861638 (good), 864180 (bad)], roughly 9 steps left.
Trying revision 862756...
Revision 862756 is [(g)ood/(b)ad/(r)etry/(u)nknown/(s)tdout/(q)uit]: g
Downloading revision 863476...
Bisecting range [862756 (good), 864180 (bad)], roughly 8 steps left.
Trying revision 863476...
Revision 863476 is [(g)ood/(b)ad/(r)etry/(u)nknown/(s)tdout/(q)uit]: b
Downloading revision 863118...
Bisecting range [862756 (good), 863476 (bad)], roughly 7 steps left.
Trying revision 863118...
Revision 863118 is [(g)ood/(b)ad/(r)etry/(u)nknown/(s)tdout/(q)uit]: g
Downloading revision 863238...
Bisecting range [863118 (good), 863476 (bad)], roughly 6 steps left.
Trying revision 863238...
Revision 863238 is [(g)ood/(b)ad/(r)etry/(u)nknown/(s)tdout/(q)uit]: g
Downloading revision 863310...
Bisecting range [863238 (good), 863476 (bad)], roughly 5 steps left.
Trying revision 863310...
Revision 863310 is [(g)ood/(b)ad/(r)etry/(u)nknown/(s)tdout/(q)uit]: g
Downloading revision 863378...
Bisecting range [863310 (good), 863476 (bad)], roughly 4 steps left.
Trying revision 863378...
Revision 863378 is [(g)ood/(b)ad/(r)etry/(u)nknown/(s)tdout/(q)uit]: b
Downloading revision 863339...
Bisecting range [863310 (good), 863378 (bad)], roughly 3 steps left.
Trying revision 863339...
Revision 863339 is [(g)ood/(b)ad/(r)etry/(u)nknown/(s)tdout/(q)uit]: g
Downloading revision 863351...
Bisecting range [863339 (good), 863378 (bad)], roughly 2 steps left.
Trying revision 863351...
Revision 863351 is [(g)ood/(b)ad/(r)etry/(u)nknown/(s)tdout/(q)uit]: g
Downloading revision 863371...
Bisecting range [863351 (good), 863378 (bad)], roughly 2 steps left.
Trying revision 863371...
Revision 863371 is [(g)ood/(b)ad/(r)etry/(u)nknown/(s)tdout/(q)uit]: g
You are probably looking for a change made after 863371 (known good), but no later than 863378 (first known bad).
CHANGELOG URL:
  https://chromium.googlesource.com/chromium/src/+log/1174b24d4ab875ef8ecd10138990e00b57eb8939..ab1016da76663ac8f0b060e156425acd5def27a3

```

Which points to myself:
https://chromium.googlesource.com/chromium/src/+/e0d975fcd7e9675b732667639a8be249c22ed01a

Version: 91.0.4449.0

### gi...@appspot.gserviceaccount.com (2021-10-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ab32e8aacb08c9fce0dc4bf09eec456ba46e3710

commit ab32e8aacb08c9fce0dc4bf09eec456ba46e3710
Author: Arthur Sonzogni <arthursonzogni@chromium.org>
Date: Tue Oct 19 12:05:04 2021

[sandbox] Add WPT. Inheritance popup/empty iframe.

From a sandboxed iframe allowing popups, scripts, and same-origin. Open
a popup using the WindowProxy of a new iframe that is still on the
initial empty document. Check the sandbox flags are properly inherited.

Bug: 1256822
Change-Id: I0c21f2b909f61483559ebf22dca1c4369c9fcdf5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3225890
Auto-Submit: Arthur Sonzogni <arthursonzogni@chromium.org>
Reviewed-by: Antonio Sartori <antoniosartori@chromium.org>
Commit-Queue: Antonio Sartori <antoniosartori@chromium.org>
Commit-Queue: Arthur Sonzogni <arthursonzogni@chromium.org>
Cr-Commit-Position: refs/heads/main@{#932960}

[modify] https://crrev.com/ab32e8aacb08c9fce0dc4bf09eec456ba46e3710/third_party/blink/web_tests/external/wpt/html/browsers/sandboxing/window-open-blank-from-different-initiator.html
[add] https://crrev.com/ab32e8aacb08c9fce0dc4bf09eec456ba46e3710/third_party/blink/web_tests/external/wpt/html/browsers/sandboxing/resources/execute-postmessage.html
[modify] https://crrev.com/ab32e8aacb08c9fce0dc4bf09eec456ba46e3710/third_party/blink/web_tests/external/wpt/html/browsers/sandboxing/resources/executor.html
[add] https://crrev.com/ab32e8aacb08c9fce0dc4bf09eec456ba46e3710/third_party/blink/web_tests/external/wpt/html/browsers/sandboxing/popup-from-initial-empty-sandboxed-document.window-expected.txt
[add] https://crrev.com/ab32e8aacb08c9fce0dc4bf09eec456ba46e3710/third_party/blink/web_tests/external/wpt/html/browsers/sandboxing/popup-from-initial-empty-sandboxed-document.window.js


### gi...@appspot.gserviceaccount.com (2021-10-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/62f4f82ad39f177538f733b37cdd5dabd8f333de

commit 62f4f82ad39f177538f733b37cdd5dabd8f333de
Author: Arthur Sonzogni <arthursonzogni@chromium.org>
Date: Thu Oct 21 11:44:35 2021

sandbox: Fix sandbox inheritance.

Patch description:
------------------
When creating a new frame and the initial empty document, blink was only
sending the frame's sandbox attribute, but without combining with its owner's
(=document) sandbox flags.

This patch combines frame's attribute with its document sandbox flags.

🎁 Arthur Sonzogni wishes for a better future: 🎁
-------------------------------------------------
There are no good reasons sandbox flags inheritance to be complicated.
See: content/browser/renderer_host/sandbox_flags.md

For legacy reasons, Chrome's developers were confused about what objects
have frame or document semantic. On the browser process, the
FrameTreeNode represents the frame and the RenderFrameHost is almost
(%RenderDocument) the document/execution-context.

Currently, sandbox flags is plumbed inside FramePolicy, and it is not
clear to me whether FramePolicy is a frame-scoped or document-scoped
property (or both).
The current logic speak about "pending" FramePolicy (=frame) and
"active" FramePolicy (=document) and store both type into the
FrameTreeNode and RenderFrameHost, which is not ideal.

I believe we should extract SandboxFlags outside of FramePolicy and
make a very clean implementation, parallel to the PolicyContainer logic.
In a second step it could also be integrated into PolicyContainer, if we
resolve the additional property that sandbox flags can also be further
restricted at the frame level, similar to CSP embedded enforcement.

Bug: 1256822, 1262061
Change-Id: Id38de6d7eeeb1e4fa7722ab56288666763fae838
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3231298
Commit-Queue: Antonio Sartori <antoniosartori@chromium.org>
Auto-Submit: Arthur Sonzogni <arthursonzogni@chromium.org>
Reviewed-by: Antonio Sartori <antoniosartori@chromium.org>
Reviewed-by: Mike West <mkwst@chromium.org>
Cr-Commit-Position: refs/heads/main@{#933845}

[modify] https://crrev.com/62f4f82ad39f177538f733b37cdd5dabd8f333de/content/browser/bad_message.h
[modify] https://crrev.com/62f4f82ad39f177538f733b37cdd5dabd8f333de/content/browser/renderer_host/render_frame_host_impl.cc
[modify] https://crrev.com/62f4f82ad39f177538f733b37cdd5dabd8f333de/third_party/blink/renderer/core/frame/web_local_frame_impl.cc
[delete] https://crrev.com/23df32844f0c76a1f75bb3484b15232586cda45d/third_party/blink/web_tests/external/wpt/html/browsers/sandboxing/popup-from-initial-empty-sandboxed-document.window-expected.txt
[modify] https://crrev.com/62f4f82ad39f177538f733b37cdd5dabd8f333de/tools/metrics/histograms/enums.xml
[modify] https://crrev.com/62f4f82ad39f177538f733b37cdd5dabd8f333de/content/browser/renderer_host/frame_tree_node.cc


### nd...@protonmail.com (2021-10-21)

SameSite cookies still get sent without the "allow-same-origin" sandbox attribute when doing window.open in a sandboxed iframe,
Since this allows a sandboxed window to have an authenticated response from a origin its not meant to access.
Please confirm if a sandboxed iframe with "allow-scripts allow-popups" is allowed to send cookies on window.open and only on the first request.


### nd...@protonmail.com (2021-10-27)

[Comment Deleted]

### ar...@google.com (2021-10-27)

Re https://crbug.com/chromium/1256822#c16: Yes, sandbox without allow-same-origin do not make the document to access separate Cookie jar. I was surprised myself. For instance, recently I added "Baseline sandbox test." to better understand cookies vs sandbox on Chrome/Firefox/Webkit:
https://chromium-review.googlesource.com/c/chromium/src/+/3136916
The current behavior (same cookie jar) is the currently expected behavior. IMO, it would be nice to change, but this would be an extremly large compatibility issue, breaking a large number of websites.


Re https://crbug.com/chromium/1256822#c17: I don't understand. This issue is indeed a bug. It has been fixed by https://crbug.com/chromium/1256822#c15. I will now ask to cherry-pick it back to lower versions.



### ar...@google.com (2021-10-27)

I am requesting cherry-picking the fix from https://crbug.com/chromium/1256822#c15 into M96.
It landed on 97.0.4678.0
https://chromiumdash.appspot.com/commit/62f4f82ad39f177538f733b37cdd5dabd8f333de

### [Deleted User] (2021-10-27)

Merge review required: M96 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ar...@chromium.org (2021-10-27)

I ran a bisection, verifying this is fixed by https://crbug.com/chromium/1256822#c15:
```
Scanning from 934307 to 933313 (994 revisions).
Downloading list of known revisions... 
Loaded revisions 41523-931993 from /home/arthursonzogni/chromium/src/tools/.bisect-builds-cache.json
Saved revisions 41523-935337 to /home/arthursonzogni/chromium/src/tools/.bisect-builds-cache.json
Downloading revision 934103...
Received 149757926 of 149757926 bytes, 100.00%
Bisecting range [933319 (bad), 934307 (good)], roughly 8 steps left.
Trying revision 934103...
Revision 934103 is [(g)ood/(b)ad/(r)etry/(u)nknown/(s)tdout/(q)uit]: g
Downloading revision 933699...
Received 149723866 of 149723866 bytes, 100.00%
Bisecting range [933319 (bad), 934103 (good)], roughly 7 steps left.
Trying revision 933699...
Revision 933699 is [(g)ood/(b)ad/(r)etry/(u)nknown/(s)tdout/(q)uit]: b
Downloading revision 933864...
Received 149735110 of 149735110 bytes, 100.00%
Bisecting range [933699 (bad), 934103 (good)], roughly 6 steps left.
Trying revision 933864...
Revision 933864 is [(g)ood/(b)ad/(r)etry/(u)nknown/(s)tdout/(q)uit]: g
Downloading revision 933783...
Received 149725905 of 149725905 bytes, 100.00%
Bisecting range [933699 (bad), 933864 (good)], roughly 5 steps left.
Trying revision 933783...
Revision 933783 is [(g)ood/(b)ad/(r)etry/(u)nknown/(s)tdout/(q)uit]: b
Downloading revision 933810...
Received 149727248 of 149727248 bytes, 100.00%
Bisecting range [933783 (bad), 933864 (good)], roughly 4 steps left.
Trying revision 933810...
Revision 933810 is [(g)ood/(b)ad/(r)etry/(u)nknown/(s)tdout/(q)uit]: b
Downloading revision 933845...
Received 149729247 of 149729247 bytes, 100.00%
Bisecting range [933810 (bad), 933864 (good)], roughly 3 steps left.
Trying revision 933845...
Revision 933845 is [(g)ood/(b)ad/(r)etry/(u)nknown/(s)tdout/(q)uit]: g
Downloading revision 933812...
Bisecting range [933810 (bad), 933845 (good)], roughly 2 steps left.
Trying revision 933812...
Revision 933812 is [(g)ood/(b)ad/(r)etry/(u)nknown/(s)tdout/(q)uit]: b
Downloading revision 933844...
Bisecting range [933812 (bad), 933845 (good)], roughly 2 steps left.
Trying revision 933844...
Revision 933844 is [(g)ood/(b)ad/(r)etry/(u)nknown/(s)tdout/(q)uit]: b
You are probably looking for a change made after 933844 (known bad), but no later than 933845 (first known good).
CHANGELOG URL:
  https://chromium.googlesource.com/chromium/src/+log/23df32844f0c76a1f75bb3484b15232586cda45d..62f4f82ad39f177538f733b37cdd5dabd8f333de
```


### ar...@chromium.org (2021-10-27)

1. Why does your merge fit within the merge criteria for these milestones?
=> This is a web platform security fix.

2. What changes specifically would you like to merge? Please link to Gerrit.
=> https://chromium-review.googlesource.com/c/chromium/src/+/3231298

3. Have the changes been released and tested on canary?
=> Yes. I double verified against the reproducer in bisection from https://crbug.com/chromium/1256822#c21

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
=> No

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
=> N/A (not Chrome OS Only)

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
=> This address an issue on the stable channel. However, I don't think this require a stable merge. Beta is fine, it will be stable on Nov 16th.

### nd...@protonmail.com (2021-10-27)

This report type has changed from "Bug-Security" to "Bug" is this intentional?

### ar...@google.com (2021-10-27)

> This report type has changed from "Bug-Security" to "Bug" is this intentional?

No, it changed from "" to "Bug". I can also use "Bug-Security".

### nd...@protonmail.com (2021-10-27)

I was not aware no type was an option, I thought it was the default based of other reports.

### am...@chromium.org (2021-10-27)

hi Arthur, presuming this bug is fully fixed since you manually requested a merge. Can you please update the status to Fixed, then sheriffbot can automatically request appropriate merges. Thanks! 

### ar...@google.com (2021-10-27)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-29)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-29)

[Empty comment from Monorail migration]

### am...@google.com (2021-10-29)

merge approved to M96, please merge to branch 4664 at your earliest convenience

### [Deleted User] (2021-11-02)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2021-11-02)

Please complete the merges to M96 branch today before 2pm PST so these changes can go out in beta release tomorrow and get beta verification and baking before stable promotion.

### sr...@google.com (2021-11-02)

mkwst@ or others on the bug, I tried creating a CP to M96 as Arthur is OOO but getting merge conflicts, can one of you help complete the merge to M96 asap.

### ar...@chromium.org (2021-11-03)

Pending cherry-pick here:
https://chromium-review.googlesource.com/c/chromium/src/+/3256558

### gi...@appspot.gserviceaccount.com (2021-11-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/855df1837e97de265be9cd9d5565d247348a823a

commit 855df1837e97de265be9cd9d5565d247348a823a
Author: Arthur Sonzogni <arthursonzogni@chromium.org>
Date: Wed Nov 03 12:49:50 2021

sandbox: Fix sandbox inheritance [M96 merge]

This is a cherry-pick of the following patch:
https://chromium-review.googlesource.com/c/chromium/src/+/3231298

Patch description:
------------------
When creating a new frame and the initial empty document, blink was only
sending the frame's sandbox attribute, but without combining with its owner's
(=document) sandbox flags.

This patch combines frame's attribute with its document sandbox flags.

🎁 Arthur Sonzogni wishes for a better future: 🎁
-------------------------------------------------
There are no good reasons sandbox flags inheritance to be complicated.
See: content/browser/renderer_host/sandbox_flags.md

For legacy reasons, Chrome's developers were confused about what objects
have frame or document semantic. On the browser process, the
FrameTreeNode represents the frame and the RenderFrameHost is almost
(%RenderDocument) the document/execution-context.

Currently, sandbox flags is plumbed inside FramePolicy, and it is not
clear to me whether FramePolicy is a frame-scoped or document-scoped
property (or both).
The current logic speak about "pending" FramePolicy (=frame) and
"active" FramePolicy (=document) and store both type into the
FrameTreeNode and RenderFrameHost, which is not ideal.

I believe we should extract SandboxFlags outside of FramePolicy and
make a very clean implementation, parallel to the PolicyContainer logic.
In a second step it could also be integrated into PolicyContainer, if we
resolve the additional property that sandbox flags can also be further
restricted at the frame level, similar to CSP embedded enforcement.

Bug: 1256822, 1262061
Change-Id: Id38de6d7eeeb1e4fa7722ab56288666763fae838
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3231298
Commit-Queue: Antonio Sartori <antoniosartori@chromium.org>
Auto-Submit: Arthur Sonzogni <arthursonzogni@chromium.org>
Reviewed-by: Antonio Sartori <antoniosartori@chromium.org>
Reviewed-by: Mike West <mkwst@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#933845}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3256558
Commit-Queue: Daniel Cheng <dcheng@chromium.org>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Cr-Commit-Position: refs/branch-heads/4664@{#695}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/855df1837e97de265be9cd9d5565d247348a823a/content/browser/bad_message.h
[modify] https://crrev.com/855df1837e97de265be9cd9d5565d247348a823a/content/browser/renderer_host/render_frame_host_impl.cc
[modify] https://crrev.com/855df1837e97de265be9cd9d5565d247348a823a/third_party/blink/renderer/core/frame/web_local_frame_impl.cc
[modify] https://crrev.com/855df1837e97de265be9cd9d5565d247348a823a/tools/metrics/histograms/enums.xml
[modify] https://crrev.com/855df1837e97de265be9cd9d5565d247348a823a/content/browser/renderer_host/frame_tree_node.cc


### am...@google.com (2021-11-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-11-03)

Congratulations! The VRP Panel has decided to award you $2500 for this report. Nice finding! 
In the future, please upload/attach the POC directly to the report rather than directing to an external website. In the future, the security sheriff triaging the report will not be able to pass this on to developers for work until the POC is directly attached to the report. 
Thank you! 

### nd...@protonmail.com (2021-11-03)

Thanks, it was not attached directly because it uses two origins and terjanq is also in this report.

### am...@google.com (2021-11-04)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-11-11)

[Empty comment from Monorail migration]

### ad...@google.com (2021-11-12)

[Empty comment from Monorail migration]

### ad...@google.com (2021-11-12)

ndevtk@protonmail.com re https://crbug.com/chromium/1256822#c38, a common approach is for people to give us a recipe to run python3 -m http.server a couple of times to make different origins (or sometimes fancier python scripts if custom headers are required, etc.)

### am...@google.com (2021-12-23)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1256822?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057525)*

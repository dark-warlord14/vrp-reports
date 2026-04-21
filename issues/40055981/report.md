# Security: Use after free in Payments

| Field | Value |
|-------|-------|
| **Issue ID** | [40055981](https://issues.chromium.org/issues/40055981) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Payments |
| **Platforms** | Mac, Windows |
| **Reporter** | zh...@gmail.com |
| **Assignee** | ma...@chromium.org |
| **Created** | 2021-05-24 |
| **Bounty** | $20,000.00 |

## Description

**VULNERABILITY DETAILS**  

<https://source.chromium.org/chromium/chromium/src/+/master:content/browser/payments/payment_instrument_icon_fetcher.cc;l=111;drc=0b4c01de4879deb0e3b288e3732641d1d9e343c9;bpv=1;bpt=1>

bool can\_download\_icon = ManifestIconDownloader::Download(  

web\_contents, icon\_url,  

payments::IconSizeCalculator::IdealIconHeight(native\_view),  

payments::IconSizeCalculator::MinimumIconHeight(),  

/\* maximum\_icon\_size\_in\_px= \*/ std::numeric\_limits<int>::max(),  

base::BindOnce(&OnIconFetched, web\_contents, copy\_icons, [1] cache a raw pointer 'web\_contents'  

std::move(callback)),  

false /\* square\_only \*/);

<https://source.chromium.org/chromium/chromium/src/+/master:content/browser/manifest/manifest_icon_downloader.cc;l=71;drc=0b4c01de4879deb0e3b288e3732641d1d9e343c9;bpv=1;bpt=1>

web\_contents->DownloadImageInFrame(  

initiator\_frame\_routing\_id, icon\_url,  

false, // is\_favicon  

ideal\_icon\_size\_in\_px, // preferred\_size  

maximum\_icon\_size\_in\_px, // max\_bitmap\_size - 0 means no maximum size.  

false, // bypass\_cache  

base::BindOnce(&ManifestIconDownloader::OnIconFetched, [2]  

ideal\_icon\_size\_in\_px, minimum\_icon\_size\_in\_px,  

square\_only,  

base::Owned(new DevToolsConsoleHelper(web\_contents)),  

std::move(callback)));

<https://source.chromium.org/chromium/chromium/src/+/master:content/browser/manifest/manifest_icon_downloader.cc;l=129;drc=0b4c01de4879deb0e3b288e3732641d1d9e343c9;bpv=1;bpt=1>

if (chosen.height() > ideal\_icon\_size\_in\_px ||  

chosen.width() > ideal\_icon\_width\_in\_px) {  

GetIOThreadTaskRunner({})->PostTask( [3] when calling ManifestIconDownloader::ScaleIcon, 'web\_contents' may have been destroyed.  

FROM\_HERE, base::BindOnce(&ManifestIconDownloader::ScaleIcon,  

ideal\_icon\_width\_in\_px, ideal\_icon\_size\_in\_px,  

chosen, std::move(callback)));  

return;  

}

<https://source.chromium.org/chromium/chromium/src/+/master:content/browser/payments/payment_instrument_icon_fetcher.cc;l=49;drc=0b4c01de4879deb0e3b288e3732641d1d9e343c9;bpv=1;bpt=1>

if (bitmap.drawsNothing()) {  

if (icons.empty()) {  

BrowserThread::GetTaskRunnerForThread(  

ServiceWorkerContext::GetCoreThreadId())  

->PostTask(FROM\_HERE,  

base::BindOnce(std::move(callback), std::string()));  

} else {  

// If could not download or decode the chosen image(e.g. not supported,  

// invalid), try it again with remaining icons.  

DownloadBestMatchingIcon(web\_contents, icons, std::move(callback)); [4]  

}  

return;  

}

<https://source.chromium.org/chromium/chromium/src/+/master:content/browser/payments/payment_instrument_icon_fetcher.cc;l=81;drc=0b4c01de4879deb0e3b288e3732641d1d9e343c9;bpv=1;bpt=1>

if (web\_contents == nullptr) {  

BrowserThread::GetTaskRunnerForThread(  

ServiceWorkerContext::GetCoreThreadId())  

->PostTask(FROM\_HERE,  

base::BindOnce(std::move(callback), std::string()));  

return;  

}

gfx::NativeView native\_view = web\_contents->GetNativeView(); [5] UAF occurs!  

GURL icon\_url = blink::ManifestIconSelector::FindBestMatchingIcon(  

icons, payments::IconSizeCalculator::IdealIconHeight(native\_view),  

payments::IconSizeCalculator::MinimumIconHeight(),  

ManifestIconDownloader::kMaxWidthToHeightRatio,  

blink::mojom::ManifestImageResource\_Purpose::ANY);

holding a raw pointer 'web\_contents' is not safe here[1], 'web\_contents' can be destroyed before OnIconFetched execute.

**VERSION**  

Chrome Version: [ 92.0.4506.0] + [dev]  

Operating System: [ubuntu20.10]

**REPRODUCTION CASE**

1. unzip poc.zip
2. patch renderer with renderer\_patch.diff
3. run python3 -m http.server
4. out/ReleaseAsan/chrome --user-data-dir=/tmp/nonexists/ <http://localhost:8000/poc.html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [browser]  

**Crash State: [see link above: stack trace \*with symbols\*, registers,**  

**exception record]**  

**Client ID (if relevant): [see link above]**

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

**Reporter credit: [goes here]**

## Attachments

- [poc.zip](attachments/poc.zip) (application/octet-stream, 4.7 KB)
- [asan.txt](attachments/asan.txt) (text/plain, 17.0 KB)
- [debuginfo.txt](attachments/debuginfo.txt) (text/plain, 8.2 KB)

## Timeline

### [Deleted User] (2021-05-24)

[Empty comment from Monorail migration]

### va...@chromium.org (2021-05-25)

[Empty comment from Monorail migration]

[Monorail components: Blink>Payments]

### ma...@chromium.org (2021-05-25)

Still confirming.

### ma...@chromium.org (2021-05-25)

I have not been able to reproduce the crash. zhanjiasong45@, How frequent does the crash happen on your side?

### va...@chromium.org (2021-05-26)

Thanks for the report! I've not been able to confirm this because it requires building with the patch. Doesn't reproduce with unpatched Chrome on Linux 92.0.4512.4 (Official Build) dev (64-bit).

Does the patch make it easier to repro or does it require a compromised renderer?
Setting severity High assuming compromised renderer requirement.

Setting impact HEAD based on the report.

### va...@chromium.org (2021-05-26)

[Empty comment from Monorail migration]

### zh...@gmail.com (2021-05-26)

this is a race condition, you may need to adjust the delay of setTimeout in poc.html.

### zh...@gmail.com (2021-05-26)

[Comment Deleted]

### [Deleted User] (2021-05-26)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### va...@chromium.org (2021-05-26)

[Empty comment from Monorail migration]

### zh...@gmail.com (2021-05-26)

this is a sandbox issue, it need a compromised renderer, the renderer-side patch renderer_patch.diff
 simulates a compromised renderer state.

### zh...@gmail.com (2021-05-26)

sorry for not noting that.

### ma...@chromium.org (2021-05-26)

One possible solution is to use GetWebContentsFromFrameRoutingIds() to get WebContents each time WebContents* is possible to have been released.

### ma...@chromium.org (2021-05-26)

[Empty comment from Monorail migration]

### ro...@google.com (2021-05-26)

Agreed, that's a good idea. Do you have cycles to work on this, Max?

### ma...@chromium.org (2021-05-26)

WIP: https://chromium-review.googlesource.com/c/chromium/src/+/2917455

### ro...@google.com (2021-05-26)

Thank you for the patch, Max. Can you audit the rest of WebContents*, RenderFrameHost*, and RenderFrameProcess* usage (or any other raw pointer) in the payments code, please?

### ma...@chromium.org (2021-05-26)

Audited WebContents*[1], I can't find any other callback related use case in payments.

[1] https://source.chromium.org/search?q=f:payments%20web_contents%5Cs%5C%3D%20-f:debug%20-f:java%20-f:test&start=11

### ma...@chromium.org (2021-05-26)

Had a more comprehensive for audit[1] to look for WebContents* usage in callbacks in payments. I have not been able to find any.

[1] https://source.chromium.org/search?q=f:payments%20bind%20Web_Contents%20-f:debug%20-f:java%20-f:test%20f:%5C.cc&start=31

### ma...@chromium.org (2021-05-26)

Had a audit to look for RenderFrameHost*[1] usage in callbacks in payments, I haven't been able to find any.

[1] https://source.chromium.org/search?q=f:payments%20bind%20RenderFrameHost%20-f:debug%20-f:java%20-f:test%20f:%5C.cc&start=1

### [Deleted User] (2021-05-26)

Setting milestone and target because of Security_Impact=Head and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2021-05-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/82f07b001803a52bd6aa4f287f2e7ac661c0036a

commit 82f07b001803a52bd6aa4f287f2e7ac661c0036a
Author: Liquan (Max) Gu <maxlg@chromium.org>
Date: Wed May 26 17:21:31 2021

chrome_payment_request_delegate null-checks WebContents before use

In ChromePaymentRequestDelegate::DoFullCardRequest(), WebContents*
should be null-check before use.

This is a preventative fix. We haven't seen any bug report about it.

Bug: 1212612
Change-Id: I629449c06eca09be539a12b00af20d860d9a6dd4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2920406
Reviewed-by: Rouslan Solomakhin <rouslan@chromium.org>
Commit-Queue: Liquan (Max) Gu <maxlg@chromium.org>
Cr-Commit-Position: refs/heads/master@{#886783}

[modify] https://crrev.com/82f07b001803a52bd6aa4f287f2e7ac661c0036a/chrome/browser/payments/chrome_payment_request_delegate.cc


### [Deleted User] (2021-05-26)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2021-05-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c82fe5cfc4ec0b05ba2ff6f799570a0464e1ef49

commit c82fe5cfc4ec0b05ba2ff6f799570a0464e1ef49
Author: Liquan (Max) Gu <maxlg@chromium.org>
Date: Wed May 26 17:22:34 2021

PaymentInstrumentIconFetcher avoids using released WebContents

Before the change, PaymentInstrumentIconFetcher uses WebContents* as a
callback parameter and WebContents* is possible to have been released
when the callback is invoked. This patch changes to make the class
avoids using WebContents as a callback parameter. Instead, it retrieves
WebContents* when the callbacks needs it so that the released
WebContents* will be null and UAF can be avoided.

Bug: 1212612
Change-Id: I028839986e259a780ff449dc9b73deb417a82e21
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2917455
Reviewed-by: Rouslan Solomakhin <rouslan@chromium.org>
Commit-Queue: Liquan (Max) Gu <maxlg@chromium.org>
Cr-Commit-Position: refs/heads/master@{#886784}

[modify] https://crrev.com/c82fe5cfc4ec0b05ba2ff6f799570a0464e1ef49/content/browser/payments/payment_instrument_icon_fetcher.cc


### ma...@chromium.org (2021-05-26)

[Empty comment from Monorail migration]

### ma...@chromium.org (2021-05-26)

 zhanjiasong45@, are you still able to trigger the issue after https://crbug.com/chromium/1212612#c24?

### [Deleted User] (2021-05-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-26)

This release blocking issue appears to be targeted for M92, which has already branched. Because this issue was marked as fixed after branch point, a merge of any CLs which landed on or after May 20 may be required. Please review whether or not any CLs should be merged ASAP, and if a merge is necessary apply the label Merge-Request-92 to begin the merge review process. If no merge is required, please simply remove the Merge-TBD label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@chromium.org (2021-05-26)

It seems like this issue is hard to be exploited. It requires a compromised renderer and it only happens rarely in a race condition. It's also an old issue.

So, no merging is needed.

### zh...@gmail.com (2021-05-27)

after patch with https://crbug.com/chromium/1212612#c24,  I get a NULL crash .

### gi...@appspot.gserviceaccount.com (2021-05-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2fa1a7d6fa1cd2135b11c3f81056f20785b90e7d

commit 2fa1a7d6fa1cd2135b11c3f81056f20785b90e7d
Author: Liquan (Max) Gu <maxlg@chromium.org>
Date: Thu May 27 04:44:17 2021

Revert "PaymentInstrumentIconFetcher avoids using released WebContents"

This reverts commit c82fe5cfc4ec0b05ba2ff6f799570a0464e1ef49.

Reason for revert: it causes a null pointer crash.

Original change's description:
> PaymentInstrumentIconFetcher avoids using released WebContents
>
> Before the change, PaymentInstrumentIconFetcher uses WebContents* as a
> callback parameter and WebContents* is possible to have been released
> when the callback is invoked. This patch changes to make the class
> avoids using WebContents as a callback parameter. Instead, it retrieves
> WebContents* when the callbacks needs it so that the released
> WebContents* will be null and UAF can be avoided.
>
> Bug: 1212612
> Change-Id: I028839986e259a780ff449dc9b73deb417a82e21
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2917455
> Reviewed-by: Rouslan Solomakhin <rouslan@chromium.org>
> Commit-Queue: Liquan (Max) Gu <maxlg@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#886784}

Bug: 1212612
Change-Id: I00e457a7df6c8030be723e7ac611aed99b9309e5
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2920970
Auto-Submit: Liquan (Max) Gu <maxlg@chromium.org>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#887044}

[modify] https://crrev.com/2fa1a7d6fa1cd2135b11c3f81056f20785b90e7d/content/browser/payments/payment_instrument_icon_fetcher.cc


### ro...@google.com (2021-05-27)

Sorry I missed that during the code review. The null pointer crash is due to a "use after move" of frame_routing_ids on line 121 in the patch:

https://chromium-review.googlesource.com/c/chromium/src/+/2917455/7/content/browser/payments/payment_instrument_icon_fetcher.cc#36

The frame_routing_ids have previously been moved into GetWebContentsFromFrameRoutingIds() on line 82.

The solution is to make GetWebContentsFromFrameRoutingIds() function take a const-ref of the frame_routing_ids instead of moving the std::unique_ptr<> into there:

WebContents* GetWebContentsFromFrameRoutingIds(
    const GURL& scope,
    const std::vector<GlobalFrameRoutingId>& frame_routing_ids);

### ro...@google.com (2021-05-27)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-27)

[Empty comment from Monorail migration]

### ma...@chromium.org (2021-05-27)

WIP reland: https://chromium-review.googlesource.com/c/chromium/src/+/2920672

### gi...@appspot.gserviceaccount.com (2021-05-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/908e3e3a134cb3b9a741ea31aedb2f035696c2ca

commit 908e3e3a134cb3b9a741ea31aedb2f035696c2ca
Author: Liquan (Max) Gu <maxlg@chromium.org>
Date: Fri May 28 13:31:10 2021

Reland: PaymentInstrumentIconFetcher avoids using released WebContents

* Original CL: crrev.com/c/2917455
* Reverting CL: crrev.com/c/2920970
* Reverting reason: The unique pointer frame_routing_ids was used after
  std::move.
* Relanding change: Change frame_routing_ids to be a reference instead.

Bug: 1212612
Change-Id: Ic96718d25f70948bbf4bd7650649172395868fbb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2920672
Reviewed-by: Rouslan Solomakhin <rouslan@chromium.org>
Commit-Queue: Liquan (Max) Gu <maxlg@chromium.org>
Cr-Commit-Position: refs/heads/master@{#887497}

[modify] https://crrev.com/908e3e3a134cb3b9a741ea31aedb2f035696c2ca/content/browser/payments/payment_instrument_icon_fetcher.cc


### ma...@chromium.org (2021-05-31)

[Empty comment from Monorail migration]

### ma...@chromium.org (2021-05-31)

Tested on the tip of trunk with the diff patch. Not being able to reproduce.

### [Deleted User] (2021-06-01)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-01)

This release blocking issue appears to be targeted for M92, which has already branched. Because this issue was marked as fixed after branch point, a merge of any CLs which landed on or after May 20 may be required. Please review whether or not any CLs should be merged ASAP, and if a merge is necessary apply the label Merge-Request-92 to begin the merge review process. If no merge is required, please simply remove the Merge-TBD label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@chromium.org (2021-06-01)

No merge is required, see https://crbug.com/chromium/1212612#c29

### am...@google.com (2021-06-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-06-10)

Congratulations, the VRP Panel has decided to award you $20,000 for this report. Excellent work! 

### ma...@chromium.org (2021-06-11)

Discussed with wfh@, we conclude that it's necessary to request a merge because:

```
requiring a compromised renderer does not preclude a security bug from being valid.
in addition, a race doesn't preclude it, since the attacker might still be able to exploit a race condition.
and also, the length of time that a bug has existed normally doesn't affect mergeability either.
```

### wf...@chromium.org (2021-06-11)

Hi re: #41 and #29 I think this might still need to be merged because, even if it requires a compromised renderer, we do always assume that renderers might be fully compromised when evaluating the severity of bugs in the browser. In addition, while it might be a rare race condition, attackers can be pretty crafty in turning unreliable races into reliable exploits :) So I wonder if it's possible to re-evaluate the mergeability of this CL to M92? Thanks!

### [Deleted User] (2021-06-11)

This bug requires manual review: Reverts referenced in bugdroid comments after merge request.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: govind@(Android), benmason@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@chromium.org (2021-06-11)

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines

Yes.
2. Links to the CLs you are requesting to merge.
https://chromium-review.googlesource.com/c/chromium/src/+/2920672

3. Has the change landed and been verified on ToT?
Yes. https://crbug.com/chromium/1212612#c38

4. Does this change need to be merged into other active release branches (M-1, M+1)?
Yes. M92, M91.

5. Why are these changes required in this milestone after branch?
It's a high priority security fix https://crbug.com/chromium/1212612#c45.

6. Is this a new feature?
No

7. If it is a new feature, is it behind a flag using finch?
N/A

### am...@google.com (2021-06-14)

[Empty comment from Monorail migration]

### sr...@google.com (2021-06-14)

Merge approved for M92 branch:4515 please merge asap

### sr...@google.com (2021-06-14)

Please merge your changes to branch:4515 before tuesday ( June 15, 2021) 3pm PST, I will be cutting Beta RC build at that time so would like to get all approved changes into this weeks beta release so we get more beta coverage. 

### ma...@chromium.org (2021-06-14)

Merge CL WIP: https://chromium-review.googlesource.com/c/chromium/src/+/2958670

### gi...@appspot.gserviceaccount.com (2021-06-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/dcb0b589a9150fc4dc05c19ff8d0dd1a423c2f92

commit dcb0b589a9150fc4dc05c19ff8d0dd1a423c2f92
Author: Liquan (Max) Gu <maxlg@chromium.org>
Date: Tue Jun 15 13:38:06 2021

[M92] Reland: PaymentInstrumentIconFetcher avoids using released WebContents

* Original CL: crrev.com/c/2917455
* Reverting CL: crrev.com/c/2920970
* Reverting reason: The unique pointer frame_routing_ids was used after
  std::move.
* Relanding change: Change frame_routing_ids to be a reference instead.

(cherry picked from commit 908e3e3a134cb3b9a741ea31aedb2f035696c2ca)

Bug: 1212612
Change-Id: Ic96718d25f70948bbf4bd7650649172395868fbb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2920672
Reviewed-by: Rouslan Solomakhin <rouslan@chromium.org>
Commit-Queue: Liquan (Max) Gu <maxlg@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#887497}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2958670
Cr-Commit-Position: refs/branch-heads/4515@{#618}
Cr-Branched-From: 488fc70865ddaa05324ac00a54a6eb783b4bc41c-refs/heads/master@{#885287}

[modify] https://crrev.com/dcb0b589a9150fc4dc05c19ff8d0dd1a423c2f92/content/browser/payments/payment_instrument_icon_fetcher.cc


### am...@chromium.org (2021-06-15)

approved for merge to M91; please merge to branch 4472 asap/before EOD tomorrow for the next M91 security respin. Thank you! 

### ma...@chromium.org (2021-06-15)

WIP CL: https://chromium-review.googlesource.com/c/chromium/src/+/2965503

### gi...@appspot.gserviceaccount.com (2021-06-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/06bd377774567ca95508bf8424cff3ad7883e645

commit 06bd377774567ca95508bf8424cff3ad7883e645
Author: Liquan (Max) Gu <maxlg@chromium.org>
Date: Wed Jun 16 01:56:58 2021

[M91] Reland: PaymentInstrumentIconFetcher avoids using released WebContents

* Original CL: crrev.com/c/2917455
* Reverting CL: crrev.com/c/2920970
* Reverting reason: The unique pointer frame_routing_ids was used after
  std::move.
* Relanding change: Change frame_routing_ids to be a reference instead.

(cherry picked from commit 908e3e3a134cb3b9a741ea31aedb2f035696c2ca)

Bug: 1212612
Change-Id: Ic96718d25f70948bbf4bd7650649172395868fbb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2920672
Reviewed-by: Rouslan Solomakhin <rouslan@chromium.org>
Commit-Queue: Liquan (Max) Gu <maxlg@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#887497}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2965503
Commit-Queue: Rouslan Solomakhin <rouslan@chromium.org>
Auto-Submit: Liquan (Max) Gu <maxlg@chromium.org>
Cr-Commit-Position: refs/branch-heads/4472@{#1486}
Cr-Branched-From: 3d60439cfb36485e76a1c5bb7f513d3721b20da1-refs/heads/master@{#870763}

[modify] https://crrev.com/06bd377774567ca95508bf8424cff3ad7883e645/content/browser/payments/payment_instrument_icon_fetcher.cc


### ma...@chromium.org (2021-06-16)

https://crbug.com/chromium/1212612#c53. Done.

### ro...@google.com (2021-06-16)

Should this be marked fixed now?

### ma...@chromium.org (2021-06-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1212612?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055981)*

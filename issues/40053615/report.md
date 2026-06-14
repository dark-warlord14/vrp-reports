# Security: webrtc container-overflow in the browser process

| Field | Value |
|-------|-------|
| **Issue ID** | [40053615](https://issues.chromium.org/issues/40053615) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>WebRTC |
| **Platforms** | Windows |
| **Reporter** | 0x...@gmail.com |
| **Assignee** | jo...@chromium.org |
| **Created** | 2020-10-14 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

The navigator.mediaDevices.getDisplayMedia will cause container-overflow in the frame when open two tags.

**VERSION**  

Chrome Version: [88.0.4291.0] + [dev]  

{  

"kind": "storage#object",  

"mediaLink": "<https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/win32-release_x64%2Fasan-win32-release_x64-816154.zip?generation=1602515468887798&alt=media>",  

"name": "win32-release\_x64/asan-win32-release\_x64-816154.zip",  

"size": "1572936229",  

"updated": "2020-10-12T15:11:08.887Z",  

"metadata": {  

"cr-commit-position": "refs/heads/master@{#816154}",  

"cr-commit-position-number": "816154",  

"cr-git-commit": "3b5c790b614cddf6300be2f6f5b938f8f66abd69"  

}  

}  

Operating System: Windows 10 2004

**REPRODUCTION CASE** :  

unzip the webrtc.7z  

run the command:  

asan-win32-release\_x64-816154>chrome.exe --allow-running-insecure-content --incognito <https://test.com/webrtc/main.html> <https://test.com/webrtc/trigger.html>

The two domain names in the poc(test.com && self.com) point to the same IP.  

I create two servers listening on port 80 and 443 respectively.

In fact the argv '--allow-running-insecure-content' is not necessary

PS:  

This poc cannot be triggered 100%.  

If the poc don't crash within 1 minute, you can close the browser and run the command again.  

Try a few more times and you will succeed.

Type of crash: browser

## Attachments

- [webrtc.7z](attachments/webrtc.7z) (application/octet-stream, 669 B)
- [asan.txt](attachments/asan.txt) (text/plain, 19.7 KB)

## Timeline

### 0x...@gmail.com (2020-10-14)

[Comment Deleted]

### pa...@chromium.org (2020-10-14)

zijiehe, it looks like you own the code near the top of the stack. Could you please take a look? Thank you!

main.html:

```
Hi
<iframe  src='https://asnine.com/webrtc/webrtc.html'></iframe>
```

webrtc.html:

```
<!DOCTYPE html>
<html>

<head>
    <title>WebRTC Screen container-overflow</title>
</head>

<body>
    <video id=videoElement>

    </video>
    <script>
        navigator.mediaDevices.getDisplayMedia({
            video: true
        }).then(screenStream => {
            videoElement.srcObject = screenStream
        }).catch(function (error) {
            console.log('error!!!')
        });

    </script>
</body>

</html>
```

[Monorail components: Blink>WebRTC]

### [Deleted User] (2020-10-15)

Setting milestone and target because of Security_Impact=Head and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jo...@chromium.org (2020-10-15)

Zijie no longer works on this component so I will take a look.

### [Deleted User] (2020-10-15)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jo...@chromium.org (2020-10-15)

I'm still building ASAN on my local machine so I can get a local repro but based on the data provided, I suspect this was introduced in this CL:
https://webrtc-review.googlesource.com/c/src/+/170470

In that CL, the way that the size of the vector of move_rects was increased changed from reserve to resize (which affects the size reported by the vector).  Since the ASAN error is 'container-overflow' and the count of move rects is determined by a calculation based on the vector's capacity, I suspect the code is accessing 'valid' memory owned by the vector but which didn't contain a valid object.

That's my hunch for now, once I have a local repro I will get a better look and can work on a fix.

### jo...@chromium.org (2020-10-15)

I've confirmed that the referenced CL is the cause of the ASAN crash but AFAICT it isn't a problem that would affect production (i.e. end users).  The DxgiOutputDuplicator uses a vector of bytes to store the dirty rects.  The code checks the vector's capacity() to determine if it needs to be resized and it uses the capacity() value in all of its calculations.  In the CL above, the change from reserve to resize meant that size() and capacity() could now return different values (capacity() might be larger than size()).

When running in the field, there won't be a crash as the vector does have enough space for the frame data however when running under ASAN, if the space needed is > size() then ASAN reports the 'crash' as container-overflow.

I can make a fix (call shrink_to_fit() after resize() or just use size() instead of capacity()) which will satisfy ASAN but I don't think the change will require merging since there isn't any end-user impact.  Someone please correct me if that is an incorrect assumption : )

### jo...@chromium.org (2020-10-16)

I have a CL out for review and I'm removing the merge tags given that there isn't end-user impact.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-10-16)

The following revision refers to this bug:
  https://webrtc.googlesource.com/src.git/+/ea3e3215e0d0e6c986788ec931a0499ed05930b8

commit ea3e3215e0d0e6c986788ec931a0499ed05930b8
Author: Joe Downing <joedow@google.com>
Date: Fri Oct 16 18:31:44 2020

Fixing ASAN container-overflow error in DxgiOutputDuplicator

The DxgiOutputDuplicator uses a vector<byte> to hold the rects
that have changed on the screen.  It then iterates over the
vector to grab each rect and apply it to the updated_region.

There is vector resizing logic which checks the 'capacity' of
the vector and determines whether there is enough space for the
changed rect data.  Often the 'capacity' and 'size' of the
vector are equal but that isn't always true.  When the capacity
is greater than size, and the number of changed rects is high
enough, rect data will be written past the element pointed to
by (data() + size()) and this is the error that ASAN is warning
of.

The fix is to use size() instead of capacity() when determining
whether to resize the vector and as the buffer size we provide
to the Windows API.  There are no other usages of this vector so
there aren't any problems caused by the size/capacity discrepancy
in the existing builds.  The ASAN issue is worth fixing in case
someone comes along and decides to use the vector differently (e.g
rely on the size instead of capacity so some of the rects are
not counted).

Bug: chromium:1138446
Change-Id: I3041091423de889e0f8aabc56ece9466a3000b4f
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/188900
Reviewed-by: Jamie Walch <jamiewalch@chromium.org>
Commit-Queue: Joe Downing <joedow@google.com>
Cr-Commit-Position: refs/heads/master@{#32425}

[modify] https://crrev.com/ea3e3215e0d0e6c986788ec931a0499ed05930b8/modules/desktop_capture/win/dxgi_output_duplicator.cc


### [Deleted User] (2020-10-16)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jo...@chromium.org (2020-10-16)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-10-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/28125109b0a7f2ab232a350fe6b5276259e01c7c

commit 28125109b0a7f2ab232a350fe6b5276259e01c7c
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Sat Oct 17 01:21:14 2020

Roll WebRTC from 9cee07983fc9 to fba124a48346 (3 revisions)

https://webrtc.googlesource.com/src.git/+log/9cee07983fc9..fba124a48346

2020-10-16 chromium-webrtc-autoroll@webrtc-ci.iam.gserviceaccount.com Roll chromium_revision e7588486bf..2aa0b3d2fd (817908:818053)
2020-10-16 joedow@google.com Fixing ASAN container-overflow error in DxgiOutputDuplicator
2020-10-16 hta@webrtc.org Deprecate GetRemoteAudioSSLCertificate

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/webrtc-chromium-autoroll
Please CC webrtc-chromium-sheriffs-robots@google.com on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/master/autoroll/README.md

Bug: chromium:1138446
Tbr: webrtc-chromium-sheriffs-robots@google.com
Change-Id: If173831dc9addf52127f4f37482cbc5154db4486
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2481936
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#818189}

[modify] https://crrev.com/28125109b0a7f2ab232a350fe6b5276259e01c7c/DEPS


### [Deleted User] (2020-10-17)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-18)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-21)

We discussed this at the VRP panel. The explanation in https://crbug.com/chromium/1138446#c7 makes sense if it's _writing_ beyond the size() bounds but within the capacity() bounds.

But based on https://crbug.com/chromium/1138446#c0 and https://crbug.com/chromium/1138446#c1 this is an OOB _read_, which means that a cunning attacker could potentially use this to leak sensitive data from process memory (e.g. for ASLR bypasses or similar). That would make this medium severity. The only reason this wouldn't be a problem is if the code knows it's previously written to that area of the vector and there's no possibility it could have been reallocated between the write and the read.

In general please don't reset severity without discussing with security sheriffs joedow@!

Also, the offending CL was commit b52f7fb5933a098c48f907bb488ef3097c1c4bd9 (according to https://crbug.com/chromium/1138446#c6) so the security impact was wrong in https://crbug.com/chromium/1138446#c2. Fixing that as well :)

I anticipate Sheriffbot will add a merge request to M87 tomorrow.

### ad...@google.com (2020-10-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-10-21)

Congratulations, the VRP panel has awarded $5000 for this bug.

### ad...@google.com (2020-10-22)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-22)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jo...@chromium.org (2020-10-22)

I had thought the bug was being monitored which is why I asked about downgrading it and then did so a day later.  I'll add the proper folks next time as I didn't realize that no one was watching it.

For https://crbug.com/chromium/1138446#c15, the reason why I didn't think it was severe is that the read comes *right* after the write.  It isn't done in different contexts.  The pseudo code for the only function which uses this member is:
- Resize vector if capacity < required_size
- Write to vector up to capacity
- Read from vector up to capacity

The vector isn't written to and then read from somewhere else.  The logic which resizes, writes, and reads to it is all in the same function.

I'm happy to merge if you still think this is a critical issue, but it still seems benign based on the code.  Maybe I'm missing some subtlety.


### [Deleted User] (2020-10-22)

Requesting merge to beta M87 because latest trunk commit (818189) appears to be after beta branch point (812852).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-10-22)

This bug requires manual review: DEPS changes referenced in bugdroid comments.
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
Owners: benmason@(Android), bindusuvarna @(iOS), cindyb@(ChromeOS), lakpamarthy@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2020-10-22)

No problem about the downgrading. You're right that in an ideal world we in security would be looking out for all comments and severity changes on all security bugs; we're just not that good :)

On the bug itself.

> - Resize vector if capacity < required_size
> - Write to vector up to capacity
> - Read from vector up to capacity

Comments 0 and 15 are reporting this third step, not the second step.

So either:
a) You're wrong
b) ASAN is wrong (for some reason it didn't spot the write but did spot the read)

I'm certainly willing to believe ASAN is wrong. It is, after all, deep voodoo magic. Quite possibly, the container-overflow checks in ASAN are only detecting reads not writes.

But meanwhile, if there's even a whiff of uncertainty, we should err on the side of caution.

> I'm happy to merge if you still think this is a critical issue, but it still seems benign based on the code. 

I know you don't mean "critical" in the formal sense of our security severities (https://chromium.googlesource.com/chromium/src/+/master/docs/security/severity-guidelines.md), but I want to emphasize that this is quite far from being Critical. Nobody even considers it High. As an OOB read, it's only medium severity. For that reason we won't be merging this back to M86, but Sheriffbot probably will ask us to merge it back to M87. Last year we had 1200+ security bugs which were ≥medium severity, so please don't feel like this is an unusual situation. It's just an abundance of caution for us to merge it to M87 just in case.

Having said all that: if you can prove that ASAN is detecting the container-overflow-read but not the container-overflow-write, we should report a bug against ASAN.

### jo...@chromium.org (2020-10-22)

Thanks!  I do think it is related to the ASAN logic but I also think the code it identified is error-prone and worth fixing (I was mostly interested in making sure I hadn't missed an obvious bug in the code).

Merge template:
1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
Yes

2. Links to the CLs you are requesting to merge.
https://webrtc-review.googlesource.com/c/src/+/188900

3. Has the change landed and been verified on ToT?
Yes

4. Does this change need to be merged into other active release branches (M-1, M+1)?
No (per security team, M87 only)

5. Why are these changes required in this milestone after branch?
Issue found and fixed after branchpoint, issue is a ~medium security risk and very low regression potential

6. Is this a new feature?
No

7. If it is a new feature, is it behind a flag using finch?
N/A

### la...@google.com (2020-10-23)

merge approved for M87 branch 4280

### jo...@chromium.org (2020-10-23)

I've create the merge request (https://webrtc-review.googlesource.com/c/src/+/190165) but I can't CQ+2 myself (I'm assuming it is because I used my Google account for the original patch).  Jamie is back on Monday so I'll see if he can lgtm + CQ it for me.

### jo...@chromium.org (2020-10-26)

FYI this was merged to M87 on Friday (https://webrtc-review.googlesource.com/c/src/+/190165)

### [Deleted User] (2020-10-27)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jo...@chromium.org (2020-10-27)

AFAICT this is in the release branch though it is in WebRTC (https://webrtc.googlesource.com/src.git/+log/refs/branch-heads/4280) and not Chromium so perhaps the commit bot didn't update this bug.

### ad...@google.com (2020-11-16)

[Empty comment from Monorail migration]

### ad...@google.com (2020-11-16)

[Empty comment from Monorail migration]

### to...@chromium.org (2020-11-27)

[Empty comment from Monorail migration]

### hu...@chromium.org (2020-12-01)

[Empty comment from Monorail migration]

### vs...@google.com (2020-12-10)

[Empty comment from Monorail migration]

### vs...@google.com (2020-12-10)

[Empty comment from Monorail migration]

### ke...@google.com (2020-12-11)

[Empty comment from Monorail migration]

### jo...@chromium.org (2020-12-12)

I've created a cherry-pick for this change for the M86 release branch:
https://webrtc-review.googlesource.com/c/src/+/197143

I can't +2 it though as I'm not a webrtc committer.  Assuming this is the right branch for 86-LTS, can someone with commit power lgtm and +2 it?

### [Deleted User] (2020-12-14)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jo...@chromium.org (2020-12-16)

Quick update, I've been trying to get the M86 merge submitted for a few days (thanks to terelius@ and jamiewalch@ for helping to +2).

Jamie was able to get my account added to the committers list for WebRTC so I am trying to +2 it again now.

### jo...@chromium.org (2020-12-16)

Hmm, the error I see now is:
CQ couldn't submit your CL because CQ is not allowed to do so in your Gerrit project config. Contact your project admin or Chrome Operations team https://goo.gl/f3mzjN

Is M86 still open for merges?

### jo...@chromium.org (2021-01-05)

I gave this another try today and I'm seeing the same error as I did back in December.  If there is interest in getting this merged back to M86, I'll need some help from someone more familiar with merging into old release branches.

### ad...@google.com (2021-01-07)

[Empty comment from Monorail migration]

### vs...@google.com (2021-01-08)

M86 is still open for merges as the LTS branch. We do want this to land for the next ChromeOS release.

### jo...@chromium.org (2021-01-08)

Any idea what the CQ error is then?  I'm happy to finish the merge but I had no idea how to address that error.  Is it possible that the Chromium release branch is still open for M86 merges but the WebRTC release branch is not?

### vs...@google.com (2021-01-08)

Unfortunately I'm not sure what is missing. I don't have permissions to click the submit button at all. This is the first CL that is being backported to the M86 branch during the LTS. Chrome and ChromeOS are working as expected, but I'm not familiar with how the subprojects work.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-08)

The following revision refers to this bug:
  https://webrtc.googlesource.com/src/+/a21f08afa80ba16fee1f2d51e36a1ac6c824f112

commit a21f08afa80ba16fee1f2d51e36a1ac6c824f112
Author: Joe Downing <joedow@google.com>
Date: Fri Jan 08 18:21:33 2021

Fixing ASAN container-overflow error in DxgiOutputDuplicator

The DxgiOutputDuplicator uses a vector<byte> to hold the rects
that have changed on the screen.  It then iterates over the
vector to grab each rect and apply it to the updated_region.

There is vector resizing logic which checks the 'capacity' of
the vector and determines whether there is enough space for the
changed rect data.  Often the 'capacity' and 'size' of the
vector are equal but that isn't always true.  When the capacity
is greater than size, and the number of changed rects is high
enough, rect data will be written past the element pointed to
by (data() + size()) and this is the error that ASAN is warning
of.

The fix is to use size() instead of capacity() when determining
whether to resize the vector and as the buffer size we provide
to the Windows API.  There are no other usages of this vector so
there aren't any problems caused by the size/capacity discrepancy
in the existing builds.  The ASAN issue is worth fixing in case
someone comes along and decides to use the vector differently (e.g
rely on the size instead of capacity so some of the rects are
not counted).

NOTRY=true
(cherry picked from commit ea3e3215e0d0e6c986788ec931a0499ed05930b8)

Bug: chromium:1138446
Change-Id: I3041091423de889e0f8aabc56ece9466a3000b4f
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/188900
Reviewed-by: Jamie Walch <jamiewalch@chromium.org>
Commit-Queue: Joe Downing <joedow@google.com>
Cr-Original-Commit-Position: refs/heads/master@{#32425}
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/197143
Commit-Queue: Mirko Bonadei <mbonadei@webrtc.org>
Reviewed-by: Joe Downing <joedow@chromium.org>
Reviewed-by: Björn Terelius <terelius@webrtc.org>
Cr-Commit-Position: refs/branch-heads/4240@{#16}
Cr-Branched-From: 93a9d19d4eb53b3f4fb4d22e6c54f2e2824437eb-refs/heads/master@{#31969}

[modify] https://crrev.com/a21f08afa80ba16fee1f2d51e36a1ac6c824f112/modules/desktop_capture/win/dxgi_output_duplicator.cc


### jo...@chromium.org (2021-01-08)

Thanks for your help getting this merged Mirko!

### ja...@google.com (2021-01-19)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1138446?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053615)*

# Security:  Memory-safety bug in Image11::map

| Field | Value |
|-------|-------|
| **Issue ID** | [40082666](https://issues.chromium.org/issues/40082666) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>GPU>ANGLE |
| **Reporter** | [Deleted User] |
| **Assignee** | jm...@chromium.org |
| **Created** | 2015-08-11 |
| **Bounty** | $1,000.00 |

## Description

[I reported the following bug to Mozilla (for its manifestations in Firefox, Thunderbird, etc.) at https://bugzilla.mozilla.org/show_bug.cgi?id=1187459 . Since the bug is in Angle, a Google library, I am also reporting it here. I found the bug via code inspection in Angle v.2422 (from the readme.chromium file in the Angle root folder), which appears in Mozilla codebase 39.0. The discussion below pertains to that version of the Mozilla codebase, except that I have updated the line numbers to correspond to the latest available Angle, in which the bug appears still to be present: github.com/google/angle/blob/master/src/libANGLE/renderer/d3d/d3d11/Image11.cpp]

------

Image11::map (gfx\angle\src\libGLESv2\renderer\d3d\d3d11\image11.cpp) does not properly report error status if its call to deviceContext -> Map fails due to a "device lost" error. Instead, it returns GL_NO_ERROR. This can cause a caller to use an uninitialized D3D11_MAPPED_SUBRESOURCE object. One such caller is Image11::loadData, which uses an uninitialized D3D11_MAPPED_SUBRESOURCE to determine where to copy the data specified by its |input| argument. This can cause loadData to overwrite an arbitrary (and possibly quite large) block of memory with data from |input|.

The bug is at line [639], which should be followed by something like |return result;|

614:gl::Error Image11::map(D3D11_MAP mapType, D3D11_MAPPED_SUBRESOURCE *map)
... [*map is not initialized]
634:    HRESULT result = deviceContext->Map(stagingTexture, subresourceIndex, mapType, 0, map);
635:
636:    // this can fail if the device is removed (from TDR)
637:    if (d3d11::isDeviceLostError(result))
638:    {
639:        mRenderer->notifyDeviceLost();
640:    }
641:    else if (FAILED(result))
642:    {
643:        return gl::Error(GL_OUT_OF_MEMORY, "Failed to map staging texture, result: 0x%X.", result);
644:    }
645:
646:    mDirty = true;
647:
648:    return gl::Error(GL_NO_ERROR);
649:}

The bug is activated by, e.g., loadData:

...
257:    D3D11_MAPPED_SUBRESOURCE mappedImage;
258:    gl::Error error = map(D3D11_MAP_WRITE, &mappedImage);
259:    if (error.isError())
260:    {
261:        return error;
262:    }
263:
264:    uint8_t* offsetMappedData = (reinterpret_cast<uint8_t*>(mappedImage.pData) + (yoffset * mappedImage.RowPitch + xoffset * outputPixelSize + zoffset * mappedImage.DepthPitch));
265:    loadFunction(area.width, area.height, area.depth,
266:                 reinterpret_cast<const uint8_t*>(input), inputRowPitch, inputDepthPitch,
267:                 offsetMappedData, mappedImage.RowPitch, mappedImage.DepthPitch);
268:
269:    unmap();
270:
271:    return gl::Error(GL_NO_ERROR);
272:}

mappedImage is neither explicitly nor implicitly initialized before line 258 passes it to map. Line 264 then uses it to compute the destination address for a copy operation, and line 265 calls loadFunction to do the copy (which it does without testing for the error status set by map at line 639).

I have verified the above [for the version of Angle included in Mozilla's 39.0 codebase] by using the debugger to to skip line 634 and force isDeviceLostError on line 637 to return |true|.

Additionally, unmap() on line 269 probably does something bad if line 608 fails.

****
It also appears that the following other callers in Image11.cpp are affected by the same bug:

Image11::loadCompressedData
Image11::copy
Image11::generateMipmap



## Timeline

### [Deleted User] (2015-08-11)

jschuh@, can you help triage?

### [Deleted User] (2015-08-11)

[Empty comment from Monorail migration]

### [Deleted User] (2015-08-11)

Oops:

"Additionally, unmap() on line 269 probably does something bad if line 608 fails" should refer to the new line 608, which is line 634.


### rs...@chromium.org (2015-08-13)

kbr: Can you help triage?

### cl...@chromium.org (2015-08-13)

[Empty comment from Monorail migration]

### kb...@chromium.org (2015-08-17)

Could you please add kbrussel [at] alum.mit.edu to the CC: list of https://bugzilla.mozilla.org/show_bug.cgi?id=1187459 ?

Do you have a reproduction?

Jamie, could you help investigate this? CC'ing Geoff as well.



### [Deleted User] (2015-08-17)

I don't have a packaged POC for this bug, but it's easy to emulate the problem by using the debugger to skip line 634 and cause |isDeviceLostError| to return |true|. I suppose an attacker might trigger it with content that causes the GPU driver temporarily to lose its mind and reset the device, as by causing it to run out of texture memory, compute something lengthy enough to cause a timeout, etc.

### [Deleted User] (2015-08-17)

[Comment Deleted]

### [Deleted User] (2015-08-17)

Added kbrussel@alum.mit.edu to CC list.



### kb...@chromium.org (2015-08-17)

Thanks for the CC: on the Mozilla bug. Anyone wanting to see it, please email me your Mozilla Bugzilla email address. The report's the same as this one. Clearly it should be fixed, but it's difficult to see how it could be reliably provoked from user code, since provoking a TDR in Chromium usually invalidates the context promptly.


### jm...@chromium.org (2015-08-17)

Can confirm this is still present in ToT ANGLE. The fix is likely to just remove the 'else' close before the unconditional error check.

I agree with Ken that it's quite clearly a security hole, but seems hard to lead to a reproducible exploit. Will take a look at fixing tomorrow morning.

### bu...@chromium.org (2015-08-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/39939686b3731eaaf6c0b639ab64db0277c72475

commit 39939686b3731eaaf6c0b639ab64db0277c72475
Author: Jamie Madill <jmadill@chromium.org>
Date: Tue Aug 18 14:37:22 2015

Fix improper error handling in Image11.

A device lost event would improperly skip returning an error, which
could lead us down a code path that would read/write to invalid
locations.

BUG=519642

Change-Id: Iba437b9b24cdf44320a944a85146f5f73be9f7a6
Reviewed-on: https://chromium-review.googlesource.com/293903
Tested-by: Jamie Madill <jmadill@chromium.org>
Reviewed-by: Geoff Lang <geofflang@chromium.org>
Reviewed-by: Kenneth Russell <kbr@chromium.org>

[modify] http://crrev.com/39939686b3731eaaf6c0b639ab64db0277c72475/src/libANGLE/renderer/d3d/d3d11/Image11.cpp


### bu...@chromium.org (2015-08-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d8cd310f60278b06beee8be328a1d402be06d1dc

commit d8cd310f60278b06beee8be328a1d402be06d1dc
Author: cwallez <cwallez@google.com>
Date: Mon Aug 24 21:08:28 2015

Roll ANGLE 1e94979..4001e1d

https://chromium.googlesource.com/angle/angle.git/+log/1e94979..4001e1d

BUG=519642,522557

TEST=bots

Review URL: https://codereview.chromium.org/1313433004

Cr-Commit-Position: refs/heads/master@{#345179}

[modify] http://crrev.com/d8cd310f60278b06beee8be328a1d402be06d1dc/DEPS


### jm...@chromium.org (2015-08-26)

Ken, should this warrant a merge?

### cl...@chromium.org (2015-08-26)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### kb...@chromium.org (2015-08-27)

Jamie (re #14): I don't think it's worth the trouble -- no proof of concept was produced -- but I leave it to you. The fix was small enough that it's a low-risk merge.


### ti...@google.com (2015-08-30)

If the severity is high for this bug (as marked), we should consider merging it all the way down to stable. Based on comments around the exploitability of this issue, bumping it down to Medium.

Either way, let's at least merge this into M46 before it hits beta and get the fix out to more users.

Merge-Requested for M46 (branch 2490).

Adding reward-topanel for consideration under the Google Reward program: https://www.google.com/about/appsecurity/chrome-rewards/

### pe...@google.com (2015-08-30)

Approved for M46 (branch: 2490)

### bu...@chromium.org (2015-08-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/a7b483f2940c8267c4115b4b47ffbc1d6a9913f3

commit a7b483f2940c8267c4115b4b47ffbc1d6a9913f3
Author: Jamie Madill <jmadill@chromium.org>
Date: Tue Aug 18 14:37:22 2015

Merge "Fix improper error handling in Image11."

A device lost event would improperly skip returning an error, which
could lead us down a code path that would read/write to invalid
locations.

BUG=519642

Change-Id: Iba437b9b24cdf44320a944a85146f5f73be9f7a6
Reviewed-on: https://chromium-review.googlesource.com/293903
Tested-by: Jamie Madill <jmadill@chromium.org>
Reviewed-by: Geoff Lang <geofflang@chromium.org>
Reviewed-by: Kenneth Russell <kbr@chromium.org>
(cherry picked from commit 39939686b3731eaaf6c0b639ab64db0277c72475)
Reviewed-on: https://chromium-review.googlesource.com/295249
Reviewed-by: Jamie Madill <jmadill@chromium.org>

[modify] http://crrev.com/a7b483f2940c8267c4115b4b47ffbc1d6a9913f3/src/libANGLE/renderer/d3d/d3d11/Image11.cpp


### bu...@chromium.org (2015-08-31)

The following revision refers to this bug:
  http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=77984

------------------------------------------------------------------
r77984 | jmadill@google.com | 2015-08-31T17:54:18.660045Z

-----------------------------------------------------------------

### ti...@google.com (2015-10-12)

[Empty comment from Monorail migration]

### ti...@google.com (2015-10-13)

Congrats - $1,000 for this report.

Panel notes: Interesting out-of-bounds write. For your info, the reward would have been higher if a PoC was provided - more details here: https://www.google.com/about/appsecurity/chrome-rewards/

We'll credit you in our release notes tomorrow as "lastland.net". If you would like to use another name, please update this bug with your preferred credit name.

I'll update this issue with a CVE shortly and we'll start the payment process this week. Thanks again for helping to secure Chrome!

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### ti...@google.com (2015-10-13)

[Empty comment from Monorail migration]

### [Deleted User] (2015-10-13)

Thank you for working through the bounty process. You can credit me as "Ronald Crane, an independent security researcher". BTW, do you know where https://code.google.com/p/chromium/issues/detail?id=518206 is in the bounty process?

### ti...@google.com (2015-10-14)

Updated the release notes as well as https://crbug.com/chromium/518206. Thanks!

### ti...@google.com (2015-10-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-12-03)

Bulk update: removing view restriction from closed bugs.

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/519642?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-12)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082666)*

# Use after free in gl::VertexArray::setDependentDirtyBit

| Field | Value |
|-------|-------|
| **Issue ID** | [40057631](https://issues.chromium.org/issues/40057631) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Windows |
| **Reporter** | sj...@gmail.com |
| **Assignee** | jm...@chromium.org |
| **Created** | 2021-10-18 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36

Steps to reproduce the problem:
1. run chromium with --no-sandbox.
2. visit to uafpoc.html

What is the expected behavior?

What went wrong?
## Title
    Use after free in gl::VertexArray::setDependentDirtyBit

## Test environment
- Windows 10 64bit
- Chromium ASAN build 932300
- run with --no-sandbox

## Details

the vulnerability caused by commit 47619f0d30b971eda071f1f1b193dded986c41be

In my opinion, it seems to be a problem caused by not validate for the case where the `vertexArray` is deleted in the newly added `VertexArray::onBufferContentsChange`, `Buffer::onContentsChange` method.

When the `bufferData` WebGL method is called, the following c++ method is called.

- bufferData
- bufferDataImpl
- Buffer::onContentsChange *
- VertexArray::onBufferContentsChange *
- VertexArray::setDependentDirtyBit

* https://source.chromium.org/chromium/chromium/src/+/47619f0d30b971eda071f1f1b193dded986c41be:third_party/angle/src/libANGLE/Buffer.cpp;l=103
```c++
angle::Result Buffer::bufferDataImpl(Context *context,
                                     BufferBinding target,
                                     const void *data,
                                     GLsizeiptr size,
                                     BufferUsage usage,
                                     GLbitfield flags)
{
//...
//...
//...
    bool wholeBuffer = size == mState.mSize;

    mIndexRangeCache.clear();
    mState.mUsage                = usage;
    mState.mSize                 = size;
    mState.mImmutable            = (usage == BufferUsage::InvalidEnum);
    mState.mStorageExtUsageFlags = flags;

    // Notify when storage changes.
    if (wholeBuffer)
    {
        onContentsChange(); //[1]
    }
    else
    {
        onStateChange(angle::SubjectMessage::SubjectChanged);
    }

    return angle::Result::Continue;
}
```

The `Buffer::onContentsChange` method added in the comment `[1]` is called.

following is `Buffer::onContentsChange` method.

* https://source.chromium.org/chromium/chromium/src/+/47619f0d30b971eda071f1f1b193dded986c41be:third_party/angle/src/libANGLE/Buffer.cpp;l=437
```c++
void Buffer::onContentsChange()
{
    for (const ContentsObserver &observer : mContentsObservers)
    {
        observer.vertexArray->onBufferContentsChange(observer.bufferIndex); //[2]
    }
}
```

The above snippet iterates over observer and call to `observer.vertexArray->onBufferContentsChange`. However, there is no validation for vertexArray.

The following are `onBufferContentsChange` and `setDependentDirtyBit` where the UAF crash occurred.

* https://source.chromium.org/chromium/chromium/src/+/47619f0d30b971eda071f1f1b193dded986c41be:third_party/angle/src/libANGLE/VertexArray.cpp;l=767
```c++
void VertexArray::onBufferContentsChange(uint32_t bufferIndex)
{
    setDependentDirtyBit(true, bufferIndex);
}
```

https://source.chromium.org/chromium/chromium/src/+/47619f0d30b971eda071f1f1b193dded986c41be:third_party/angle/src/libANGLE/VertexArray.cpp;l=698
* 
```c++
void VertexArray::setDependentDirtyBit(bool contentsChanged, angle::SubjectIndex index)
{
    DirtyBitType dirtyBit = getDirtyBitFromIndex(contentsChanged, index);
    ASSERT(!mDirtyBitsGuard.valid() || mDirtyBitsGuard.value().test(dirtyBit));
    mDirtyBits.set(dirtyBit);
    onStateChange(angle::SubjectMessage::ContentsChanged); //here, occur heap use after free.
}
```

## PoC
- attached `uafpoc-asan.txt`

## Asan Log
- attached `uafpoc-asan.txt`

## Credits
- Jeonghoon Shin at Theori

Did this work before? N/A 

Chrome version: 94.0.4606.81  Channel: stable
OS Version: 10.0

## Attachments

- [uafpoc.html](attachments/uafpoc.html) (text/plain, 1.7 KB)
- deleted (application/octet-stream, 0 B)

## Timeline

### [Deleted User] (2021-10-18)

[Empty comment from Monorail migration]

### sj...@gmail.com (2021-10-18)

When I attach the file to the original text, an error occurs, so I leave it as a comment.

### sj...@gmail.com (2021-10-18)

In my opinion, this bug occurred in this commit. https://chromium-review.googlesource.com/c/angle/angle/+/3182706

### bd...@chromium.org (2021-10-18)

[Empty comment from Monorail migration]

[Monorail components: Internals>GPU>ANGLE]

### [Deleted User] (2021-10-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-19)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sj...@gmail.com (2021-10-30)

hi, any updates?

### jm...@chromium.org (2021-11-01)

Was fixed independently in https://chromium-review.googlesource.com/c/angle/angle/+/3236206 by an external contributor.

### sj...@gmail.com (2021-11-01)

ah,,,! thanks for the check :)

### [Deleted User] (2021-11-02)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-02)

[Empty comment from Monorail migration]

### sj...@gmail.com (2021-11-03)

I reported this issue earlier than https://chromium-review.googlesource.com/c/angle/angle/+/3236206

How is this case?

### jm...@chromium.org (2021-11-03)

The fix was authored before I had a chance to look at this bug. It was a pretty serious and obvious bug that was caught by multiple sources.

### sj...@gmail.com (2021-11-03)

thanks for the comment.

### am...@google.com (2021-11-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-11-17)

Congratulations -- the VRP Panel has decided to award you $5000 for this report as this report was filed before the external contributor report to the ANGLE project and CL with the fix was landed. Thank you for your efforts! 

### sj...@gmail.com (2021-11-18)

thank you always!

### am...@google.com (2021-11-18)

[Empty comment from Monorail migration]

### ad...@google.com (2021-11-23)

Bumping to high severity based on internal chat - this is UaF in GPU process directly reachable from web content.

### rs...@chromium.org (2021-11-23)

[Empty comment from Monorail migration]

### rs...@chromium.org (2021-11-23)

[Empty comment from Monorail migration]

### rs...@chromium.org (2021-11-23)

[Empty comment from Monorail migration]

### rs...@chromium.org (2021-11-23)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-24)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M96. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M97. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-24)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

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
Owners: benmason (Android), harrysouders (iOS), ceb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-24)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

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

### jm...@chromium.org (2021-11-24)

1. use after free
2.  https://chromium-review.googlesource.com/c/angle/angle/+/3236206
3. yes
4. no

### am...@chromium.org (2021-11-29)

merge approved for M97 - please merge to branch 4692 so this can be included in tomorrow's beta cut -- thank you! 

merge also approved for M96 -- please merge to branch 4664 at your earliest convenience 

### pb...@google.com (2021-11-29)

Your change has been approved for M97 branch,please go ahead and merge the CL's to M97 branch:4692 manually asap so that they would be part of this week's first M97 Beta release.

### jm...@chromium.org (2021-11-30)

Merged to M96 here: https://chromium.googlesource.com/angle/angle/+/3154874c603b7d472cc73990028bd0db113ba18d

was already in M97

### [Deleted User] (2022-02-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-12-13)

Hello Jeonghoon, since the fix for this issue (as noted in https://crbug.com/chromium/1260783#c30) did not link to this crbug issue, our automation was not able include this issue in acknowledgment in the appropriate release notes and CVE processing -- sincere apologies for that! This fix for this issue shipped in v96.0.4664.93, so I've updated labels accordingly so this should be updated in the coming days. 

### sj...@gmail.com (2022-12-14)

thanks for the update :)

### pg...@google.com (2023-02-12)

[Empty comment from Monorail migration]

### pg...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### pg...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1260783?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/angleproject/6599]
[Monorail mergedwith: crbug.com/chromium/1272216]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-12)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057631)*

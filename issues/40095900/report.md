# Security: Security: CSP does not propagate to blob: URIs

| Field | Value |
|-------|-------|
| **Issue ID** | [40095900](https://issues.chromium.org/issues/40095900) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature>ContentSecurityPolicy |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ti...@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2019-08-03 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

When setting a CSP that allows blob: URIs, creating a blob: of type "text/html" and then navigating to that blob removes the CSP restrictions with script-src 'unsafe-inline'. That means an eval() call can been executed.Just like <https://crbug.com/chromium/905301>.

**VERSION**  

Chrome Version: [76.0.3809.87] + [stable]  

Operating System: [Windows10 1903]

**REPRODUCTION CASE**  

When navigating to the blob, the eval() function in the blob gets executed.  

This security feature is worked in Firefox/MicrosoftEdge(Dev).  

POC:

```
<head>  
    <meta http-equiv="Content-Security-Policy" content="script-src 'unsafe-inline' ">  
</head>  
  
<body>  
    <script>  
        let blob = new Blob([`  
        <script>      
        eval('alert(location.href)');  
        <\/script>  
    `], {  
            type: "text/html"  
        });  
        let url = URL.createObjectURL(blob);  
        location.href = url  
    </script>  
</body>  

```

## Attachments

- [firefox.png](attachments/firefox.png) (image/png, 23.0 KB)
- [microsoftedge_dev.png](attachments/microsoftedge_dev.png) (image/png, 26.4 KB)

## Timeline

### do...@chromium.org (2019-08-05)

+Web Platform security folks.

[Monorail components: Blink>SecurityFeature>ContentSecurityPolicy]

### do...@chromium.org (2019-08-05)

Upping to medium to match https://crbug.com/chromium/905301

### sh...@chromium.org (2019-08-05)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-08-05)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-08-17)

andypaicu: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-09-01)

andypaicu: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### an...@chromium.org (2019-10-11)

[Empty comment from Monorail migration]

### an...@chromium.org (2019-10-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-23)

[Empty comment from Monorail migration]

### jd...@chromium.org (2019-10-25)

vogelheim@: can you TAL and/or help route this to a more appropriate person? Thanks!

### sh...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-02-05)

[Empty comment from Monorail migration]

### ar...@chromium.org (2020-03-20)

I am actually looking at how CSP are inherited in blink.
For local-scheme like blob: the CSP are inherted for the navigation initiator. This is already implemented.

I verified and the example above was working.
I will mark this as "fixed". Feel free to re-open it if needed.

### [Deleted User] (2020-03-21)

[Empty comment from Monorail migration]

### na...@google.com (2020-03-23)

[Empty comment from Monorail migration]

### [Deleted User] (2020-03-23)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M81. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-03-23)

This bug requires manual review: Request affecting a post-stable build
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna@(iOS), geohsu@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pb...@google.com (2020-03-23)

+adetaylor@(Security TPM)

### ad...@chromium.org (2020-03-23)

arthursozogni@ re https://crbug.com/chromium/990581#c14 - thanks. Can you point us to the CL where this was fixed? The VRP panel will need this to determine whether to reward the reporter, we'll need it to denote the fix in release notes appropriately, and we'll also need it in case we want to merge through to M80/M81/etc.

### ar...@chromium.org (2020-03-24)

https://crbug.com/chromium/990581#c20:
I just pointed out the current implementation is theoretically working and verified the bug was not reproducible.
I haven't verified it failed for previous versions of Chrome and I haven't bisected Chrome to find the the CL that has fixed this.

Looking at the tests, I think andypaicu@ might have fixed it one or two years ago? Or maybe mkwst@ know more about this?

### an...@chromium.org (2020-03-24)

Yes I believe this was fixed with https://chromium-review.googlesource.com/c/chromium/src/+/1314633, apologies I missed closing this bug, there were a couple of them that had the same root cause. No merge needed.

### ad...@chromium.org (2020-03-24)

Great, thank you. This looks like a direct duplicate of https://crbug.com/chromium/905301; the title is identical.

### [Deleted User] (2020-03-24)

[Empty comment from Monorail migration]

### ad...@google.com (2020-03-25)

Actually andypaicu@ maybe it's not a duplicate. The reporter filed this in Aug 2019, six months after the CL https://chromium-review.googlesource.com/c/chromium/src/+/1314633 landed. They also mentioned that CL's crbug in the original bug description.

Could you and arthursonzogni@ have another look at how this might have been fixed? Thanks!

### ti...@gmail.com (2020-03-26)

[Comment Deleted]

### ti...@gmail.com (2020-03-26)

I test it in the file:// protocal and the poc still works. 
If I test it in the http:// protocal, the poc doesn't work.

Then I download the chromium Developer build before the date I submitted. It seems that it has been fixed. 


### ti...@gmail.com (2020-03-26)

Maybe this issue still exists in the file:// protocal.
I'm not sure whether the file:// protocal applies to CSP policy.

### ad...@chromium.org (2020-03-26)

Reopening - please take another look.

### ar...@chromium.org (2020-03-26)

We define local-scheme as:
~~~
(
  url.IsEmpty() ||  
  url.ProtocolIsAbout() ||
  url.ProtocolIsData() ||
  url.ProtocolIs("blob") || 
  url.ProtocolIs("filesystem"))
);
~~~

e.g. file: is not included.
mkwst@ do we need to include it? I think we don't, because a 'file' is coming from the operating system, it is not created from the navigation initiator, so it must not inherit from it.


### ar...@chromium.org (2020-03-26)

[Comment Deleted]

### mk...@chromium.org (2020-03-26)

Yes. Two `file:` documents, like two `http:` documents, will have distinct policies. One will not inherit from the other.

### ad...@chromium.org (2020-03-26)

OK, I'm glad this is fixed, but I'm afraid we still need more information about how this was fixed so the VRP panel can work out what to do. https://crbug.com/chromium/990581#c22 says it was fixed by https://chromium-review.googlesource.com/c/chromium/src/+/1314633, but that's incorrect as that CL landed in M72 and the bug was filed against M76.

So presumably it's a duplicate of something more recent?

### na...@google.com (2020-04-01)

+andypaicu@chromium.org - The Vulnerability Rewards Panel needs some more information to assess whether this report is eligible for a reward. Can you clarify whether this is a duplicate?

### an...@chromium.org (2020-04-09)

I am not aware of any work that has been done that might fix this after M76. I had a quick look through bugs related to navigation initiator and nothing stands out. So I don't know how or why it was fixed, and how or why it was broken before (since it was actually supposed to be fixed in M73 anyway).

### ar...@chromium.org (2020-04-09)

I verified it was:
76.0.3809.0 => Reproducible.
80.0.3987.163 => Non reproducible.



### ar...@chromium.org (2020-04-09)

[Empty comment from Monorail migration]

### na...@google.com (2020-04-15)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-04-15)

Congrats! The Panel decided to award you $500 for this report! 

### na...@google.com (2020-04-15)

[Empty comment from Monorail migration]

### na...@google.com (2020-04-15)

[Empty comment from Monorail migration]

### ad...@google.com (2020-05-13)

Per https://crbug.com/chromium/990581#c36 assuming this was fixed in M80. I'll retrospectively amend the release notes to include it in due course.

### ad...@google.com (2020-06-01)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-06-03)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-06-03)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/990581?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedinto: crbug.com/chromium/905301]
[Monorail components added to Component Tags custom field.]

### dt...@google.com (2025-02-13)

Bulk update of issues accidentally marked as duplicate in issue tracker migration (b/325072672)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095900)*

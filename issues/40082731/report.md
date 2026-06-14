# Adobe Flash Player AdBreakTimelineItem class Memory Corruption Vulnerability

| Field | Value |
|-------|-------|
| **Issue ID** | [40082731](https://issues.chromium.org/issues/40082731) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>Flash |
| **Reporter** | we...@gmail.com |
| **Assignee** | na...@google.com |
| **Created** | 2015-08-26 |
| **Bounty** | $3,000.00 |

## Description

I. Summary
Adobe Flash Player is prone to a vulnerability which leads to memory corruption because of improper initialization of AdBreakTimelineItem.
------------------------------------------------------------------
II. Description
Adobe Flash is a multimedia and software platform used for authoring of vector graphics, animation, games and rich Internet applications (RIAs) that can be viewed, played and executed in Adobe Flash Player. 
Normally, AdBreakTimelineItem is not intented to be created directly.

If its construction function is invoked directly, some inner class instance will be absent. Calling its member function will cause a memory crash.

POC Source Code:

package
{
    import flash.display.Sprite;
    import com.adobe.mediacore.timeline.advertising.AdBreakTimelineItem;
    public class crash_AdBreakTimelineItem extends Sprite
    {
        public function crash_AdBreakTimelineItem()
        {
            var obj:AdBreakTimelineItem = new AdBreakTimelineItem();
            obj.adBreak;
            obj.items;
            
        }
    }
}


Lastest version of Adobe Flash Player has been tested under Windows 7 x64.
------------------------------------------------------------------
III. Impact
Memory Corruption
------------------------------------------------------------------
IV. Affected
Adobe Flash Player 19.
Other versions may also be affected.
------------------------------------------------------------------
V. Credit
Wen Guanxing from Venustech ADLAB is credited for this vulnerability.

## Attachments

- [crash_AdBreakTimelineItem.swf](attachments/crash_AdBreakTimelineItem.swf) (application/octet-stream, 697 B)

## Timeline

### lg...@chromium.org (2015-08-26)

[Empty comment from Monorail migration]

### lg...@chromium.org (2015-08-26)

[Empty comment from Monorail migration]

### lg...@chromium.org (2015-08-26)

Adding the Flash label. I can't reproduce on my computer, so I can't measure impact or severity.

### na...@google.com (2015-08-26)

Same here. Can you let us know what browser and platform (32-bit versus 64-bit) this PoC works on for you? Or are you able to provide a more reliable PoC? Thanks!

### we...@gmail.com (2015-08-26)

Any browser will do, while as the report mentioned, only Flash Player 19 is affected since AdbreakTimeLineItem is a newly added class. 
I have tested the poc under windows 7 32bit with IE 11 + Flash Player 19.
Flash Player 19 can be downloaded from labs.adobe.com.

### lg...@chromium.org (2015-08-27)

From your description, this does not appear to be a security bug in Chrome/with the version of Flash that ships with Chrome. If that's not the case, would you mind providing reproducible instructions that can crash a current version of Chrome (44 or above)?

Have you also reported this to Adobe?

[I"m keeping assigned and labeled with Restrict-View-SecurityTeam for now. natashenka@, I defer to your judgment about how we should handle with this.]

### we...@gmail.com (2015-08-27)

Currently, Chrome 44 or above is shipped with Flash Player version 18.
If testing the crash in Chrome, there is a pepper-flash version 19 that could be downloaded from labs.adobe.com.

But start from Flash Player 12, its version is updated every 3 months.
2014.1  - Flash Player 12
2014.4  - Flash Player 13
2014.6  - Flash Player 14
2014.9  - Flash Player 15
2014.12 - Flash Player 16
2015.3  - Flash Player 17
2015.6  - Flash Player 18

So, it is very likely that Flash Player 19 will be released in 2015.9
That means chrome will be officially shipped with Flash Player 19 by then.

I thought it would be better to fix the issue in advance.

This issue haven't reported to Adobe yet.

### lg...@chromium.org (2015-08-27)

Ah, thanks for the clarification. I don't work much with Flash, so I didn't realize it 19 is an upcoming version that will reach Chrome.

I'll tentatively add the labels back.

### ti...@google.com (2015-08-27)

The version of Chrome Dev (v46) that I'm running pulls in Flash Player 19, so I'm happy to argue that this falls within our VRP scope.

Wen - we'll report this to Adobe via Project Zero as usual. Let me know if you have any questions.

@natashenka - can you please create the Project Zero tracker entry and provide the link back to this issue?

### lg...@chromium.org (2015-08-27)

[Empty comment from Monorail migration]

### wf...@chromium.org (2015-08-29)

[Empty comment from Monorail migration]

### lg...@chromium.org (2015-08-29)

Because the reports are very similar (memory corruption due to bad initialization when a constructor is called directly)*, I'm going to deduplicate 19 other bugs into this.

https://crbug.com/chromium/525863: Timeline
https://crbug.com/chromium/525862: Reservation
https://crbug.com/chromium/525861: QOSProvider
https://crbug.com/chromium/525860: PSDKEventTargetInterface
https://crbug.com/chromium/525859: PSDKEventDispatcher
https://crbug.com/chromium/525858: PSDK
https://crbug.com/chromium/525856: Profile
https://crbug.com/chromium/525854: PlaybackMetrics
https://crbug.com/chromium/525853: MediaPlayerItem
https://crbug.com/chromium/525852: LoadInformation
https://crbug.com/chromium/525851: DRMPolicy
https://crbug.com/chromium/525850: DRMPlaybackTimeWindow
https://crbug.com/chromium/525848: DRMMetadataInfo
https://crbug.com/chromium/525847: DRMMetadata
https://crbug.com/chromium/525846: DRMManager
https://crbug.com/chromium/525843: DRMLicenseDomain
https://crbug.com/chromium/525842: DRMLicense
https://crbug.com/chromium/525841: DeviceInformation
https://crbug.com/chromium/525840: AdPolicyInfo
https://crbug.com/chromium/524899: AdBreakTimelineItem

* Also, because I want to clean up the sheriff queue without marking these all as high severity.

### lg...@chromium.org (2015-08-29)

[Comment Deleted]

### lg...@chromium.org (2015-08-29)

[Comment Deleted]

### lg...@chromium.org (2015-08-29)

[Comment Deleted]

### lg...@chromium.org (2015-08-29)

[Comment Deleted]

### lg...@chromium.org (2015-08-29)

[Comment Deleted]

### lg...@chromium.org (2015-08-29)

[Comment Deleted]

### lg...@chromium.org (2015-08-29)

[Comment Deleted]

### lg...@chromium.org (2015-08-29)

[Comment Deleted]

### lg...@chromium.org (2015-08-29)

[Comment Deleted]

### lg...@chromium.org (2015-08-29)

[Comment Deleted]

### lg...@chromium.org (2015-08-29)

[Comment Deleted]

### lg...@chromium.org (2015-08-29)

[Comment Deleted]

### lg...@chromium.org (2015-08-29)

[Comment Deleted]

### lg...@chromium.org (2015-08-29)

[Comment Deleted]

### lg...@chromium.org (2015-08-29)

[Comment Deleted]

### lg...@chromium.org (2015-08-29)

[Comment Deleted]

### lg...@chromium.org (2015-08-29)

[Comment Deleted]

### na...@google.com (2015-08-29)

I tested this on the released version of Flash 19, and it crashes, however it does not appear to crash in the latest google-chrome-unstable or Flash mainline (the swf throws Error: Error #2014, which is "Feature not available"), so I suspect this feature may have been pulled from Flash 19. That said, I've reported this issue to Adobe and will see what they say about it. Hopefully I will have an update for you soon. 

### lg...@chromium.org (2015-08-29)

[Comment Deleted]

### lg...@chromium.org (2015-08-29)

[Comment Deleted]

### lg...@chromium.org (2015-08-29)

natashenka@: This PoC is crashing for me on Beta, Dev, and Canary on Mac.

(I also checked the other 19 PoCs on Beta; they all crash.)

### na...@google.com (2015-08-29)

Interesting, I tried this on Windows canary and it also crashes. Maybe the feature isn't implemented on Linux. 

### we...@gmail.com (2015-09-23)

Adobe have released Flash 19.0.0.185 today and it's weird that all of these memory corruptions are fixed without any credits and demonstrations.

### na...@google.com (2015-09-23)

Sorry about this, I can confirm that the API containing these bugs was removed from the current release. I'm not sure why you weren't credited on the bulletin, I'll follow up with Adobe. 

### we...@gmail.com (2015-09-24)

Thanks for your attention.
Adobe do mention my name at https://helpx.adobe.com/security/products/flash-player/apsb15-23.html
but no CVEs on these bugs.
Is that a signal that one should report bugs after the formal edition is published, rather than help them during the beta release?

### we...@gmail.com (2015-09-24)

Actually, I'm considering about publishing a blog relating to a fuzz testing approach.
The approach would be much more persuasive if these CVEs is present there.

### na...@google.com (2015-09-24)

Reporting these bugs during the beta release is the best time to report them. By reporting them early, you prevented these issues from ever making it into a release. No CVEs were assigned for these issues, as CVEs can only be assigned to security issues that impact users of a piece of software, and fortunately in this case these bugs never made it into an official release.

### na...@google.com (2015-09-24)

I've unrestricted these bugs so you can link to them in your blog

### lg...@chromium.org (2015-09-24)

Sending to the rewards panel because this was on beta and I believe it was the first place we were made aware of this issue.

### lg...@chromium.org (2015-09-25)

(To clarify https://crbug.com/chromium/524899#c41: It was on beta the week before stable promotion.)

### rm...@gmail.com (2015-10-05)

[Comment Deleted]

### rm...@gmail.com (2015-10-05)

It's not the best place to ask for but .. @wengx...@gmail.com, did you blog post about that fuzz test approach ? 

Many Thanks.

### cl...@chromium.org (2015-10-26)

You have far exceeded the 60-day deadline for fixing this high severity security vulnerability.

We commit ourselves to this deadline and appreciate your utmost priority on this issue.

If you are unable to look into this soon, please find someone else to own this.

- Your friendly ClusterFuzz

### na...@google.com (2015-10-26)

Sorry, forgot to mark this as fixed.

### ti...@google.com (2015-11-28)

This bug is on the next reward panel - you should have an answer within a week.

### ti...@google.com (2015-12-01)

Congrats Wen - $3000 from us for this report. We'll add this in the next payment run using the details that you've already provided. 

### ti...@google.com (2015-12-14)

[Empty comment from Monorail migration]

### ti...@google.com (2016-01-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/524899?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/525840, crbug.com/chromium/525841, crbug.com/chromium/525842, crbug.com/chromium/525843, crbug.com/chromium/525846, crbug.com/chromium/525847, crbug.com/chromium/525848, crbug.com/chromium/525850, crbug.com/chromium/525851, crbug.com/chromium/525852, crbug.com/chromium/525853, crbug.com/chromium/525854, crbug.com/chromium/525856, crbug.com/chromium/525858, crbug.com/chromium/525859, crbug.com/chromium/525860, crbug.com/chromium/525861, crbug.com/chromium/525862, crbug.com/chromium/525863]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082731)*

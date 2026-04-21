# Security: ChromeOS Guest User Can Force Persistent Rollback on Stable Channel

| Field | Value |
|-------|-------|
| **Issue ID** | [40062019](https://issues.chromium.org/issues/40062019) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Enterprise |
| **Platforms** | ChromeOS |
| **Reporter** | hi...@gmail.com |
| **Assignee** | ki...@chromium.org |
| **Created** | 2022-12-02 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

There are three problems with the rollback command in crosh:

1. It states, "Only available on non-stable channels and non-enterprise enrolled devices.". But on a stable channel ChromeOS, we can use this command (see the reproduce section below).
2. A guest user can use this command to force a system-wide version rollback, thus making other users vulnerable to 1-day vulnerabilities.
3. After the guest user forces a system-wide rollback, other users can't update the system, thus making the downgrade attack persistent.

**VERSION**  

Chrome Version: Version 107.0.5304.110 (Official Build) (64-bit) stable  

Operating System: Chrome OS Flex

**REPRODUCTION CASE**  

Environment: Version 107.0.5304.110 (Official Build) (64-bit), xps13 9360.

1. Log in to the OS with a google account A, and update the OS. (in my case, I upgrade from 107.0.5304.110 to 108.0.5359.75)
2. Sign out.
3. Enter the guest mode, open crosh, execute the rollback command and click "reset to update."
4. Log in to the OS as A again. Now the OS is downgraded to 107.
5. Try to update the OS in settings. It will show "Updates are blocked by your administrator."

Fix Suggestions

1. Disable the rollback command on the stable channel.
2. Forbid rollback in the guest mode.
3. Fix the unable to update flaw after the guest user triggers rollback.

**CREDIT INFORMATION**  

Reporter credit: Qiuhao Li

## Attachments

- [Persisten_Downgrade.png](attachments/Persisten_Downgrade.png) (image/png, 40.3 KB)
- [Screenshot 2022-12-21 04.06.32.png](attachments/Screenshot 2022-12-21 04.06.32.png) (image/png, 26.3 KB)

## Timeline

### [Deleted User] (2022-12-02)

[Empty comment from Monorail migration]

### ca...@chromium.org (2022-12-02)

[Empty comment from Monorail migration]

### al...@google.com (2022-12-06)

[Empty comment from Monorail migration]

### al...@google.com (2022-12-06)

The check ought to be in update_engine rather than crosh because otherwise it would still be reachable from update_engine_client users.

### le...@google.com (2022-12-06)

This function should check whether the device is enrolled:
https://source.corp.google.com/chromeos_public/src/aosp/system/update_engine/update_manager/enterprise_rollback_policy_impl.cc
Introduced in this CL:
https://chromium.git.corp.google.com/aosp/platform/system/update_engine/+/ac83488b5d904320a4af8355fee3284ef311036c

Also whether the user can update should not depend on the currently installed version being a rolled back one.
Instead it should be checked, if the device is enrolled first. Not enrolled devices should always be able to update.

The security impact is the same as not updating the OS for a long time. Given that is also requires physical access, I set severity to Low.

[Monorail components: Enterprise]

### [Deleted User] (2022-12-06)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-06)

[Empty comment from Monorail migration]

### le...@google.com (2022-12-07)

[Empty comment from Monorail migration]

### hi...@gmail.com (2022-12-21)

Hello, any updates?

### at...@google.com (2022-12-21)

Miriam, can you follow up on https://crbug.com/chromium/1395323#c5 above?

### mp...@google.com (2022-12-21)

Thanks for the report and the code pointers!

This is not enterprise rollback but update_engine (legacy) rollback. (CCing kimjae@). Looks like we're not correctly checking whether device is enterprise enrolled or not. I can take a look as to why this may be happening. I see you're on flex, maybe it's related to that.

As to "always updating if the device is enrolled", no, we shouldn't do that. (non enterprise) rollback also takes place if the device isn't able to boot the new image, and in that case, we should not update and try again. 

The reason why you see something about enterprise rollback in the UI is this bug: b/246691369 (sorry if it's not public, in my opinion we should make more bugs public), tldr it's just a wrong error message.

### mp...@google.com (2022-12-21)

[Empty comment from Monorail migration]

### mp...@google.com (2022-12-21)

I could not reproduce this on a non-flex device @hiter727, could you, after running rollback command in guest mode in crosh, file a feedback report, put this bug's number (1395323) into the description and then answer here?

CC'ing Igor who may also be able to help after we have feedback report.

This is the rollback command in crosh: http://cs/chromeos_public/src/platform2/crosh/src/base/rollback.rs

it runs "update_engine_client --rollback"
which ends up here: http://cs/chromeos_public/src/aosp/system/update_engine/cros/update_engine_client.cc;l=571;rcl=74d8b9a897112e995ce547a736059f31e2a48c9d
and a few indirections later this if: http://cs/chromeos_public/src/aosp/system/update_engine/cros/update_attempter.cc;l=927;rcl=74d8b9a897112e995ce547a736059f31e2a48c9d
should prevent rollback.

Device policy GetOwner is implemented here: http://cs/chromeos_public/src/platform2/libbrillo/policy/device_policy_impl.cc;l=518;rcl=9f014716aba7554253f89c4c368017c0e29b76cd

So far I see no obvious bug, this should check device policy file, and that one either has request token or a management mode. It could be that case the device policy can't be loaded on your device, or some flex-specific issue, but I doubt this because flex devices have the same device policy file as normal devices (as far as I know).

### hi...@gmail.com (2022-12-21)

Hi mpolzer@, I can still reproduce this issue on 108.0.5359.111 (64-bit, Flex, xps 3960), and I sent feedbacks after the rollback command and after we reenter the normal account. Specifically, I can reproduce:

1. The guest mode can rollback the OS to 108.0.5359.75.
2. The rollback is persistent.



### mp...@google.com (2022-12-21)

Can you please file a feedback report with alt+shift+i after running rollback command in guest mode, put this bug's number (1395323) into the description and then answer here?

### hi...@gmail.com (2022-12-21)

Hi mpolzer@, yes I have filed a feedback with alt+shift+i and it contains 1395323 in the description. Please check the first feedback I filed. The second one is when I reentered in the is after the reset reboot.

### mp...@google.com (2022-12-21)

Thanks! https://listnr.corp.google.com/product/208/reports?searchText=1395323&filter=0&dateRange=30 shows that your device is not enterprise managed.
In this case, everything is working as intended from the enterprise point of view. I see now that I may have misunderstood the initial problem, you were expecting not to be able to roll back because you're on stable channel.

Passing to kimjae to clarify whether (non enterprise) rollback should be blocked on stable channel (would be new to me, so maybe documentation is just wrong).

### mp...@google.com (2022-12-21)

[Empty comment from Monorail migration]

### hi...@gmail.com (2022-12-21)

Hi mpolzer@, Thanks for the reply and information! From a Chrome OS Flex user's perspective, allowing a system-wide rollback in the guest mode may not be secure, especially if the guest can make the rollback persistent?

### ki...@google.com (2022-12-21)

Thanks Qiuhao for filing this.


> 1. It states, "Only available on non-stable channels and non-enterprise enrolled devices.". But on a stable channel ChromeOS, we can use this command (see the reproduce section below).

The crosh documentation is stale, so we will update the printout info for crosh.
I can go ahead and dig up some history, but rollbacks never treated stable channel "special".

Also, it becomes a bit confusing to have the client only allow users on non-stable to run this rollback flow.
The client doesn't "really" care about channels, as that's what the server side uses to determine CrOS builds to serve clients.

e.g. a client can be on channel dev or beta or stable, but on CrOS version 888.0.0
Should rollbacks be blocked when clients switch channels locally targeting stable? idk, that can be brought up for discussion, but it's simpler to allow rollbacks to inactive slots. [A]

The later portion of the message about ent clients, ent clients are and will always be completely blocked from running this non-ent rollback.


> 2. A guest user can use this command to force a system-wide version rollback, thus making other users vulnerable to 1-day vulnerabilities.

Guest users are still "valid" users at the end of the day and require local access to the CrOS device.

But Qiuhao point is a valid one, with on caveat, if we decide to block guest user or non-owners from having the capability to rollback explicitly it also blocks recovery cases of bad OS pushes (such as login being bricked/etc).

Maybe this can be considered a required security fix or not. [B]


> 3. After the guest user forces a system-wide rollback, other users can't update the system, thus making the downgrade attack persistent.

One can actually perform another rollback to get back to the previously active (current inactive - original version).

Also to note, if there is a new target push on the server side, it will apply that update without hesitation.

But will leave it up to [B].



Routing to security for [A] + [B] to discuss or not.

### ki...@google.com (2022-12-21)

[Empty comment from Monorail migration]

### al...@google.com (2022-12-28)

In response to [A]. From the perspective of security I think we are OK with allowing a user to switch to the inactive slot, but we might want to consider not allowing it if the inactive slot is old enough (older than the current stable milestone).

What we don't want is for a user to not be able to apply updates after a rollback. If a roll-back is performed, it should be obvious to the user how to update to the latest version.

In response to [B], I don't believe we should block guest and non-owners from performing a roll-back, but again it should be obvious to whoever the current user is how to get back to the latest version.

One possibility would be to update the language on the update screen to tell the user to perform another rollback to get to the latest version. An alternative would be for the update screen to provide a button for directly starting the rollback to the latest version.


### al...@google.com (2022-12-28)

We might need to get input from UX before doing anything though.

### hi...@gmail.com (2023-01-10)

Hi kimjae@, thanks for the explanations. I agree with Allen Webb's suggestions: 1. The rollback shouldn't make the version older than the current stable milestone. 2. It should be obvious for the user to roll back to the lasted version (instead of showing "Updates are blocked by your administrator." / waiting for a push on the server side). Do you have any plans?

### ki...@google.com (2023-02-27)

[A]

The downside about blocking rollback from not being allowed to go to versions older than current stable milestones is that it brings in a networking check component.
e.g. if a device is now offline, it can't rollback (whether or not the device is good to perform the action -- unless we let this be lenient)

On the other hand, the current flow on rollback from A to B, doesn't apply future updates if it's to A -- until the condition of server side updates.
Or users can rollback the rollback.

Does security team still think we should add this?

[B]

>One possibility would be to update the language on the update screen to tell the user to perform another rollback to get to the latest version. An alternative would be for the update screen to provide a button for directly starting the rollback to the latest version.

SGTM, is this all that's required from platform end? (e.g. we might want to expose to ash if platform is holding onto excluded OS versions -- due to rollback)

### al...@google.com (2023-04-11)

> [A]
> 
> The downside about blocking rollback from not being allowed to go to versions older than current stable milestones is that it brings in a networking check component.
e.g. if a device is now offline, it can't rollback (whether or not the device is good to perform the action -- unless we let this be lenient)
>
> On the other hand, the current flow on rollback from A to B, doesn't apply future updates if it's to A -- until the condition of server side updates.
Or users can rollback the rollback.
>
> Does security team still think we should add this?

I think we can get rid of the network requirement if we look at what we are rolling back from. For example if we are already on a stable milestone it doesn't make sense to allow a rollback (slot change) unless we are going to a future version.

If we are on a beta, dev or canary image; we can allow rollback if the network isn't available.

> [B]
>
> > One possibility would be to update the language on the update screen to tell the user to perform another rollback to get to the latest version. An alternative would be for the update screen to provide a button for directly starting the rollback to the latest version.
> 
> SGTM, is this all that's required from platform end? (e.g. we might want to expose to ash if platform is holding onto excluded OS versions -- due to rollback)

We really need to get UI/UX to help design a flow for this. Ideally from the security perspective, if updates are blocked, we should surface it prior to login and give a quick way for the user to resolve the issue. The risk is an out-of-date version has public security bugs that are potentially exploitable, and the remedy would be for the user to be able to update to the latest stable version prior to signing in.

We can schedule time to talk through this if it would help.

### ki...@google.com (2023-04-11)

>I think we can get rid of the network requirement if we look at what we are rolling back from. For example if we are already on a stable milestone it doesn't make sense to allow a rollback (slot change) unless we are going to a future version.

In the case where stable release is being fractionally rolled out AND it happens to cause issues for users (e.g. can't login/etc) it might make sense to still allow the rollback even on stable channels? (This consumer rollback is useful in cases like that)

>We really need to get UI/UX to help design a flow for this. Ideally from the security perspective, if updates are blocked, we should surface it prior to login and give a quick way for the user to resolve the issue. The risk is an out-of-date version has public security bugs that are potentially exploitable, and the remedy would be for the user to be able to update to the latest stable version prior to signing in.

Agreed, it might make sense for users to be allowed to clear out the blockers or at least be informed that users can perform another rollback (to actually rollforward - in the case that the rollback partition has a newer build than current).

>We can schedule time to talk through this if it would help.

Please do so! I think a sync would be helpful to clarify the specifics of what should be allowed for consumer rollback.

### ch...@google.com (2023-04-12)

Your report will be worked on in the Buganizer system ( link: https://issuetracker.google.com/issues/277837574 ).


[Monorail blocking: b/277837574]

### al...@google.com (2023-04-14)

[Empty comment from Monorail migration]

### ki...@google.com (2023-04-14)

[Empty comment from Monorail migration]

### xi...@chromium.org (2023-04-24)

[Empty comment from Monorail migration]

### xi...@chromium.org (2023-04-24)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### ch...@google.com (2023-07-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-17)

[Empty comment from Monorail migration]

### ch...@google.com (2023-09-18)

Exploitability - Explain why/why not the bug is reachable and/or exploitable For example, if a bug mentions a race, details are needed about how easy that race would be to achieve / can the attack retry infinite times to win the race, etc..

This bug requires direct access to the device such as through guest mode. The bug is only effective for one release before the attacker would need to use it again.

Privileges and Capabilities - Identify which process is exploited and where code execution potentially can be achieved if the attacker can break out of that process, and explain why

This isn't a traditional exploit; rather it is a feature with broken/confusing messaging that could be used to prevent updates from being applied to a device without a clearly communicated resolution.

Origin of fix - Is the issue already known upstream, fixed by work from a previously known or reported issue, provided by the reporter, or any other information that would be relevant toward reward eligibility

The fix was a change in the error message string on the settings page where updates are applied.

Mitigations - Detail any regarding mitigation considerations (we're run across a few comments, such as "we considered this issue to be highly mitigated" without explanation)

This requires physical access to the device and isn't useful to an attacker on its own---it only makes it easier to exploit other bugs by increasing the time window they can be exploited by delaying updates.

Severity assessment - why not higher, why not lower

This is clearly at most a low severity bug and some might argue it is not a security bug.

### am...@chromium.org (2023-09-26)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-11-06)

Congratulations! 
The VRP Panel has decided to award you $500 for this report. 
A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts in discovering and reporting this issue to us -- great work! 
Please be mindful that previous reward decisions made by the Chrome VRP should not be considered precedent for potential future ChromeOS VRP reward amounts or decisions.

### am...@google.com (2023-11-11)

[Empty comment from Monorail migration]

### is...@google.com (2023-11-11)

This issue was migrated from crbug.com/chromium/1395323?no_tracker_redirect=1

[Monorail blocking: b/277837574]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062019)*

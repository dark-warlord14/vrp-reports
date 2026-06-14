# sandbox escape using ppapi broker

| Field | Value |
|-------|-------|
| **Issue ID** | [40084270](https://issues.chromium.org/issues/40084270) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>Flash |
| **Platforms** | Mac |
| **Reporter** | 70...@gmail.com |
| **Assignee** | yz...@chromium.org |
| **Created** | 2016-05-10 |
| **Bounty** | $15,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36

Steps to reproduce the problem:
run attached code

What is the expected behavior?
it fails

What went wrong?
Attached is a proof of concept exploit demonstrating how a compromised renderer process can escape the sandbox, without user interaction, using the Flash PPAPI broker. I believe that this affects all operating systems, but I have only tested the exploit on OS X, on official Chrome builds 50.0.2661.94 (stable) and 52.0.2729.0 (canary).  Some modification is required to get it to work on other versions.

The broker process for a given plugin, which is unsandboxed, accepts two different types of messages:

a) BrokerProcessDispatcher handles Flash-specific messages that correspond to the PPP_Flash_BrowserOperations interface, such as 'PpapiMsg_SetSitePermission', and forwards them directly to the plugin (using function pointers obtained with the plugin's PPP_GetInterface export).
b) BrokerDispatcher, a superclass, handles a single message, PpapiMsg_ConnectToPlugin, which sends the plugin a file descriptor (using the 'connect_instance' function pointer obtained from PPP_InitializeBroker) over which it can serve a plugin-specific IPC interface.

The first type of message is normally sent by PepperFlashSettingsManager in the browser process in order to manage Flash settings from the browser settings interface: clearing Flash LSOs, updating camera/mic permissions, etc. The second is normally sent by PepperBrokerDispatcherWrapper in the renderer process on behalf of a normal (sandboxed, non-broker) instance of a plugin (via the PPB_Broker interface); Flash uses this communication channel to provide unsandboxed operations to SWFs, such as installing Adobe AIR applications.

The bug is simply that the same channel accepts both message types, with nothing to prevent the renderer from sending the BrowserOperations messages. The PepperFlashPlayer plugin appears to treat messages sent through the ConnectToPlugin channel as untrusted (sanitizing parameters, checking the signature of helper applications to be installed, etc.), but not the BrowserOperations ones: several of them take a "plugin_data_path" argument, which is treated as an absolute filesystem path and accessed without any checks.

Also, while the following is less clearly categorized as a bug:

Even without the above bypass, the Flash broker would still be providing a scary-looking interface (via ConnectToPlugin) that tries to enforce security but may have vulnerabilities. Plugins themselves cannot get access to the broker at all without user approval based on the origin. This is the "Unsandboxed plugin access" category under "Content settings", and its default value gates access behind an infobar (although the infobar has the rather vague and not especially scary message "Adobe Flash Player on http://xxx wants to access your computer.") But in order to enforce this, the browser depends on the renderer sending ViewHostMsg_RequestPpapiBrokerPermission, which from its perspective is completely independent from the message that actually opens the channel, FrameHostMsg_OpenChannelToPpapiBroker. If the renderer rather than the plugin is compromised, there is nothing stopping it from skipping the permission check, which is what my exploit does.

This generally makes sense, since site isolation for Chromium is not fully implemented and currently there is nothing preventing a renderer from pretending to be any origin it wants. (Which is a *serious* limitation, considering how much access a UXSS already gets you.) But in this case, since Flash only uses the broker for relatively uncommon operations, chances are that a significant fraction of users have no exceptions added at all, not to mention that some highly security-conscious users might have explicitly chosen to deny all access under content settings. If the broker connection IPC interface were rearchitected to verify an origin before providing a handle, both types of users would be protected from silent broker access, which in turn would limit the generality of Flash broker exploits.

Exploitation notes are included in the attachment. It's not a "real" exploit in that it doesn't have a start to the chain, i.e. any way to actually take over the renderer process. Instead, I use Frida (http://www.frida.re) to inject code into it.

Did this work before? N/A 

Chrome version: 50.0.2661.94  Channel: stable
OS Version: OS X 10.11.5
Flash Version: Shockwave Flash 21.0 r0

## Attachments

- [ppapithing.zip](attachments/ppapithing.zip) (application/octet-stream, 11.7 KB)

## Timeline

### mb...@chromium.org (2016-05-10)

Does anyone cced know if there's anyone still working this code? From what I can gather, it hasn't been touched in a while.

### mb...@chromium.org (2016-05-10)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>Flash]

### wf...@chromium.org (2016-05-10)

The description in #0 doesn't really describe fully what's going on here.

The vulnerability here seems to use PpapiMsg_SetSitePermission to call  BrokerProcessDispatcher::SetSitePermission to write a file to a specified path.

The exploit uses this to write to /net/127.0.0.1/foo

there should probably be a check somewhere that the plugin_data_path is valid before doing these operations. This is old code with no current owner.

### wf...@chromium.org (2016-05-10)

yzshen, a long time ago you touched this code, can you take a look at who might be able to look into this?

### wf...@chromium.org (2016-05-10)

[Empty comment from Monorail migration]

### js...@chromium.org (2016-05-11)

[Empty comment from Monorail migration]

### 70...@gmail.com (2016-05-11)

@wfh Checking plugin_data_path is a possible solution, but since only the browser process is supposed to send that message in the first place, it seems suboptimal.  If you do do that, make sure to check the site names too, as they are included in one of the written paths, also without validation.

### sh...@chromium.org (2016-05-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-05-11)

[Empty comment from Monorail migration]

### yz...@chromium.org (2016-05-16)

I haven't touched this code for a very long time.

Because the channel between the broker and its peer is always established by the browser, it seems possible to tell the broker process whether the channel is for the browser itself or for a renderer. That way the broker can disallow certain requests if the peer is a renderer.

WDYT?

+CC raymes who worked on flash and also deals with security stuff.
Raymes: is this something that you could help with? Thanks! 

### js...@chromium.org (2016-05-16)

Re: #10 - sounds good.

### sh...@chromium.org (2016-05-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-05-31)

yzshen: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### js...@chromium.org (2016-06-10)

Hm.. very concerning that there's been no movement on this, although raymes@ is probably a better owner.

raymes@, do you expect to have time to work on this?

### yz...@chromium.org (2016-06-10)

Sorry I haven't got a chance to work on it. Have been busy with some things that blocks quite some people.

Raymes: if you can work on it, that would be great and really appreciated! But if you don't have time and we cannot find other people, please let me know and I will find time to work on it (for real this time).

### ra...@chromium.org (2016-06-11)

Hey Yuzhu - putting time aside (I think we're both busy :) the problem is that I really don't have any background with the code in this area and don't understand the issue. That's why I came to chat a few weeks back to try to figure out what needed to be done. I think at that point you indicated it was easier for you to try to fix the bug yourself? If that's not still the case let's have a VC and figure out what needs to be done together :) 

### yz...@chromium.org (2016-06-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-06-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/92cad45212731b59e74c8f2a2913691db3e9d770

commit 92cad45212731b59e74c8f2a2913691db3e9d770
Author: yzshen <yzshen@chromium.org>
Date: Fri Jun 17 20:40:09 2016

Ignore certain messages in plugin broker process if they are not sent by the
browser.

BUG=610600
CQ_INCLUDE_TRYBOTS=tryserver.chromium.linux:linux_site_isolation

Review-Url: https://codereview.chromium.org/2069853002
Cr-Commit-Position: refs/heads/master@{#400495}

[modify] https://crrev.com/92cad45212731b59e74c8f2a2913691db3e9d770/content/browser/frame_host/render_frame_message_filter.cc
[modify] https://crrev.com/92cad45212731b59e74c8f2a2913691db3e9d770/content/browser/ppapi_plugin_process_host.cc
[modify] https://crrev.com/92cad45212731b59e74c8f2a2913691db3e9d770/content/browser/ppapi_plugin_process_host.h
[modify] https://crrev.com/92cad45212731b59e74c8f2a2913691db3e9d770/content/ppapi_plugin/OWNERS
[modify] https://crrev.com/92cad45212731b59e74c8f2a2913691db3e9d770/content/ppapi_plugin/broker_process_dispatcher.cc
[modify] https://crrev.com/92cad45212731b59e74c8f2a2913691db3e9d770/content/ppapi_plugin/broker_process_dispatcher.h
[modify] https://crrev.com/92cad45212731b59e74c8f2a2913691db3e9d770/content/ppapi_plugin/ppapi_thread.cc
[modify] https://crrev.com/92cad45212731b59e74c8f2a2913691db3e9d770/content/ppapi_plugin/ppapi_thread.h
[modify] https://crrev.com/92cad45212731b59e74c8f2a2913691db3e9d770/ppapi/proxy/ppapi_messages.h


### yz...@chromium.org (2016-06-17)

Hi, Anthony and Justin.

Please advise whether this should be merged to M51 (or any version). If yes, I will wait for a few days to make sure that the patch is safe and then request to merge.

### la...@chromium.org (2016-06-17)

Yup, we should get it on to M51, once it's baked.

### yz...@chromium.org (2016-06-22)

I searched on our crash server, didn't see crashes resulted from this CL. I think it should be safe.



### ti...@google.com (2016-06-22)

[Automated comment] Request affecting a post-stable build (M51), manual review required.

### cl...@chromium.org (2016-06-22)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges.

- Your friendly ClusterFuzz

### sh...@chromium.org (2016-06-23)

[Empty comment from Monorail migration]

### yz...@chromium.org (2016-06-27)

friendly ping, merge reviewers

### la...@chromium.org (2016-06-27)

Hey Shruthi, could you review this for inclusion in M51?

### ss...@chromium.org (2016-06-27)

Is this on beta yet, and does it need to be?

### yz...@chromium.org (2016-06-27)

It is currently on dev according to the omahaproxy page.

### go...@chromium.org (2016-06-27)

[Comment Deleted]

### go...@chromium.org (2016-06-27)

Is this require a merge to M52? If yes, please request a merge to M52 by applying "Merge-Request-52" label. Thank you.

### ss...@chromium.org (2016-06-27)

Thanks yzshen@. We are dealing with some stability issues on stable currently, and would like to be as safe as possible with merges into the post-stable branch. Since this does not look like a trivial change to me, if this is needed on M52, let's get it in there first, let bake for a couple days and then request a merge to M51, please. Let me know if there are any concerns.  

### yz...@chromium.org (2016-06-27)

Thanks for the info, Shruthi!

I don't have concerns about your suggestion. But I will defer to the security experts.



### go...@chromium.org (2016-06-27)

+ awhalley@ (Security TPM)

### aw...@chromium.org (2016-07-01)

Sorry I'm late to the party. Yep, it would be good to get this fix in. Adding Merge-Request-52 and I agree that letting it bake there for a bit is good.

### la...@chromium.org (2016-07-06)

Let's get this merged to 52 (2743).

### bu...@chromium.org (2016-07-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a803c8e2cdd77727d2e9ba2e39ad6f69fcd9de1d

commit a803c8e2cdd77727d2e9ba2e39ad6f69fcd9de1d
Author: Yuzhu Shen <yzshen@chromium.org>
Date: Wed Jul 06 20:40:10 2016

Ignore certain messages in plugin broker process if they are not sent by the browser.

BUG=610600
CQ_INCLUDE_TRYBOTS=tryserver.chromium.linux:linux_site_isolation

Review-Url: https://codereview.chromium.org/2069853002
Cr-Commit-Position: refs/heads/master@{#400495}
(cherry picked from commit 92cad45212731b59e74c8f2a2913691db3e9d770)

Review URL: https://codereview.chromium.org/2122313004 .

Cr-Commit-Position: refs/branch-heads/2743@{#588}
Cr-Branched-From: 2b3ae3b8090361f8af5a611712fc1a5ab2de53cb-refs/heads/master@{#394939}

[modify] https://crrev.com/a803c8e2cdd77727d2e9ba2e39ad6f69fcd9de1d/content/browser/frame_host/render_frame_message_filter.cc
[modify] https://crrev.com/a803c8e2cdd77727d2e9ba2e39ad6f69fcd9de1d/content/browser/ppapi_plugin_process_host.cc
[modify] https://crrev.com/a803c8e2cdd77727d2e9ba2e39ad6f69fcd9de1d/content/browser/ppapi_plugin_process_host.h
[modify] https://crrev.com/a803c8e2cdd77727d2e9ba2e39ad6f69fcd9de1d/content/ppapi_plugin/OWNERS
[modify] https://crrev.com/a803c8e2cdd77727d2e9ba2e39ad6f69fcd9de1d/content/ppapi_plugin/broker_process_dispatcher.cc
[modify] https://crrev.com/a803c8e2cdd77727d2e9ba2e39ad6f69fcd9de1d/content/ppapi_plugin/broker_process_dispatcher.h
[modify] https://crrev.com/a803c8e2cdd77727d2e9ba2e39ad6f69fcd9de1d/content/ppapi_plugin/ppapi_thread.cc
[modify] https://crrev.com/a803c8e2cdd77727d2e9ba2e39ad6f69fcd9de1d/content/ppapi_plugin/ppapi_thread.h
[modify] https://crrev.com/a803c8e2cdd77727d2e9ba2e39ad6f69fcd9de1d/ppapi/proxy/ppapi_messages.h


### ss...@chromium.org (2016-07-11)

Please verify on the next beta and then update this thread for consideration into M51. 

### yz...@chromium.org (2016-07-12)

Sure, when will be the next beta may I ask?

### ss...@chromium.org (2016-07-12)

We have one planned this week, if there are no issues qualifying the candidate. 

### aw...@chromium.org (2016-07-14)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-20)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-20)

Nice one - $15,000 for this bug.

### aw...@chromium.org (2016-07-25)

[Empty comment from Monorail migration]

### yz...@chromium.org (2016-07-27)

sshruthi: I have verified that the patch works fine on M52 beta.
Do we still need to merge it to M51? I noticed that M52 has been pushed to the stable channel.

### ss...@google.com (2016-07-27)

Nope, no need to merge into M51 at this point. 

### sh...@chromium.org (2016-09-29)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-02-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/02612b1e0615618c3350f29f7f54fc836bd25e64

commit 02612b1e0615618c3350f29f7f54fc836bd25e64
Author: scottmg <scottmg@chromium.org>
Date: Fri Feb 24 18:09:28 2017

Remove DumpWithoutCrashing() from broker_process_dispatcher

There seems to be very few instances of these dumps on the crash server,
but if no one is looking at them, I'd like to remove calls to it.
DumpWithoutCrashing() can hide legitimate crashes due to crash
throttling.

R=yzshen@chromium.org
BUG=610600,694688

Review-Url: https://codereview.chromium.org/2717473003
Cr-Commit-Position: refs/heads/master@{#452871}

[modify] https://crrev.com/02612b1e0615618c3350f29f7f54fc836bd25e64/content/ppapi_plugin/broker_process_dispatcher.cc


### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### la...@chromium.org (2021-02-25)

[Empty comment from Monorail migration]

### is...@google.com (2021-02-25)

This issue was migrated from crbug.com/chromium/610600?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084270)*

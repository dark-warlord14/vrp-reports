# Chrome_ChromeOS: Crash Report - views::Widget::CloseWithReason via TabStripPageHandler::OnTabGroupChanged

| Field | Value |
|-------|-------|
| **Issue ID** | [40057826](https://issues.chromium.org/issues/40057826) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>TopChrome>TabStrip>ThumbnailTabStrip |
| **Platforms** | Linux, Mac, ChromeOS |
| **Reporter** | le...@gmail.com |
| **Assignee** | yu...@chromium.org |
| **Created** | 2021-11-05 |
| **Bounty** | $1,000.00 |

## Description

Reported by: kaznacheev@google.com

Crash link: https://crash.corp.google.com/browse?q=product_name%3D%27Chrome_ChromeOS%27+AND+report_type.is_fatal+AND+expanded_custom_data.ChromeCrashProto.ptype%3D%27browser%27+AND+product.Version%3D%2794.0.4606.114%27+AND+expanded_custom_data.ChromeCrashProto.magic_signature_1.name%3D%27views%3A%3AWidget%3A%3ACloseWithReason%27+AND+EXISTS+%28SELECT+1+FROM+UNNEST%28CrashedStackTrace.StackFrame%29+WHERE+FunctionName%3D%27TabStripPageHandler%3A%3AOnTabGroupChanged%28TabGroupChange+const%26%29%27%29&stbtiq=&reportid=&index=0

-------------------------------------------------------------------------------
Sample Report
-------------------------------------------------------------------------------
Product name: Chrome_ChromeOS
Magic Signature : views::Widget::CloseWithReason
Product Version: 94.0.4606.114
Process type: browser
Report ID: 636c8cf75050c7f9
Report Url: https://crash.corp.google.com/636c8cf75050c7f9
Report Time: 2021-11-03T20:05:03.696-07:00
Upload Time: 2021-11-04T16:52:31.418-07:00
Uptime: 14966000 ms
OS Name: Linux
OS Version: 4.19.202-12117-ga5d7f069c423 #1 SMP PREEMPT Wed Oct 27 21:42:42 PDT 2021
CPU Architecture: arm
CPU Info: ARMv0

-------------------------------------------------------------------------------
Exception Record
-------------------------------------------------------------------------------
Exception code: 11
Flags: 1
Exception address: 0x393532f5

-------------------------------------------------------------------------------
Crashing thread: Thread index: 0. Stack Quality: 100%. Thread id: 1548.
-------------------------------------------------------------------------------
0x09572fca (chrome - widget.cc: 662)	views::Widget::CloseWithReason(views::Widget::ClosedReason)
0x0a6c9bf1 (chrome - tab_strip_page_handler.cc: 236)	TabStripPageHandler::OnTabGroupChanged(TabGroupChange const&)
0x0a2a89b5 (chrome - tab_strip_model.cc: 1252)	TabStripModel::CloseTabGroup(tab_groups::TabGroupId const&)
0x0a2a47fd (chrome - tab_strip_model.cc: 2238)	TabStripModel::UngroupTab(int)
0x0a2a3f37 (chrome - tab_strip_model.cc: 475)	TabStripModel::DetachWebContentsImpl(int, int, bool, TabStripModelChange::RemoveReason)
0x0a2a6247 (chrome - tab_strip_model.cc: 1870)	TabStripModel::CloseTabs(base::span<content::WebContents* const, 4294967295u>, unsigned int)
0x0a2a65a1 (chrome - tab_strip_model.cc: 767)	TabStripModel::CloseWebContentsAt(int, unsigned int)
0x04ae05bf (chrome - callback.h: 98)	crosapi::mojom::AccountManager_ShowReauthAccountDialog_ForwardToCallback::Accept(mojo::Message*)
0x07fc2003 (chrome - interface_endpoint_client.cc: 893)	mojo::InterfaceEndpointClient::HandleIncomingMessageThunk::Accept(mojo::Message*)
0x07f7be79 (chrome - message_dispatcher.cc: 43)	mojo::MessageDispatcher::Accept(mojo::Message*)
0x07f7bd81 (chrome - interface_endpoint_client.cc: 655)	mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*)
0x07f7bca3 (chrome - ipc_mojo_bootstrap.cc: 981)	IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message)
0x088e01bf (chrome - bind_internal.h: 509)	base::internal::Invoker<base::internal::BindState<void (mojo::(anonymous namespace)::ThreadSafeInterfaceEndpointClientProxy::*)(mojo::Message), scoped_refptr<mojo::(anonymous namespace)::ThreadSafeInterfaceEndpointClientProxy>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase*)
0x07f7cab5 (chrome - callback.h: 98)	base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()
0x0725d69f (chrome - thread_controller_with_message_pump_impl.cc)	non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()
0x088dbcf1 (chrome - message_pump_libevent.cc: 207)	base::MessagePumpLibevent::Run(base::MessagePump::Delegate*)
0x0725d7c1 (chrome - thread_controller_with_message_pump_impl.cc: 467)	base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)
0x07243f07 (chrome - run_loop.cc: 134)	base::RunLoop::Run(base::Location const&)
0x055c806d (chrome - browser_main_loop.cc: 987)	content::BrowserMainLoop::RunMainMessageLoop()
0x055c9af5 (chrome - browser_main_runner_impl.cc: 152)	content::BrowserMainRunnerImpl::Run()
0x055c584d (chrome - browser_main.cc: 49)	content::BrowserMain(content::MainFunctionParams const&)
0x06eb028f (chrome - content_main_runner_impl.cc: 608)	content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams&, bool)
0x06eafb2f (chrome - content_main_runner_impl.cc: 971)	content::ContentMainRunnerImpl::Run(bool)
0x06eae1e1 (chrome - content_main.cc: 390)	content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*)
0x06eae8e5 (chrome - content_main.cc: 418)	content::ContentMain(content::ContentMainParams const&)
0x04a48609 (chrome - chrome_main.cc: 172)	ChromeMain
0xe9da7a9b (libc.so.6 - libc-start.c: 314)	__libc_start_main
0x04a14273 (chrome + 0x0138e273)	_start
0x0bedb0a7 (chrome - elf-init.c: 90)	__libc_csu_init
0xffe1f39e 

-------------------------------------------------------------------------------
Manual regression range finder link
-------------------------------------------------------------------------------
https://crash.corp.google.com/browse?q=product_name+IN+%28%27AndroidWebView%27%2C+%27Chrome%27%2C+%27Chrome_Android%27%2C+%27Chrome_ChromeOS%27%2C+%27Chrome_Headless%27%2C+%27Chrome_Lacros%27%2C+%27Chrome_Linux%27%2C+%27Chrome_Mac%27%2C+%27Chrome_iOS%27%2C+%27FuchsiaCastRunner%27%2C+%27FuchsiaWebEngine%27%2C+%27WebLayer%27%29+AND+expanded_custom_data.ChromeCrashProto.magic_signature_1.name%3D%27views%3A%3AWidget%3A%3ACloseWithReason%27+AND+expanded_custom_data.ChromeCrashProto.ptype%3D%27browser%27#-property-selector,-samplereports,+productversion:1000,+directory,-clientid,+operatingsystem,+url,+simplifiedurl,+extensions,+day:60,-country


## Timeline

### ka...@chromium.org (2021-11-05)

[Chrome OS Stability Triage]

Note that views::Widget::CloseWithReason is a common signature. This issue is specifically for crashes where the stack trace contains TabStripPageHandler::OnTabGroupChanged (different from recently resolved https://crbug.com/chromium/1250230)

This issue is labeled with the Stability-Impact-Medium label due to its relatively low frequency: 
5 CPMH in M94 Stable, 13 CPMH in M96 Beta, 2 CPMH in M97 Beta

More data: https://data.corp.google.com/sites/cros-ui-stability-triage/graph?f=signature:in:views::Widget::CloseWithReason

There is no SLO for this label. It is up to the component owner to decide on the feasibility and the timeline on the fix.

[Monorail components: -Internals>Views UI>Browser>TopChrome>TabStrip>TabGroups]

### ka...@chromium.org (2021-11-05)

[Empty comment from Monorail migration]

### em...@google.com (2021-11-08)

From discussion, it looks like this is likely related to crbug/1235069.

Tentatively assigning to dfried@, feel free to reassign if a different owner is appropriate

### df...@chromium.org (2021-11-11)

This appears to be a WebUI tab strip issue, passing to that team.

### dl...@chromium.org (2021-11-19)

[Empty comment from Monorail migration]

[Monorail components: -UI>Browser>TopChrome>TabStrip>TabGroups UI>Browser>TopChrome>TabStrip>ThumbnailTabStrip]

### rs...@chromium.org (2021-11-29)

This is a use-after-free that has been reported externally as well. Adding security flags.

### [Deleted User] (2021-11-29)

[Empty comment from Monorail migration]

### rs...@chromium.org (2021-11-29)

[Empty comment from Monorail migration]

### rs...@chromium.org (2021-11-29)

https://crbug.com/chromium/1274518 was the external report and c#2 contains some useful information including suggested fix. CCing that reporter here and for potential VRP.

### [Deleted User] (2021-11-29)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-30)

yuhengh: Uh oh! This issue still open and hasn't been updated in the last 25 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-30)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### le...@gmail.com (2021-12-02)

It seems that this issue hasn't been updated in a long time. According to https://crbug.com/chromium/1239057 and https://crbug.com/chromium/1228557, johntlee@ or dpenning@ should be familiar with this problem. And the patch in https://crbug.com/chromium/1274518 #2 could solve it.

### rs...@chromium.org (2021-12-02)

johntlee/dpenning: Could one of you take a look at this?

### yu...@chromium.org (2021-12-02)

[Empty comment from Monorail migration]

### tl...@chromium.org (2021-12-02)

[Empty comment from Monorail migration]

### yu...@chromium.org (2021-12-02)

I'm looking into it right now. Will ping you guys if I need any help.

### gi...@appspot.gserviceaccount.com (2021-12-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/276a8bd1ca3292472b84199be83357f94e434c2a

commit 276a8bd1ca3292472b84199be83357f94e434c2a
Author: Yuheng Huang <yuhengh@chromium.org>
Date: Thu Dec 02 23:05:41 2021

WebUI tab strip: fix invalid pointer access for edit group bubble

This CL fixes a crash of closing the edit group bubble right after
creating a tab group in WebUI tab strip since editor_bubble_widget_
can be a random pointer address if it's not set.

Bug: 1271849,1267060
Change-Id: Id5b4216a5291f5837ee09e4da1cfdce53dd11cd3
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3312608
Reviewed-by: Dana Fried <dfried@chromium.org>
Commit-Queue: Yuheng Huang <yuhengh@chromium.org>
Cr-Commit-Position: refs/heads/main@{#947708}

[modify] https://crrev.com/276a8bd1ca3292472b84199be83357f94e434c2a/chrome/browser/ui/views/frame/webui_tab_strip_container_view.h


### yu...@chromium.org (2021-12-02)

[Empty comment from Monorail migration]

### yu...@chromium.org (2021-12-02)

Fixed on 98.0.4744.0

### [Deleted User] (2021-12-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-03)

Requesting merge to stable M96 because latest trunk commit (947708) appears to be after stable branch point (929512).

Requesting merge to beta M97 because latest trunk commit (947708) appears to be after beta branch point (938553).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-03)

Merge review required: M97 is already shipping to beta.

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

### [Deleted User] (2021-12-03)

Merge review required: M96 is already shipping to stable.

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

### dg...@google.com (2021-12-03)

Please provide the info requested in https://crbug.com/chromium/1267060#c25

### yu...@chromium.org (2021-12-04)

This code can only execute from an experiment on Chrome OS stable. Do we want to merge it to M96? (I did not add the merge request)

### am...@chromium.org (2021-12-06)

updating OS as this issue also affects all desktop platforms of Chrome browser, not just Chrome OS 

### yu...@chromium.org (2021-12-06)

Although this can happen on Windows or Linux, WebUI tab strip is not turned on by default and not running any experiments on Windows or Linux. The feature is not supported on Mac. I'm removing the merge review M96 and M97 for now, if anyone thinks the merge is still necessary please add it back.

### am...@google.com (2021-12-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-12-06)

Congratulations, leecraso@ -- this issue was already known to us, but we wanted to extend a patch bonus for the patch you provided. Thank you for efforts and your suggested patch!

### le...@gmail.com (2021-12-07)

Thanks for this extra reward!

### am...@google.com (2021-12-07)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-02-01)

[Empty comment from Monorail migration]

### am...@google.com (2022-02-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-04-05)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-25)

[Empty comment from Monorail migration]

### is...@google.com (2022-08-25)

This issue was migrated from crbug.com/chromium/1267060?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1259842, crbug.com/chromium/1271849, crbug.com/chromium/1274518]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057826)*

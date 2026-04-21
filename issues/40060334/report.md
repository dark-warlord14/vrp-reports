# UAF in AccessCodeCastSinkService

| Field | Value |
|-------|-------|
| **Issue ID** | [40060334](https://issues.chromium.org/issues/40060334) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Internals>Cast |
| **Platforms** | Mac, Windows |
| **Reporter** | ha...@gmail.com |
| **Assignee** | gb...@google.com |
| **Created** | 2022-07-20 |
| **Bounty** | $9,500.00 |

## Description

**Steps to reproduce the problem:**  

Will attch details and PoC soon.

**Problem Description:**  

above all.

**Additional Comments:**

\*\*Chrome version: \*\* 105.0.5189.0 \*\*Channel: \*\* Stable

**OS:** Windows

## Attachments

- deleted (application/octet-stream, 0 B)
- [asan1.txt](attachments/asan1.txt) (text/plain, 14.5 KB)
- [asan2.txt](attachments/asan2.txt) (text/plain, 33.6 KB)
- [poc.html](attachments/poc.html) (text/plain, 63 B)
- [suggested_fix.patch](attachments/suggested_fix.patch) (text/plain, 874 B)

## Timeline

### ha...@gmail.com (2022-07-20)

`AccessCodeCastSinkService` is the Keyed Service. When the `AccessCodeCastRememberDevices` feature is enabled (note that `AccessCodeCastRememberDevices` feature is enabled by default), it will observe the network monitor in [1]. `DiscoveryNetworkMonitor` (i.e., network_monitor) [2] is a singleton class, and will notify the service when the network is changed. However, when the keyed service `AccessCodeCastSinkService` is destroyed, it doesn't remove itself from the observer of the DiscoveryNetworkMonitor. Therefore, DiscoveryNetworkMonitor could still notify the freed AccessCodeCastSinkService and call its freed `AccessCodeCastSinkService::OnNetworksChanged` [3], resulting in UAF.

[1]https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/media/router/discovery/access_code/access_code_cast_sink_service.cc;l=131-136

AccessCodeCastSinkService::AccessCodeCastSinkService(
    Profile* profile,
    MediaRouter* media_router,
    CastMediaSinkServiceImpl* cast_media_sink_service_impl,
    DiscoveryNetworkMonitor* network_monitor,
    PrefService* prefs)
    : profile_(profile),
      media_router_(media_router),
      media_routes_observer_(
          std::make_unique<AccessCodeMediaRoutesObserver>(media_router, this)),
      cast_media_sink_service_impl_(cast_media_sink_service_impl),
      task_runner_(base::SequencedTaskRunnerHandle::Get()),
      network_monitor_(network_monitor),
      prefs_(prefs),
      identity_manager_(IdentityManagerFactory::GetForProfile(profile_)) {
...

  if (base::FeatureList::IsEnabled(features::kAccessCodeCastRememberDevices)) {
    // We don't need to post this task per the DiscoveryNetworkMonitor's
    // promise: "All observers will be notified of network changes on the thread
    // from which they registered."
    pref_updater_ = std::make_unique<AccessCodeCastPrefUpdater>(prefs_);
    network_monitor_->AddObserver(this); // ---------- [1] observe network monitor

[2]https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/media/router/discovery/discovery_network_monitor.cc;l=58-61;drc=717a5ba32f0aba300c860d5bff7c87bbcff44afc

[3]https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/media/router/discovery/access_code/access_code_cast_sink_service.cc;l=808-815;drc=717a5ba32f0aba300c860d5bff7c87bbcff44afc


### [Deleted User] (2022-07-20)

[Empty comment from Monorail migration]

### ha...@gmail.com (2022-07-20)

There are many way to trigger this UAF. Firstly, apply the following patch in order to make AccessCodeCast enabled.

```
diff --git a/chrome/browser/media/router/discovery/access_code/access_code_cast_feature.cc b/chrome/browser/media/router/discovery/access_code/access_code_cast_feature.cc
index 5354a36a14e01..bb264ed7333c6 100644
--- a/chrome/browser/media/router/discovery/access_code/access_code_cast_feature.cc
+++ b/chrome/browser/media/router/discovery/access_code/access_code_cast_feature.cc
@@ -38,7 +38,7 @@ void RegisterAccessCodeProfilePrefs(PrefRegistrySimple* registry) {
 }

 bool GetAccessCodeCastEnabledPref(PrefService* pref_service) {
-  return pref_service->GetBoolean(prefs::kAccessCodeCastEnabled);
+  return true;
 }

 base::TimeDelta GetAccessCodeDeviceDurationPref(PrefService* pref_service) {
```

Take two methods in order to exploit it for an example:

Method 1: On Mac, we could launch chrome with the attache poc.html, leaving the Chromium tray on the task docker. (by running .`/Chromium.app/Contents/MacOS/Chromium http://127.0.0.1:8000/poc.html`) Then change the network (either turn on/off the network, change another network id, or anything will affect the network), then the UAF occurs. For more details, please see attached video `1345921_1.mp4` and the attached stack trace `asan1.txt`. (This is a very likely way to exploit, tested on Version 105.0.5189.0)

Method 2: On Windows/Linux/Mac (or any platform except Android), we could launch chrome with two profile enabled, letting one of the profile visit poc.html. Then change the network as the method 1 described. Reproduced on Windows Chrome Version 105.0.5178.0 and the stack trace is attached as `asan2.txt`.

### ha...@gmail.com (2022-07-20)

Since the root cause is the lacking `RemoveObserver` during the AccessCodeCastSinkService shutdown, the possible fix here is to add `RemoveObserver` during shutdown.  I've attached an candidate fix patch as `suggested_fix.patch` and could confirm that the UAF doesn't occur after apply this fix patch. 

Moreover, we could also use ScopedObservation as a fix here, in order to ensure that RemoveObserver is called when the AccessCodeCastSinkService is freed.

diff --git a/chrome/browser/media/router/discovery/access_code/access_code_cast_sink_service.cc b/chrome/browser/media/router/discovery/access_code/access_code_cast_sink_service.cc
index b7cd65a225e82..d75b2bd730254 100644
--- a/chrome/browser/media/router/discovery/access_code/access_code_cast_sink_service.cc
+++ b/chrome/browser/media/router/discovery/access_code/access_code_cast_sink_service.cc
@@ -830,6 +830,9 @@ void AccessCodeCastSinkService::OnEnabledPrefChange() {
 }

 void AccessCodeCastSinkService::Shutdown() {
+  if (base::FeatureList::IsEnabled(features::kAccessCodeCastRememberDevices)) {
+    network_monitor_->RemoveObserver(this);
+  }
   // There's no guarantee that MediaRouter is still in the
   // MediaRoutesObserver. |media_routes_observer_| accesses MediaRouter in its
   // dtor. Since MediaRouter and |this| are both KeyedServices, we must not

### rs...@chromium.org (2022-07-20)

Thank you for the detailed report and the suggested fix.

As best I can tell, kAccessCodeCastEnabled is never enabled so GetAccessCodeCastEnabledPref() will never return true, which would make this Impact-None. Please let me know if that is not the case.

[Monorail components: Internals>Cast]

### gb...@google.com (2022-07-20)

Hi -- thanks so much for doing this investigation. 

GetAccessCodeCastEnabled is currently not enabled for the general population, but will be soon as this product is rolled out.

The suggested fix looks good to me and should be implemented. What are the next steps for this process?

George

### ta...@chromium.org (2022-07-20)

George, correct me if I'm wrong, but isn't it the case that kAccessCodeCastEnabled will always be disabled by default, and will only be manually enabled via an admin policy?

### gb...@google.com (2022-07-20)

Yes, you are correct Takumi I misspoke there -- it will only be manually enabled via an admin policy. 

But a large component of the general Chrome/ChromeOS population could have this policy enabled.

### rs...@chromium.org (2022-07-20)

happyercat: If you would like to upload a fix and send it through code review, please let us know (instructions are https://chromium.googlesource.com/chromium/src/+/main/docs/contributing.md)

gbj: Otherwise you can adopt the patch and credit the reporter in the CL description.

Regarding the security assessment: when/if this is currently enable-able by admin policy, that is a supported configuration, so that would mean the bug has Security_Impact. But if it is currently not possible to enable, then Impact-None is correct.

### gb...@google.com (2022-07-20)

Let me know how you feel happyercat: I would love to get this CL submitted ASAP if possible.

### ha...@gmail.com (2022-07-21)

Hi team, I've uploaded an candidate fix at https://chromium-review.googlesource.com/c/chromium/src/+/3778903/

Feel free to discuss about the patch there, thank you.

### gb...@google.com (2022-07-21)

The patch looks good to me and should be submitted once it passes a dry run -- my question for the security team is, should we try to cherry-pick this into M105? The saved devices feature (which is still protected by the admin policy AccessCodeCastEnabled) was officially enabled by default for patch M104, so we should probably try to get this in asap.

### rs...@chromium.org (2022-07-21)

M105 hasn’t branched yet, but if this code is reachable/vulnerable in M104 then I need to adjust the flags and we will probably want to merge it there.

### gb...@google.com (2022-07-21)

Correct me if I am wrong but I believe a user could turn on the AccessCodeCastingEnabled policy (https://chromeenterprise.google/policies/?policy=AccessCodeCastEnabled) and then reach this vulnerability. 

What do you mean by adjust the flags?

### rs...@chromium.org (2022-07-21)

Your team is most familiar with this code and to determine what the affected versions are; please do that and let us know. If the feature can be enabled by admin policy without the user enabling a feature flag, then that is considered enabled in the affected versions.

By flags I mean the Security* labels attached to the bug.

### gb...@google.com (2022-07-21)

The feature can be enabled by admin policy without the user enabling a feature flag, so by this definition it should be considered enabled in the affected versions. 

@happyercat I have LGTM your CL since the dry run looks good to me. Merge by m104 sounds good.

### rs...@chromium.org (2022-07-21)

Was this feature under field trial prior to M104, or was it enabled by default in M104?

### [Deleted User] (2022-07-21)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-22)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-22)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gb...@google.com (2022-07-22)

It was enabled by default in M104 -- see https://chromium-review.googlesource.com/c/chromium/src/+/3664082

happyercat's CL is being submitted as we speak as well.

### rs...@chromium.org (2022-07-22)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-07-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0491dbf0e9b071a1918e3d63df912cb1940fbb9d

commit 0491dbf0e9b071a1918e3d63df912cb1940fbb9d
Author: Smith Richard <happyercat@gmail.com>
Date: Sat Jul 23 00:56:17 2022

Remove observer during AccessCodeCastSinkService shutdown.

Bug: 1345921
Change-Id: Ib97e796d3c8dc3ee972cc132f5bf41995ee78e66
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3778903
Reviewed-by: George Benz <gbj@google.com>
Commit-Queue: George Benz <gbj@google.com>
Cr-Commit-Position: refs/heads/main@{#1027498}

[modify] https://crrev.com/0491dbf0e9b071a1918e3d63df912cb1940fbb9d/chrome/browser/media/router/discovery/access_code/access_code_cast_sink_service.cc
[modify] https://crrev.com/0491dbf0e9b071a1918e3d63df912cb1940fbb9d/AUTHORS


### [Deleted User] (2022-07-23)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-25)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gb...@google.com (2022-07-25)

Hi -- is this something that I should make sure to cherry pick as well into M104? Is that my responsibility here or the security teams?

### rs...@chromium.org (2022-07-25)

Marking the bug as Fixed will trigger sheriffbot to evaluate for merges, but then it is your responsibility to do them if/when approved.

### gb...@google.com (2022-07-25)

Ok, so I will start the process to get this chang merged into M104 then? 

Thanks so much for your time here.

### [Deleted User] (2022-07-25)

Requesting merge to beta M104 because latest trunk commit (1027498) appears to be after beta branch point (1012729).

Requesting merge to dev M105 because latest trunk commit (1027498) appears to be after dev branch point (1027018).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-25)

Merge approved: your change passed merge requirements and is auto-approved for M105. Please go ahead and merge the CL to branch 5195 (refs/branch-heads/5195) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), harrysouders (iOS),  matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-25)

Merge review required: M104 is already shipping to beta.

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
Owners: eakpobaro (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-07-25)

merge tentatively approved for M104; gbj@, once you have confirmed there are stability issues or other concerns with this fix from its performance on Canary, please merge this fix to M104 (branch 5112) before noon PST tomorrow, Tuesday, 26 July, so this fix can be included in M104 stable cut -- thank you

### gb...@google.com (2022-07-25)

Thanks amy -- I am verifying the new merge on Chrome canary for both MacOS and ChromeOS with asan to be totally sure. After that is done I will merge the fix into M104 -- thanks!

### gi...@appspot.gserviceaccount.com (2022-07-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/969f20d7b623946077febd093d5e1ad3eaeb96e2

commit 969f20d7b623946077febd093d5e1ad3eaeb96e2
Author: Smith Richard <happyercat@gmail.com>
Date: Mon Jul 25 20:49:16 2022

Remove observer during AccessCodeCastSinkService shutdown.

(cherry picked from commit 0491dbf0e9b071a1918e3d63df912cb1940fbb9d)

Bug: 1345921
Change-Id: Ib97e796d3c8dc3ee972cc132f5bf41995ee78e66
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3778903
Reviewed-by: George Benz <gbj@google.com>
Commit-Queue: George Benz <gbj@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#1027498}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3785425
Auto-Submit: George Benz <gbj@google.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5195@{#17}
Cr-Branched-From: 7aa3f074a7907975b001346cc0288d0214af8451-refs/heads/main@{#1027018}

[modify] https://crrev.com/969f20d7b623946077febd093d5e1ad3eaeb96e2/chrome/browser/media/router/discovery/access_code/access_code_cast_sink_service.cc
[modify] https://crrev.com/969f20d7b623946077febd093d5e1ad3eaeb96e2/AUTHORS


### gi...@appspot.gserviceaccount.com (2022-07-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7cc12d3b0df57d767382e0241f47d6b1f3916851

commit 7cc12d3b0df57d767382e0241f47d6b1f3916851
Author: Smith Richard <happyercat@gmail.com>
Date: Mon Jul 25 23:28:25 2022

Remove observer during AccessCodeCastSinkService shutdown.

(cherry picked from commit 0491dbf0e9b071a1918e3d63df912cb1940fbb9d)

Bug: 1345921
Change-Id: Ib97e796d3c8dc3ee972cc132f5bf41995ee78e66
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3778903
Reviewed-by: George Benz <gbj@google.com>
Commit-Queue: George Benz <gbj@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#1027498}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3785497
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Auto-Submit: George Benz <gbj@google.com>
Cr-Commit-Position: refs/branch-heads/5112@{#1178}
Cr-Branched-From: b13d3fe7b3c47a56354ef54b221008afa754412e-refs/heads/main@{#1012729}

[modify] https://crrev.com/7cc12d3b0df57d767382e0241f47d6b1f3916851/chrome/browser/media/router/discovery/access_code/access_code_cast_sink_service.cc
[modify] https://crrev.com/7cc12d3b0df57d767382e0241f47d6b1f3916851/AUTHORS


### gb...@google.com (2022-07-25)

This change has been merged into both 5112 and 5195 now. Thanks for the help everyone!

### [Deleted User] (2022-07-26)

[Empty comment from Monorail migration]

### gb...@google.com (2022-07-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-26)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-08-05)

Congratulations! The VRP Panel has decided to award you $9500 for this report. The reward amount was decided upon based on this issue being mitigated by profile destruction, but received a patch bonus by both suggesting and committing the patch for this bug. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-08-08)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1345921?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060334)*

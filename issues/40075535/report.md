# iOS Chrome Media Permission Privilege Escalation

| Field | Value |
|-------|-------|
| **Issue ID** | [40075535](https://issues.chromium.org/issues/40075535) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>GetUserMedia, Internals>Permissions>Model |
| **Platforms** | iOS |
| **Reporter** | pr...@gmail.com |
| **Assignee** | aj...@google.com |
| **Created** | 2023-10-24 |
| **Bounty** | $3,000.00 |

## Description

**Steps to reproduce the problem:**  

We are able to escalate Media Permission privilege to Top-level Origin when it's framed.

PoC:

Legitimate.site: <iframe src="https://pwning.click/mediaspoof.php"/></iframe>

Malicious.site (<https://pwning.click> for this test demo):

<input onclick="start()" type="button" value="Click here" />
<script>
function start(){
var recognition = new webkitSpeechRecognition();
recognition.start();
navigator.webkitGetUserMedia({audio: true}, function(){}, function(){});
}
</script>

**Problem Description:**  

Media Permission Privilege Escalation is possible in iOS Chrome

**Additional Comments:**  

If you want to test without <https://pwning.click/mediaspoof.php> then download this file and upload to your server for malicious.site demo.

\*\*Chrome version: \*\* 118.0.0.0 \*\*Channel: \*\* Stable

**OS:** iOS

## Attachments

- [mediaspoof.html](attachments/mediaspoof.html) (text/plain, 268 B)

## Timeline

### [Deleted User] (2023-10-24)

[Empty comment from Monorail migration]

### pr...@gmail.com (2023-10-25)

This works no matter how deeply frames with documents are nested; which means attacker can access to microphone and such permission by malicious ad on voice chat website for example, with no user interaction.

### pa...@chromium.org (2023-10-25)

[security shepherd] Thanks for the report!

This might be related to crbug.com/1495516, although I think those are different issues (but targeting the same API). Assigning to @japhet@chromium.org. Again, I do not have a device to test that on, so please feel free to re-assign/close if not reproducible. Not setting severity until this is confirmed.

[Monorail components: Blink>GetUserMedia Internals>Permissions>Model]

### ja...@chromium.org (2023-10-25)

Assiging to someone on webrtc for further triage...but given that this is specific to iOS chrome - this is a WebKit issue, not a chromium issue, right?

### ja...@chromium.org (2023-10-25)

[Comment Deleted]

### pa...@chromium.org (2023-10-26)

Hello reporter!

I figured a way to reproduce, and unfortunately, similarly to https://crbug.com/1495521, it also requests user permission on my hand. Can you provide more information on how to reproduce what you are referring to?

### pa...@chromium.org (2023-10-26)

[Empty comment from Monorail migration]

### pr...@gmail.com (2023-10-26)

That's from iOS and expected behaviour if you didn't allow iOS Chrome to access your microphone on your device, tap on ok to reproduce this issue.

### [Deleted User] (2023-10-26)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pa...@chromium.org (2023-10-26)

Assigning to @ajuma as well to further triage this, as it is related to crbug.com/1495521. If I understand correctly, it shouldn't be requesting this access?

### pa...@chromium.org (2023-10-26)

[Empty comment from Monorail migration]

### aj...@google.com (2023-10-26)

Does this also reproduce in Safari on iOS?

### pr...@gmail.com (2023-10-26)

This does and partially for issues on https://crbug.com/1495521

### [Deleted User] (2023-10-27)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aj...@chromium.org (2023-10-27)

I've filed https://bugs.webkit.org/show_bug.cgi?id=263795

### [Deleted User] (2023-10-28)

[Empty comment from Monorail migration]

### aj...@chromium.org (2023-10-30)

Debugging some more, I think the main issue here is that WebKit is allowing iframes to request camera/microphone permission even when the main frame has not granted this using feature policy (e.g., the iframe doesn't have `allow="camera,microphone"`), and the call to webkitSpeechRecognition().start() is somehow confusing WebKit into allowing this.

*If* the main frame does use feature policy to grant iframes this ability, then I think it is correct to show the main frame origin in the prompt, since even non-iOS Chrome does this, and it makes sense to me (effectively the main frame is delegating its power to request camera/microphone access to the iframe).

So the fix needed in WebKit is to make sure that frames that have not be granted camera/microphone access by feature policy cannot request camera/microphone permissions.


### pr...@gmail.com (2023-10-30)

[Comment Deleted]

### pr...@gmail.com (2023-10-30)

Thanks for the comment, please allow iOS Chrome to access Media to confirm this could be exploited for unauth microphone access with no user interaction as I described in this main report and https://bugs.chromium.org/p/chromium/issues/detail?id=1495521#c18

https://malicious.ad2.site shouldn't be able to access users devices' microphone on https://legitimate.voicechat.site which could be really bad.

I figured out how to allow permissions without using webkitSpeechRecognition().start() which is different root cause and I'll report that soon.

### aj...@chromium.org (2023-10-30)

> https://malicious.ad2.site shouldn't be able to access users devices' microphone on https://legitimate.voicechat.site which could be really bad.

Yes, agreed, and feature policy (when working properly) would prevent this, since https://legitimate.voicechat.site would not grant https://malicious.ad2.site the ability to request media permissions.

### pg...@google.com (2023-11-27)

[Empty comment from Monorail migration]

### is...@google.com (2023-11-27)

This issue was migrated from crbug.com/chromium/1495516?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>GetUserMedia, Internals>Permissions>Model]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-02-04)

ajuma: Uh oh! This issue still open and hasn't been updated in the last 96 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2024-02-19)

ajuma: Uh oh! This issue still open and hasn't been updated in the last 111 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pr...@gmail.com (2024-02-19)

This has a same impact to this $5000 reward https://issues.chromium.org/issues/40075537 since users are chatting on https://legitimate.voicechat.site where microphone access has been allowed by default from users for https://legitimate.voicechat.site and as a result, the malicious ad inside nested frames can listen to https://legitimate.voicechat.site with no user interaction.

### aj...@chromium.org (2024-02-19)

Marking fixed since the WebKit change (https://commits.webkit.org/270432@main) is in iOS 17.4 beta.

### pe...@google.com (2024-02-19)

Dear owner, thanks for fixing this bug. We've reopened it because security bugs need the Severity (S0-S3) and the Found In set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

### am...@google.com (2024-02-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-02-22)

Congratulations, James! The Chrome VRP Panel has decided to award you $3,000 for this report. The reward decision was made based on the preconditions and mitigations to exploit this as conveyed in c#21. We also realized you linked another report of yours in c#26 as an example of reward amount you are expecting for this report. The reward amount here is lower, because the overall report quality of this issue is lower than the previous report. The reward amount was increased for the other issue based on the additional information provided, including demonstration and impact.
Thank you for your efforts and reporting this issue to us!

### pr...@gmail.com (2024-02-23)

Thanks for the reward. 

To understand correctly and for clarification, that comment #c21 is agreeing to the impact I've shown and mentioning that feature policy would prevent this exploit, but not indicating preconditions whatsoever.

Thanks for letting me know that decision is due to lower quality report; FWIW the length of report is definitely shorter but overall impacts were clearly noted and we didn't need to add any further information in this case, so I'd agree it's less quantity but not sure about the quality due to following explanation: https://issues.chromium.org/issues/40075535#comment3 and https://issues.chromium.org/issues/40075535#comment20 .

### pe...@google.com (2024-02-27)

The Found In field may only contain numeric values.
Some values couldn't be corrected but were removed, please verify that any important data wasn't lost.
You can see the changes by toggling full history on the issue.

### pe...@google.com (2024-02-27)

Dear owner, thanks for fixing this bug. We've reopened it because security bugs need the Severity (S0-S3) and the Found In set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

### am...@chromium.org (2024-02-27)

blintz is not allowing keeping external dependency bugs closed when they lack a (solely numeric) foundin value
setting a somewhat arbitrary foundin- value with SI-none to keep this issue closed as fixed

### pe...@google.com (2024-06-05)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40075535)*

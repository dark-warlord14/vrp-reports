# Security: use-after-free in ManagePasswordsUIController::OnChooseCredentials

| Field | Value |
|-------|-------|
| **Issue ID** | [40063412](https://issues.chromium.org/issues/40063412) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Passwords |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | du...@gmail.com |
| **Assignee** | va...@chromium.org |
| **Created** | 2023-03-06 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**  

There is a heap use-after-free vulnerability in ManagePasswordsUIController.

There is a unique pointer dialog\_controller\_ in `manage_passwords_ui_controller.h`. It can be reset as the controller of three prompts in the following three functions.  

**-------------------------** -------------------------------------------------  

// The controller for the blocking dialogs.  

std::unique\_ptr<PasswordBaseDialogController> dialog\_controller\_;

ManagePasswordsUIController::OnChooseCredentials  

ManagePasswordsUIController::OnPromptEnableAutoSignin  

ManagePasswordsUIController::OnCredentialLeak  

**-------------------------** -------------------------------------------------

Unlike the other two, in OnChooseCredentials there is no check for `if (dialog_controller_)`  before reset.

**-------------------------** -------------------------------------------------  

bool ManagePasswordsUIController::OnChooseCredentials(  

std::vector<std::unique\_ptr<password\_manager::PasswordForm>>  

local\_credentials,  

const url::Origin& origin,  

ManagePasswordsState::CredentialsCallback callback) {  

DCHECK(!local\_credentials.empty());  

if (!HasBrowserWindow())  

return false;  

// If |local\_credentials| contains PSL matches they shouldn't be propagated to  

// the state (unless they are also web affiliations) because PSL matches  

// aren't saved for current page. This logic is implemented here because  

// Android uses ManagePasswordsState as a data source for account chooser.  

CredentialManagerDialogController::FormsVector locals;  

if (password\_manager\_util::GetMatchType(\*local\_credentials[0]) !=  

password\_manager\_util::GetLoginMatchType::kPSL) {  

locals = CopyFormVector(local\_credentials);  

}  

passwords\_data\_.OnRequestCredentials(std::move(locals), origin);  

passwords\_data\_.set\_credentials\_callback(std::move(callback));  

auto\* raw\_controller = new CredentialManagerDialogControllerImpl(  

Profile::FromBrowserContext(web\_contents()->GetBrowserContext()), this);  

dialog\_controller\_.reset(raw\_controller); <--------------------------  

raw\_controller->ShowAccountChooser(CreateAccountChooser(raw\_controller),  

std::move(local\_credentials));  

UpdateBubbleAndIconVisibility();  

return true;  

}  

**-------------------------** -------------------------------------------------

If dialog\_controller\_ is not null at this time, for example, the credential leak prompt pops up at this time.  

`dialog_controller_.reset(raw_controller);` will reset the current dialog\_controller\_, and then invokes the following call.

**-------------------------** -------------------------------------------------  

`dialog\_controller\_.reset(raw\_controller)  

~CredentialLeakDialogControllerImpl  

CredentialLeakDialogControllerImpl::ResetDialog  

CredentialLeakDialogView::ControllerGone  

Widget::Close  

CredentialLeakDialogController::OnCloseDialog  

ManagePasswordsUIController::OnLeakDialogHidden  

**-------------------------** -------------------------------------------------

Finally calling dialog\_controller\_.reset() again in OnLeakDialogHidden.  

It will cause the newly created CredentialManagerDialogControllerImpl to be destroyed.  

That is raw\_controller.  

Then the using of raw\_controller will cause the use-after-free.

**-------------------------** -------------------------------------------------  

void ManagePasswordsUIController::OnLeakDialogHidden() {  

dialog\_controller\_.reset();  

if (GetState() == password\_manager::ui::PENDING\_PASSWORD\_UPDATE\_STATE) {  

bubble\_status\_ = BubbleStatus::SHOULD\_POP\_UP;  

UpdateBubbleAndIconVisibility();  

return;  

}  

if (GetState() == password\_manager::ui::PENDING\_PASSWORD\_STATE) {  

if (!IsSavingPromptBlockedExplicitlyOrImplicitly()) {  

bubble\_status\_ = BubbleStatus::SHOULD\_POP\_UP;  

}  

UpdateBubbleAndIconVisibility();  

}  

}  

**-------------------------** -------------------------------------------------

Might since <https://chromium.googlesource.com/chromium/src/+/1c7739d398cf302c984dc91f88740e38943849d4>, not sure.

**REPRODUCTION CASE**

1. apply render.diff and browser.diff
2. chrome --enable-blink-features=MojoJS --user-data-dir=TMP/noexist
3. login a google account
4. open <http://127.0.0.1:8000/poc.html>

browser.diff is a shortcut to simulate the password leaked behavior.  

render.diff simulate a compromised renderer to presave a password into the password store.

**CREDIT INFORMATION**  

Reporter credit: Wan Choi of Seoul National University

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 1.5 KB)
- [render.diff](attachments/render.diff) (text/plain, 3.2 KB)
- [browser.diff](attachments/browser.diff) (text/plain, 2.8 KB)
- [asan.txt](attachments/asan.txt) (text/plain, 65.4 KB)
- [patch.txt](attachments/patch.txt) (text/plain, 5.9 KB)
- [leak.png](attachments/leak.png) (image/png, 15.0 KB)
- [save.png](attachments/save.png) (image/png, 13.0 KB)
- [copy_mojo_js_bindings.py](attachments/copy_mojo_js_bindings.py) (text/plain, 512 B)
- [poc.diff](attachments/poc.diff) (text/plain, 6.8 KB)
- [poc.html](attachments/poc.html) (text/plain, 1.6 KB)
- [leak.zip](attachments/leak.zip) (application/octet-stream, 165.6 KB)
- [leak.html](attachments/leak.html) (text/plain, 1.2 KB)
- [poc.diff](attachments/poc.diff) (text/plain, 8.1 KB)
- [poc.html](attachments/poc.html) (text/plain, 1.8 KB)
- [pic1.png](attachments/pic1.png) (image/png, 172.1 KB)
- [pic2.png](attachments/pic2.png) (image/png, 63.5 KB)
- [poc.diff](attachments/poc.diff) (text/plain, 4.6 KB)
- [poc.html](attachments/poc.html) (text/plain, 1.8 KB)

## Timeline

### [Deleted User] (2023-03-06)

[Empty comment from Monorail migration]

### es...@chromium.org (2023-03-07)

Note: the patches didn't apply for some reason for me, git thinks they're corrupt, so I applied manually; here's the diff from my checkout

### es...@chromium.org (2023-03-07)

I wasn't able to reproduce this on ToT. Are there any further instructions you can provide to help us reproduce?

[Monorail components: UI>Browser>Passwords]

### du...@gmail.com (2023-03-07)

[Comment Deleted]

### [Deleted User] (2023-03-07)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2023-03-07)

(I am a bot: this is an auto-cc on a security bug)

### du...@gmail.com (2023-03-09)

[Comment Deleted]

### am...@chromium.org (2023-03-09)

I did a quick attempt to reproduce this only to be unsuccessful. In an effort to move this issue along, assigning to jkeitel@ and cc'ing vasilii@ based on work on 1351969. Apologies we have to move this along to y'all before we were able to reproduce. 

Assigning medium severity based on preconditions and user interaction required.  
An attempt to bisect to a commit was provided in the report, but appears speculative; FoundIn-Not, since unable to reproduce, will need input or information to determine when issue was introduced and update to a correct foundin- 

### du...@gmail.com (2023-03-10)

[Comment Deleted]

### du...@gmail.com (2023-03-10)

First, whether the prompt in leak.png pops up normally during the reproduction process?
If not, please check whether the current network can access "https://passwordsleakcheck-pa.googleapis.com/v1/leaks:lookupSingle"[+].

[+] https://source.chromium.org/chromium/chromium/src/+/main:components/password_manager/core/browser/leak_detection/leak_detection_request.h;drc=26d5a0721a1b21ded47b31a3fc0a5ef4928d5b80;bpv=0;bpt=1;l=38

If the leak prompt pops up normally, it may be the problem about the password store. 
You can try to manually click the save button in the window shown in save.png before the leak prompt pops up, and wait for a moment.
Note that this gesture is just for testing, it can be replaced by the code in render.patch

### jk...@google.com (2023-03-10)

Changing owner to Vasilii as the PWM TLM - I don't think this has anything to do with code that I ever touched.

That being said, I tried (and failed) to reproduce - couldn't even apply the patches cleanly. I can, however, follow the reasoning above. To be on the safe side, one should probably call reset() on `dialog_controller_` prior to assigning it the new value.

### du...@gmail.com (2023-03-10)

[Comment Deleted]

### gi...@appspot.gserviceaccount.com (2023-03-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/201d4253812f9548b7bb774a3827bb31c8d17272

commit 201d4253812f9548b7bb774a3827bb31c8d17272
Author: Vasilii Sukhanov <vasilii@chromium.org>
Date: Fri Mar 10 10:30:42 2023

Hide the password leak detection dialog before the account chooser is
displayed.

Fixed: 1421773
Change-Id: Icfde6d126801e87cec09ffea941ae61f3a087703
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4329269
Reviewed-by: Viktor Semeniuk <vsemeniuk@google.com>
Commit-Queue: Vasilii Sukhanov <vasilii@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1115622}

[modify] https://crrev.com/201d4253812f9548b7bb774a3827bb31c8d17272/chrome/browser/ui/passwords/manage_passwords_ui_controller.cc


### va...@chromium.org (2023-03-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-10)

Merge rejected: M112 is already shipping to beta and this issue is marked as a Pri-2, Pri-3, or Type-Feature.

Please contact the milestone owner if you have questions.
Owners: govind (Android), govind (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-03-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-10)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-03-10)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-03-10)

Thanks vasilii@ for landing a fix so quickly on this one. 

Updating to FoundIn-110 as this issue appears to have been around for awhile and M110 is current Extended and oldest active release channel. 
Merge was rejected because foundin- was not updated so that Security_Impact could be applied by the bot. Given that there was already human intervention in requesting merges, I'm not sure the bot will re-tag this for a merge so I'll manually monitor it and may need to manually ad it to my merge queue for review on Monday, allowing it to get some bake time on Canary first. 

### du...@gmail.com (2023-03-11)

The fix works fine in tests.

And about severity. As https://crbug.com/chromium/1421773#c9 said, this vulnerability does not require any user interaction. The only precondition is a compromised renderer.

I upload a clean patch based on commit 69aba5a4050bb338f5c34d70034d038fc0c9a6ed. If needed.

Reproduction:
1. apply poc.diff
2. python copy_mojo_js_bindings.py /path/to/chromium/gen && python3 -m http.server 8000
3. chrome --enable-blink-features=MojoJS --user-data-dir=TMP/noexist http://127.0.0.1:8000/poc.html
4. wait 3 seconds

Sorry for wasting time due to lack of experience about submitting bug.

### [Deleted User] (2023-03-13)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-03-13)

the bot did not re-add the merge request labels, approving for merge now
due to rather trivial nature of patch, approving to backmerge out of an abundance of caution, the logging into or having to be logged into a Google account is not considered a user interaction or mitigation, but AIUI you would need to close the leak password prompts to trigger the uaf 

### du...@gmail.com (2023-03-14)

[Comment Deleted]

### gi...@appspot.gserviceaccount.com (2023-03-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1ae8d9410010b689c1afb0729837dd5d5c4687f8

commit 1ae8d9410010b689c1afb0729837dd5d5c4687f8
Author: Vasilii Sukhanov <vasilii@chromium.org>
Date: Tue Mar 14 10:17:17 2023

Hide the password leak detection dialog before the account chooser is
displayed.

(cherry picked from commit 201d4253812f9548b7bb774a3827bb31c8d17272)

Fixed: 1421773
Change-Id: Icfde6d126801e87cec09ffea941ae61f3a087703
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4329269
Reviewed-by: Viktor Semeniuk <vsemeniuk@google.com>
Commit-Queue: Vasilii Sukhanov <vasilii@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1115622}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4336318
Auto-Submit: Vasilii Sukhanov <vasilii@chromium.org>
Commit-Queue: Viktor Semeniuk <vsemeniuk@google.com>
Cr-Commit-Position: refs/branch-heads/5615@{#468}
Cr-Branched-From: 9c6408ef696e83a9936b82bbead3d41c93c82ee4-refs/heads/main@{#1109224}

[modify] https://crrev.com/1ae8d9410010b689c1afb0729837dd5d5c4687f8/chrome/browser/ui/passwords/manage_passwords_ui_controller.cc


### [Deleted User] (2023-03-14)

LTS Milestone M108

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-03-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f0837036aadbd42784b425506b56ce1c274f0b3a

commit f0837036aadbd42784b425506b56ce1c274f0b3a
Author: Vasilii Sukhanov <vasilii@chromium.org>
Date: Tue Mar 14 10:31:32 2023

Hide the password leak detection dialog before the account chooser is
displayed.

(cherry picked from commit 201d4253812f9548b7bb774a3827bb31c8d17272)

Fixed: 1421773
Change-Id: Icfde6d126801e87cec09ffea941ae61f3a087703
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4329269
Reviewed-by: Viktor Semeniuk <vsemeniuk@google.com>
Commit-Queue: Vasilii Sukhanov <vasilii@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1115622}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4336319
Commit-Queue: Viktor Semeniuk <vsemeniuk@google.com>
Auto-Submit: Vasilii Sukhanov <vasilii@chromium.org>
Cr-Commit-Position: refs/branch-heads/5563@{#1141}
Cr-Branched-From: 3ac59a6729cdb287a7ee629a0004c907ec1b06dc-refs/heads/main@{#1097615}

[modify] https://crrev.com/f0837036aadbd42784b425506b56ce1c274f0b3a/chrome/browser/ui/passwords/manage_passwords_ui_controller.cc


### gi...@appspot.gserviceaccount.com (2023-03-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0ead4d590446363caf3e1a9c2c9770ce2f7953da

commit 0ead4d590446363caf3e1a9c2c9770ce2f7953da
Author: Vasilii Sukhanov <vasilii@chromium.org>
Date: Tue Mar 14 10:58:54 2023

Hide the password leak detection dialog before the account chooser is
displayed.

(cherry picked from commit 201d4253812f9548b7bb774a3827bb31c8d17272)

Fixed: 1421773
Change-Id: Icfde6d126801e87cec09ffea941ae61f3a087703
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4329269
Reviewed-by: Viktor Semeniuk <vsemeniuk@google.com>
Commit-Queue: Vasilii Sukhanov <vasilii@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1115622}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4335721
Commit-Queue: Viktor Semeniuk <vsemeniuk@google.com>
Auto-Submit: Vasilii Sukhanov <vasilii@chromium.org>
Cr-Commit-Position: refs/branch-heads/5481@{#1353}
Cr-Branched-From: 130f3e4d850f4bc7387cfb8d08aa993d288a67a9-refs/heads/main@{#1084008}

[modify] https://crrev.com/0ead4d590446363caf3e1a9c2c9770ce2f7953da/chrome/browser/ui/passwords/manage_passwords_ui_controller.cc


### vo...@google.com (2023-03-14)

[Empty comment from Monorail migration]

### vo...@google.com (2023-03-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-14)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### va...@chromium.org (2023-03-14)

The bug isn't a regression but existed for a few years probably.

### vo...@google.com (2023-03-16)

1. Just one https://crrev.com/c/4335651
2. Low - no conflicts
3. Yes, M110
4. Yes

### gm...@google.com (2023-03-16)

For LTS: Merged to 110 only 2 days ago. Delaying until 111 goes out

### am...@google.com (2023-03-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-03-17)

Congratulations, Wan Choi! The VRP Panel has decided to award you $10,000 for this mildly mitigated security bug based on the preconditions and the rather significant patch in your updated POC. If you can demonstrate this issue as fully remote exploitable without preconditions or significant functional changes to Chrome, we would be happy to reassess for a potentially higher reward amount.
A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts in reporting this issue to us -- nice work! 

### du...@gmail.com (2023-03-17)

First of all thanks a lot for the reward.

As https://crbug.com/chromium/1421773#c20 said, this vulnerability does not require any user interaction or account login or significant functional changes to Chrome. The only precondition is a compromised renderer and the shortcut patch to simulate the password leaked behavior.

I noticed that this should not be a mildly mitigated security bug based on historical vulnerabilities.

I don't know what improvements I need to make, do I need to complete the password leaked behavior?

### du...@gmail.com (2023-03-17)

Actually, after my test, this shortcut is not necessary on the stable channel of Chrome. Therefore, this vulnerability can be triggered without the browser patch.

It seems that in the developer version of chromium, you need to configure related api environment before you can use this check leak api.

Above all, the only precondition for triggering this vulnerability is a compromised renderer.

### am...@chromium.org (2023-03-17)

Is this also based on the POC in https://crbug.com/chromium/1421773#c20? Would it be possible for you to provide a demonstration of that, with a patch for a compromised renderer in of your functional patch? 

### am...@google.com (2023-03-17)

[Empty comment from Monorail migration]

### du...@gmail.com (2023-03-18)

Yes. And the poc of https://crbug.com/chromium/1421773#c20 is the same as the original poc, the poc of https://crbug.com/chromium/1421773#c20 just provides a clean patch based on commit 69aba5a4050bb338f5c34d70034d038fc0c9a6ed.

The browser.patch in the poc is just to pop up the password leak prompt. 
The password leak prompt pops up needs to access the Google api of passwordsleakcheck. Using this api in the developer version of Chromium requires configuring some environment variables. I didn't figure out how to configure it, so I modified this part of the logic by using browser.patch. But it can be used in stable channel Chrome without configuration, so browser.patch is not needed.

You can verify this behavior with the attached leak.html. 

python -m http.server 8000
PATH\TO\Google\Chrome\Application\chrome.exe --enable-blink-features=MojoJS --user-data-dir=TMP/noexist http://127.0.0.1:8000/poc.html
Wait for about 3 seconds, the password leak prompt will pop up normally.

### am...@chromium.org (2023-03-21)

[Empty comment from Monorail migration]

### du...@gmail.com (2023-03-21)

May I ask if the reward amount will be re-discussed? Or do I need to provide anything else?

### am...@chromium.org (2023-03-21)

Yes, we can reassess this at a future VRP panel session. Due to scheduling, it may not occur this week so we may not get back to you until late next week. 

Regarding >>The poc of https://crbug.com/chromium/1421773#c20 just provides a clean patch based on commit 69aba5a4050bb338f5c34d70034d038fc0c9a6ed.
Can you please confirm the commit you linked? This commit is simply a change to the Sync owners file. 



### pg...@google.com (2023-03-21)

[Empty comment from Monorail migration]

### pg...@google.com (2023-03-21)

[Empty comment from Monorail migration]

### du...@gmail.com (2023-03-22)

[Comment Deleted]

### gm...@google.com (2023-03-28)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-03-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1d299a5ac37a3ddd1f9590831fd28a86a23f4ea8

commit 1d299a5ac37a3ddd1f9590831fd28a86a23f4ea8
Author: Vasilii Sukhanov <vasilii@chromium.org>
Date: Thu Mar 30 11:37:57 2023

[M108-LTS] Hide the password leak detection dialog before the account chooser is
displayed.

(cherry picked from commit 201d4253812f9548b7bb774a3827bb31c8d17272)

(cherry picked from commit 0ead4d590446363caf3e1a9c2c9770ce2f7953da)

Fixed: 1421773
Change-Id: Icfde6d126801e87cec09ffea941ae61f3a087703
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4329269
Commit-Queue: Vasilii Sukhanov <vasilii@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/main@{#1115622}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4335721
Commit-Queue: Viktor Semeniuk <vsemeniuk@google.com>
Auto-Submit: Vasilii Sukhanov <vasilii@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/5481@{#1353}
Cr-Original-Branched-From: 130f3e4d850f4bc7387cfb8d08aa993d288a67a9-refs/heads/main@{#1084008}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4335651
Owners-Override: Michael Ershov <miersh@google.com>
Commit-Queue: Zakhar Voit <voit@google.com>
Reviewed-by: Michael Ershov <miersh@google.com>
Reviewed-by: Vasilii Sukhanov <vasilii@chromium.org>
Cr-Commit-Position: refs/branch-heads/5359@{#1420}
Cr-Branched-From: 27d3765d341b09369006d030f83f582a29eb57ae-refs/heads/main@{#1058933}

[modify] https://crrev.com/1d299a5ac37a3ddd1f9590831fd28a86a23f4ea8/chrome/browser/ui/passwords/manage_passwords_ui_controller.cc


### vo...@google.com (2023-03-30)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-03-30)

Uploading POC from https://crbug.com/chromium/1421773#c40; I'm only current active release builds right now and haven't had opportunity to repro without the patch for this issue.

### du...@gmail.com (2023-03-31)

The attachment in https://crbug.com/chromium/1421773#c40 is only used to prove that the leak prompt could be popped up without the browser.patch in the Chrome used by the user in the actual scenario (not the locally compiled Chromium). You can verify this in Chrome without any patches.

However, if you want to trigger the vulnerability in the locally compiled Chromium, you still need to use the original POC (or the clean patch version in https://crbug.com/chromium/1421773#c20). 

* The browser.patch was only used to pop up the leak prompt in the original POC. I think the browser.patch may be the reason why this bug is considered as a mildly mitigated security bug, so I raised https://crbug.com/chromium/1421773#c40 to explain that the browser.patch is not needed in actual scenarios.

I don't know if I explained clearly, please feel free to contact me if you have any questions.

### am...@chromium.org (2023-03-31)

in https://crbug.com/chromium/1421773#c40 you conveyed: 
>>> The password leak prompt pops up needs to access the Google api of passwordsleakcheck. Using this api in the developer version of Chromium requires configuring some environment variables. I didn't figure out how to configure it, so I modified this part of the logic by using browser.patch. But it can be used in stable channel Chrome without configuration, so browser.patch is not needed.

This level of modification in the dev version of Chromium would be considered as a mitigation. 
So, yes, I am purposely uploading the POC from https://crbug.com/chromium/1421773#c40, so that we can evaluate that POC, but also so that we can reproduce it to verify this claim -- that the modification via the browser patch is not required in shipped, Stable channel versions of Chrome that would impact users in this way. 

I uploaded it into a VM I am using for reproductions ,and while I do have locally compiled builds of Chromium, I also am running production version of Google Chrome. The issue I am running into at this time, however, that to attempt to reproduce it did not result in a crash or potential UAF but also my VM configuration has only up-to-date configurations of Stable Chrome, which include the fix for this issue, thus I am not able to successfully reproduce this as-is at this time. 

### du...@gmail.com (2023-04-02)

If the leak prompt pops up correctly, there may be a problem with the pre-stored password. I wrote a new version of the POC, please try it.
Sorry again for the additional validation work.

1. apply poc.diff
2. chrome --enable-blink-features=MojoJS --user-data-dir=TMP/noexist http://127.0.0.1:8000/poc.html


### du...@gmail.com (2023-04-06)

Hello, may I ask if the problem has been reproduced successfully? 

After I tested multiple versions of the code on multiple machines, the POC in https://crbug.com/chromium/1421773#c53 is very stable. 

You can use this on your locally compiled Chromium to verify the UAF, and use the attachment in https://crbug.com/chromium/1421773#c40 to verify that the leak prompt could be popped up without the browser.patch in the production version of Google Chrome.

And no matter which way you choose, make sure your test environment can access "https://passwordsleakcheck-pa.googleapis.com/v1/leaks:lookupSingle"[+].

[+] https://source.chromium.org/chromium/chromium/src/+/main:components/password_manager/core/browser/leak_detection/leak_detection_request.h;drc=26d5a0721a1b21ded47b31a3fc0a5ef4928d5b80;bpv=0;bpt=1;l=38

### du...@gmail.com (2023-04-11)

Hi, may I ask if this issue has been reassessed at the VRP panel or is there any feedback?

It is definitely a high-risk vulnerability that does not require user interaction and is not mitigated. And the POC in https://crbug.com/chromium/1421773#c53 is pretty stable in various version tests.

So could someone please deal with it or tell me what can I do?

### am...@chromium.org (2023-04-11)

Hello, apologies for the delay in response as this bug is still under evaluation. When it was originally evaluated, there was a significant browser patch to prompt the password leakage in Chromium builds. We generally reproduce bugs via Chromium asan builds in VMs or emulators. Given that the POC and information related to reproduction in production versions of Chrome was provided after the issue was patched, we're having to find an environment with an unpatched version of Chrome, predating the version of M111 with the fix for this issue. Given this challenge, we need a few more days before we reassessment can be completed to verify the POC and it's stated impact on production versions of Chrome. 

### du...@gmail.com (2023-04-12)

[Comment Deleted]

### du...@gmail.com (2023-04-26)

Hello, two weeks have passed, is there any news?

I think you can use the POC in https://crbug.com/chromium/1421773#c53 on your locally compiled Chromium to verify the UAF, and use the attachment in https://crbug.com/chromium/1421773#c40 to verify that the leak prompt could be popped up without the browser.patch in the production version of Google Chrome(It can be verified on the current version).

It is not necessary to find an environment with an unpatched version of Chrome, predating the version of M111 with the fix for this issue.

### am...@chromium.org (2023-04-26)

Thank you for checking in. All the analysis we are able to perform based on the POCs provided has already been completed. The VRP Panel only meets once per week, so we'll be discussing this issue later this week. Updates will be provided directly here after that has occurred. Thank you for your patience.  

### am...@chromium.org (2023-04-28)

After two people on the team attempted to reproduce this issue as described with various attempts using the POCs and attachments provided in the various comments above and also / including on a build of Chrome without the patch for this issue, we were not able reproduce this UAF as you've described without preconditions. As such, the VRP Panel has decided the reward amount is sufficient for this issue. Thanks again for your patience while we worked to fully reassess this issue. 

### du...@gmail.com (2023-04-28)

[Comment Deleted]

### du...@gmail.com (2023-04-28)

I used windbg to debug the stable version of Chrome, and found that the api key used by default in the production version Chrome can call the passwordleakcheck api service, which is the reason why it can pop up the leak prompt. (pic1)

But this api service does not seem open to developers, so my api key cannot apply for this service(https://console.developers.google.com/apis/api/passwordsleakcheck-pa.googleapis.com/overview).

So you can directly use the stable api key for locally compiled Chromium tests:

set GOOGLE_API_KEY=AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw

After setting this, you don't need to patch the browser process code to verify the UAF on your locally compiled Chromium.

In summary, reproduce this UAF without preconditions:
1. Set environment variable: set GOOGLE_API_KEY=AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw
2. Use the POC in https://crbug.com/chromium/1421773#c53 on your locally compiled Chromium to verify the UAF, and the browser process patch code in poc.diff is unnecessary (the patch for leak_detection_check_impl.cc and leak_detection_check_impl.cc).

But it seems that if the request is too frequent there will be a 429 error (pic2). If the leak prompt did not pop up in the production version before, this is probably the reason.

### wf...@chromium.org (2023-04-28)

I tested this manually using 110.0.5481.78, I tried both official build at that release, and also asan build manually at that revision.

I was able to trigger the dialog and the credential leak prompt, and the save password as you describe, but I was unable to trigger any memory corruption, I tried many many combinations of dismissing the prompts in different order and/or waiting, and no UAF triggered.

### du...@gmail.com (2023-05-04)

Hello, wfh@. Do you mean that you can verify that the leak prompt can pop up without browser patch on the production version, but the use-after-free cannot be triggered on any version?

I test it using 110.0.5481.78, and I can trigger the use-after-free:
https://drive.google.com/file/d/12zTFBlCfcCrNg4ncxyAKfSmMV5wfIxwq/view

I use the POC provided in https://crbug.com/chromium/1421773#c53 and set the stable API key as an environment variable:
set GOOGLE_API_KEY=AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw

### du...@gmail.com (2023-05-06)

Correction: https://crbug.com/chromium/1421773#c64 uses the POC version based on https://crbug.com/chromium/1421773#c53 without the browser process code patch, you can access it in the attachment of https://crbug.com/chromium/1421773#c64.

### du...@gmail.com (2023-05-10)

Hi, any feedback? Can it be successfully reproduced according to https://crbug.com/chromium/1421773#c64, and is there any difference from the demonstration in the video?

### am...@chromium.org (2023-05-10)

Hello, the team has gone through great measures in an attempt to reproduce this issue already, unfortunately, we were not able to reproduce as described and have since ended repro efforts for this already resolved issue and not further assessments will be possible. 

### du...@gmail.com (2023-05-12)

Sorry to hear that. Such a weird reporting experience. Anyway, thanks for your patience in trying.

### [Deleted User] (2023-06-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1421773?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063412)*

# Security: HeapOverflow in PluralStringHandler::HandleGetPluralString 

| Field | Value |
|-------|-------|
| **Issue ID** | [40059988](https://issues.chromium.org/issues/40059988) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>WebUI |
| **Platforms** | ChromeOS |
| **Reporter** | ya...@gmail.com |
| **Assignee** | mi...@google.com |
| **Created** | 2022-06-17 |
| **Bounty** | $3,000.00 |

## Description

This issue is the same as https://crbug.com/chromium/1303613.The problem seems to be triggered by diagnostics in chromeos, I'm not sure either.


void PluralStringHandler::HandleGetPluralString(const base::ListValue* args) {
  AllowJavascript();
  CHECK_EQ(3U, args->GetListDeprecated().size());
  const std::string callback = args->GetListDeprecated()[0].GetString();
  const std::string name = args->GetListDeprecated()[1].GetString();
  const int count = args->GetListDeprecated()[2].GetInt();
  DCHECK(base::Contains(string_id_map_, name));
  const std::u16string localized_string =
      l10n_util::GetPluralStringFUTF16(string_id_map_.at(name), count);
  ResolveJavascriptCallback(base::Value(callback),
                            base::Value(localized_string));
}



PoC
chrome.send("getPluralString",["","",0]);

## Timeline

### [Deleted User] (2022-06-17)

[Empty comment from Monorail migration]

### xi...@chromium.org (2022-06-17)

Thanks for the report! +michaelcheco@ based on git blame. Could you check if the "DCHECK(base::Contains(string_id_map_, name));" can fail in some cases? If not, this is likely a non-security bug. Triage the same way as https://crbug.com/1303613.

Code link: https://source.chromium.org/chromium/chromium/src/+/main:ash/webui/common/backend/plural_string_handler.cc;l=32;drc=169c6cc102b39295a5bfe2f2a176b42b1c2fe2c4;bpv=0;bpt=0

[Monorail components: UI>Browser>WebUI]

### [Deleted User] (2022-06-17)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-18)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-01)

michaelcheco: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-07-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/296b64df351ec5e33d685c0b4f17fcb776c5e905

commit 296b64df351ec5e33d685c0b4f17fcb776c5e905
Author: Michael Checo <michaelcheco@google.com>
Date: Fri Jul 01 22:40:06 2022

Handle invalid GetPluralString calls

Bug: 1337132
Test: ash_webui_unittests --gtest_filter=*PluralStringHandlerTest*
Change-Id: I7bc86f869f1501ab6c3cf04abe2c3ab336b476f5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3741270
Commit-Queue: Michael Checo <michaelcheco@google.com>
Reviewed-by: Gavin Williams <gavinwill@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1020267}

[modify] https://crrev.com/296b64df351ec5e33d685c0b4f17fcb776c5e905/ash/webui/common/backend/plural_string_handler_unittest.cc
[modify] https://crrev.com/296b64df351ec5e33d685c0b4f17fcb776c5e905/ash/webui/common/backend/plural_string_handler.cc


### ya...@gmail.com (2022-07-03)

looks fixed, change status to fixed

### jo...@chromium.org (2022-07-08)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-09)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-09)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-08-04)

Congratulations! The VRP Panel has decided to award you $3000 for this report. The reward amount decided was based on this issue being mitigated by not being remote exploitable and by user interaction and needing access to/interaction with devtools. A member of our finance team will reach out to you soon to arrange payment. In the meantime, please let us know what name/handle/tag/other identifier you would like us to use for acknowledging you for this issue. 
Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-08-08)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-29)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-30)

[Empty comment from Monorail migration]

### gm...@google.com (2022-08-30)

[Empty comment from Monorail migration]

### rz...@google.com (2022-08-31)

[Empty comment from Monorail migration]

### rz...@google.com (2022-09-02)

[Empty comment from Monorail migration]

### rz...@google.com (2022-09-02)

gmpritchard,  here's the answer for the questionnaire, the bot isn't adding it to this bug:

1. Just https://crrev.com/c/3865517
2. Low, no conflicts
3. 105
4. Yes

### gm...@google.com (2022-09-06)

[Empty comment from Monorail migration]

### gm...@google.com (2022-09-12)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-09-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ff56af5bd0ef21b522507b2b6822cc7cb3ab8e42

commit ff56af5bd0ef21b522507b2b6822cc7cb3ab8e42
Author: Michael Checo <michaelcheco@google.com>
Date: Tue Sep 13 12:10:49 2022

[M102-LTS] Handle invalid GetPluralString calls

M102 merge issues:
  ash/webui/common/backend/plural_string_handler.cc:
    Conflicting ways of checking args

(cherry picked from commit 296b64df351ec5e33d685c0b4f17fcb776c5e905)

Bug: 1337132
Test: ash_webui_unittests --gtest_filter=*PluralStringHandlerTest*
Change-Id: I7bc86f869f1501ab6c3cf04abe2c3ab336b476f5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3741270
Commit-Queue: Michael Checo <michaelcheco@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#1020267}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3865517
Reviewed-by: Oleh Lamzin <lamzin@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Owners-Override: Oleh Lamzin <lamzin@google.com>
Cr-Commit-Position: refs/branch-heads/5005@{#1345}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/ff56af5bd0ef21b522507b2b6822cc7cb3ab8e42/ash/webui/common/backend/plural_string_handler_unittest.cc
[modify] https://crrev.com/ff56af5bd0ef21b522507b2b6822cc7cb3ab8e42/ash/webui/common/backend/plural_string_handler.cc


### rz...@google.com (2022-09-13)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1337132?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059988)*

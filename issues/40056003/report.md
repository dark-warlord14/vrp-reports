# Security: HeapOverflow in FillPhoneCountryCode

| Field | Value |
|-------|-------|
| **Issue ID** | [40056003](https://issues.chromium.org/issues/40056003) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Autofill |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, iOS, ChromeOS |
| **Reporter** | le...@gmail.com |
| **Assignee** | ma...@chromium.org |
| **Created** | 2021-05-26 |
| **Bounty** | $15,000.00 |

## Description

**VULNERABILITY DETAILS**  

In function FillPhoneCountryCodeSelectControl[1], the size of field->option\_contents could mismatch with the size of field->option\_values. If the size of option\_contents is larger than the size of option\_values, the HeapOverflow will be trigger when field->option\_values[i] gets accessed.

[1]. <https://source.chromium.org/chromium/chromium/src/+/main:components/autofill/core/browser/field_filler.cc;l=795;drc=1156b5f891de178171e71b9221a96bef1ced3d3b>

**VERSION**  

Chrome Version: stable but need a flag  

Operating System: All

**REPRODUCTION CASE**

1. Apply the attached patch.diff to enable "kAutofillEnableAugmentedPhoneCountryCode" flag and emulates a compromised renderer.
2. $ python -m SimpleHTTPServer  
   
   $ out/asan/chrome --user-data-dir=/tmp/xxxx "<http://localhost:8000/poc.html>"

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see asan file

**CREDIT INFORMATION**  

Reporter credit: Leecraso and Guang Gong of 360 Alpha Lab

## Attachments

- [asan](attachments/asan) (text/plain, 17.0 KB)
- [patch.diff](attachments/patch.diff) (text/plain, 1.5 KB)
- [poc.html](attachments/poc.html) (text/plain, 1.2 KB)
- [trigger.html](attachments/trigger.html) (text/plain, 392 B)
- [uaf-asan](attachments/uaf-asan) (text/plain, 27.7 KB)

## Timeline

### [Deleted User] (2021-05-26)

[Empty comment from Monorail migration]

### ad...@google.com (2021-05-26)

Reproduced on Chrome revision 3d60439cfb36485e76a1c5bb7f513d3721b20da1, 870763, M91 branch point. Setting security impact stable, and security severity medium as an OOB read in the browser which can be triggered by a compromised renderer.

[Monorail components: UI>Browser>Autofill]

### ma...@chromium.org (2021-05-27)

[Empty comment from Monorail migration]

### ma...@chromium.org (2021-05-27)

[Empty comment from Monorail migration]

### ma...@chromium.org (2021-05-27)

[Empty comment from Monorail migration]

### ma...@chromium.org (2021-05-27)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-05-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/05303a33a5a31d74709ddaff9e54fed2fd0ebaa8

commit 05303a33a5a31d74709ddaff9e54fed2fd0ebaa8
Author: Mohamed Amir Yosef <mamir@chromium.org>
Date: Thu May 27 17:01:40 2021

[Autofill] Check the size of both contents and values in FormFieldData

Details are in the linked bug.

Bug: 1213313
Change-Id: I8e0a4d55ddd5c0c00ce350378fab0f282a36019f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2922343
Reviewed-by: Christoph Schwering <schwering@google.com>
Commit-Queue: Mohamed Amir Yosef <mamir@chromium.org>
Cr-Commit-Position: refs/heads/master@{#887197}

[modify] https://crrev.com/05303a33a5a31d74709ddaff9e54fed2fd0ebaa8/components/autofill/core/browser/field_filler.cc
[modify] https://crrev.com/05303a33a5a31d74709ddaff9e54fed2fd0ebaa8/components/autofill/core/browser/form_data_importer.cc


### [Deleted User] (2021-05-27)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-05-27)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### le...@gmail.com (2021-05-27)

Hi, thanks for the quick fix. But I think those should be marked as fixed, rather than be duplicated into one medium severity issue.

### sc...@google.com (2021-05-28)

Thanks for the report! I think the three are really the different instances of the same bug (wrong loop condition of the same two fields).

### le...@gmail.com (2021-05-28)

yes, it's the same pattern, but the call path is different. It seems that different CVEs will be assigned for these before:
https://chromium-review.googlesource.com/c/chromium/src/+/2440620
https://chromium-review.googlesource.com/c/chromium/src/+/2891080

And there seems to be a mistake in the patch:
https://chromium-review.googlesource.com/c/chromium/src/+/2922343/3/components/autofill/core/browser/form_data_importer.cc
```for (size_t i = 0; items_count; ++i) {``` should be ```for (size_t i = 0; i < items_count; ++i) {```

### gi...@appspot.gserviceaccount.com (2021-05-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b58aa12c8cefee013d0ab82be4b78eb053e7c439

commit b58aa12c8cefee013d0ab82be4b78eb053e7c439
Author: Mohamed Amir Yosef <mamir@chromium.org>
Date: Fri May 28 06:39:38 2021

Revert "[Autofill] Check the size of both contents and values in FormFieldData"

This reverts commit 05303a33a5a31d74709ddaff9e54fed2fd0ebaa8.

Reason for revert: Created a regression in form_data_importer.cc

Original change's description:
> [Autofill] Check the size of both contents and values in FormFieldData
>
> Details are in the linked bug.
>
> Bug: 1213313
> Change-Id: I8e0a4d55ddd5c0c00ce350378fab0f282a36019f
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2922343
> Reviewed-by: Christoph Schwering <schwering@google.com>
> Commit-Queue: Mohamed Amir Yosef <mamir@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#887197}

Bug: 1213313
Change-Id: Ia5bee585277ea7020cca982d05e10d91475defe9
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2922886
Auto-Submit: Mohamed Amir Yosef <mamir@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Mohamed Amir Yosef <mamir@chromium.org>
Cr-Commit-Position: refs/heads/master@{#887479}

[modify] https://crrev.com/b58aa12c8cefee013d0ab82be4b78eb053e7c439/components/autofill/core/browser/field_filler.cc
[modify] https://crrev.com/b58aa12c8cefee013d0ab82be4b78eb053e7c439/components/autofill/core/browser/form_data_importer.cc


### ma...@chromium.org (2021-05-28)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-05-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/624f194d9f2d988a7f8e450bc39f5f1120865312

commit 624f194d9f2d988a7f8e450bc39f5f1120865312
Author: Mohamed Amir Yosef <mamir@chromium.org>
Date: Fri May 28 12:02:23 2021

[Autofill] Check the size of both contents and values in FormFieldData

Details are in the linked bug.

Bug: 1213313
Change-Id: I9f018cd0d6a5820f9496a494dbb210445ae99f61
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2923844
Auto-Submit: Mohamed Amir Yosef <mamir@chromium.org>
Reviewed-by: Matthias Körber <koerber@google.com>
Commit-Queue: Christoph Schwering <schwering@google.com>
Cr-Commit-Position: refs/heads/master@{#887493}

[modify] https://crrev.com/624f194d9f2d988a7f8e450bc39f5f1120865312/components/autofill/core/browser/field_filler.cc
[modify] https://crrev.com/624f194d9f2d988a7f8e450bc39f5f1120865312/components/autofill/core/browser/form_data_importer.cc


### ma...@chromium.org (2021-05-31)

[Empty comment from Monorail migration]

### ma...@chromium.org (2021-05-31)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-31)

This bug requires manual review: Reverts referenced in bugdroid comments after merge request.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: govind@(Android), bindusuvarna@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@chromium.org (2021-05-31)

1- Yes, it's a security fix.
2- https://chromium-review.googlesource.com/c/chromium/src/+/2923844
3- Yes, landed on Canary already. (93.0.4526.0)
4- Yes, merging to M91 would make sense. It's a safe change and addresses a security issue.
5- It's a security fix.
6- No, not a new feature.
7- The fix is safe and is not *not* behind a feature flag.

### [Deleted User] (2021-05-31)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-31)

[Empty comment from Monorail migration]

### le...@gmail.com (2021-06-01)

Hi, is the final decision to duplicate these issues into this medium severity issue? Some of them could leak memory by reallocating the freed space without user interaction. I think it should be high severity at least.

### sr...@google.com (2021-06-02)

Merge approved for M92 branch:4515 please merge asap

### gi...@appspot.gserviceaccount.com (2021-06-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/be223652b6078b56540a6cb5db2d442674d0f073

commit be223652b6078b56540a6cb5db2d442674d0f073
Author: Mohamed Amir Yosef <mamir@chromium.org>
Date: Wed Jun 02 20:36:58 2021

[Autofill] Check the size of both contents and values in FormFieldData

Details are in the linked bug.

(cherry picked from commit 624f194d9f2d988a7f8e450bc39f5f1120865312)

Bug: 1213313
Change-Id: I9f018cd0d6a5820f9496a494dbb210445ae99f61
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2923844
Auto-Submit: Mohamed Amir Yosef <mamir@chromium.org>
Reviewed-by: Matthias Körber <koerber@google.com>
Commit-Queue: Christoph Schwering <schwering@google.com>
Cr-Original-Commit-Position: refs/heads/master@{#887493}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2933900
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Mohamed Amir Yosef <mamir@chromium.org>
Cr-Commit-Position: refs/branch-heads/4515@{#254}
Cr-Branched-From: 488fc70865ddaa05324ac00a54a6eb783b4bc41c-refs/heads/master@{#885287}

[modify] https://crrev.com/be223652b6078b56540a6cb5db2d442674d0f073/components/autofill/core/browser/field_filler.cc
[modify] https://crrev.com/be223652b6078b56540a6cb5db2d442674d0f073/components/autofill/core/browser/form_data_importer.cc


### ma...@chromium.org (2021-06-08)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-06-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d805a11b69ccfc6376a1a5e05bfe603a4481c3a5

commit d805a11b69ccfc6376a1a5e05bfe603a4481c3a5
Author: Christoph Schwering <schwering@google.com>
Date: Wed Jun 09 16:37:48 2021

[Autofill] Replaced pair of value/label vectors with vector of pairs.

Bug: 1213313
Change-Id: Iab2688936636676157bdcdd0b3db6f80f8a53cea
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2935277
Reviewed-by: Mohamed Amir Yosef <mamir@chromium.org>
Reviewed-by: Mike West <mkwst@chromium.org>
Reviewed-by: Michael Bai <michaelbai@chromium.org>
Commit-Queue: Christoph Schwering <schwering@google.com>
Cr-Commit-Position: refs/heads/master@{#890810}

[modify] https://crrev.com/d805a11b69ccfc6376a1a5e05bfe603a4481c3a5/chrome/renderer/autofill/form_autofill_browsertest.cc
[modify] https://crrev.com/d805a11b69ccfc6376a1a5e05bfe603a4481c3a5/components/android_autofill/browser/form_field_data_android.cc
[modify] https://crrev.com/d805a11b69ccfc6376a1a5e05bfe603a4481c3a5/components/autofill/content/renderer/autofill_agent.cc
[modify] https://crrev.com/d805a11b69ccfc6376a1a5e05bfe603a4481c3a5/components/autofill/content/renderer/form_autofill_util.cc
[modify] https://crrev.com/d805a11b69ccfc6376a1a5e05bfe603a4481c3a5/components/autofill/core/browser/autofill_test_utils.cc
[modify] https://crrev.com/d805a11b69ccfc6376a1a5e05bfe603a4481c3a5/components/autofill/core/browser/field_filler.cc
[modify] https://crrev.com/d805a11b69ccfc6376a1a5e05bfe603a4481c3a5/components/autofill/core/browser/field_filler_unittest.cc
[modify] https://crrev.com/d805a11b69ccfc6376a1a5e05bfe603a4481c3a5/components/autofill/core/browser/form_data_importer.cc
[modify] https://crrev.com/d805a11b69ccfc6376a1a5e05bfe603a4481c3a5/components/autofill/core/browser/form_data_importer_unittest.cc
[modify] https://crrev.com/d805a11b69ccfc6376a1a5e05bfe603a4481c3a5/components/autofill/core/browser/form_parsing/credit_card_field.cc
[modify] https://crrev.com/d805a11b69ccfc6376a1a5e05bfe603a4481c3a5/components/autofill/core/browser/form_parsing/credit_card_field_unittest.cc
[modify] https://crrev.com/d805a11b69ccfc6376a1a5e05bfe603a4481c3a5/components/autofill/core/browser/form_parsing/parsing_test_utils.cc
[modify] https://crrev.com/d805a11b69ccfc6376a1a5e05bfe603a4481c3a5/components/autofill/core/browser/form_parsing/parsing_test_utils.h
[modify] https://crrev.com/d805a11b69ccfc6376a1a5e05bfe603a4481c3a5/components/autofill/core/browser/form_parsing/phone_field.cc
[modify] https://crrev.com/d805a11b69ccfc6376a1a5e05bfe603a4481c3a5/components/autofill/core/browser/form_parsing/phone_field_unittest.cc
[modify] https://crrev.com/d805a11b69ccfc6376a1a5e05bfe603a4481c3a5/components/autofill/core/common/autofill_data_validation.cc
[modify] https://crrev.com/d805a11b69ccfc6376a1a5e05bfe603a4481c3a5/components/autofill/core/common/autofill_data_validation.h
[modify] https://crrev.com/d805a11b69ccfc6376a1a5e05bfe603a4481c3a5/components/autofill/core/common/form_data_unittest.cc
[modify] https://crrev.com/d805a11b69ccfc6376a1a5e05bfe603a4481c3a5/components/autofill/core/common/form_field_data.cc
[modify] https://crrev.com/d805a11b69ccfc6376a1a5e05bfe603a4481c3a5/components/autofill/core/common/form_field_data.h
[modify] https://crrev.com/d805a11b69ccfc6376a1a5e05bfe603a4481c3a5/components/autofill/core/common/form_field_data_unittest.cc
[modify] https://crrev.com/d805a11b69ccfc6376a1a5e05bfe603a4481c3a5/components/autofill/core/common/mojom/autofill_types.mojom
[modify] https://crrev.com/d805a11b69ccfc6376a1a5e05bfe603a4481c3a5/components/autofill/core/common/mojom/autofill_types_mojom_traits.cc
[modify] https://crrev.com/d805a11b69ccfc6376a1a5e05bfe603a4481c3a5/components/autofill/core/common/mojom/autofill_types_mojom_traits.h
[modify] https://crrev.com/d805a11b69ccfc6376a1a5e05bfe603a4481c3a5/components/autofill/ios/browser/autofill_util.mm
[modify] https://crrev.com/d805a11b69ccfc6376a1a5e05bfe603a4481c3a5/components/password_manager/core/browser/form_saver_impl.cc
[modify] https://crrev.com/d805a11b69ccfc6376a1a5e05bfe603a4481c3a5/components/password_manager/core/browser/password_manager_unittest.cc


### am...@google.com (2021-06-23)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-06-23)

Congratulations, Leecraso and Guang Gong! The VRP Panel has decided to award you $15,000 for this report. Nice work!  

### am...@google.com (2021-06-30)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-07-19)

[Empty comment from Monorail migration]

### am...@google.com (2021-07-19)

[Empty comment from Monorail migration]

### rz...@google.com (2021-07-29)

[Empty comment from Monorail migration]

### am...@google.com (2021-08-03)

[Empty comment from Monorail migration]

### gi...@google.com (2021-08-05)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-08-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/57b95ba2c39ae6a806cfe644ab0a5ac5ef30ac1b

commit 57b95ba2c39ae6a806cfe644ab0a5ac5ef30ac1b
Author: Mohamed Amir Yosef <mamir@chromium.org>
Date: Thu Aug 05 13:27:38 2021

[M90-LTS][Autofill] Check the size of both contents and values in FormFieldData

Details are in the linked bug.

(cherry picked from commit 624f194d9f2d988a7f8e450bc39f5f1120865312)

Bug: 1213313
Change-Id: I9f018cd0d6a5820f9496a494dbb210445ae99f61
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2923844
Auto-Submit: Mohamed Amir Yosef <mamir@chromium.org>
Commit-Queue: Christoph Schwering <schwering@google.com>
Cr-Original-Commit-Position: refs/heads/master@{#887493}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3056955
Reviewed-by: Jana Grill <janagrill@google.com>
Owners-Override: Jana Grill <janagrill@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1554}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/57b95ba2c39ae6a806cfe644ab0a5ac5ef30ac1b/components/autofill/core/browser/field_filler.cc
[modify] https://crrev.com/57b95ba2c39ae6a806cfe644ab0a5ac5ef30ac1b/components/autofill/core/browser/form_data_importer.cc


### rz...@google.com (2021-08-05)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-08-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/88c291f2388668bcf44d97d8259476cfc71f50ad

commit 88c291f2388668bcf44d97d8259476cfc71f50ad
Author: Christoph Schwering <schwering@google.com>
Date: Thu Aug 05 14:26:19 2021

[M90-LTS][Autofill] Replaced pair of value/label vectors with vector of pairs.

Since https://chromium-review.googlesource.com/c/chromium/src/+/2752287
isn't on M90, //comp/autofill is still using base::string16 instead of
std::u16string.

A few changes were made the original cl:
- changed all occurrences of std::u16string to base::string16
- keep using base::ASCIIToUTF16 where needed
- Added changes to //comp/autofill/core/browser/form_structure.cc
  and //comp/autofill/core/browser/form_structure_unittest.cc, not
  included in the original cl (build fixes).

(cherry picked from commit d805a11b69ccfc6376a1a5e05bfe603a4481c3a5)

Bug: 1213313
Change-Id: Iab2688936636676157bdcdd0b3db6f80f8a53cea
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2935277
Commit-Queue: Christoph Schwering <schwering@google.com>
Cr-Original-Commit-Position: refs/heads/master@{#890810}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3056956
Reviewed-by: Jana Grill <janagrill@google.com>
Owners-Override: Jana Grill <janagrill@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1559}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/88c291f2388668bcf44d97d8259476cfc71f50ad/chrome/renderer/autofill/form_autofill_browsertest.cc
[modify] https://crrev.com/88c291f2388668bcf44d97d8259476cfc71f50ad/components/autofill/android/provider/form_field_data_android.cc
[modify] https://crrev.com/88c291f2388668bcf44d97d8259476cfc71f50ad/components/autofill/content/renderer/autofill_agent.cc
[modify] https://crrev.com/88c291f2388668bcf44d97d8259476cfc71f50ad/components/autofill/content/renderer/form_autofill_util.cc
[modify] https://crrev.com/88c291f2388668bcf44d97d8259476cfc71f50ad/components/autofill/core/browser/autofill_test_utils.cc
[modify] https://crrev.com/88c291f2388668bcf44d97d8259476cfc71f50ad/components/autofill/core/browser/field_filler.cc
[modify] https://crrev.com/88c291f2388668bcf44d97d8259476cfc71f50ad/components/autofill/core/browser/field_filler_unittest.cc
[modify] https://crrev.com/88c291f2388668bcf44d97d8259476cfc71f50ad/components/autofill/core/browser/form_data_importer.cc
[modify] https://crrev.com/88c291f2388668bcf44d97d8259476cfc71f50ad/components/autofill/core/browser/form_data_importer_unittest.cc
[modify] https://crrev.com/88c291f2388668bcf44d97d8259476cfc71f50ad/components/autofill/core/browser/form_parsing/credit_card_field.cc
[modify] https://crrev.com/88c291f2388668bcf44d97d8259476cfc71f50ad/components/autofill/core/browser/form_parsing/credit_card_field_unittest.cc
[modify] https://crrev.com/88c291f2388668bcf44d97d8259476cfc71f50ad/components/autofill/core/browser/form_parsing/parsing_test_utils.cc
[modify] https://crrev.com/88c291f2388668bcf44d97d8259476cfc71f50ad/components/autofill/core/browser/form_parsing/parsing_test_utils.h
[modify] https://crrev.com/88c291f2388668bcf44d97d8259476cfc71f50ad/components/autofill/core/browser/form_parsing/phone_field.cc
[modify] https://crrev.com/88c291f2388668bcf44d97d8259476cfc71f50ad/components/autofill/core/browser/form_parsing/phone_field_unittest.cc
[modify] https://crrev.com/88c291f2388668bcf44d97d8259476cfc71f50ad/components/autofill/core/browser/form_structure.cc
[modify] https://crrev.com/88c291f2388668bcf44d97d8259476cfc71f50ad/components/autofill/core/browser/form_structure_unittest.cc
[modify] https://crrev.com/88c291f2388668bcf44d97d8259476cfc71f50ad/components/autofill/core/common/autofill_data_validation.cc
[modify] https://crrev.com/88c291f2388668bcf44d97d8259476cfc71f50ad/components/autofill/core/common/autofill_data_validation.h
[modify] https://crrev.com/88c291f2388668bcf44d97d8259476cfc71f50ad/components/autofill/core/common/form_data_unittest.cc
[modify] https://crrev.com/88c291f2388668bcf44d97d8259476cfc71f50ad/components/autofill/core/common/form_field_data.cc
[modify] https://crrev.com/88c291f2388668bcf44d97d8259476cfc71f50ad/components/autofill/core/common/form_field_data.h
[modify] https://crrev.com/88c291f2388668bcf44d97d8259476cfc71f50ad/components/autofill/core/common/form_field_data_unittest.cc
[modify] https://crrev.com/88c291f2388668bcf44d97d8259476cfc71f50ad/components/autofill/core/common/mojom/autofill_types.mojom
[modify] https://crrev.com/88c291f2388668bcf44d97d8259476cfc71f50ad/components/autofill/core/common/mojom/autofill_types_mojom_traits.cc
[modify] https://crrev.com/88c291f2388668bcf44d97d8259476cfc71f50ad/components/autofill/core/common/mojom/autofill_types_mojom_traits.h
[modify] https://crrev.com/88c291f2388668bcf44d97d8259476cfc71f50ad/components/autofill/ios/browser/autofill_util.mm
[modify] https://crrev.com/88c291f2388668bcf44d97d8259476cfc71f50ad/components/password_manager/core/browser/form_saver_impl.cc
[modify] https://crrev.com/88c291f2388668bcf44d97d8259476cfc71f50ad/components/password_manager/core/browser/password_manager_unittest.cc


### [Deleted User] (2021-09-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-10-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1672129b7790b651a2b7b90d7a66ae9be50d9208

commit 1672129b7790b651a2b7b90d7a66ae9be50d9208
Author: Christoph Schwering <schwering@google.com>
Date: Fri Oct 20 09:32:16 2023

[Autofill] Merge FormFieldData::datalist_{values,labels}

This CL merges the two vectors FormFieldData::datalist_{values,labels}
into one FormFieldData::datalist_options, analogous to the
existing FormFieldData::options that had been merged earlier.

Bug: 1213313
Change-Id: I58b6a89f99e4df9eb80eb85b8f617f3928927b44
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4935534
Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
Reviewed-by: Dominic Battre <battre@chromium.org>
Reviewed-by: Mohamed Amir Yosef <mamir@chromium.org>
Reviewed-by: Mike Dougherty <michaeldo@chromium.org>
Commit-Queue: Christoph Schwering <schwering@google.com>
Reviewed-by: Olivier Robin <olivierrobin@chromium.org>
Reviewed-by: Nate Fischer <ntfschr@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1212643}

[modify] https://crrev.com/1672129b7790b651a2b7b90d7a66ae9be50d9208/components/autofill/content/renderer/form_autofill_util.h
[modify] https://crrev.com/1672129b7790b651a2b7b90d7a66ae9be50d9208/components/autofill/core/common/mojom/autofill_types.mojom
[modify] https://crrev.com/1672129b7790b651a2b7b90d7a66ae9be50d9208/components/android_autofill/browser/autofill_provider_android.cc
[modify] https://crrev.com/1672129b7790b651a2b7b90d7a66ae9be50d9208/chrome/browser/ui/autofill/chrome_autofill_client.cc
[modify] https://crrev.com/1672129b7790b651a2b7b90d7a66ae9be50d9208/chrome/browser/ui/autofill/autofill_popup_controller_impl_mac.h
[modify] https://crrev.com/1672129b7790b651a2b7b90d7a66ae9be50d9208/ios/web_view/internal/autofill/web_view_autofill_client_ios.mm
[modify] https://crrev.com/1672129b7790b651a2b7b90d7a66ae9be50d9208/components/autofill/content/renderer/autofill_agent.cc
[modify] https://crrev.com/1672129b7790b651a2b7b90d7a66ae9be50d9208/components/autofill/core/browser/autofill_external_delegate_unittest.cc
[modify] https://crrev.com/1672129b7790b651a2b7b90d7a66ae9be50d9208/components/android_autofill/browser/autofill_provider_android_unittest.cc
[modify] https://crrev.com/1672129b7790b651a2b7b90d7a66ae9be50d9208/chrome/browser/ui/autofill/autofill_popup_controller_impl.h
[modify] https://crrev.com/1672129b7790b651a2b7b90d7a66ae9be50d9208/ios/web_view/internal/autofill/web_view_autofill_client_ios.h
[modify] https://crrev.com/1672129b7790b651a2b7b90d7a66ae9be50d9208/android_webview/browser/aw_autofill_client.h
[modify] https://crrev.com/1672129b7790b651a2b7b90d7a66ae9be50d9208/chrome/browser/ui/autofill/autofill_popup_controller_interactive_uitest.cc
[modify] https://crrev.com/1672129b7790b651a2b7b90d7a66ae9be50d9208/components/autofill/core/browser/autofill_client.h
[modify] https://crrev.com/1672129b7790b651a2b7b90d7a66ae9be50d9208/chrome/browser/ui/autofill/autofill_popup_controller_impl_mac.mm
[modify] https://crrev.com/1672129b7790b651a2b7b90d7a66ae9be50d9208/components/autofill/core/common/mojom/autofill_types_mojom_traits.h
[modify] https://crrev.com/1672129b7790b651a2b7b90d7a66ae9be50d9208/components/android_autofill/browser/autofill_provider_android_bridge_impl.cc
[modify] https://crrev.com/1672129b7790b651a2b7b90d7a66ae9be50d9208/components/android_autofill/browser/autofill_provider_android_bridge_impl.h
[modify] https://crrev.com/1672129b7790b651a2b7b90d7a66ae9be50d9208/components/autofill/core/browser/test_autofill_client.h
[modify] https://crrev.com/1672129b7790b651a2b7b90d7a66ae9be50d9208/components/autofill/core/browser/autofill_external_delegate.cc
[modify] https://crrev.com/1672129b7790b651a2b7b90d7a66ae9be50d9208/chrome/browser/ui/autofill/autofill_popup_controller_impl.cc
[modify] https://crrev.com/1672129b7790b651a2b7b90d7a66ae9be50d9208/components/autofill/content/renderer/form_autofill_util_browsertest.cc
[modify] https://crrev.com/1672129b7790b651a2b7b90d7a66ae9be50d9208/components/autofill/core/common/mojom/autofill_types_mojom_traits.cc
[modify] https://crrev.com/1672129b7790b651a2b7b90d7a66ae9be50d9208/components/android_autofill/browser/autofill_provider_android_bridge.h
[modify] https://crrev.com/1672129b7790b651a2b7b90d7a66ae9be50d9208/ios/chrome/browser/ui/autofill/chrome_autofill_client_ios.mm
[modify] https://crrev.com/1672129b7790b651a2b7b90d7a66ae9be50d9208/components/autofill/core/common/form_field_data.h
[modify] https://crrev.com/1672129b7790b651a2b7b90d7a66ae9be50d9208/components/password_manager/core/browser/password_manager_util_unittest.cc
[modify] https://crrev.com/1672129b7790b651a2b7b90d7a66ae9be50d9208/chrome/browser/ui/autofill/autofill_popup_controller_impl_unittest.cc
[modify] https://crrev.com/1672129b7790b651a2b7b90d7a66ae9be50d9208/ios/chrome/browser/ui/autofill/chrome_autofill_client_ios.h
[modify] https://crrev.com/1672129b7790b651a2b7b90d7a66ae9be50d9208/components/android_autofill/browser/form_field_data_android_bridge_impl.cc
[modify] https://crrev.com/1672129b7790b651a2b7b90d7a66ae9be50d9208/components/autofill/content/renderer/form_autofill_util.cc
[modify] https://crrev.com/1672129b7790b651a2b7b90d7a66ae9be50d9208/android_webview/browser/aw_autofill_client.cc
[modify] https://crrev.com/1672129b7790b651a2b7b90d7a66ae9be50d9208/chrome/browser/ui/autofill/chrome_autofill_client.h
[modify] https://crrev.com/1672129b7790b651a2b7b90d7a66ae9be50d9208/components/autofill/core/browser/autofill_external_delegate.h
[modify] https://crrev.com/1672129b7790b651a2b7b90d7a66ae9be50d9208/components/autofill/core/browser/browser_autofill_manager.cc
[modify] https://crrev.com/1672129b7790b651a2b7b90d7a66ae9be50d9208/components/autofill/core/browser/browser_autofill_manager.h
[modify] https://crrev.com/1672129b7790b651a2b7b90d7a66ae9be50d9208/components/autofill/core/common/autofill_test_utils.cc


### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1213313?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1211263, crbug.com/chromium/1211266, crbug.com/chromium/1213312]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056003)*

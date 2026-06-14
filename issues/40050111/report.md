# PDFium (XFA) Use-after-free in CXFA_FFCheckButton::OnProcessEvent

| Field | Value |
|-------|-------|
| **Issue ID** | [40050111](https://issues.chromium.org/issues/40050111) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | my...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2019-09-12 |
| **Bounty** | $6,000.00 |

## Description

Steps to reproduce the problem:
1. Compile the latest chromium with enabled XFA PDFium.
2. Open file test.pdf with chrome (PageHeap is enabled).
3. Click to any place in the first page then press "Tab" key and then press "Space" key to trigger (MUST press 
"Tab" key before "Space" key)

What is the expected behavior?

What went wrong?
CXFA_FFCheckButton object use-after-free in function CXFA_FFCheckButton::OnProcessEvent

Did this work before? N/A 

Chrome version: Lasted  Channel: n/a
OS Version: Windows 10 
Flash Version:

The bug is in function CXFA_FFCheckButton::OnProcessEvent() 

void CXFA_FFCheckButton::OnProcessEvent(CFWL_Event* pEvent) {
  CXFA_FFField::OnProcessEvent(pEvent);
  switch (pEvent->GetType()) {
    case CFWL_Event::Type::CheckStateChanged: {
      CXFA_EventParam eParam;
      eParam.m_eType = XFA_EVENT_Change;
      eParam.m_wsPrevText = m_pNode->GetValue(XFA_VALUEPICTURE_Raw);

      CXFA_Node* exclNode = m_pNode->GetExclGroupIfExists();
      if (ProcessCommittedData()) {
        eParam.m_pTarget = exclNode;
        if (exclNode) {
          m_pDocView->AddValidateNode(exclNode);
          m_pDocView->AddCalculateNode(exclNode);
          exclNode->ProcessEvent(GetDocView(), XFA_AttributeValue::Change,			// ==> can trigger JS function
                                 &eParam);
        }
        eParam.m_pTarget = m_pNode.Get();
        m_pNode->ProcessEvent(GetDocView(), XFA_AttributeValue::Change,				// ==> can trigger JS function
                              &eParam);
      } else {
        SetFWLCheckState(m_pNode->GetCheckState());
      }
      if (exclNode) {
        eParam.m_pTarget = exclNode;
        exclNode->ProcessEvent(GetDocView(), XFA_AttributeValue::Click,				// ==> can trigger JS function
                               &eParam);
      }
      eParam.m_pTarget = m_pNode.Get();
      m_pNode->ProcessEvent(GetDocView(), XFA_AttributeValue::Click, &eParam);		// ==> can trigger JS function
      break;
    }
    default:
      break;
  }
  m_pOldDelegate->OnProcessEvent(pEvent);
}

We can see that there are 4 calls to function ProcessEvent(). This function can trigger to JS code base on event parameter 
that passed to function. Read above code, we know that we can trigger 2 event JS handlers: change and click in this function.    
In proof-of-concept file, I use "click" event of a "checkButton" field to trigger the bug.
  
A XML template that in the poc is like below 

<exclGroup name="RadioButtonList">
    <field name="checkButton0">
        <ui>
            <checkButton size="100in"/>
        </ui>
        <caption>
            <value>
                <text>Check_0</text>
            </value>
        </caption>
        <items>
            <text>Check_0</text>
        </items>
    </field>
    <field y="20mm" name="checkButton1">
        <ui>
            <checkButton size="100in"/>
        </ui>
        <caption>
            <value>
                <text>Check_1</text>
            </value>
        </caption>
        <items>
            <text>Check_1</text>
        </items>
    </field>
    <event activity="click">
        <script contentType="application/x-javascript">
            a += 1;
            if (a == 2)
            {
                list1 = xfa.resolveNode("ChoiceList");
                xfa.host.setFocus(list1);
                xfa.template.remerge();    
                xfa.host.openList(list1);
            }
        </script>
    </event>
</exclGroup>

We setup a check box with 2 "checkButton" fields (name 'checkButton0' and 'checkButton1') inside an "exclGroup" and 
JS handler for "click" event of this "exclGroup". This JS code in 'click' event will be executed when function 
exclNode->ProcessEvent() is called and it'll free the object CXFA_FFCheckButton (|this| object). After JS event handler, 
it backs to function CXFA_FFCheckButton::OnProcessEvent(), the object |this| will be used again in instruction 
"eParam.m_pTarget = m_pNode.Get();" with accessing to field |m_pNode|


## Attachments

- [crash_log.txt](attachments/crash_log.txt) (text/plain, 19.7 KB)
- [test.pdf](attachments/test.pdf) (application/pdf, 6.7 KB)

## Timeline

### dt...@chromium.org (2019-09-13)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### dr...@chromium.org (2019-09-13)

Triaging to PDF owners

### hn...@chromium.org (2019-09-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-27)

thestig: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-10-12)

thestig: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### th...@chromium.org (2019-10-17)

XFA is not shipped.

### my...@gmail.com (2019-10-17)

Although XFA is not shipped, can you confirm that the bug existed? I already commit a patch for this. Let me know if you have any alternative solution.

### th...@chromium.org (2019-10-17)

I can certainly do that. Sorry for being slow on the XFA bugs.

### th...@chromium.org (2019-10-18)

Yes, I am confirming this bug exists, and you have a pending CL. It's in my queue mainly because I want to look into alternative solutions. Thank you for being patient and waiting for me.

### my...@gmail.com (2020-01-06)

Hi, I understand that @tsepez recently patched my previous UAF bugs with the same ObservedPtr technique. It've been so long, did you find any alternative solutions?

### my...@gmail.com (2020-01-07)

[Comment Deleted]

### my...@gmail.com (2020-01-14)

I believe this bug must be "Security_Severity-High". Also, It's 4 months already, can you do anything about this? @thestig @tsepez

### my...@gmail.com (2020-01-17)

Although, this bug is about FFCheckButton, my CL contains patches for several others such as FFComboBox.
@tsepez used the same technique in his patch: https://pdfium-review.googlesource.com/c/pdfium/+/64712
It makes my CL "Merge conflict": https://pdfium-review.googlesource.com/c/pdfium/+/60710
I understand that you want to find the most optimal solution but while you are looking at FFComboBox, can you look at my CL as well? 

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-02-12)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/0844b9a3b6259ff2af9e77425aa4bd3dcf71d861

commit 0844b9a3b6259ff2af9e77425aa4bd3dcf71d861
Author: Lei Zhang <thestig@chromium.org>
Date: Wed Feb 12 18:10:05 2020

Prevent destruction of CXFA_FFWidget across FWL events.

The current strategy of using ObservedPtr lets the destruction happen,
and then dealing with the destruction. Instead, use RetainPtr on the
CXFA_ContentLayoutItem that owns CXFA_FFWidget to prevent destruction
altogether for the duration of the events.

Bug: chromium:1003501,chromium:1039629
Change-Id: I5d185c752b93904fafb060e13fc18bb5e3ddee52
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/66370
Reviewed-by: Tom Sepez <tsepez@chromium.org>
Commit-Queue: Lei Zhang <thestig@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/0844b9a3b6259ff2af9e77425aa4bd3dcf71d861/xfa/fxfa/cxfa_fflistbox.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/0844b9a3b6259ff2af9e77425aa4bd3dcf71d861/xfa/fxfa/cxfa_ffcheckbutton.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/0844b9a3b6259ff2af9e77425aa4bd3dcf71d861/xfa/fxfa/cxfa_ffnumericedit.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/0844b9a3b6259ff2af9e77425aa4bd3dcf71d861/xfa/fxfa/cxfa_fftextedit.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/0844b9a3b6259ff2af9e77425aa4bd3dcf71d861/xfa/fxfa/cxfa_ffdatetimeedit.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/0844b9a3b6259ff2af9e77425aa4bd3dcf71d861/xfa/fxfa/cxfa_ffcombobox.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/0844b9a3b6259ff2af9e77425aa4bd3dcf71d861/xfa/fxfa/cxfa_ffpushbutton.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/0844b9a3b6259ff2af9e77425aa4bd3dcf71d861/xfa/fxfa/cxfa_ffimageedit.cpp


### th...@chromium.org (2020-02-12)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-02-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/7a72613982f3986ec2bd484b61094d2c5426ceb0

commit 7a72613982f3986ec2bd484b61094d2c5426ceb0
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Feb 12 21:12:10 2020

Roll src/third_party/pdfium d9bd62fafb66..0844b9a3b625 (3 commits)

https://pdfium.googlesource.com/pdfium.git/+log/d9bd62fafb66..0844b9a3b625

git log d9bd62fafb66..0844b9a3b625 --date=short --first-parent --format='%ad %ae %s'
2020-02-12 thestig@chromium.org Prevent destruction of CXFA_FFWidget across FWL events.
2020-02-12 tsepez@chromium.org Add test case for PDF password annotations
2020-02-12 aadhir@microsoft.com Sending focused annotation update to the host

Created with:
  gclient setdep -r src/third_party/pdfium@0844b9a3b625

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/pdfium-autoroll
Please CC pdfium-deps-rolls@chromium.org on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

Bug: chromium:1003501,chromium:1039629,chromium:989027
Tbr: pdfium-deps-rolls@chromium.org
Change-Id: I769609126ada35d6238d4f6d756ea4b5a126c5ce
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2052095
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#740821}

[modify] https://crrev.com/7a72613982f3986ec2bd484b61094d2c5426ceb0/DEPS


### [Deleted User] (2020-02-15)

[Empty comment from Monorail migration]

### na...@google.com (2020-02-18)

[Empty comment from Monorail migration]

### na...@google.com (2020-02-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-02-20)

Congrats! The Panel decided to award $5,000 for this report and a $1,000 patch bonus. Nice work! 

### na...@google.com (2020-02-20)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-05-20)

This issue was migrated from crbug.com/chromium/1003501?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050111)*

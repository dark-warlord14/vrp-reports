# Security: PDFium OOB Access in CXFA_ViewLayoutProcessor::GetNextAvailContentHeight

| Field | Value |
|-------|-------|
| **Issue ID** | [40060649](https://issues.chromium.org/issues/40060649) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | 0x...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2022-08-23 |
| **Bounty** | $7,000.00 |

## Description

**VULNERABILITY DETAILS**

Pdfium version: <https://pdfium.googlesource.com/pdfium/+/5337c83fbb82c66079a412d83df775443f25ed79>  

Compile options: XFA enabled, V8 enabled, ASAN disabled

This issue only reproduces when ASAN was not enabled. Both x86 and x64 reproduces.

The attached poc.pdf can crash pdfium\_test.exe. According to the disassembly code, this can lead to type confusion issues.

Repro steps:  

Enable page heap option for pdfium\_test.exe and open poc.pdf with it.

**-------------------------** ---  

(730.2c54): Access violation - code c0000005 (!!! second chance !!!)  

eax=000222e8 ebx=001cd848 ecx=10de2158 edx=10de2350 esi=001cd83b edi=001cd858  

eip=01624e3e esp=001ccb60 ebp=001ccd08 iopl=0 nv up ei pl nz na pe nc  

cs=0023 ss=002b ds=002b es=002b fs=0053 gs=002b efl=00010206  

pdfium\_test!cppgc::internal::RawPointer::Load [inlined in pdfium\_test!CXFA\_ViewLayoutProcessor::GetNextAvailContentHeight+0x6e]:  

01624e3e 8b08 mov ecx,dword ptr [eax] ds:002b:000222e8=????????

0:000> k

# ChildEBP RetAddr

00 (Inline) -------- pdfium\_test!cppgc::internal::RawPointer::Load [pdfium\v8\include\cppgc\internal\member-storage.h @ 163]  

01 (Inline) -------- pdfium\_test!cppgc::internal::MemberBase::GetRaw [pdfium\v8\include\cppgc\member.h @ 54]  

02 (Inline) -------- pdfium\_test!cppgc::internal::BasicMember<CXFA\_ViewLayoutItem,cppgc::internal::StrongMemberTag,cppgc::internal::DijkstraWriteBarrierPolicy,cppgc::internal::DisabledCheckingPolicy>::Get [pdfium\v8\include\cppgc\member.h @ 264]  

03 (Inline) -------- pdfium\_test!cppgc::internal::BasicMember<CXFA\_ViewLayoutItem,cppgc::internal::StrongMemberTag,cppgc::internal::DijkstraWriteBarrierPolicy,cppgc::internal::DisabledCheckingPolicy>::operator-> [pdfium\v8\include\cppgc\member.h @ 252]  

04 001ccd08 01610837 pdfium\_test!CXFA\_ViewLayoutProcessor::GetNextAvailContentHeight+0x6e [pdfium\xfa\fxfa\layout\cxfa\_viewlayoutprocessor.cpp @ 1526]  

05 001cd04c 0160d8a3 pdfium\_test!CXFA\_ContentLayoutProcessor::InsertFlowedItem+0x1677 [pdfium\xfa\fxfa\layout\cxfa\_contentlayoutprocessor.cpp @ 2604]  

06 001cd994 016070c5 pdfium\_test!CXFA\_ContentLayoutProcessor::DoLayoutFlowedContainer+0x2c03 [pdfium\xfa\fxfa\layout\cxfa\_contentlayoutprocessor.cpp @ 1834]  

07 001cd9dc 0160f6ca pdfium\_test!CXFA\_ContentLayoutProcessor::DoLayoutInternal+0x1f5 [pdfium\xfa\fxfa\layout\cxfa\_contentlayoutprocessor.cpp @ 2108]  

08 001cdd20 0160d8a3 pdfium\_test!CXFA\_ContentLayoutProcessor::InsertFlowedItem+0x50a [pdfium\xfa\fxfa\layout\cxfa\_contentlayoutprocessor.cpp @ 2399]  

09 001ce668 016070c5 pdfium\_test!CXFA\_ContentLayoutProcessor::DoLayoutFlowedContainer+0x2c03 [pdfium\xfa\fxfa\layout\cxfa\_contentlayoutprocessor.cpp @ 1834]  

0a 001ce6b0 0160f6ca pdfium\_test!CXFA\_ContentLayoutProcessor::DoLayoutInternal+0x1f5 [pdfium\xfa\fxfa\layout\cxfa\_contentlayoutprocessor.cpp @ 2108]  

0b 001ce9f4 0160d8a3 pdfium\_test!CXFA\_ContentLayoutProcessor::InsertFlowedItem+0x50a [pdfium\xfa\fxfa\layout\cxfa\_contentlayoutprocessor.cpp @ 2399]  

0c 001cf33c 016070c5 pdfium\_test!CXFA\_ContentLayoutProcessor::DoLayoutFlowedContainer+0x2c03 [pdfium\xfa\fxfa\layout\cxfa\_contentlayoutprocessor.cpp @ 1834]  

0d 001cf384 016046fe pdfium\_test!CXFA\_ContentLayoutProcessor::DoLayoutInternal+0x1f5 [pdfium\xfa\fxfa\layout\cxfa\_contentlayoutprocessor.cpp @ 2108]  

0e 001cf3a4 01617ed8 pdfium\_test!CXFA\_ContentLayoutProcessor::DoLayout+0x4e [pdfium\xfa\fxfa\layout\cxfa\_contentlayoutprocessor.cpp @ 2087]  

0f 001cf46c 014f3a62 pdfium\_test!CXFA\_LayoutProcessor::DoLayout+0x1a8 [pdfium\xfa\fxfa\layout\cxfa\_layoutprocessor.cpp @ 92]  

10 001cf484 016d7d8e pdfium\_test!CXFA\_FFDocView::DoLayout+0x22 [pdfium\xfa\fxfa\cxfa\_ffdocview.cpp @ 119]  

11 001cf52c 00e11bca pdfium\_test!CPDFXFA\_Context::LoadXFADoc+0x3de [pdfium\fpdfsdk\fpdfxfa\cpdfxfa\_context.cpp @ 190]  

12 001cf544 00d647a1 pdfium\_test!FPDF\_LoadXFA+0x5a [pdfium\fpdfsdk\fpdf\_view.cpp @ 269]  

13 001cf710 00d6198c pdfium\_test!`anonymous namespace'::ProcessPdf+0x781 [pdfium\samples\pdfium\_test.cc @ 1015]  

14 001cf918 0175920d pdfium\_test!main+0x98c [pdfium\samples\pdfium\_test.cc @ 1319]  

15 001cf938 01759377 pdfium\_test!invoke\_main+0x2d [D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl @ 107]  

16 001cf994 0175944d pdfium\_test!\_\_scrt\_common\_main\_seh+0x157 [D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl @ 288]  

17 001cf99c 01759458 pdfium\_test!\_\_scrt\_common\_main+0xd [D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl @ 331]  

18 001cf9a4 75fffa29 pdfium\_test!WinMainCRTStartup+0x8 [D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe\_winmain.cpp @ 17]  

19 001cf9b4 772f7a9e KERNEL32!BaseThreadInitThunk+0x19  

1a 001cfa10 772f7a6e ntdll!\_\_RtlUserThreadStart+0x2f  

1b 001cfa20 00000000 ntdll!\_RtlUserThreadStart+0x1b

0:000> ub eip La  

pdfium\_test!CXFA\_ViewLayoutProcessor::GetNextAvailContentHeight+0x36 [pdfium\xfa\fxfa\layout\cxfa\_viewlayoutprocessor.cpp @ 1526]:  

01624e06 e8e57fffff call pdfium\_test!CXFA\_ViewLayoutProcessor::GetCurrentViewRecord (0161cdf0)  

01624e0b 83c008 add eax,8  

01624e0e 8985dcfeffff mov dword ptr [ebp-124h],eax  

01624e14 8b85dcfeffff mov eax,dword ptr [ebp-124h]  

01624e1a 8985e0feffff mov dword ptr [ebp-120h],eax  

01624e20 8b85e0feffff mov eax,dword ptr [ebp-120h]  

01624e26 898500ffffff mov dword ptr [ebp-100h],eax  

01624e2c 8b8500ffffff mov eax,dword ptr [ebp-100h]  

01624e32 898504ffffff mov dword ptr [ebp-0FCh],eax  

01624e38 8b8504ffffff mov eax,dword ptr [ebp-0FCh]

0:000> u eip  

pdfium\_test!cppgc::internal::RawPointer::Load [pdfium\xfa\fxfa\layout\cxfa\_viewlayoutprocessor.cpp @ 1526] [inlined in pdfium\_test!CXFA\_ViewLayoutProcessor::GetNextAvailContentHeight+0x6e [pdfium\xfa\fxfa\layout\cxfa\_viewlayoutprocessor.cpp @ 1526]]:  

01624e3e 8b08 mov ecx,dword ptr [eax]  

01624e40 e89b56e2ff call pdfium\_test!CXFA\_LayoutItem::GetFormNode (0144a4e0)  

01624e45 8985c4feffff mov dword ptr [ebp-13Ch],eax  

01624e4b 83bdc4feffff00 cmp dword ptr [ebp-13Ch],0  

01624e52 0f850c000000 jne pdfium\_test!CXFA\_ViewLayoutProcessor::GetNextAvailContentHeight+0x94 (01624e64)  

01624e58 c685cffeffff00 mov byte ptr [ebp-131h],0  

01624e5f e93d080000 jmp pdfium\_test!CXFA\_ViewLayoutProcessor::GetNextAvailContentHeight+0x8d1 (016256a1)  

01624e64 8b8dc4feffff mov ecx,dword ptr [ebp-13Ch]

0:000> ?eax-8  

Evaluate expression: 140000 = 000222e0

0:000> dx Debugger.Sessions[0].Processes[1840].Threads[11348].Stack.Frames[4].SwitchTo();dv /t /v  

Debugger.Sessions[0].Processes[1840].Threads[11348].Stack.Frames[4].SwitchTo()  

001ccbd0 class CXFA\_ViewLayoutProcessor \* this = 0x10de213c  

001ccd10 float fChildHeight = 16.83496094  

001ccbcc class CXFA\_Node \* pCurContentNode = 0xffffffff  

001ccbc4 class CXFA\_Node \* pPageNode = 0x10f387ec  

001ccbc0 class CXFA\_Node \* pOccurNode = 0x06c76fe8  

001ccbbc int iMax = 0n21351738  

001cccf4 class absl::optional<int> ret = class absl::optional<int>  

001ccba0 class CXFA\_Node \* pContentArea = 0x00d668a5  

001ccb9c float fNextContentHeight = 2.644451989e-039

0:000> dv  

this = 0x10de213c  

fChildHeight = 16.83496094  

pCurContentNode = 0xffffffff  

pPageNode = 0x10f387ec  

pOccurNode = 0x06c76fe8  

iMax = 0n21351738  

ret = class absl::optional<int>  

pContentArea = 0x00d668a5  

fNextContentHeight = 2.644451989e-039  

0:000> dx -r1 ((pdfium\_test!CXFA\_ViewLayoutProcessor \*)0x10de213c)  

((pdfium\_test!CXFA\_ViewLayoutProcessor \*)0x10de213c) : 0x10de213c [Type: CXFA\_ViewLayoutProcessor \*]  

[+0x000] prefinalizer\_dummy\_ [Type: cppgc::internal::PrefinalizerRegistration]  

[+0x004] m\_pHeap [Type: fxcrt::UnownedPtr[cppgc::Heap](javascript:void(0);)]  

[+0x008] m\_pLayoutProcessor [Type: cppgc::internal::BasicMember<CXFA\_LayoutProcessor,cppgc::internal::StrongMemberTag,cppgc::internal::DijkstraWriteBarrierPolicy,cppgc::internal::DisabledCheckingPolicy>]  

[+0x00c] m\_pPageSetNode [Type: cppgc::internal::BasicMember<CXFA\_Node,cppgc::internal::StrongMemberTag,cppgc::internal::DijkstraWriteBarrierPolicy,cppgc::internal::DisabledCheckingPolicy>]  

[+0x010] m\_pCurPageArea [Type: cppgc::internal::BasicMember<CXFA\_Node,cppgc::internal::StrongMemberTag,cppgc::internal::DijkstraWriteBarrierPolicy,cppgc::internal::DisabledCheckingPolicy>]  

[+0x014] m\_pPageSetRootLayoutItem [Type: cppgc::internal::BasicMember<CXFA\_ViewLayoutItem,cppgc::internal::StrongMemberTag,cppgc::internal::DijkstraWriteBarrierPolicy,cppgc::internal::DisabledCheckingPolicy>]  

[+0x018] m\_pPageSetCurLayoutItem [Type: cppgc::internal::BasicMember<CXFA\_ViewLayoutItem,cppgc::internal::StrongMemberTag,cppgc::internal::DijkstraWriteBarrierPolicy,cppgc::internal::DisabledCheckingPolicy>]  

[+0x01c] m\_ProposedViewRecords : { size=0x222e0 } [Type: std::Cr::list<cppgc::internal::BasicMember<CXFA\_ViewLayoutProcessor::CXFA\_ViewRecord,cppgc::internal::StrongMemberTag,cppgc::internal::DijkstraWriteBarrierPolicy,cppgc::internal::DisabledCheckingPolicy>,std::Cr::allocator<cppgc::internal::BasicMember<CXFA\_ViewLayoutProcessor::CXFA\_ViewRecord,cppgc::internal::StrongMemberTag,cppgc::internal::DijkstraWriteBarrierPolicy,cppgc::internal::DisabledCheckingPolicy> > >]  

[+0x028] m\_CurrentViewRecordIter [Type: std::Cr::\_\_list\_iterator<cppgc::internal::BasicMember<CXFA\_ViewLayoutProcessor::CXFA\_ViewRecord,cppgc::internal::StrongMemberTag,cppgc::internal::DijkstraWriteBarrierPolicy,cppgc::internal::DisabledCheckingPolicy>,void \*>]  

[+0x02c] m\_nAvailPages : 140000 [Type: int]  

[+0x030] m\_nCurPageCount : 0 [Type: int]  

[+0x034] m\_ePageSetMode : OrderedOccurrence (0x64) [Type: XFA\_AttributeValue]  

[+0x036] m\_bCreateOverFlowPage : false [Type: bool]  

[+0x038] m\_pPageSetMap : { size=0x1 } [Type: std::Cr::map<CXFA\_Node \*,int,std::Cr::less<CXFA\_Node \*>,std::Cr::allocator<std::Cr::pair<CXFA\_Node \*const,int> > >]  

[+0x044] m\_PageArray : { size=140000 } [Type: std::Cr::vector<cppgc::internal::BasicMember<CXFA\_ViewLayoutItem,cppgc::internal::StrongMemberTag,cppgc::internal::DijkstraWriteBarrierPolicy,cppgc::internal::DisabledCheckingPolicy>,std::Cr::allocator<cppgc::internal::BasicMember<CXFA\_ViewLayoutItem,cppgc::internal::StrongMemberTag,cppgc::internal::DijkstraWriteBarrierPolicy,cppgc::internal::DisabledCheckingPolicy> > >]

**VERSION**  

**Chrome Version: [x.x.x.x] + [stable, beta, or dev]**  

**Operating System: [Please indicate OS, version, and service pack level]**

**REPRODUCTION CASE**  

**Please include a demonstration of the security bug, such as an attached**  

**HTML or binary file that reproduces the bug when loaded in Chrome. PLEASE**  

**make the file as small as possible and remove any content not required to**  

**demonstrate the bug, or any personal or confidential information.**

**Please attach files directly, not in zip or other archive formats, and if**  

**you've created a demonstration site please also attach the files needed to**  

**reproduce the demonstration locally.**

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

**Type of crash: [tab, browser, etc.]**  

**Crash State: [see link above: stack trace \*with symbols\*, registers,**  

**exception record]**  

**Client ID (if relevant): [see link above]**

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

**Reporter credit: [goes here]**

## Attachments

- [poc.pdf](attachments/poc.pdf) (application/pdf, 59.4 KB)

## Timeline

### [Deleted User] (2022-08-23)

[Empty comment from Monorail migration]

### 0x...@gmail.com (2022-08-23)

Simple analysis maybe useful for you:

1. This case was found by fuzzing. After minimizing the proof-of-concept file, there's only one mutated place: The value of `min` property of the `occur`` element was changed form 1 to 69999 at line 151.

```
      <pageSet>
         <pageArea name="mpgPage1" id="Page1">
            <contentArea x="9mm" y="26mm" w="197mm" h="271mm" name="areaPage1" id="areaPage1_ID"/>
            <medium stock="a4" short="210mm" long="297mm"/>
            <occur min="69999" max="1"/>
            <draw w="75.1mm" h="15mm" x="126mm" y="7mm">
               <value>
               </value>
```

2. The process crashed in `CXFA_ViewLayoutProcessor::GetNextAvailContentHeight`.

```
bool CXFA_ViewLayoutProcessor::GetNextAvailContentHeight(float fChildHeight) {
  CXFA_Node* pCurContentNode =
      GetCurrentViewRecord()->pCurContentArea->GetFormNode();
  if (!pCurContentNode)
    return false;
```

3. `GetCurrentViewRecord ()` returned 140000 = 0x222e0. OOB Access occurred here and type confusion maybe triggered when calling `CXFA_LayoutItem::GetFormNode`.

```
01624e06 e8e57fffff      call    pdfium_test!CXFA_ViewLayoutProcessor::GetCurrentViewRecord (0161cdf0)
01624e0b 83c008          add     eax,8
01624e0e 8985dcfeffff    mov     dword ptr [ebp-124h],eax
01624e14 8b85dcfeffff    mov     eax,dword ptr [ebp-124h]
01624e1a 8985e0feffff    mov     dword ptr [ebp-120h],eax
01624e20 8b85e0feffff    mov     eax,dword ptr [ebp-120h]
01624e26 898500ffffff    mov     dword ptr [ebp-100h],eax
01624e2c 8b8500ffffff    mov     eax,dword ptr [ebp-100h]
01624e32 898504ffffff    mov     dword ptr [ebp-0FCh],eax
01624e38 8b8504ffffff    mov     eax,dword ptr [ebp-0FCh]
01624e3e 8b08            mov     ecx,dword ptr [eax]    ; -------------------> Crash!!!
01624e40 e89b56e2ff      call    pdfium_test!CXFA_LayoutItem::GetFormNode (0144a4e0)
```

4. There is a member called `m_PageArray` for `CXFA_ViewLayoutProcessor`. The size of it was 140000 when crashed. And that's the same as what `GetCurrentViewRecord()` returned.

```
[+0x044] m_PageArray      : { size=140000 }
```

### th...@chromium.org (2022-08-23)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### es...@chromium.org (2022-08-23)

tsepez, could you help triage please? Thanks!

### th...@chromium.org (2022-08-24)

FWIW, ASAN reports "SEGV on unknown address" for me.

### th...@chromium.org (2022-08-24)

[Empty comment from Monorail migration]

### th...@chromium.org (2022-08-24)

CXFA_ViewLayoutProcessor::GetNextAvailContentHeight() probably just needs a !HasCurrentViewRecord() check at the top.

### ts...@chromium.org (2022-08-25)

seting min="nnnn" gives control over the faulting address. yikes.

### ts...@chromium.org (2022-08-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-25)

[Empty comment from Monorail migration]

### ts...@chromium.org (2022-08-25)

Adding the proposed fix seems to result in a hang -- or at  least a long time processing the form.

### ts...@chromium.org (2022-08-25)

Dropping the min to, say, 99, still triggers the crash but allows the rendering to finish following application of the patch.

### gi...@appspot.gserviceaccount.com (2022-08-25)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/0d76a139d7ffbbdfb0ef5f5e714597a25f9767c4

commit 0d76a139d7ffbbdfb0ef5f5e714597a25f9767c4
Author: Tom Sepez <tsepez@chromium.org>
Date: Thu Aug 25 22:20:45 2022

Avoid de-referencing end() in GetNextAvailContentHeight().

Add the same HasCurrentViewRecord() check as in other methods.

Bug: chromium:1355682
Change-Id: I466f386f037801daa82ead30239f34e025748748
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/96910
Reviewed-by: Lei Zhang <thestig@chromium.org>
Auto-Submit: Tom Sepez <tsepez@chromium.org>
Commit-Queue: Lei Zhang <thestig@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/0d76a139d7ffbbdfb0ef5f5e714597a25f9767c4/xfa/fxfa/layout/cxfa_viewlayoutprocessor.cpp


### ts...@chromium.org (2022-08-25)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-08-25)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/f28915d98ab049ff928106c1b636b06a56c4d290

commit f28915d98ab049ff928106c1b636b06a56c4d290
Author: Tom Sepez <tsepez@chromium.org>
Date: Thu Aug 25 22:39:16 2022

Make GetCurrentViewRecord() safe even when at end().

Avoid any potential variants on the linked issue.

Bug: chromium:1355682
Change-Id: Id8c24ee24a316439447f5ca2c0dfa8740502b7a3
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/96911
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/f28915d98ab049ff928106c1b636b06a56c4d290/xfa/fxfa/layout/cxfa_viewlayoutprocessor.h


### [Deleted User] (2022-08-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-26)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-26)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M104. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M105. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M106. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-26)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

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
Owners: eakpobaro (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-26)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

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
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-26)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

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

### sr...@google.com (2022-08-29)

Merge approved for M106 branch: pls refer to go/chrome-branches for more info

### sr...@google.com (2022-08-29)

This merge has been approved for M106, please help complete your merges asap (before 4pm PST) today, so the change can be included in this weeks RC build for dev/beta releases. 

We would like to get the changes as much beta time as possible, so please compelete your merges asap.

### gi...@appspot.gserviceaccount.com (2022-08-29)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/ab0a1fadcbc15874b1a164a842aa8a18ebf301f6

commit ab0a1fadcbc15874b1a164a842aa8a18ebf301f6
Author: Tom Sepez <tsepez@chromium.org>
Date: Mon Aug 29 21:45:34 2022

[M106] Avoid de-referencing end() in GetNextAvailContentHeight().

Add the same HasCurrentViewRecord() check as in other methods.

Bug: chromium:1355682
Change-Id: I466f386f037801daa82ead30239f34e025748748
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/96910
Reviewed-by: Lei Zhang <thestig@chromium.org>
Auto-Submit: Tom Sepez <tsepez@chromium.org>
Commit-Queue: Lei Zhang <thestig@chromium.org>
(cherry picked from commit 0d76a139d7ffbbdfb0ef5f5e714597a25f9767c4)
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/97011
Commit-Queue: Tom Sepez <tsepez@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/ab0a1fadcbc15874b1a164a842aa8a18ebf301f6/xfa/fxfa/layout/cxfa_viewlayoutprocessor.cpp


### [Deleted User] (2022-08-29)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-08-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4147082c9d4cc8583e2d6ebff344bc7e2bbd3ce0

commit 4147082c9d4cc8583e2d6ebff344bc7e2bbd3ce0
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Mon Aug 29 23:56:47 2022

Roll PDFium from 6f3c624233f9 to 8479a083aa9f (21 revisions)

https://pdfium.googlesource.com/pdfium.git/+log/6f3c624233f9..8479a083aa9f

2022-08-29 tsepez@chromium.org Fix bad probe on span assignment operator.
2022-08-29 tsepez@chromium.org Avoid pointer arithmetic in cpdf_streamparser.cpp
2022-08-29 tsepez@chromium.org Use spans in place of pointers in fx_font.cpp
2022-08-29 tsepez@chromium.org Give PDFium's top-level build a "default" group
2022-08-29 awscreen@chromium.org Refactor fpdf_view_embeddertest for runtime renderer selection
2022-08-27 tsepez@chromium.org Use Substr() in cpdf_syntax_parser.cpp
2022-08-27 tsepez@chromium.org Vastly simplify CPDF_Type3Cache::m_SizeMap
2022-08-26 awscreen@chromium.org Refactor fpdf_ppo_embeddertest for runtime renderer selection
2022-08-26 tsepez@chromium.org Avoid pointer arithmetic in FindFullName().
2022-08-26 awscreen@chromium.org Refactor fpdf_transformpage_embeddertest for runtime renderer selection
2022-08-26 tsepez@chromium.org Avoid pointer arithmetic in cfx_datetime.cpp
2022-08-26 tsepez@chromium.org Avoid pointer arithmetic in RemoveAllHighLights().
2022-08-26 nigi@chromium.org [Skia] Enable FPDFEditEmbedderTest.GetRenderedBitmapHandlesSMask
2022-08-26 nigi@chromium.org [Skia] Convert Skia rendering results into an unpremultiplied format.
2022-08-25 tsepez@chromium.org Re-work some HasCurrentViewRecord() calls.
2022-08-25 tsepez@chromium.org Make GetCurrentViewRecord() safe even when at end().
2022-08-25 tsepez@chromium.org Avoid de-referencing end() in GetNextAvailContentHeight().
2022-08-25 nigi@chromium.org Update some corpus test expectations
2022-08-25 thestig@chromium.org Improve memory management in CFGAS_GEFont::LoadFontInternal().
2022-08-25 thestig@chromium.org Document FPDF_RenderPageSkp().
2022-08-25 thestig@chromium.org Remove some new statements from fx_skia_device.cpp.

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/pdfium-autoroll
Please CC pdfium-deps-rolls@chromium.org on the revert to ensure that a human
is aware of the problem.

To file a bug in PDFium: https://bugs.chromium.org/p/pdfium/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1355557,chromium:1355682
Tbr: pdfium-deps-rolls@chromium.org
Change-Id: Id5ead4924ac13b7e2b56dc6cd06553fac633a79f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3863025
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1040672}

[modify] https://crrev.com/4147082c9d4cc8583e2d6ebff344bc7e2bbd3ce0/DEPS


### rz...@google.com (2022-08-31)

[Empty comment from Monorail migration]

### rz...@google.com (2022-08-31)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-31)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-08-31)

1. Just https://pdfium-review.googlesource.com/c/pdfium/+/97170
2. Low, no conflicts
3. 106
4. Yes

### gm...@google.com (2022-09-01)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-09-08)

M105 and M104 merge approved, please merge this fix to 105 (branch 5195) and 104 (branch 5112) ASAP / before 10am PDT tomorrow, Friday 9 September so this fix can be included in the next stable and extended stable respins -- thank you! 

### pb...@google.com (2022-09-08)

This merge has been approved for M105, please help complete your merges asap (before 4pm PST) today, so the change can be included in next weeks RC build for Stable releases.





### sr...@google.com (2022-09-08)

chatted with thomas , he is working on merges to all 3 branches

### gi...@appspot.gserviceaccount.com (2022-09-08)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/7f0bb5197ed133c92ceac8c0009f569caea4f065

commit 7f0bb5197ed133c92ceac8c0009f569caea4f065
Author: Tom Sepez <tsepez@chromium.org>
Date: Thu Sep 08 23:45:54 2022

[M104] Avoid de-referencing end() in GetNextAvailContentHeight().

Add the same HasCurrentViewRecord() check as in other methods.

Bug: chromium:1355682
Change-Id: I466f386f037801daa82ead30239f34e025748748
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/96910
Reviewed-by: Lei Zhang <thestig@chromium.org>
Auto-Submit: Tom Sepez <tsepez@chromium.org>
Commit-Queue: Lei Zhang <thestig@chromium.org>
(cherry picked from commit 0d76a139d7ffbbdfb0ef5f5e714597a25f9767c4)
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/97738
Commit-Queue: Tom Sepez <tsepez@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/7f0bb5197ed133c92ceac8c0009f569caea4f065/xfa/fxfa/layout/cxfa_viewlayoutprocessor.cpp


### gi...@appspot.gserviceaccount.com (2022-09-09)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/8f99374cbe5dd5a7737133d26c52316939a86a17

commit 8f99374cbe5dd5a7737133d26c52316939a86a17
Author: Tom Sepez <tsepez@chromium.org>
Date: Fri Sep 09 00:18:24 2022

[M105] Avoid de-referencing end() in GetNextAvailContentHeight().

Add the same HasCurrentViewRecord() check as in other methods.

Bug: chromium:1355682
Change-Id: I466f386f037801daa82ead30239f34e025748748
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/96910
Reviewed-by: Lei Zhang <thestig@chromium.org>
Auto-Submit: Tom Sepez <tsepez@chromium.org>
Commit-Queue: Lei Zhang <thestig@chromium.org>
(cherry picked from commit 0d76a139d7ffbbdfb0ef5f5e714597a25f9767c4)
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/97737

[modify] https://pdfium.googlesource.com/pdfium/+/8f99374cbe5dd5a7737133d26c52316939a86a17/xfa/fxfa/layout/cxfa_viewlayoutprocessor.cpp


### am...@google.com (2022-09-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-09-09)

Congratulations! The VRP Panel has decided to award you $7,000 for this report. A member of our finance team will be in touch to arrange payment. In the interim, please let us know what name/handle/tag you would like us to use in acknowledging you for reporting this issue. Thank you for your efforts and reporting this issue to us-- nice work! 

### 0x...@gmail.com (2022-09-10)

Please credit to MerdroidSG. Thanks.

### am...@chromium.org (2022-09-12)

Hi tsepez@, there were two fixes: https://pdfium-review.googlesource.com/c/pdfium/+/96910 and https://pdfium-review.googlesource.com/c/pdfium/+/96911 -- it appears that 96910 got backmerged to beta/stable/extended while 96911 was not. The fix in https://pdfium-review.googlesource.com/c/pdfium/+/96911 was part of the pdfium roll (4147082c9d4cc8583e2d6ebff344bc7e2bbd3ce0), on 107 and but that roll commit nor the individual fix in 96911 do not appear to have been backmerged to 106/105/104. 

I believe that https://pdfium-review.googlesource.com/c/pdfium/+/96911 needs to get backmerged to 106, 105, and 104 and this issue is not to be considered fixed in the forthcoming respin tomorrow. Please let me know if I'm incorrect and there is something I've missed /gotten incorrect here.
If there's nothing I'm missing, please backmerge the fix in 96911 to 106 at soonest. 
I'd also generally request the backmerge to 105/stable and 104/extended, however, tomorrow's respin is the last planned respin of 105/stable and 104/extended. 


### ts...@chromium.org (2022-09-12)

Re 96911, that was precautionary. Should be OK as-is.

### am...@chromium.org (2022-09-12)

Thanks for checking/confirming, Tom. 

### am...@google.com (2022-09-13)

[Empty comment from Monorail migration]

### am...@google.com (2022-09-14)

[Empty comment from Monorail migration]

### gm...@google.com (2022-09-20)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-09-22)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/873bffafa8fd75541250149685153d7c083ee950

commit 873bffafa8fd75541250149685153d7c083ee950
Author: Tom Sepez <tsepez@chromium.org>
Date: Thu Sep 22 18:09:04 2022

[M102-LTS] Avoid de-referencing end() in GetNextAvailContentHeight().

Add the same HasCurrentViewRecord() check as in other methods.

Bug: chromium:1355682
Change-Id: I466f386f037801daa82ead30239f34e025748748
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/96910
Auto-Submit: Tom Sepez <tsepez@chromium.org>
Commit-Queue: Lei Zhang <thestig@chromium.org>
(cherry picked from commit 0d76a139d7ffbbdfb0ef5f5e714597a25f9767c4)
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/97170
Reviewed-by: Tom Sepez <tsepez@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/873bffafa8fd75541250149685153d7c083ee950/xfa/fxfa/layout/cxfa_viewlayoutprocessor.cpp


### rz...@google.com (2022-09-23)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1355682?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060649)*

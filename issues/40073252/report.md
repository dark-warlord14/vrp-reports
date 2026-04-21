# Security: Out Of Bound in PDF web view plugin

| Field | Value |
|-------|-------|
| **Issue ID** | [40073252](https://issues.chromium.org/issues/40073252) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | pw...@gmail.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2023-09-24 |
| **Bounty** | Confirmed (amount unknown) |

## Description

**VULNERABILITY DETAILS**  

An Assert error occurs due to incorrect index checking for the getPageBoundingBox and saveAttachment messages in the PDF view web Plugin.

```
void PdfViewWebPlugin::HandleGetPageBoundingBoxMessage(  
    const base::Value::Dict& message) {  
  const int page_index = message.FindInt("page").value(); // [1] Get page value  
  base::Value::Dict reply =  
      PrepareReplyMessage("getPageBoundingBoxReply", message);  
  
  gfx::RectF bounding_box = engine_->GetPageBoundingBox(page_index);  
  gfx::Rect page_bounds = engine_->GetPageBoundsRect(page_index); // [2] Call GetPageBoundsRect with page_index  
  
  // Flip the origin from bottom-left to top-left.  
  bounding_box.set_y(static_cast<float>(page_bounds.height()) -  
                     bounding_box.bottom());  
  reply.Set("x", bounding_box.x());  
  reply.Set("y", bounding_box.y());  
  reply.Set("width", bounding_box.width());  
  reply.Set("height", bounding_box.height());  
  
  client_->PostMessage(std::move(reply));  
}  

```
```
gfx::Rect PDFiumEngine::GetPageBoundsRect(int index) {  
  return pages_[index]->rect(); // [3] Directly accesses the index  
}  

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:pdf/pdf_view_web_plugin.cc;l=1374;drc=8f5c47fd8d80208c191fe575f0817b26a9093837>  

[2] <https://source.chromium.org/chromium/chromium/src/+/main:pdf/pdf_view_web_plugin.cc;l=1379;drc=8f5c47fd8d80208c191fe575f0817b26a9093837>  

[3] <https://source.chromium.org/chromium/chromium/src/+/main:pdf/pdfium/pdfium_engine.cc;l=2562;drc=8f5c47fd8d80208c191fe575f0817b26a9093837>

```
void PdfViewWebPlugin::HandleSaveAttachmentMessage(  
    const base::Value::Dict& message) {  
  const int index = message.FindInt("attachmentIndex").value(); // [1] Get attachmentIndex value  
  
  const std::vector<DocumentAttachmentInfo>& list =  
      engine_->GetDocumentAttachmentInfoList();  
  DCHECK_GE(index, 0);  
  DCHECK_LT(static_cast<size_t>(index), list.size());  
  DCHECK(list[index].is_readable);  
  DCHECK(IsSaveDataSizeValid(list[index].size_bytes));  
  
  std::vector<uint8_t> data = engine_->GetAttachmentData(index); // [2] Call GetAttachmentData with index  
  base::Value data_to_save(  
      IsSaveDataSizeValid(data.size()) ? data : std::vector<uint8_t>());  
  
  base::Value::Dict reply = PrepareReplyMessage("saveAttachmentReply", message);  
  reply.Set("dataToSave", std::move(data_to_save));  
  client_->PostMessage(std::move(reply));  
}  

```
```
std::vector<uint8_t> PDFiumEngine::GetAttachmentData(size_t index) {  
  DCHECK_LT(index, doc_attachment_info_list_.size());  
  DCHECK(doc_attachment_info_list_[index].is_readable);  
  unsigned long length_bytes = doc_attachment_info_list_[index].size_bytes; // [3] Directly accesses the index  
  DCHECK_NE(length_bytes, 0u);  
  
  FPDF_ATTACHMENT attachment = FPDFDoc_GetAttachment(doc(), index);  
  std::vector<uint8_t> content_buf(length_bytes);  
  unsigned long data_size_bytes;  
  bool is_attachment_readable = FPDFAttachment_GetFile(  
      attachment, content_buf.data(), length_bytes, &data_size_bytes);  
  DCHECK(is_attachment_readable);  
  DCHECK_EQ(length_bytes, data_size_bytes);  
  
  return content_buf;  
}  

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:pdf/pdf_view_web_plugin.cc;l=1438;drc=8f5c47fd8d80208c191fe575f0817b26a9093837>  

[2] <https://source.chromium.org/chromium/chromium/src/+/main:pdf/pdf_view_web_plugin.cc;l=1447;drc=8f5c47fd8d80208c191fe575f0817b26a9093837>  

[3] <https://source.chromium.org/chromium/chromium/src/+/main:pdf/pdfium/pdfium_engine.cc;l=2359;drc=8f5c47fd8d80208c191fe575f0817b26a9093837>

**VERSION**  

Chrome Version: 119.0.6011.0 (Official Build)  

Operating System: Windows 11

**REPRODUCTION CASE**

1. Open the PDF.
2. Enter the following code into the developer console.

```
this.postMessage_({  
    type: 'getPageBoundingBox',  
    page: 0x1337  
})  

```
```
this.postMessage_({  
    type: 'saveAttachment',  
    page: 0x1337  
})  

```

**CREDIT INFORMATION**  

Reporter credit: [pwn2car]

## Timeline

### [Deleted User] (2023-09-24)

[Empty comment from Monorail migration]

### do...@chromium.org (2023-09-24)

Thanks for the report. It looks to me that the only way this is exploitable is through a physically-local attack[1], since it requires code to be run in DevTools to trigger. That means it's not a security vulnerability in Chrome.

However, it probably still makes sense for the code to check the bounds here, so +PDF folks to take a look at that.

1. https://chromium.googlesource.com/chromium/src/+/master/docs/security/faq.md#Why-arent-physically_local-attacks-in-Chromes-threat-model

[Monorail components: Internals>Plugins>PDF]

### th...@chromium.org (2023-09-25)

FYI, the GetAttachmentData part is https://crbug.com/chromium/1308312.

### th...@chromium.org (2023-09-25)

And the GetPageBoundsRect portion of this bug is just https://crbug.com/chromium/1453872, but triggered via Devtools.

### is...@google.com (2023-09-25)

This issue was migrated from crbug.com/chromium/1486324?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### an...@chromium.org (2025-12-10)

`getPageBoundingBox()` is fixed after <https://crrev.com/1363484> added a `CHECK`.

Then, it seems like `GetAttachmentData()` just needs to update the `DCHECK`s to `CHECK`s?

### dx...@google.com (2025-12-10)

Project: chromium/src  

Branch:  main  

Author:  Andy Phan [andyphan@chromium.org](mailto:andyphan@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7247909>

[PDF] Upgrade DCHECKs to CHECKs in attachment save flow

---


Expand for full commit details
```
     
    Add better bounds checking for the "saveAttachment" message in 
    PdfViewWebPlugin::HandleSaveAttachmentMessage() and 
    PDFiumEngine::GetAttachmentData() by upgrading DCHECKs to CHECKs. 
     
    Bug: 40073252, 40828986 
    Change-Id: Ia7897928521de5f7ac58e25269d3fa68bac0093c 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7247909 
    Commit-Queue: Andy Phan <andyphan@chromium.org> 
    Reviewed-by: Lei Zhang <thestig@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1557009}

```

---

Files:

- M `pdf/pdf_view_web_plugin.cc`
- M `pdf/pdfium/pdfium_engine.cc`

---

Hash: [9866dc8a44a625f54a6b42dbba1cd1ab3db24e89](https://chromiumdash.appspot.com/commit/9866dc8a44a625f54a6b42dbba1cd1ab3db24e89)  

Date: Wed Dec 10 23:04:39 2025


---

### wf...@chromium.org (2025-12-16)

Agree with #3 here.

### sp...@google.com (2025-12-18)

*NOTE: This is an automatically generated email*

Hello,

Chrome Vulnerability Rewards Program (VRP) Panel has decided that the security impact of this
issue does not meet the criteria to qualify for a reward.

Rationale for this decision:

the panel decided that because of the steps required for a user to be exposed to this bug a reasonable and prudent user would not be at risk here so declined to reward

Note that the fact that this issue is not being rewarded does not mean
that the product team won't fix the issue. We have filed a bug with the product
team and they will review your report and decide if a fix is required. We'll
let you know if the issue was fixed.

Regards,   

Google Security Bot

*How did we do? Please fill out a [short anonymous survey](https://goo.gl/IR3KRH).*

### ch...@google.com (2026-03-19)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> the panel decided that because of the steps required for a user to be exposed to this bug a reasonable and prudent user would not be at risk here so declined to reward
> 
> 
> Note that the fact that this issue is not being rewarded does not mean
> that the product team won't fix the issue. We have filed a bug with the product
> team and they will review your report and decide if a fix is required. We'll
> let you know if the issue was fixed.
> 
> Regards, \
> Google Security Bot
> 
> *How did we do? Please fill out 

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40073252)*

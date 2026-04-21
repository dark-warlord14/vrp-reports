# Security: chromeos  Root priv escalation to write file

| Field | Value |
|-------|-------|
| **Issue ID** | [40059949](https://issues.chromium.org/issues/40059949) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Shell |
| **Platforms** | ChromeOS |
| **Reporter** | wx...@gmail.com |
| **Assignee** | ha...@chromium.org |
| **Created** | 2022-06-13 |
| **Bounty** | $1,000.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/HEAD/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

**VULNERABILITY DETAILS**  

**Please provide a brief explanation of the security issue.**

**VERSION**  

**Chrome Version: [x.x.x.x] + [stable, beta, or dev]**  

**Operating System: [Please indicate OS, version, and service pack level]**  

chromeos system

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

## Timeline

### [Deleted User] (2022-06-13)

[Empty comment from Monorail migration]

### wx...@gmail.com (2022-06-13)

we can use dbus-send  to execute the function "OpenFileById"(https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/platform2/virtual_file_provider/service.cc;l=140?q=OpenFileById&ss=chromiumos%2Fchromiumos%2Fcodesearch:src%2Fplatform2%2Fvirtual_file_provider%2F)

```c++
void Service::OpenFileById(
    dbus::MethodCall* method_call,
    dbus::ExportedObject::ResponseSender response_sender) {
  DCHECK(thread_checker_.CalledOnValidThread());

  dbus::MessageReader reader(method_call);
  std::string id;
  if (!reader.PopString(&id)) {
    std::move(response_sender)
        .Run(dbus::ErrorResponse::FromMethodCall(
            method_call, DBUS_ERROR_INVALID_ARGS, "Id must be provided."));
    return;
  }

  // An ID corresponds to a file name in the FUSE file system.
  base::FilePath path = fuse_mount_path_.AppendASCII(std::move(id));  // we can set the id to "../../../../etc/passwd" to cause path traversal

  // Create a new FD associated with the ID.
  base::ScopedFD fd(
      HANDLE_EINTR(open(path.value().c_str(), O_RDONLY | O_CLOEXEC))); // it will read file to reponse
  if (!fd.is_valid()) {
    std::move(response_sender)
        .Run(dbus::ErrorResponse::FromMethodCall(
            method_call, DBUS_ERROR_INVALID_ARGS, "Invalid Id."));
    return;
  }

  // Send response.
  std::unique_ptr<dbus::Response> response =
      dbus::Response::FromMethodCall(method_call);
  dbus::MessageWriter writer(response.get());
  writer.AppendFileDescriptor(fd.get());
  std::move(response_sender).Run(std::move(response)); //we can get thre repsonse 
}
```

- how to fix
  - chck the filepath contains ("..")

### wx...@gmail.com (2022-06-13)

I use amd64-generic to build  virtual_file_provider and try to execute it, but it shows that I have an undefined symbol error, So I can't provider poc, just submit the report.

### ye...@google.com (2022-06-13)

[Empty comment from Monorail migration]

### al...@google.com (2022-06-28)

The root filesystem (and by extension /etc/) is not writeable on ChromeOS, so I don't see an root priv escalation here.

It is possible the file ID's are not being scoped properly.

[Monorail components: UI>Shell]

### [Deleted User] (2022-06-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-28)

[Empty comment from Monorail migration]

### ha...@chromium.org (2022-06-29)

Thank you for reporting. The ID string must be checked to avoid unexpected behavior.

That said, virtual_file_provider runs in a jail as a non-root user so I don't think this immediately results in a root priv escalation.

### wx...@gmail.com (2022-06-29)

Yes, my title is wrong,  it may cause virtual_file_provider to read any files to find file exists. I think it's a low vulnerability 

### [Deleted User] (2022-06-29)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-07-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/platform2/+/6c7e50d91c3cd4c58751084ba660d0e34b5814d6

commit 6c7e50d91c3cd4c58751084ba660d0e34b5814d6
Author: Ryo Hashimoto <hashimoto@google.com>
Date: Thu Jun 30 08:32:22 2022

virtual_file_provider: Check the given ID

BUG=chromium:1335902
TEST=dbus-send --system --dest=org.chromium.VirtualFileProvider --type=method_call --print-reply /org/chromium/VirtualFileProvider org.chromium.VirtualFileProvider.OpenFileById string:foo

Change-Id: I9405e9b46f59956ba2c7c0abba2c596c8eb9a832
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/platform2/+/3736407
Tested-by: Ryo Hashimoto <hashimoto@chromium.org>
Commit-Queue: Ryo Hashimoto <hashimoto@chromium.org>
Reviewed-by: Satoshi Niwa <niwa@chromium.org>

[modify] https://crrev.com/6c7e50d91c3cd4c58751084ba660d0e34b5814d6/virtual_file_provider/service.h
[modify] https://crrev.com/6c7e50d91c3cd4c58751084ba660d0e34b5814d6/virtual_file_provider/service.cc
[add] https://crrev.com/6c7e50d91c3cd4c58751084ba660d0e34b5814d6/virtual_file_provider/service_test.cc
[modify] https://crrev.com/6c7e50d91c3cd4c58751084ba660d0e34b5814d6/virtual_file_provider/BUILD.gn


### ha...@chromium.org (2022-07-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-13)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-10-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-10-14)

Congratulations, raven! The VRP Panel has decided to award you $1,000 for this report. While the quality and components of this bug report are below baseline, and there are substantial preconditions to exploit this, we did have enough information to make a security relevant change. Thank you for your efforts in reporting this issue to us. 

### am...@google.com (2022-10-14)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### is...@google.com (2023-05-24)

This issue was migrated from crbug.com/chromium/1335902?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059949)*

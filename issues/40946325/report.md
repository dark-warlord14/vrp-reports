# Elevation of Privilege in GoogleUpdate with Windows

| Field | Value |
|-------|-------|
| **Issue ID** | [40946325](https://issues.chromium.org/issues/40946325) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Updater |
| **Platforms** | Windows |
| **Reporter** | do...@pksecurity.io |
| **Assignee** | ga...@chromium.org |
| **Created** | 2023-11-28 |
| **Bounty** | $5,000.00 |

## Description

---

### Report description


Elevation of Privilege in GoogleUpdate with Windows


---

### Bug location


#### Which product or website have you found a vulnerability in?

Google Chrome


---

### The problem


#### Please describe the technical details of the vulnerability

### VULNERABILITY SUMMARY
A local EoP vulnerability has been discovered in the Google Update Service, which can be exploited by an attacker to gain SYSTEM privileges on a PC with Google Chrome.

### VERSION
Chrome: 1.3.36.332
Tested OS Version: Windows 10 x64 22H2 Latest Build

### VULNERABILITY DETAIL
The GoogleUpdate service, which runs periodically in the background, creates and deletes files in the %AppData$\Local folder, where full control exists for the normal user.
Example file name: `C:\Users\mike\AppData\Local\{F9728908-AC7D-46D3-B6E8-358979215701}`
Below is the call stack for this action.
```"20","KernelBase.dll","DeleteFileW + 0x171","0x75a191b1","C:\Windows\SysWOW64\KernelBase.dll"
"21","goopdate.dll","DllEntry + 0x41c2b","0x74225eb5","C:\Program Files (x86)\Google\Update\1.3.36.332\goopdate.dll"
"22","goopdate.dll","DllEntry + 0x46180","0x7422a40a","C:\Program Files (x86)\Google\Update\1.3.36.332\goopdate.dll"
"23","goopdate.dll","DllEntry + 0x21ee9","0x74206173","C:\Program Files (x86)\Google\Update\1.3.36.332\goopdate.dll"
"24","goopdate.dll","DllEntry + 0x21f8a","0x74206214","C:\Program Files (x86)\Google\Update\1.3.36.332\goopdate.dll"
"25","goopdate.dll","DllEntry + 0xc5ee8","0x742aa172","C:\Program Files (x86)\Google\Update\1.3.36.332\goopdate.dll"
"26","goopdate.dll","DllEntry + 0xc6213","0x742aa49d","C:\Program Files (x86)\Google\Update\1.3.36.332\goopdate.dll"
"27","goopdate.dll","DllEntry + 0x22053","0x742062dd","C:\Program Files (x86)\Google\Update\1.3.36.332\goopdate.dll"
"28","goopdate.dll","DllEntry + 0x13f56","0x741f81e0","C:\Program Files (x86)\Google\Update\1.3.36.332\goopdate.dll"
"29","goopdate.dll","DllEntry + 0x13af2","0x741f7d7c","C:\Program Files (x86)\Google\Update\1.3.36.332\goopdate.dll"
"30","goopdate.dll","DllEntry + 0x13554","0x741f77de","C:\Program Files (x86)\Google\Update\1.3.36.332\goopdate.dll"
"31","goopdate.dll","DllEntry + 0x1314a","0x741f73d4","C:\Program Files (x86)\Google\Update\1.3.36.332\goopdate.dll"
"32","goopdate.dll","DllEntry + 0xcb","0x741e4355","C:\Program Files (x86)\Google\Update\1.3.36.332\goopdate.dll"
"33","GoogleUpdate.exe","GoogleUpdate.exe + 0x681f","0x15681f","C:\Program Files (x86)\Google\Update\GoogleUpdate.exe"
"34","GoogleUpdate.exe","GoogleUpdate.exe + 0x73be","0x1573be","C:\Program Files (x86)\Google\Update\GoogleUpdate.exe"
"35","kernel32.dll","BaseThreadInitThunk + 0x19","0x768afcc9","C:\Windows\SysWOW64\kernel32.dll"
"36","ntdll.dll","RtlGetAppContainerNamedObjectPath + 0x11e","0x77927c6e","C:\Windows\SysWOW64\ntdll.dll"
"37","ntdll.dll","RtlGetAppContainerNamedObjectPath + 0xee","0x77927c3e","C:\Windows\SysWOW64\ntdll.dll"```

This behavior is performed with SYSTEM privileges, and there is currently known primitive in the latest version of Windows that can achieve EoP to SYSTEM via high privilege file deletion.
Below is a description of the primitives, followed by their implementations.
https://www.zerodayinitiative.com/blog/2022/3/16/abusing-arbitrary-file-deletes-to-escalate-privilege-and-other-great-tricks
https://github.com/thezdi/PoC/tree/master/FilesystemEoPs

### ATTACK SCENARIO
1. An attacker with Medium privileges and local code execution monitors the %Appdata%\Local folder, waiting for a file in GUID format to be created. 
2. Once that file is created, create a symbolic link at the same path, using multi-threading, deleting the file's handle as soon as it is closed. (It's not that hard to win the race. If attacker don't want to race, can use Oplock.)
3. An attacker gains an arbitrary file deletion vulnerability with SYSTEM privilege.
4. Gain SYSTEM privilege by deleting arbitrary files. (The primitives introduced above are just the most well-known, but there are many more.)

### PATCH SUGGESTION
The simplest way to do this is to store the file under "Program Files", which is not vulnerable because normal users do not have write and delete permissions on the file.
Additional alternatives include resetting the file's DACL, or having DeleteFileW called from a Medium privilege.

### Reference
Exploiting Windows Symbolic Link - https://nixhacker.com/understanding-and-exploiting-symbolic-link-in-windows/
File deletion to EoP - https://www.zerodayinitiative.com/blog/2022/3/16/abusing-arbitrary-file-deletes-to-escalate-privilege-and-other-great-tricks
File deletion to EoP (Implemetation) - https://github.com/thezdi/PoC/tree/master/FilesystemEoPs


#### Please briefly explain who can exploit the vulnerability, and what they gain when doing so

It can be exploited by an attacker to gain SYSTEM privileges on a PC with Google Chrome.

### ATTACK SCENARIO
1. An attacker with Medium privileges and local code execution monitors the %Appdata%\Local folder, waiting for a file in GUID format to be created. 
2. Once that file is created, create a symbolic link at the same path, using multi-threading, deleting the file's handle as soon as it is closed. (It's not that hard to win the race. If attacker don't want to race, can use Oplock.)
3. An attacker gains an arbitrary file deletion vulnerability with SYSTEM privilege.
4. Gain SYSTEM privilege by deleting arbitrary files. (The primitives introduced above are just the most well-known, but there are many more.)

### Reference
Exploiting Windows Symbolic Link - https://nixhacker.com/understanding-and-exploiting-symbolic-link-in-windows/
File deletion to EoP - https://www.zerodayinitiative.com/blog/2022/3/16/abusing-arbitrary-file-deletes-to-escalate-privilege-and-other-great-tricks
File deletion to EoP (Implemetation) - https://github.com/thezdi/PoC/tree/master/FilesystemEoPs


---

### The cause




## Attachments

- [goopdate.dll](attachments/goopdate.dll) (application/octet-stream, 1.9 MB)
- [TEST_goopdate_unsigned.pdb.zip](attachments/TEST_goopdate_unsigned.pdb.zip) (application/octet-stream, 9.3 MB)

## Timeline

### do...@pksecurity.io (2023-11-28)

[Empty comment from Monorail migration]

### ch...@appspot.gserviceaccount.com (2023-11-28)

[Empty comment from Monorail migration]

### sk...@chromium.org (2023-11-28)

[Empty comment from Monorail migration]

[Monorail components: Internals>Updater]

### sk...@chromium.org (2023-11-28)

[Empty comment from Monorail migration]

### wa...@chromium.org (2023-11-28)

[Empty comment from Monorail migration]

### ga...@chromium.org (2023-11-28)

Hi, thank you for reporting this issue. Could you please get us a symbolized stack trace? I'm attaching the symbols for goopdate.dll (unzip and copy the PDB to the "C:\Program Files (x86)\Google\Update\1.3.36.332" directory). Thank you!

### ga...@chromium.org (2023-11-28)

This is the line where the delete happens:

SimpleRequest::~SimpleRequest() {
  Close();
  callback_ = NULL;

  // If download failed, try to clean up the target file.
  if (!download_completed_ && !filename_.IsEmpty()) {
    if (!::DeleteFile(filename_) && ::GetLastError() != ERROR_FILE_NOT_FOUND) {
      NET_LOG(LW, (_T("[SimpleRequest][Failed to delete file: %s][0x%08x]."),
                   filename_.GetString(), HRESULTFromLastError()));
    }
  }
}

This is the root cause:
HRESULT DownloadCodeRedFileAsLoggedOnUser(const TCHAR* url,
                                      const TCHAR* file_path,
                                      void* callback_argument,
                                      int* http_status_code) {
  ASSERT1(http_status_code);
  *http_status_code = 0;
  scoped_handle logged_on_user_token(
      goopdate_utils::GetImpersonationTokenForMachineProcess(true));
  if (!valid(logged_on_user_token)) {
    return E_FAIL;
  }

  HRESULT hr = S_OK;
  CString download_target_path;
  {
    scoped_impersonation impersonate_user(get(logged_on_user_token));
    hr = HRESULT_FROM_WIN32(impersonate_user.result());
    if (FAILED(hr)) {
      return hr;
    }

    hr = CreateUniqueTempFileForLoggedOnUser(&download_target_path);
    if (FAILED(hr)) {
      return hr;
    }

Stack:
 [omaha\net\simple_request.cc @ 106] (18045e86)   goopdate!omaha::SimpleRequest::~SimpleRequest+0x2f   
 [omaha\net\network_request_impl.cc @ 133] (1804a3eb)   goopdate!omaha::internal::NetworkRequestImpl::~NetworkRequestImpl+0x1f   
 [omaha\goopdate\code_red_check.cc @ 141] (180260e2)   goopdate!omaha::`anonymous namespace'::DownloadCodeRedFileAsLoggedOnUser+0x91   
 [omaha\goopdate\code_red_check.cc @ 173] (180261f0)   goopdate!omaha::`anonymous namespace'::CodeRedDownloadCallback+0x24   
 [omaha\recovery\client\google_update_recovery.cc @ 468] (180ca0b6)   goopdate!omaha::`anonymous namespace'::DownloadRepairFile+0xbc   
 [omaha\recovery\client\google_update_recovery.cc @ 625] (180ca41b)   goopdate!FixGoogleUpdate+0x82   
 [omaha\goopdate\code_red_check.cc @ 210] (18026265)   goopdate!omaha::CheckForCodeRed+0x78   
 [omaha\goopdate\goopdate.cc @ 1125] (1801817c)   goopdate!omaha::detail::GoopdateImpl::HandleCodeRedCheck+0x64   
 [omaha\goopdate\goopdate.cc @ 850] (18017a98)   goopdate!omaha::detail::GoopdateImpl::ExecuteMode+0x2e4   
 [omaha\goopdate\goopdate.cc @ 662] (18017556)   goopdate!omaha::detail::GoopdateImpl::DoMain+0x288   
 [omaha\goopdate\goopdate.cc @ 482] (180173b2)   goopdate!omaha::detail::GoopdateImpl::Main+0x22


### ga...@chromium.org (2023-11-28)

The code above impersonates the medium token for the logged on user when running as system. The creation/deletion of the folder is with impersonation in place. 

This would ordinarily not allow for elevation of privilege. Do you have an actual exploit?

### do...@pksecurity.io (2023-11-29)

Obviously, the first attempt will impersonate the logged-on user, but if that attempt fails at any point, it will do it again without impersonation.

HRESULT CodeRedDownloadCallback(const TCHAR* url,
                                const TCHAR* file_path,
                                void* callback_argument) {
  ++metric_cr_callback_total;

  int http_status_code = 0;
  HRESULT hr = DownloadCodeRedFileAsLoggedOnUser(url,
                                                 file_path,
                                                 callback_argument,
                                                 &http_status_code);
  if (FAILED(hr) && (http_status_code != HTTP_STATUS_NO_CONTENT)) {
    hr = DownloadCodeRedFile(url,
                             file_path,
                             callback_argument,
                             &http_status_code);
  }

In fact, it's very easy to make DownloadCodeRedFileAsLoggedOnUser fail (return <0).
Below is an excerpt from DownloadCodeRedFileAsLoggedOnUser.

  HRESULT hr = S_OK;
  CString download_target_path;
  {
    scoped_impersonation impersonate_user(get(logged_on_user_token));
    hr = HRESULT_FROM_WIN32(impersonate_user.result());
    if (FAILED(hr)) {
      return hr;
    }

    hr = CreateUniqueTempFileForLoggedOnUser(&download_target_path);
    if (FAILED(hr)) {
      return hr;
    }
    if (download_target_path.IsEmpty()) {
      return E_FAIL;
    }

    hr = DownloadCodeRedFile(url,
                             download_target_path,
                             callback_argument,
                             http_status_code);
    if (FAILED(hr)) {
      ::DeleteFile(download_target_path);
      return hr;
    }
  }

  const DWORD kMoveFlag = MOVEFILE_COPY_ALLOWED |
                          MOVEFILE_REPLACE_EXISTING |
                          MOVEFILE_WRITE_THROUGH;
  if (!::MoveFileEx(download_target_path,
                    file_path,
                    kMoveFlag)) {
    hr = HRESULT_FROM_WIN32(::GetLastError());
  }

If, in the part of the call to MoveFileEx, another process has already set the SHARED_MODE to SHARED_READ on the file at the destination path and has a handle to it, MoveFileEx's attempt will fail, and DownloadCodeRedFileAsLoggedOnUser will return a failure.
This will call DownloadCodeRedFile, which does not impersonate the logged-on user.

Below is an example of a program that implements such behavior.

#include <stdio.h>
#include <windows.h>

int wmain(int argc, wchar_t** argv)
{
	if (argc < 2)
		return 0;
	HANDLE fh = INVALID_HANDLE_VALUE;

	while (fh == INVALID_HANDLE_VALUE)
	{
		fh = CreateFile(argv[1], GENERIC_READ | GENERIC_WRITE, FILE_SHARE_READ, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
	}

	Sleep(10000000);
	return 0;
}


### ga...@chromium.org (2023-11-29)

[Empty comment from Monorail migration]

### ga...@chromium.org (2023-11-30)

Thank you again for reporting this. A fix for this issue is expected to ship out to GoogleUpdate users in about 7 business days.

### so...@chromium.org (2023-11-30)

+Amy for the next steps here.

### [Deleted User] (2023-11-30)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-11-30)

I gave bad advice to the person who did security triage of this issue and had them put SI-None on this issue, since the merge labels that the bot applies based on FoundIn and SI don't apply to Omaha issues. However, they do impact things like security advisory notes and CVEs, so I'm fixing that. 
The reporter reported this issue based on version 1.3.36.332, according to Omaha releases that coincides with 1.3.36.331 (release candidate, 10-31-2023). Looking at this issue, I presume it goes back a bit farther. Chatting off bug with ganesh@, it does indeed for quite some time, since almost the beginning. 

Updating to FoundIn-118 (only since 118 is the oldest active release channel and it's not worth going back farther than that for this issue) and SI-Extended. 
My apologies for the forthcoming merge nags from the bot. I'll try to clean them up as soon as I see them. 



### am...@chromium.org (2023-11-30)

Hmm, this didn't get a reward-topanel label. There was a bug that impacting windows only issues from getting updated but that was fixed awhile back. 
I'll look into this, but in the meantime, manually adding the label so this can be in our VRP queue. 

### [Deleted User] (2023-12-01)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-12-01)

This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M118. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to other stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M119. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M120. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [118, 119, 120].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-12-02)

This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M118. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to other stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M119. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M120. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [118, 119, 120].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-12-03)

This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M118. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to other stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M119. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M120. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [118, 119, 120].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-12-04)

as mentioned in c#14, no merges needed here since Omaha release process is outside of Chrome release process 

### am...@google.com (2023-12-07)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-12-07)

Congratulations! The Chrome VRP Panel has decided to award you $5,000 for this report. A member of our p2p-vrp@ finance team will be in touch with you soon to arrange payment. In the meantime, please let us know the name / handle or other identifier you would like us to use in acknowledging you for this finding. Thank you for your efforts and reporting this issue to us -- nice work! 

### do...@pksecurity.io (2023-12-08)

Thanks for the quick processing.
My name and handle is Kim Dong-uk (@justlikebono).



### am...@google.com (2023-12-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### do...@pksecurity.io (2024-01-14)

When will the CVE issue and patch release be carried out for this vulnerability?

### is...@google.com (2024-01-14)

This issue was migrated from crbug.com/chromium/1505686?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### pg...@google.com (2024-02-21)

A CVE will be assigned momentarily (:

### pe...@google.com (2024-03-08)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40946325)*

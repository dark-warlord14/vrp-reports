# Security: Arbitrary file read when caching file using CallAsSelfAndImpersonate2

| Field | Value |
|-------|-------|
| **Issue ID** | [40055353](https://issues.chromium.org/issues/40055353) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Installer |
| **Platforms** | Windows |
| **Reporter** | ve...@gmail.com |
| **Assignee** | ga...@chromium.org |
| **Created** | 2021-03-27 |
| **Bounty** | $5,000.00 |

## Description

Summary:
The Google Update service expose a COM object that is accessible locally to low privileges users, the object exposes an interface that can be used to read arbitrary files.

Description:
Google Updater is a service designed to allow low privileged users to run a highly privileges update without the needing of an administrative approval. To achieve that, the service expose a COM class that exposes certain methods and dispatches to low and medium integrity processes. The service run as SYSTEM privileges to serve those requests, so any improper file operation can be abused to elevate privileges.
The following COM class can be found in https://chromium.googlesource.com/chromium/src/+/32352ad08ee673a4d43e8593ce988b224f6482d3/google_update/google_update_idl.idl
[
  object,
  dual,
  uuid(494B20CF-282E-4BDD-9F5D-B70CB09D351E),
  helpstring("IGoogleUpdate3Web Interface"),
  pointer_default(unique)
]
interface IGoogleUpdate3Web : IDispatch {
  HRESULT createAppBundleWeb([out, retval] IDispatch** app_bundle_web);
};
[
  object,
  uuid(2D363682-561D-4c3a-81C6-F2F82107562A),
  helpstring("IGoogleUpdate3WebSecurity Interface"),
  pointer_default(unique)
]

According to the comments and the COM object ACL this class interface is accessible to low/medium integrity processes, the IGoogleUpdate3Web allow us to create an instance of another COM interface IAppBundleWeb

[
  object,
  dual,
  uuid(DD42475D-6D46-496a-924E-BD5630B4CBBA),
  helpstring("IAppBundleWeb Interface"),
  pointer_default(unique)
]
interface IAppBundleWeb : IDispatch {
  [id(2)] HRESULT createApp([in] BSTR app_guid,
                            [in] BSTR brand_code,
                            [in] BSTR language,
                            [in] BSTR ap);
  [id(3)] HRESULT createInstalledApp([in] BSTR app_id);
  [id(4)] HRESULT createAllInstalledApps();
  [propget] HRESULT displayLanguage([out, retval] BSTR*);
  [propput] HRESULT displayLanguage([in] BSTR);
  [propput] HRESULT parentHWND([in] ULONG_PTR hwnd);
  [propget] HRESULT length([out, retval] int* index);
  [id(DISPID_VALUE), propget] HRESULT appWeb(
      [in] int index, [out, retval] IDispatch** app_web);
  HRESULT initialize();
  HRESULT checkForUpdate();
  HRESULT download();
  HRESULT install();
  HRESULT pause();
  HRESULT resume();
  HRESULT cancel();
  HRESULT downloadPackage([in] BSTR app_id, [in] BSTR package_name);
  [propget] HRESULT currentState([out, retval] VARIANT* current_state);
};

The IAppBundleWeb exposes methods as shown above to initialize & check for updates & download and install. Unfortunately the IAppBundleWeb->download exposes an arbitrary file read vulnerability to the users. The function that serve IAppBundle->download is AppBundleStateReady::DownloadPackage https://chromium.googlesource.com/external/omaha/+/e2c3f15816f1a394e56433de4fb58db30548fdb0/goopdate/app_bundle_state_ready.cc#73 which by itself call another function DoDownloadPackage https://chromium.googlesource.com/external/omaha/+/e2c3f15816f1a394e56433de4fb58db30548fdb0/goopdate/download_manager.cc#325
The DoDownloadPackage attempt to cache the package as soon it's possible. Unfortunately DownloadManager::CachePackage is done without impersonation as shown below
hr = CallAsSelfAndImpersonate2(
      this,
      &DownloadManager::CachePackage,
      static_cast<const Package*>(package),
      static_cast<const CString*>(&unique_filename_path));

DownloadManager::CachePackage will copy the file from %USER_TEMP%\%random_name%_chrome_installer.exe to C:\Program Files (x86)\Google\Update\Download\%random_gui%\%chrome_new_version%\%random_name%_chrome_installer.exe and since the user TEMP dir is write-able and C:\Program Files (x86)\Google\Update\Download ACL also allow read access the DownloadManager::CachePackage, we can easily redirect DownloadManager::CachePackage with a reparse point, so we can abuse the bug to read the users SAM file which contain the administrator password.
Several Notes;
Please use any version prior to the latest one to test the PoC, it's required to do that in order to make sure IAppBundleWeb->download succeed, I uploaded v87.0.4280.66 for testing
https://drive.google.com/file/d/1CRPpBCbVhjfYOgEq-5Gv6SWMOJFHPvFA/view?usp=sharing
And also make sure to kill any instance of GoogleUpdate.exe, and MAKE SURE THAT NOTHING lock the user temp directory such as OneDrive.exe or chrome.exe and optionally make sure to clean-up "C:\Program Files (x86)\Google\Update\Download"
Another note, sometime the PoC will drop an empty file due to a race failure, just redo the steps described above and run the PoC again.

The PoC has been tested in windows 10 20H2 with google chrome v87.0.4280.66

Reporter credit: Abdelhamid Naceri (halov)

## Attachments

- [GoogleOmaha.zip](attachments/GoogleOmaha.zip) (application/octet-stream, 195.3 KB)

## Timeline

### [Deleted User] (2021-03-27)

[Empty comment from Monorail migration]

### ke...@chromium.org (2021-03-29)

waffles@: Can you PTAL?

Also cc wfh@ who might have thoughts on this report.

[Monorail components: Internals>Updater]

### wa...@chromium.org (2021-03-30)

+sorin and ganesh.

### so...@chromium.org (2021-03-30)

This is a bug in Omaha not in the //chrome/updater.

[Monorail components: -Internals>Updater Internals>Installer]

### wf...@chromium.org (2021-03-30)

[Empty comment from Monorail migration]

### fo...@chromium.org (2021-03-31)

I've dug into this a bit, definitely the CachePackage call seems to be done under the service's identity which is going to be SYSTEM. I've no idea why exactly we download the file to the user's temporary directory only to copy it to the download cache. I guess it might be due to ensuring you perform the HTTP operation as the user incase there's a proxy or authentication needed to get out? It would still make far more sense to download the URL directly as SYSTEM into the the download cache, or at least modify the code to open the writable file as SYSTEM then the Web request itself could be run as the user and just write the file data into the existing cache file.

Incidentally it's probably slightly easier to exploit than it might first appear. The temporary directory is extracted using the ExpandEnvironmentStringsForUser API in base/app_util.cc!GetTempDirForImpersonatedUser, which reads the user's registry for the environment variables and doesn't cache the results. Therefore a user could change their own TMP environment variable in the registry to point to a path such as \\?\GLOBALROOT\SOMETHING which gives more control over the download and source file locations, for example you could get it to write to a localhost WebDAV share to capture the file name and switch the directory to grab the SAM. At the very least you wouldn't need to worry about any other application locking the temp folder as you could use a completely fresh one.

### so...@chromium.org (2021-03-31)

Yes, we want to download with the user identity for authentication purposes. Also, Omaha does several validations of the
file content. One validation is done when the file is written to the cache. Subsequent validations are also done when the file is read out from the cache. We don't assume that the files in the cache are trusted, but we prefer to not store untrusted files in the cache, as a defense in depth mechanism.


### fo...@chromium.org (2021-03-31)

Okay, well then one of two possible fixes come to mind. Either open the source file and use GetFinalPathNameByHandle to ensure the file you're copying it the file you expected to copy. Or open the source file as the user and then open the destination file as SYSTEM, then manually copy or move the file from that handle.

### ve...@gmail.com (2021-04-01)

If you could take my advice, the best solution here is to impersonate the user when opening the source file for reading.
This has been already implemented in chrome elevation service
https://chromium.googlesource.com/chromium/src/+/lkgr/chrome/elevation_service/elevated_recovery_impl.cc#114


### ga...@chromium.org (2021-04-01)

Thank you everyone, especially the OP and forshaw. We are taking the following fix:

"We now open the downloaded file as the current (impersonated) user. This ensures that we are not reading any privileged files that are otherwise inaccessible to the impersonated user.  We then hand-copy the file to the Package Cache unimpersonated, since the package cache is in a privileged location."

This fix is expected to start shipping out mid-April.

### [Deleted User] (2021-04-01)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-02)

[Empty comment from Monorail migration]

### am...@google.com (2021-04-07)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-04-07)

Congratulations, ve23halo@! The VRP Panel has decided to award you $5000 for this report. Nice work and thank you for reporting this issue to us!

### ve...@gmail.com (2021-04-07)

Thank You !

### am...@google.com (2021-04-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-05)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and Security_Impact labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues Impact guidelines: https://chromium.googlesource.com/chromium/src/+/master/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### wf...@chromium.org (2021-05-05)

Dear Sheriffbot. This doesn't require merging because the fix was shipped with Omaha. Adding tags, but please don't request a merge for me.

### ad...@chromium.org (2021-05-05)

This is delightful.

### [Deleted User] (2021-08-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pg...@google.com (2022-12-13)

[Empty comment from Monorail migration]

### pg...@google.com (2023-02-12)

[Empty comment from Monorail migration]

### pg...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### pg...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### is...@google.com (2023-07-28)

This issue was migrated from crbug.com/chromium/1193233?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055353)*

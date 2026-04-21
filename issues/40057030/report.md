# Security: RCE - Download Silently *.exe or *.dll to users Desktop or Downloads folder 

| Field | Value |
|-------|-------|
| **Issue ID** | [40057030](https://issues.chromium.org/issues/40057030) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Storage>FileSystem |
| **Platforms** | Windows |
| **Reporter** | ma...@gmail.com |
| **Assignee** | as...@chromium.org |
| **Created** | 2021-08-26 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

By holding for 5 seconds ENTER button, we can save any file to the user's desktop. For instance: virus.exe, user32.dll, or more.

**VERSION**  

Chrome Version: 92.0.4515.159 (Official Build) (64-bit) (cohort: Stable)  

Operating System: Windows (possible Linux and Mac vulnerable)

**REPRODUCTION CASE**  

Video Proof of Concept: <https://youtu.be/NIYMTTdWwOE>

I have created an example Proof of Concept:  

It is a simple game to hold the ENTER button to win $1,000,000 and rule the world! :)

Code Proof of Concept: <https://pulik.io/msexploit/rce> (make sure it is HTTPS, doesn't work in HTTP)

Game use case:  

The player holds the ENTER button for 5 seconds, and that's it.  

What happens?  

Exploit saves passwords.exe (with the folder icon) on users Desktop.  

There is a massive chance that the user open the passwords.exe

Exploit use case:

1. Silently download ransomware named passwords.exe that have folder icon to users Desktop
2. Silently download remote administration tool included in user32.dll to users Download folder, because it is a default Download folder,  
   
   user after time will download the legit .exe file, that can be vulnerable to DLL injection (RCE)
3. Silently download many random virus files to users random folders: "Desktop", "Downloads", "Documents", "Music", "Pictures", "Videos" folder. Wait for the user to open the virus.

Why is it a severe vulnerability?

- exploit works on production in Google Chrome and Microsoft Edge
- the user doesn't know that file is downloaded to one of the folders: "Desktop", "Downloads", "Documents", "Music", "Pictures", "Videos" or last position
- hacker can save any type of file for example: ".exe", ".bat", ".dll". Only .LNK is excluded.
- the user doesn't know what happened - can't read anything from pop-up - almost silence
- POSSIBLE RCE: we can save silence user32.dll to the DOWNLOAD folder and wait for the user to download legit .exe, which can be vulnerable to DLL injection (RCE)

In my opinion, the bug is Critical severity.

Google Team Users worth being added to CC, they were added in my last reports on a similar topic:  

[mek@chromium.org](mailto:mek@chromium.org)  

[asully@chromium.org](mailto:asully@chromium.org)  

[nattedted@chromium.org](mailto:nattedted@chromium.org)  

[amyressler@google.com](mailto:amyressler@google.com)

I can try to add an example with DLL Injection but need more time.

Exploit has more power when the user has unchecked "Show file extension" in file explorer. By default, the option is unchecked.

Solution:  

Default focus on the "Cancel" button in the "Save As" window.

\*\*\* On my site pulik.io there is included .exe to be downloaded. In the Attached file rce.html you need to add your own .exe file.

FAQ:

1. Does the exploit can download only one file?  
   
   No, we can download a new file every 1-2 seconds.
2. Why do I have an alert "passwords.exe already exists."  
   
   Yes, that means it is already saved. You need to delete it to rerun the exploit. To improve the exploit, we can add variables to local storage or cookies that the user already downloaded the file to avoid showing the save as dialog with alert.
3. How long user need to hold ENTER button?  
   
   I think 1-2 sec is enough to get the downloaded file

**CREDIT INFORMATION**

Reporter credit: Maciej Pulikowski (pulik.io)

## Attachments

- [rce.html](attachments/rce.html) (text/plain, 3.5 KB)
- [rceAPPDATA.html](attachments/rceAPPDATA.html) (text/plain, 3.5 KB)
- [env.html](attachments/env.html) (text/plain, 4.0 KB)
- [CommonFileDialogApp.cpp](attachments/CommonFileDialogApp.cpp) (text/plain, 10.4 KB)

## Timeline

### [Deleted User] (2021-08-26)

[Empty comment from Monorail migration]

### ma...@gmail.com (2021-08-27)

RCE via DLL injection:

Video Proof of Concept: https://youtu.be/xne97JN0MzA

Code PoC: https://pulik.io/msexploit/rceDLL

Applications are looking for required DLLs in predefined paths in the following order: application dir, system dir, windows dir, current dir, dirs listed in %PATH%. We can exploit this behavior by simply putting our dll right next to the application, in the folder where it is located. Since almost all Windows executables load version.dll I use my own "version.dll" library with some extra code which executes calc.exe and forwards rest of the calls (like GetFileVersionInfoA) to legitimate library in system32.

Please add Konrad Chrząszcz (konrad.chrzaszcz@gmail.com) to issue and update reporter credit:
Reporter credit: Maciej Pulikowski (pulik.io) and Konrad Chrząszcz

### dr...@chromium.org (2021-08-27)

This does not reproduce for me on Linux, but it does reproduce on Windows. asully@, mek@ - I'm not sure this is directly related to the File System API. Feel free to reassign to a better owner for the file picker.

I'm marking High Severity, since as far as I can tell, this only allows arbitrary files to be dropped in a well-known directory (https://wicg.github.io/file-system-access/#enumdef-wellknowndirectory), so it can't compromise arbitrary applications. But any exe in the Downloads folder could be affected by DLL injection. If there are further constraints on the downloaded data that would affect Severity, let me know.

[Monorail components: Blink>Storage>FileSystem]

### [Deleted User] (2021-08-27)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-28)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@gmail.com (2021-08-29)

It does reproduce on macOS (Catalina - 10.15.1) - however, trick with .dll will not work on macOS. 

On Windows, files can be dropped not only in the well-known directory, but we can also use system environment variables to save the File in different places.
Just need to change:
suggestedName: 'passwords'
to
suggestedName: '%APPDATA%filename.exe',
And the File will be downloaded to C:\Users\Maciej-pc\AppData\Roamingfilename.exe
I have attached rceAPPDATA.html with above example

We can combine system environment variables ex. '%HOMEDRIVE%%HOMEPATH%filename.exe'

In my opinion suggestedName should not accept '%' character.

To summarise we can save the File here:
- well-known directories: "desktop", "documents", "downloads", "music", "pictures", "videos"
- C:\Users\<user>\AppData
- C:\Users\<user>
- The last directory where file was downloaded

There are two more tricks I have tried to use, but not working:
1) Using syntax %windir:~2,1% to get only '\' character, but it doesn't work.
2) Save the File in C:\ (%windir%) or C:\Windows\system32 (%ComSpec%) but cannot do that because of permissions.

### ma...@gmail.com (2021-08-29)

Another thing is that we can read username on Windows.

let testA = await window.showSaveFilePicker({suggestedName: '%USERNAME%'})

When we read testA we get:
FileSystemFileHandle {kind: "file", name: "Maciej-pc"}

Username is "Maciej-pc".

Because of that we can guess that downloaded file path is C:/Users/Maciej-pc/<filename>.<extension>

Should I create new issue for system environment variables in suggestedName?

### ma...@gmail.com (2021-08-30)

After some research, I discovered that many popular services/applications recommend putting secrets in environments variables.

1) Microsoft Azure
https://docs.microsoft.com/en-us/azure/devops/pipelines/process/variables?view=azure-devops&tabs=yaml%2Cbatch
"We make an effort to mask secrets from appearing in Azure Pipelines output, but you still need to take precautions.
Never echo secrets as output. Some operating systems log command line arguments. Never pass secrets on the command line.
INSTEAD, WE SUGGEST THAT YOU MAP YOUR SECRETS INTO ENVIRONMENT VARIABLES."

2) Twilio
https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html
"There are some things we just shouldn’t share with our code.
These are often configuration values that depend on the environment such as debugging flags or ACCESS TOKENS for APIs like Twilio.
Environment variables are a good solution and they are easy to consume in most languages."

So we can create a list of popular environment variables that is a secret:
suggestedName: `
%username%@ //@ only to split variables
%USERDOMAIN%@
%SESSIONNAME%@
%COMPUTERNAME%@
%PROCESSOR_ARCHITECTURE%@
%PROCESSOR_IDENTIFIER%@
%KEY_VAULT_URL%@
%SECRET_NAME%@
%SECRET_VERSION%@
%AZURE_TENANT_ID%@
%AZURE_CLIENT_ID%@
%AZURE_CLIENT_SECRET%@
%TWILIO_ACCOUNT_SID%@
%TWILIO_AUTH_TOKEN%
f.f //filename
`
And the hacker could steal this informations

Video PoC: https://www.youtube.com/watch?v=q7OIEWtalg8

code PoC: https://pulik.io/msexploit/env (need to be https) or in attachments

### ma...@gmail.com (2021-09-07)

drubery@chromium.org I have created a new issue based on my comments 7 and 8

https://bugs.chromium.org/p/chromium/issues/detail?id=1247389

If you prefer to combine those issues and stick with only one issue please remove the new one.



### [Deleted User] (2021-09-10)

asully: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-09-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-26)

asully: Uh oh! This issue still open and hasn't been updated in the last 30 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-10-26)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### ma...@gmail.com (2021-11-21)

I would like to help more, so I tried to fix the bug by myself,  and here are some of my thoughts and solution. Maybe it will help somehow. 

Actual Result:
Holding the "ENTER" keyboard button on the website could cause opening the "Save As" dialog and automatically saving a file.

Expected Result:
Holding the "ENTER" keyboard button on the website could cause opening the "Save As" dialog but not saving a file. Users need to click the "ENTER" keyboard button once again or click the "SAVE" button in the saveAs dialog to download a file.

My thoughts and solution:

1. The first approach to fix the problem is to remove the focus from the Save button in the saveAs dialog. It could be done by adding dialog option: FOS_OKBUTTONNEEDSINTERACTION
	
FOS_OKBUTTONNEEDSINTERACTION -  The OK button will be disabled until the user navigates the view or edits the filename (if applicable). Note: Disabling the OK button does not prevent the dialog from being submitted by the Enter key.

(source: https://docs.microsoft.com/en-us/windows/win32/api/shobjidl_core/ne-shobjidl_core-_fileopendialogoptions)

To test the method, I have changed line 324:
https://source.chromium.org/chromium/chromium/src/+/main:ui/shell_dialogs/execute_select_file_win.cc;l=324
to :
DWORD dialog_options = FOS_OVERWRITEPROMPT | FOS_OKBUTTONNEEDSINTERACTION;

Indeed it removes focus from the Save button. However, it does not prevent the dialog from being submitted by the Enter key. In conclusion, removing focus from the "Save" button will not stop from saving button by the "ENTER" keyboard button.

The first solution doesn't work.

2. The second way is to use Hooks with the flag OFN_ENABLEHOOK  to stop the "ENTER" keyboard button. Nevertheless, after some research, I discovered that it only works with older API  - GetSaveFileName(), and chromium is already using a newer one. Moreover, the second problem is that using hooks removes the new UI for dialogs since win7. 

The second solution doesn't work.

btw. I can't debug execute_select_file_win.cc  in Visual Studio Code, because it is not included in debugging symbols file.

3. The third strategy is to use IFileDialogEvents ( source: https://docs.microsoft.com/en-us/windows/win32/api/shobjidl_core/nn-shobjidl_core-ifiledialogevents ). 
After some testing, I discovered that three events are always calling after opening IFileSaveDialog.

IFileDialogEvents::OnFolderChange - Called when the user navigates to a new folder.
IFileDialogEvents::OnFolderChanging - Called before IFileDialogEvents::OnFolderChange. This allows the implementer to stop navigation to a particular location.
IFileDialogEvents::OnSelectionChange - Called when the user changes the selection in the dialog's view.

The 4th is calling when the user is holding the "ENTER" keyboards button.
IFileDialogEvents::OnFileOk - Called just before the dialog is about to return with a result.

Straight to the point, the plan is to create a variable to collect a time when the user starts a dialog, then in OnFileOk check, if the period between start and saving file is at least 2 seconds. In my opinion, 2 seconds is enough for the user to stop holding the "Enter" button because he will get suspicious.

//PoC - Possible chromium solution
int dialogRunTime = 0; // When dialog started
bool isFirstTimeFolderChange = true;

//This event starts when dialog is opened
HRESULT CDialogEventHandler::OnFolderChange(IFileDialog*)
{    
    //save time when opened, only first time
    if(isFirstTimeFolderChange){
        dialogRunTime = GetTickCount();
        isFirstTimeFolderChange = false;
    }    
    return S_OK;
}

//This event starts before saving a file
HRESULT CDialogEventHandler::OnFileOk(IFileDialog*)
{
    int now = GetTickCount();
    int blockedSaveButtonFor = 2000; // 2 sec
    int diff = now - dialogRunTime;

    //Save clicked faster then 2 sec return false
    if (diff < blockedSaveButtonFor) {
        return S_FALSE;
    }

    return S_OK;
}

I have built a proof of concept of the above solution, and it WORKED, it is attached. It prevents saving for 2 seconds on Windows 10. 
The Events could be changed only when there is a suggested name of the filename.

Instead of preventing saving for 2 seconds, maybe there is a better way to ignore holding ENTER, but I couldn't find it.

However, I am not sure if interfering in events is not too much? What do you think?

Thanks,
Maciej Pulikowski

### ad...@google.com (2021-12-06)

Maciej thanks for thinking about possible fixes. I don't think we need additional information here. I know that asully@ and mek@ have some other things they're working on, but I'll ask them to add an update here with their plans.

### ad...@google.com (2021-12-06)

[Empty comment from Monorail migration]

### pw...@chromium.org (2021-12-06)

I think that there are two problems conflated here.

1) The user is tricked into accepting a file write. We discussed something similar in https://crbug.com/chromium/637098 and the constraints mentioned there are relevant.

2) Writing a malicious executable to the user's file system. Safe Browsing should provide a mitigation against that.

I propose that we assume the PoC only works because version.dll is not currently considered a malicious file, and focus the rest of the conversation on the dialog bypass issue.

### ma...@gmail.com (2021-12-07)

1) Never seen before the issue, it is a mine of information.

2) Safe Browsing by default blocks .dll files, but FileSystem API bypass warnings (with or without enhanced protection set ON in Safe Browsing), please check this video: https://www.youtube.com/watch?v=p-oVIeli5YM from https://crbug.com/chromium/1244076








### ct...@chromium.org (2021-12-07)

Agreed that it probably makes sense to handle https://crbug.com/chromium/1244076 separately (and drubery@ has raised some of the UX challenges for it on that bug already), so this bug can focus on problem (1). However, I do think that the severity of this overall issue might be lower if there wasn't the risk of things like DLL injection.

Some initial thoughts from re-reading https://crbug.com/chromium/637098 (to remember our previous discussions about `webkitdirectory`) and looking over these two issues:

- Could this be used to also overwrite an existing file, or will Windows trigger a separate prompt that won't get triggered automatically?
- Could we prevent triggering the filepicker dialog until keyup? This prevents the most direct keyjacking attack (having victim hold ENTER). While an attacker could get a user to instead repeatedly press ENTER, this would at least make the attack significantly more user-visible.
- Could we help a user who has accidentally fallen for this recover, beyond what the OS provides (e.g., the "Recents" view in Explorer showing an unintentionally downloaded file)?

The IFileDialogEvents solution that Maciej brought up in https://crbug.com/chromium/1243802#c16 seems like it could be a good solution as well to ensure that the user has seen the dialog, potentially letting us "cancel" the keypress until some time has passed. Conceptually, this seems similar to how we disable the "install" action in the extension install prompt for a few seconds to increase user comprehension and prevent clickjacking. However, I do not know enough about the Windows file picker dialog and the IFileDialogEvents API, so I can't comment on if we could actually implement this in practice, or how robust it would be.

### ma...@gmail.com (2021-12-07)

"- Could this be used to also overwrite an existing file, or will Windows trigger a separate prompt that won't get triggered automatically?"
No, we cannot overwrite existing files. Windows will trigger a separate prompt with focus on "cancel" button. 

"- Could we prevent triggering the filepicker dialog until keyup? This prevents the most direct keyjacking attack (having victim hold ENTER). While an attacker could get a user to instead repeatedly press ENTER, this would at least make the attack significantly more user-visible."
Maybe gesture limitation, Filesystem API could require mouse click gesture, and ignore keyboard gesture. 
However, it can be annoying for the user and give a lot of limitations to applications (keyboard shortcuts), for instance: www.vscode.dev ( Save As... - Ctrl + Shift + S )

Another idea for fix:
Let's take dangerous extensions: ".exe / .com / .msi / .dll / .src" and for them by default focus cancel button. Indeed is bad user experience, but only for dangerous files.
Disabling the Save button does not prevent the dialog from being submitted by the Enter key. Although maybe focusing Cancel Button prevents that?

Dangerous extensions list can be found here:

InsecureDownloadExtensions::kMSExecutable
https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/download/mixed_content_download_blocking.h;l=128?q=%22%22exe%22%22&ss=chromium%2Fchromium%2Fsrc

But there is missing dll extension, can be added:
{"dll", InsecureDownloadExtensions::kMSLibraries},














### pw...@chromium.org (2021-12-07)

[Comment Deleted]

### pw...@chromium.org (2021-12-07)

What https://crbug.com/chromium/1243802#c20 mentions is the executable file warning. We do additional checks for malicious content, both in downloads and in the File System Access API.

To try out the Safe Browsing checks, you can use the standardized test file at https://www.eicar.org/?page_id=3950 -- Chrome should block attempts to write the 68-character string there to a file.

### as...@chromium.org (2021-12-09)

https://crrev.com/c/3324687 just landed, which should fix the environment variable issue

### ma...@gmail.com (2021-12-10)

@pwnall 
Thanks for your explanation. Indeed to exploit the bug, the attacker needs a fully undetectable file. Otherwise, Safe browsing, Windows defender, or other AV will block it.

@asully
Would you please inform about it in the https://bugs.chromium.org/p/chromium/issues/detail?id=1247389 ?
Thank you for the fix :)

### as...@chromium.org (2021-12-10)

Whoops! Good catch. I forgot to tag both of these bugs. I left a comment and then closed the other bug

### ma...@gmail.com (2022-01-07)

any update?

### me...@chromium.org (2022-01-11)

One thing we could do is mirror pretty much what we ended up doing for the gesture laundering issue when showing a directory upload dialog: add an extra confirmation prompt (when saving to a sensitive/dangerous file). That probably could even just be the normal write access permission prompt that is shown if you try to write to a file that was opened in an open-file-dialog rather than a save-file-dialog. If it is merely to avoid the gesture laundering issue, we probably wouldn't even have to add extra text in that dialog why we're showing it, just showing it would be enough to alleviate the problem.

It wouldn't be the nicest user experience, but arguably not terrible either, and no worse than the directory upload behavior...

### ma...@gmail.com (2022-01-12)

Thank you for the answer.

In my opinion, it is a good move. I don't think many applications save files with dangerous extensions that way, so it shouldn't be a problem. The second thought is that users will only accept the write access permission prompt when they trust an owner of the website. In that case, they will not accept the prompt on a random dangerous page. Moreover, the extra benefit is that prompt will probably cancel holding ENTER action on every OS.

In conclusion, that solution is a good compromise.

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### ma...@gmail.com (2022-03-01)

any update?

### ad...@google.com (2022-03-23)

[Empty comment from Monorail migration]

### ad...@google.com (2022-03-28)

mek@/asully@ what needs to happen to make progress on https://crbug.com/chromium/1243802#c29? Do you need some PM input?

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### as...@chromium.org (2022-04-06)

[Empty comment from Monorail migration]

### aj...@chromium.org (2022-04-11)

[Empty comment from Monorail migration]

### as...@chromium.org (2022-04-18)

[Empty comment from Monorail migration]

### as...@chromium.org (2022-04-28)

We'll be adding a new prompt to be shown when saving a file with a dangerous extension. https://crbug.com/1320877 tracks the status of this new prompt


### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### sr...@google.com (2022-06-15)

Just to update the status of this security bug: there's active progress on the blocking bug as of June 7th

### ma...@gmail.com (2022-07-26)

Is there any update? 

### as...@chromium.org (2022-07-28)

I have a prototype CL up (https://crrev.com/c/3638058) but it's hung up on discussions with UX folks about the specifics of the buttons on the prompt. That thread was dropped for a while (and I was OOO for a bit) but I've since picked this back up and intend to land the CL as soon as we get agreement on the buttons.

### ma...@gmail.com (2022-07-30)

Thanks for the information and your work :)

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### as...@chromium.org (2022-08-16)

Fixed in https://crrev.com/c/3829770

### [Deleted User] (2022-08-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-16)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M104. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M105. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-16)

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

### [Deleted User] (2022-08-16)

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

### as...@chromium.org (2022-08-16)

Not requesting to merge as per https://crbug.com/1320877#c12 (hopefully sheriffbot will not add back these labels)

### am...@chromium.org (2022-08-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-08-30)

Congratulations, Maciej! The VRP Panel has decided to award you $3,000 for this report. Thank you for your efforts in reporting this to us and our your patience as the comprehensive work on the prompt upon download/saving files that was being worked after the initial systems environment variable exposure mitigation was already landed. Nice work and thanks again! 

### ma...@gmail.com (2022-08-30)

@amyressler
Thank you so much for the reward, and respect to the team for the fix, great work! :)
I have a stupid question, is there any chance that you can gift me a hoodie and cap from GoogleVRP? I would be super happy to have them xD

Also, could you save credits as:
Reporter credit: Maciej Pulikowski (@pulik_io) and Konrad Chrząszcz

Thanks again :)

### am...@google.com (2022-09-14)

[Empty comment from Monorail migration]

### ma...@gmail.com (2022-10-02)

amyressler@ 
I have a small question. I see that Chrome version 106 includes the fix.

Here is the news about Google Chrome 106 version https://chromereleases.googleblog.com/2022/09/stable-channel-update-for-desktop_27.html . The log shows the fix. However, the security bug is not listed.

Will the bug get a CVE number?

Thanks :)

### am...@chromium.org (2022-10-05)

Hi Maciej, thanks for bringing this to our attention! I was out sick when 106 release and security fix list was being put together so the person helping in my absence didn't have this whole batch of bugs solved by fix landed in https://crbug.com/chromium/1320877 on their radar at all. 

Despite my attempts at stop gaps to ensure that would not go untracked - after some troubleshooting - what I've discovered is that it seems that the build for 106 stable release was recut before release and the version number we used to feed out automation was an earlier version number than the version that was actually released, so it did not capture all the issues. We are running some clean up efforts right now and hope to have the CVEs, release notes, security fix lists, and acknowledgements updated by end of week. 

So TL;DR, this will get a CVE, but it may be a few more days. Apologies for the delay! 

### ma...@gmail.com (2022-10-06)

No worries, thank you for the update :)

### am...@chromium.org (2022-10-07)

+ pgrace@ for the manual release notes addition and CVE 

### pg...@google.com (2022-10-10)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-10-10)

Just circling back, CVE and release notes have been updated: https://chromereleases.googleblog.com/2022/09/stable-channel-update-for-desktop_27.html
Thank again for pointing this out and your patience while we got it updated! 

### ma...@gmail.com (2022-10-10)

@amyressler 
Thank you! I think it should be high, not low? 

### am...@chromium.org (2022-10-10)

The mitigation (adding a new prompt to be shown when saving a file with a dangerous extension) that shipped in this release and was resolved via the umbrella fix cl (https://crrev.com/c/3829770) is for the low severity aspect of this issue. The high severity aspect (environment variables issue) was resolved by and CVEed/reward/acknowledged via https://crbug.com/chromium/1247389 (https://crrev.com/c/3324687). Once the environment variables issue was mitigated, the remaining factor of the unprompted file save reduced down to low severity. I believed this was all covered in the comments above, but apologies for any confusion. 

### ma...@gmail.com (2022-10-13)

oh ok, thats fine. Thanks for information :) 

### pg...@google.com (2022-11-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1243802?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/chromium/1320877]
[Monorail mergedwith: crbug.com/chromium/1308132, crbug.com/chromium/1314937]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057030)*

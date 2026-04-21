# ProfilePickerHandler UAF via UI

| Field | Value |
|-------|-------|
| **Issue ID** | [376493203](https://issues.chromium.org/issues/376493203) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Profiles |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | no...@ssd-disclosure.com |
| **Assignee** | rs...@google.com |
| **Created** | 2024-10-31 |
| **Bounty** | $3,000.00 |

## Description

## Summary

Use after free in Profiles in Google Chrome allows a remote attacker who convinced a user to install a malicious extension to potentially exploit heap corruption via a crafted HTML page.

---

## Reproduction Case

1. For ease of reproduction, Apply `patch.diff`.
2. Press the UI button to open the `Chromium Profile Management` window.
3. Open a new tab, move to `chrome://profile-picker`, type `chrome.send("continueWithoutAccount", [0]);` into the `DevTools`'s console, and close the tab.

---

## Root Cause Analysis

`chrome/browser/ui/webui/signin/profile_picker_handler.cc`

```
void ProfilePickerHandler::HandleContinueWithoutAccount(
    const base::Value::List& args) {
  CHECK_EQ(1U, args.size());

  // profileColor is undefined for the default theme.
  std::optional<SkColor> profile_color;
  if (args[0].is_int())
    profile_color = args[0].GetInt();

  RecordProfilePickerAction(ProfilePickerAction::kLaunchNewProfile);
  ProfileMetrics::LogProfileAddNewUser(
      ProfileMetrics::ADD_NEW_PROFILE_PICKER_LOCAL);
  ProfilePicker::SwitchToSignedOutPostIdentityFlow(
      profile_color, profile_picked_time_on_startup_,
      base::BindOnce(
          &ProfilePickerHandler::OnProfileCreationFinished,
          // `OnProfileCreationFinished` is called when we want to close the
          // profile picker. `ProfilePickerHandler` will always be initialized
          // when we get to that call because the picker will still be open.
          base::Unretained(this))); // [0]
}

```

- `[0]`,`HandleContinueWithoutAccount` function transfers the `ProfilePickerHandler::OnProfileCreationFinished` function bound by the `this` pointer to the `ProfilePicker::SwitchToSignedOutPostIdentityFlow` function as a callback param.

`chrome/browser/ui/views/profiles/profile_picker_view.cc`

```
void ProfilePicker::SwitchToSignedOutPostIdentityFlow(
    std::optional<SkColor> profile_color,
    base::TimeTicks profile_picked_time_on_startup,
    base::OnceCallback<void(bool)> switch_finished_callback) {
  if (g_profile_picker_view) {
    g_profile_picker_view->SwitchToSignedOutPostIdentityFlow(
        profile_color, profile_picked_time_on_startup,
        std::move(switch_finished_callback)); // [1]
  }
}

```

- `[1]`, In order to execute the `g_profile_picker_view->SwitchToSignedOutPostIdentityFlow` functions, the value of the `g_profile_picker_view` pointer must be set in a normal flow.
- It is possible to create a complete chain that does not require user gestures by utilizing a chrome extension, but for simple proof, it is replaced by pressing a button directly to open the `Chromium Profile Management` window.

`chrome/browser/profiles/profile_manager.cc`

```
void ProfileManager::CreateMultiProfileAsync(
    const std::u16string& name,
    size_t icon_index,
    bool is_hidden,
    base::OnceCallback<void(Profile*)> initialized_callback,
    base::OnceCallback<void(Profile*)> created_callback) {
  DCHECK_CURRENTLY_ON(BrowserThread::UI);
  DCHECK(!name.empty());
  DCHECK(profiles::IsDefaultAvatarIconIndex(icon_index));

  ProfileManager* profile_manager = g_browser_process->profile_manager();

  ProfileAttributesStorage& storage =
      profile_manager->GetProfileAttributesStorage();
  base::FilePath new_path;
  ProfileAttributesEntry* entry = nullptr;

  do {
    new_path = profile_manager->GenerateNextProfileDirectoryPath();
    // The generated path should be unused and free to use.
    DCHECK_EQ(profile_manager->GetProfileByPath(new_path), nullptr);
    DCHECK(profile_manager->CanCreateProfileAtPath(new_path));

    entry = storage.GetProfileAttributesWithPath(new_path);
  } while (entry != nullptr);

  ProfileAttributesInitParams init_params;
  init_params.profile_path = new_path;
  init_params.profile_name = name;
  init_params.icon_index = icon_index;
  init_params.is_ephemeral = is_hidden;
  init_params.is_omitted = is_hidden;
  storage.AddProfile(std::move(init_params));

  base::ThreadPool::PostTask(
      FROM_HERE,
      {base::MayBlock(), base::TaskPriority::USER_BLOCKING,
       base::TaskShutdownBehavior::SKIP_ON_SHUTDOWN},
      base::BindOnce(&NukeProfileFromDisk, new_path,
                     base::BindOnce(&ProfileManager::CreateProfileAsync,
                                    profile_manager->weak_factory_.GetWeakPtr(),
                                    new_path, std::move(initialized_callback),
                                    std::move(created_callback)))); // [2]
}

```

- `[2]`, The callback function delivered in `[0]` was executed within the `initialized_callback` function, and it was posted to the thread pool to asynchronously process tasks.

`content/browser/webui/web_ui_message_handler.cc`

```
bool WebUIMessageHandler::IsJavascriptAllowed() {
  return javascript_allowed_ && web_ui() && web_ui()->CanCallJavascript(); // [3]
}

```

- `[3]`, the `ProfilePickerHandler::OnProfileCreationFinished` function posted in the thread pool is called back, and UAF occurs by referring to the `javascript_allowed_` variable of `WebUIMessageHandler` that has already been freed within the function.

---

## Bisect

<https://source.chromium.org/chromium/chromium/src/+/4dd469427e8a336a1ca52f9a523b78785bbdb897>

- In the process of reorganizing the function `ProfilePickerHandler::HandleCreateProfileAndOpenCustomizationDialog` to `HandleContinueWithoutAccount`, consideration of the lifetime of the object was omitted.

---

## Recommended Patch

`chrome/browser/ui/webui/signin/profile_picker_handler.h`

```
class ProfilePickerHandler : public content::WebUIMessageHandler,
                             public content::WebContentsObserver,
#if BUILDFLAG(IS_CHROMEOS_LACROS)
                             public AccountProfileMapper::Observer,
#endif  // BUILDFLAG(IS_CHROMEOS_LACROS)
                             public ProfileAttributesStorage::Observer {
...

  base::WeakPtrFactory<ProfilePickerHandler> weak_factory_{this};
};

```

- `weak_factory_` has already been declared within the `ProfilePickerHandler` class.

`fix.diff`

```
--- a/chrome/browser/ui/webui/signin/profile_picker_handler.cc	
+++ b/chrome/browser/ui/webui/signin/profile_picker_handler.cc	
@@ -617,7 +617,7 @@
           // `OnProfileCreationFinished` is called when we want to close the
           // profile picker. `ProfilePickerHandler` will always be initialized
           // when we get to that call because the picker will still be open.
-          base::Unretained(this)));
+          weak_factory_.GetWeakPtr()));
 }

 void ProfilePickerHandler::HandleGetSwitchProfile(

```

- UAF can be prevented by modifying the existing `base::Unretained(this)` to `weak_factory_.GetWeakPtr()` to verify that the object of the callback function is valid.

**It is dangerous because an attacker can use Extension to create PoCs that do not require separate user gestures.**

---

## Version

131.0.6776.0

## Credit

parkminchan, working for SSD Labs Korea.

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 68.9 KB)
- [patch.diff](attachments/patch.diff) (text/x-diff, 300 B)
- [proof.mov](attachments/proof.mov) (video/quicktime, 4.6 MB)

## Timeline

### sr...@google.com (2024-10-31)

Marking as S2 per the severity guidelines: "Memory corruption that requires a specific extension to be installed"

### pe...@google.com (2024-10-31)

Setting milestone because of s2 severity.

### pe...@google.com (2024-10-31)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### dr...@chromium.org (2024-11-04)

Assigning to dpapad for a question: this crash requires sending `chrome.send("continueWithoutAccount", [0])` from Dev tools. Is this something we actually need to fix? Should all our WebUIs be protected agains random `chrome.send()` commands from dev tools? This would be news to me, and we may have a lot of similar bugs, as I don't think this is a scenario we usually try to protect against.

Feel free to reassign to me (or close the bug if appropriate) after answering the question. Thank you!

### dp...@chromium.org (2024-11-04)

> Should all our WebUIs be protected agains random chrome.send() commands from dev tools?

AFAIK, any exploit that requires physical access to the DevTools console is considered low priority/severity. In the example above, if "0" is an invalid value, perhaps adding a CHECK() would be a good enough fix. Probably best to loop-in the security team for further guidance (cc'ed nasko@).

### na...@chromium.org (2024-11-07)

In general, if user is tricked into opening DevTools and executing code in it, a lot of damage can be inflicted in that manner. It is good to have the browser be resilient to unexpected output, that is just good engineering. We have an [FAQ entry](https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md#Does-entering-JavaScript_URLs-in-the-URL-bar-or-running-script-in-the-developer-tools-mean-there_s-an-XSS-vulnerability) that is not quite answer to this question, but it is very close.

### dp...@chromium.org (2024-11-08)

Assigning back to droger@ to address as you think is best given the guidance above.

### no...@ssd-disclosure.com (2024-11-10)

Hi,

There is no need to 'type' anything into the console - the console typing and patch is meant as means of easier reproduction and capturing of the root cause

Here are two less invasive method of triggering it

### Manual reproduction

1. For ease of reproduction, Apply `patch.diff`.
2. Press the UI button to open the `Chromium Profile Management` window.
3. Open a new tab, move to `chrome://profile-picker`, click `Add` button, and close the tab.

### Using Extension

`manifest.json`

```
{
  "name": "Test Extensions",
  "description" : "Test Ext",
  "version": "1.0",
  "background": {
    "scripts": ["background.js"]
  },
  "manifest_version": 2,
  "permissions": [
    "tabs"
  ]
}

```

`background.js`

```
  chrome.windows.create({ url: 'chrome://profile-picker' }, (tab) => {
    setTimeout(() => {
      chrome.windows.remove(tab.id);
    }, 10000);
  });

```

1. Please load the attached extension.
2. Press the `Add` button of the `profile-picker` on the tab.

If you are using multi-profile, the `profile-picker` appears by default when you start the chromium, so simply pressing the `Add` button once in the `profile-picker` that appears in a new tab is very reasonable.

**As a result, we can use extensions to trigger vulnerabilities with one click.**

### pe...@google.com (2024-11-22)

droger: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2024-12-07)

droger: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### dg...@chromium.org (2025-01-13)

[sign-in triager] [droger@google.com](mailto:droger@google.com), [rsult@google.com](mailto:rsult@google.com), PTAL for prioritisation

### dr...@chromium.org (2025-02-03)

Sorry for the delay. Assigning to Ryan who has been working on this code recently.

Ryan: if you think the scenario is not possible to encounter in practice (without the use of devtools or code changes), then we could consider adding a CHECK (see #comment6).
However if it's an actual concrete scenario we should rather handle it more gracfully (e.g. with weakpointer).

### rs...@google.com (2025-02-03)

I believe this scenario can happen in practice through the profile picker on slower machines but will most probably never happen.

However as demonstrated above, this can happen more easily through extensions (probably malicious ones only, since it would need a set of specific commands that are not useful otherwise) or the debugger tools.

For a more complete solution, I will then proceed with the suggested solution and simply use the weak pointer solution.

Patch is on the way.

Thank you all for the analysis!

### dr...@chromium.org (2025-02-03)

> I believe this scenario can happen in practice through the profile picker on slower machines

What would be the scenario? Is it:
- click on a button to create a profile
- while the profile is being created (which may require slow operation like creating a file on disk), manually close the picker

### rs...@google.com (2025-02-03)

Correct this was my thought, however I was not able to reproduce it.

We should also note that the view/handler closing is not immediate either (after closing window).

### ap...@google.com (2025-02-03)

Project: chromium/src  

Branch: main  

Author: Ryan Sultanem <[rsult@google.com](mailto:rsult@google.com)>  

Link:      <https://chromium-review.googlesource.com/6225319>

[ProfilePicker] Fix potential UAF in the handler

---


Expand for full commit details
```
[ProfilePicker] Fix potential UAF in the handler 
 
Details of the analysis and reason for the fix in the linked bug. 
 
Fixed: 376493203 
Change-Id: Id42f0af3f4e6a4318ed97c617c38a4ba75bea397 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6225319 
Reviewed-by: David Roger <droger@chromium.org> 
Commit-Queue: Ryan Sultanem <rsult@google.com> 
Cr-Commit-Position: refs/heads/main@{#1414896}

```

---

Files:

- M `chrome/browser/ui/webui/signin/profile_picker_handler.cc`

---

Hash: a7214df6d6c2bed2db9260f4f3bdac93e3e46342  

Date:  Mon Feb 03 06:58:07 2025


---

### sp...@google.com (2025-02-06)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
report of moderately mitigated memory corruption in a non-sandboxed process, mitigated by precondition to install extension and UI interaction


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-02-06)

Congratulations parkminchan! Thank you for your efforts and reporting this issue to us!

### ch...@google.com (2025-05-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> report of moderately mitigated memory corruption in a non-sandboxed process, mitigated by precondition to install extension and UI interaction

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/376493203)*

# Security: Chrome OS - Guest mode | critical commands via crosh which even persist guest by guest changes

| Field | Value |
|-------|-------|
| **Issue ID** | [40056100](https://issues.chromium.org/issues/40056100) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | he...@googlemail.com |
| **Assignee** | mn...@chromium.org |
| **Created** | 2021-06-03 |
| **Bounty** | $1,000.00 |

## Description

Hello,

When I was visiting my mother-in-law last weekend I had to use her Chromebook running

- Chrome OS v90.0.4430.218 (official build) (64-Bit)

in guest mode my very first time.

While reading the help text (here: shortcuts overview) I noticed a command to enter a console.

Unfortunately, I am wondering, why I am allowed to change system wide settings which even do persist guest by guest changes after rebooting.

In other words:

- I am able to execute the command "update_over_cellular disable"
- check tasks
- etc.

There is also the command

- vmc

I speculate whether I could export virtual machines to external storage and/or destroy/manipule stored VM via this command. These VMs might include sensitive/private data of the main users, probably (I don't know).

Steps:
================

1.) Enter guest mode
2.) Press Ctrl-Alt-T
==> shell opens
==> list of available commands is retreivable via the commend "help_advanced"

Expectation:
================

a) In my sight a guest user should not be allowed to execute commands which affect the system in general. Guest mode has to prevent this.
b) Should this is "working as intended" I would wonder why changed settings persist restarts of the guestmode; It cannot be that one is able to disable updates.
c) It is not a physical exploit, but a local one.


At the point I my sight guest mode has to be quasi read-only. Changes of any kind have to be reverted after restart.

Thank you for checking of this security issue.

Kind regards
A.

## Timeline

### [Deleted User] (2021-06-03)

[Empty comment from Monorail migration]

### bd...@chromium.org (2021-06-03)

Sending over to ChromeOS triage list

### mn...@chromium.org (2021-06-04)

Thanks for the report.

A couple points:
 * All storage of sensitive data is per-user and encrypted. This also includes VMs. I suspect the vmc commands will likely not work in guest mode though, but even if they do, the VM state would not leak out of the (ephemeral) guest session.
 * There are a couple system-wide settings that affect all users. This includes device-wide network settings, and also some auto-updating parameters (such as the one you found)
 * Whether a guest user should be able to manipulate the latter is a good question, but fundamentally these settings not being tied to user accounts is WAI. Note that you could also log in via your account and then make the same changes, and they would apply across all users.

I will raise question on whether the crosh shell should be available in guest mode internally, I can see the argument that it really doesn't mesh well with guest mode expectations.

### [Deleted User] (2021-06-04)

[Empty comment from Monorail migration]

### he...@googlemail.com (2021-06-04)

Keine Ursache.


To #1: Encryption sounds well, but, an exported VM could be brute-forced, I assume.

To #2: Yes. But they only have to set by authenticated users, aka admins, not by guests. A "bad" guest could disable updates, and a few month later some then revealed vulnerabilities can be expolited due to then missing updates.

To #3: Unfortunately, I cannot follow this. A guest mode usually cannot do anything else than read/write in a kind of sandbox, in other words all made changes are reverted for 100 %. In my reading this is confirmed in the FAQ: "If you share your computer with other people, take advantage of your operating system’s ability to manage multiple login accounts, and use a distinct account for each person. For guests, Chrome OS has a built-in Guest account for this purpose."

Mit freundlichen Grüßen / Kind regards

### [Deleted User] (2021-06-04)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### he...@googlemail.com (2021-06-25)

Hello,

regarding your explanation

" * All storage of sensitive data is per-user and encrypted. This also includes VMs. I suspect the vmc commands will likely not work in guest mode though, but even if they do, the VM state would not leak out of the (ephemeral) guest session."

The site

* https://chromium.googlesource.com/chromiumos/docs/+/refs/heads/stabilize-10575.54.B/security_severity_guidelines.md

explains that 

"Critical Severity
Critical severity issues breach vital security boundaries. The following boundaries are considered critical:

...
User isolation. One user can exploit another user or access the ENCRYPTED data of another user (i.e. crbug.com/764540)
...
They are normally assigned priority Pri-0 and assigned to the current stable milestone (or earliest milestone affected). For critical severity bugs, SheriffBot will automatically assign the milestone."

Unfortunately, I don't have experience with the VMC command, but it sounds like it would copy the encrypted containers of other users ... in other words a Pri-0 issue?

Kind regards and enjoy your weekend.


### mn...@chromium.org (2021-07-15)

In reply to #5: There are no admins by design on Chrome OS. There is also no fundamental conceptual difference between guests and authenticated users, in the default configuration anyone with a Google account can start an authenticated session.

As I explained before, vmc doesn't have access to other users' data since it's encrypted and thus inaccessible.

We discussed the case of update_over_cellular a bit, and I think the best way forward there is to either get rid of it entirely, make it a per-user setting, or disable in guest mode (in that order of preference). Filed internal tracking bug at b/193830029



### [Deleted User] (2021-08-05)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-16)

[Empty comment from Monorail migration]

### he...@googlemail.com (2022-02-25)

Hello together,

May I kindly ask you for a short update?

Thousand thanks in advance.

Best regards

### ki...@google.com (2022-02-25)

Hello,

In regards to updates over cellular, the setting is not available for control from crosh since CrOS version `14095.0.0`.

### he...@googlemail.com (2022-08-07)

[Comment Deleted]

### he...@googlemail.com (2022-08-24)

Helllo together,

Six months later - May I kindly ask you for a short update regarding this about 15 months old report? Unfortunately, I do not have access to the Issuetracker ticket (#8).

Thank you very much.

### si...@google.com (2022-08-25)

The update_over_cellular command was removed last year in crrev.com/c/3032431

Access to vmc in guest mode is not an issue, VM data is stored encrypted like other user data and so vmc won't be able to access data for logged-out users.

### [Deleted User] (2022-08-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-25)

[Empty comment from Monorail migration]

### am...@google.com (2022-10-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-10-14)

Congratulations Andr.Ess! The VRP Panel has decided to award you $1,000 as a thank you as a show of appreciation for reporting this issue to us. Thank you for your efforts in reporting this issue to us!

### am...@google.com (2022-10-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### is...@google.com (2023-05-24)

This issue was migrated from crbug.com/chromium/1215946?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056100)*

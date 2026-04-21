# Security: Heap-use-after-free in WaitForStoreInitializeTask::UpgradeDone

| Field | Value |
|-------|-------|
| **Issue ID** | [40066756](https://issues.chromium.org/issues/40066756) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Media>Feeds, UI>Browser>ContentSuggestions>Feed |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ji...@chromium.org |
| **Created** | 2023-07-03 |
| **Bounty** | $2,000.00 |

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

In WaitForStoreInitializeTask::MaybeUpgradeStreamSchema (<https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:components/feed/core/v2/tasks/wait_for_store_initialize_task.cc;l=87>), `UpgradeDone` is bound as a callback passed into `UpgradeFromStreamSchemaV0`:

```
void WaitForStoreInitializeTask::MaybeUpgradeStreamSchema() {  
  feedstore::Metadata metadata;  
  if (result_.startup_data.metadata)  
    metadata = \*result_.startup_data.metadata;  
  
  if (metadata.stream_schema_version() != 1) {  
    result_.startup_data.stream_data.clear();  
    if (metadata.gaia().empty()) {  
      metadata.set_gaia(stream_->GetAccountInfo().gaia);  
    }  
    store_->UpgradeFromStreamSchemaV0(  
        std::move(metadata),  
        base::BindOnce(&WaitForStoreInitializeTask::UpgradeDone,  
                       base::Unretained(this)));  
    return;  
  }  
  Done();  
}  

```

It is finally called and executed asynchronously in another threads in UpdateEntriesWithRemoveFilter(<https://source.chromium.org/chromium/chromium/src/+/main:components/leveldb_proto/internal/proto_leveldb_wrapper.cc;l=246>):

```
void ProtoLevelDBWrapper::UpdateEntriesWithRemoveFilter(  
    std::unique_ptr<KeyValueVector> entries_to_save,  
    const KeyFilter& delete_key_filter,  
    const std::string& target_prefix,  
    Callbacks::UpdateCallback callback) {  
  DCHECK_CALLED_ON_VALID_SEQUENCE(sequence_checker_);  
  task_runner_->PostTaskAndReplyWithResult(  
      FROM_HERE,  
      base::BindOnce(UpdateEntriesWithRemoveFilterFromTaskRunner,  
                     base::Unretained(db_), std::move(entries_to_save),  
                     delete_key_filter, target_prefix, metrics_id_),  
      std::move(callback));  
}  

```

With the destruction of FeedStream, WaitForStoreInitializeTask will also be destroyed. Since it is bound using base::Unretained(this), the Use-After-Free will be triggered when it is called.

There is another code(<https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:components/feed/core/v2/tasks/wait_for_store_initialize_task.cc;l=40>) that has the same Use-After-Free problem:

```
void WaitForStoreInitializeTask::ReadStartupDataDone(  
    FeedStore::StartupData startup_data) {  
  if (startup_data.metadata &&  
      startup_data.metadata->gaia() != stream_->GetAccountInfo().gaia) {  
    store_->ClearAll(base::BindOnce(&WaitForStoreInitializeTask::ClearAllDone,  
                                    base::Unretained(this)));  
    return;  
  }  

```

fix patch:

Use WeakPtr instead of Unretained(this) to protect the pointer in WaitForStoreInitializeTask or FeedStore.

**VERSION**  

Chrome Version: stable  

but need feature FeedWebUi.

Bisect:  

Code since <https://chromium.googlesource.com/chromium/src/+/44e3c31b37657ffad09b559762dda6fb46f2c767>

Operating System: TestOn MAC

**REPRODUCTION CASE**

Download asan-mac-release-1118297.zip(<https://storage.googleapis.com/chromium-browser-asan/mac-release/asan-mac-release-1165113.zip>) and unzip  

Start a http server at the folder of poc.html

Chromium --user-data-dir=test --enable-features=FeedWebUi poc.html

If it cannot be triggered, please fine-tune the timeout for closing the WebContent.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: anonymous

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 110 B)
- [asan](attachments/asan) (text/plain, 33.9 KB)

## Timeline

### [Deleted User] (2023-07-03)

[Empty comment from Monorail migration]

### ma...@google.com (2023-07-06)

Thanks for the report! I'm unable to repro this. (And it's unclear to me that with the given PoC it is possible to trigger this in a drive-by browsing context, since the site can't just close its own window unless it opened it somehow?)

The analysis and stack trace look believable though.

Feeds team, could you please look into this?

[Monorail components: Internals>Media>Feeds]

### ma...@google.com (2023-07-06)

(Speculatively setting OS labels for Desktop.)

### de...@chromium.org (2023-07-06)

adding to our component to get triaged.

[Monorail components: UI>Browser>ContentSuggestions>Feed]

### [Deleted User] (2023-07-17)

[Empty comment from Monorail migration]

### ji...@chromium.org (2023-07-27)

Dan, can you check if this is still the case?

### ha...@google.com (2023-08-10)

Hi, this is only a bug when FeedWebUi is enabled, and we're not currently planning on enabling that feature any time soon. For this reason, we're not prioritizing a fix

### ma...@google.com (2023-08-10)

Understood. That's why we're tracking it as Security_Impact-None for now.

If there is a tracking bug for the FeedWebUi feature, could you mark that as blocked on this issue perhaps? 


### am...@chromium.org (2023-11-14)

[security shepherd] Hi harringtond@ this issue has been active for some time, and while there is no SLO for issues in unlaunched features (other than the issue being resolve by OT, field experiments, or launch). However, it is not idea to have long-existing high severity security issues in an attack surface that is not being actively developed. Given that there is no launch bug in monorail to make this issue a blocker of and there are no plans to enable FeedWebUI "any time soon", I would like to suggest considering the removal of FeedWebUI code until there are plans to actively develop this feature. Is that something that could be considered? 

### ha...@google.com (2023-11-15)

[Empty comment from Monorail migration]

### ch...@chromium.org (2023-12-01)

[security shepherd]

dewittj@: Could you please take another look at this bug? Is there a bug for FeedWebUi code removal that we can mark this blocked on?

### de...@chromium.org (2023-12-01)

[Empty comment from Monorail migration]

### ja...@chromium.org (2024-01-17)

Hi jianli@, can you consider removing the FeedWebUi code removal suggestion from https://crbug.com/chromium/1459958#c9 and post an update to this bug? Thanks!

[secondary security shepherd]

### ja...@chromium.org (2024-01-17)

I also followed up with jianli over email.

[secondary security shepherd]

### ji...@chromium.org (2024-01-18)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2024-01-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/85c26bc2bced149f6f1ff5e37e8d6e1026d14df4

commit 85c26bc2bced149f6f1ff5e37e8d6e1026d14df4
Author: Jian Li <jianli@chromium.org>
Date: Thu Jan 18 01:30:54 2024

Pass weak pointer in WaitForStoreInitializeTask

Bug: 1459958
Change-Id: I3c64cdf3de797f7c31cf5666edbcd84139a9fd8d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5208492
Reviewed-by: Dan H <harringtond@chromium.org>
Commit-Queue: Jian Li <jianli@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1248517}

[modify] https://crrev.com/85c26bc2bced149f6f1ff5e37e8d6e1026d14df4/components/feed/core/v2/tasks/wait_for_store_initialize_task.cc
[modify] https://crrev.com/85c26bc2bced149f6f1ff5e37e8d6e1026d14df4/components/feed/core/v2/tasks/wait_for_store_initialize_task.h


### ji...@chromium.org (2024-01-18)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-19)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-19)

[Empty comment from Monorail migration]

### am...@google.com (2024-01-25)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-01-25)

Congratulations! The VRP Panel has decided to award you $2,000 for this report of a highly mitigated security bug, mitigated by shutdown and difficulty to trigger in a real-world scenario  + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2024-01-27)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-27)

This issue was migrated from crbug.com/chromium/1459958?no_tracker_redirect=1

[Multiple monorail components: Internals>Media>Feeds, UI>Browser>ContentSuggestions>Feed]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-04-26)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40066756)*

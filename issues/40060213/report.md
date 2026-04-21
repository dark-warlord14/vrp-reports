# Security: UAF in PermissionAuditingService multiple functions

| Field | Value |
|-------|-------|
| **Issue ID** | [40060213](https://issues.chromium.org/issues/40060213) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Permissions |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | et...@gmail.com |
| **Assignee** | hk...@chromium.org |
| **Created** | 2022-07-08 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**

## Root Cause

### case1

[0] PermissionAuditingService is derived from KeyedSerive, and will be release after the browser closed.

[1] The ExpireOldSessions task with this->AsWeakPtr() will be periodically sent to the thread pool by the timer in PermissionAuditingService::StartPeriodicCullingOfExpiredSessions, but WeakPtrs are \*\*not\*\* safe to use across multiple threads.

[2] PermissionAuditingService may be destroyed on the UI thread while ExpireOldSessions is running. Since PermissionAuditingService has been released at this time, accessing backend\_task\_runner\_ or db\_ will trigger UAF.

```
class PermissionAuditingService  
    : public KeyedService,       //<--------------[0]  
      public base::SupportsWeakPtr<PermissionAuditingService> {  
 public:  
  ...  
  scoped_refptr<base::SequencedTaskRunner> backend_task_runner_;  
  
  // Lives on the |backend_task_runner_|, and must only be accessed on that  
  // sequence. It is safe to assume the database is alive as long as |db_| is  
  // non-null.  
  raw_ptr<PermissionAuditingDatabase> db_ = nullptr;  
  
  base::RepeatingTimer timer_;  
};  

```
```
void PermissionAuditingService::StartPeriodicCullingOfExpiredSessions() {  
  timer_.Start(  
      FROM_HERE, kUsageSessionCullingInterval,  
      base::BindRepeating(&PermissionAuditingService::ExpireOldSessions,  
                          this->AsWeakPtr())); //----->[1]  
}  

```
```
void PermissionAuditingService::ExpireOldSessions() {  
  DCHECK(db_);  
  backend_task_runner_->PostTask( //----->[2] use!  
      FROM_HERE,  
      base::BindOnce(base::IgnoreResult(  
                         &PermissionAuditingDatabase::DeleteSessionsBetween),  
                     base::Unretained(db_), base::Time(),//----->[2] use!  
                     base::Time::Now() - kUsageSessionMaxAge));  
}  

```

[0] <https://source.chromium.org/chromium/chromium/src/+/main:components/permissions/permission_auditing_service.h;l=35;drc=2e15a0e74d1dfcd7a8f6f71b2fc5eea6019cbe25>

[1] <https://source.chromium.org/chromium/chromium/src/+/main:components/permissions/permission_auditing_service.cc;l=49;drc=d2cbb53c13bf4edc62b018a2c2276f9df2393ac6>

[2] <https://source.chromium.org/chromium/chromium/src/+/main:components/permissions/permission_auditing_service.cc;l=111;drc=d2cbb53c13bf4edc62b018a2c2276f9df2393ac6>

### case2

[0] the same as above.

[1] The StartPeriodicCullingOfExpiredSessions task with WeakPtr will be sent to the thread pool in PermissionAuditingServiceFactory::BuildServiceInstanceFor, but WeakPtrs are \*\*not\*\* safe to use across multiple threads.

[2] PermissionAuditingService may be destroyed on the UI thread while StartPeriodicCullingOfExpiredSessions is running. Since PermissionAuditingService has been released at this time, accessing this or timer\_ will trigger UAF.

```
KeyedService\* PermissionAuditingServiceFactory::BuildServiceInstanceFor(  
    content::BrowserContext\* context) const {  
  if (!base::FeatureList::IsEnabled(features::kPermissionAuditing)) {  
    return nullptr;  
  }  
  auto backend_task_runner = base::ThreadPool::CreateSequencedTaskRunner(  
      {base::MayBlock(), base::TaskPriority::USER_VISIBLE,  
       base::TaskShutdownBehavior::BLOCK_SHUTDOWN});  
  auto\* instance =  
      new permissions::PermissionAuditingService(backend_task_runner);  
  base::FilePath database_path =  
      context->GetPath().Append(FILE_PATH_LITERAL("Permission Auditing Logs"));  
  instance->Init(database_path);  
  AfterStartupTaskUtils::PostTask(  
      FROM_HERE, backend_task_runner,  
      base::BindOnce(&permissions::PermissionAuditingService::  
                         StartPeriodicCullingOfExpiredSessions,  
                     instance->AsWeakPtr()));//----->[1]   
  return instance;  
}  

```
```
void PermissionAuditingService::StartPeriodicCullingOfExpiredSessions() {  
  timer_.Start(//--->[2] use !  
      FROM_HERE, kUsageSessionCullingInterval,  
      base::BindRepeating(&PermissionAuditingService::ExpireOldSessions,  
                          this->AsWeakPtr())); //--->[2] use !  
}  

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/permissions/permission_auditing_service_factory.cc;l=60;drc=d2cbb53c13bf4edc62b018a2c2276f9df2393ac6>

[2] <https://source.chromium.org/chromium/chromium/src/+/main:components/permissions/permission_auditing_service.cc;l=46;drc=d2cbb53c13bf4edc62b018a2c2276f9df2393ac6>

### case3

In fact it is not safe to post an unretain pointer to db\_ in the thread pool in PermissionAuditingService::ExpireOldSessions, although db\_ release [0] and PermissionAuditingDatabase::DeleteSessionsBetween [1] are both executed in the same thread(backend\_task\_runner\_), which makes it appear safe.

But in fact, since the destructor of PermissionAuditingService is executed on the UI thread, if we add sleep here in [2], it will execute DeleteSoon and DeleteSessionsBetween sequentially in backend\_task\_runner\_, but due to competition, db\_ has not been set to nullptr at this time , so the UAF will be triggered here at [3].

I have attached patch3.diff and asan3.txt to demonstrate the problem.

```
PermissionAuditingService::~PermissionAuditingService() {  
  if (db_) {  
    backend_task_runner_->DeleteSoon(FROM_HERE, db_.get());//-->[0]  
    sleep(5); //-->[2]  
    db_ = nullptr;  
  }  
}  
  
void PermissionAuditingService::ExpireOldSessions() {  
  DCHECK(db_);  
  backend_task_runner_->PostTask(  
      FROM_HERE,  
      base::BindOnce(base::IgnoreResult(  
                         &PermissionAuditingDatabase::DeleteSessionsBetween),//-->[1]  
                     base::Unretained(db_), base::Time(),  
                     base::Time::Now() - kUsageSessionMaxAge));  
}  
  
bool PermissionAuditingDatabase::DeleteSessionsBetween(base::Time start_time,  
                                                       base::Time end_time) {  
  std::vector<int> ids;  
  sql::Statement statement(  
      db_.GetCachedStatement(SQL_FROM_HERE,//----->[3]  
                             "DELETE FROM uses"  
                             "WHERE usage_start_time BETWEEN ? AND ? "  
                             "OR usage_end_time BETWEEN ? AND ?"));  

```

This problem also occurs in the other function.

\*\*Since this has multiple paths that could lead to different UAFs, this could be a serious bug, please fix it soon.\*\*

## Other

### Vulnerability introduction

PermissionAuditingService is a service which allows to store and audit the basic information about the permissions usage.

The introduction of this vulnerability occurred in this commit on 2020-11-25

<https://source.chromium.org/chromium/chromium/src/+/a100f65b87f52f51dd78b4146b0755b46981568e>

### Repair suggestion

remove backend\_task\_runner\_ and use SequenceBound on the object to ensure that the tasks the object are running and the object itself are running on the same thread.

You can refer to this patch for a similar vulnerability.  

<https://chromium.googlesource.com/chromium/src/+/a8c9672ab894bf904cef2ff5c18dd3e077456b2b>

**VERSION**  

Chrome Version: Not sure  

Operating System: All

**REPRODUCTION CASE**  

[0] apply patch1.diff to repro case1 or patch2.diff to repro case2 or patch3.diff to repro case3, and build chromium with asan.

[1] python3 -m http.server 8000

[2] Run: `out/release/chrome --user-data-dir=./userdata --enable-features=PermissionAuditing http://127.0.0.1:8000/poc.html`

If all goes well, wait 5s, you should see a browser close, then trigger the UAF. You can also adjust the poc to set the SetTimeout.

Note that these vulnerability function is not only called when the browser is opened, some of them is timer function that will periodically call , potentially triggering the UAF anytime the user is using the browser.

In fact this is a race issue, I was working on chrome rce recently, but one of my fuzzes hit the issue, and through the asan log I recovered the root cause of it.

After auditing, there are potential problems in multiple similar usages, I will point out them.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see asan file

**CREDIT INFORMATION**  

Reporter credit: Nan Wang(@eternalsakura13) and Guang Gong of 360 Vulnerability Research Institute

## Attachments

- [asan1.txt](attachments/asan1.txt) (text/plain, 19.6 KB)
- [asan1.1.txt](attachments/asan1.1.txt) (text/plain, 27.9 KB)
- [asan2.txt](attachments/asan2.txt) (text/plain, 20.2 KB)
- [asan3.txt](attachments/asan3.txt) (text/plain, 23.4 KB)
- [patch1.diff](attachments/patch1.diff) (text/plain, 2.5 KB)
- [patch2.diff](attachments/patch2.diff) (text/plain, 1.9 KB)
- [patch3.diff](attachments/patch3.diff) (text/plain, 1.8 KB)
- [poc.html](attachments/poc.html) (text/plain, 177 B)
- [repro.mp4](attachments/repro.mp4) (video/mp4, 2.1 MB)

## Timeline

### [Deleted User] (2022-07-08)

[Empty comment from Monorail migration]

### et...@gmail.com (2022-07-08)

Sorry, I forgot a paragraph when copying the report.

### About Patch
In fact, adding sleep and adjusting the timer timing through patch is only for the convenience of reproducing the vulnerability.
It should be possible to reproduce the vulnerability without any patches.

For example, when I reproduced case2 through patch2.diff, I also reproduced case1 by chance, but I did not add sleep and modify the timer in ExpireOldSessions at this time.

As a proof, I keep this asan log attached as asan1.1.txt.

### dc...@chromium.org (2022-07-08)

This looks legitimate to me. WeakPtr is indeed unsafe to deref on a different thread than the thread the WeakPtrFactory is destroyed on.

The destruction of db_ and the posted tasks *would* be safe normally (since they are all sequenced through background_task_runner_).

However:
- the timer is owned on the UI thread but fires on `background_task_runner_`. This is not safe, per the comments in base/timer/timer.h: https://source.chromium.org/chromium/chromium/src/+/main:base/timer/timer.h;l=52;drc=f16856869e022ea1a4620ce5102fbc414db62e04
- the task bound to the timer runs on `background_task_runner_` but accesses state that lives on the UI thread (specifically, dereferencing `db_`

One way to make this safe is to add a helper class that owns `db_` and `timer_` and lives on `background_task_runner_` with the help of something like `base::SequenceBound`.

(Is Permission auditing off by default? I found https://source.chromium.org/chromium/chromium/src/+/main:chrome/common/chrome_features.cc;l=735;drc=d2cbb53c13bf4edc62b018a2c2276f9df2393ac6 which seems to indicate that, but I can't easily tell if something else enables it by default somehow)

Tentatively marking as high severity since this is a UaF in the browser process but requires user interaction to make profiles go away. However, if this is disabled by default, then I think this would drop to None.

If the feature is disabled by default, then this woul

[Monorail components: Internals>Permissions]

### [Deleted User] (2022-07-08)

[Empty comment from Monorail migration]

### dc...@chromium.org (2022-07-08)

> If the feature is disabled by default, then this woul

This should be "if the feature is disabled by default, then this would have a severity of none"

### et...@gmail.com (2022-07-09)

re https://crbug.com/chromium/1342896#c3:
thanks for the addition :), I think the issue should be clear now.


### [Deleted User] (2022-07-09)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### et...@gmail.com (2022-07-12)

[Comment Deleted]

### en...@chromium.org (2022-07-12)

Kamila, can you please look at this while I am OOO? My understanding is that the feature is, and always has been, fully disabled, and we are not even creating an instance of PermissionAuditingService unless the feature is enabled. So while this report needs to be addressed and the issues need to be fixed, there is not much urgency as the security impact is none.

### en...@chromium.org (2022-07-12)

Instead of "not much urgency",  what I really wanted to say is that:

 1) Please verify ASAP that my understanding of Security-Impact-None is correct.
 2) If so, then this isn't an emergency, but let's aim to get this fixed in the next month or so.

Here is the relevant check that I used for my assessment:

https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/permissions/permission_auditing_service_factory.cc;l=43-47;drc=a8c0b3303da785a9777aa25bd465a2a9690f1ca5

### hk...@google.com (2022-07-12)

I can confirm: 
1. The feature was fully disabled and never launched (through finch or otherwise). 
2. No user-visible flags so the user can't opt in. 

I also double checked that we are not creating an instance of PermissionAuditingService unless the feature is enabled. 

dcheng@ based on the above does this count as Security-Impact-None? 

### et...@gmail.com (2022-07-13)

[Comment Deleted]

### [Deleted User] (2022-07-22)

hkamila: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-07-28)

Adjusting to SI-None based https://crbug.com/chromium/1342896#c11. While the timelines for high severity fixes are not the same as for those in SI-None issues, please ensure this issue is fixed before the feature is launched (even for experiments) or could be made accessible. 

Also any type of ballpark ETA of fix or next action date that could be added to this issue would be helpful and avoid other additional check-ins from security marshals like this one. :) 

### et...@gmail.com (2022-08-11)

hello, is anyone working on fixing this bug?


### et...@gmail.com (2022-09-02)

friendly ping :)
any update?

### hk...@google.com (2022-09-02)

As this feature is not being launched for the foreseen future, I will attend to the issue by 108 branch. Thanks for pinging!

### hk...@google.com (2022-09-14)

[Empty comment from Monorail migration]

### en...@chromium.org (2022-09-14)

This issue has currently no impact and we will not enable this code in the near future. We are planning to get to it by M109, but decreasing priority to P2.

### et...@gmail.com (2022-11-03)

I noticed that dev is already 109, when will this bug be fixed? thanks :)


### am...@chromium.org (2022-11-16)

Hi Nan Wang, as stated in the comments there is no SLO for security_impact-none bugs. The only SLO for fix is before the feature is launched/enabled.

khamila@ and engedy@ that being said, it may be helpful to set a next action date to avoid additional pings from the reporter and from the security marshals that follow up on this bug (like myself) next. Thank you for the context in https://crbug.com/chromium/1342896#c19 however, that is most helpful to us as we check in on open/assigned security bugs. Thank you! 

### hk...@google.com (2022-11-16)

Thanks for the ping, I'm updating the milestone. 

### am...@chromium.org (2022-11-21)

Thanks, correcting milestone label :) 

### ma...@google.com (2022-12-21)

Security marshal checking in. Based on M111 feature freeze, I'll set a NextAction date for after the holidays here.

### et...@gmail.com (2023-01-20)

friendly ping :)
I noticed that this issue has been delayed for too long...
Is anyone fixing multiple bugs mentioned in this issue? Thanks :)

### hk...@google.com (2023-01-20)

It's on my plate, but M111 sounds unlikely due to competing priorities. 

### ja...@chromium.org (2023-02-03)

[security marshal] Hi hkamila@, are you on track for M-112? Maybe you can provide a status update and set the NextAction date. Thanks!

### ja...@chromium.org (2023-02-06)

Updating NextAction date to check back with the owner next week.

### hk...@google.com (2023-02-20)

[Empty comment from Monorail migration]

### hk...@google.com (2023-02-20)

[Empty comment from Monorail migration]

### hk...@google.com (2023-02-20)

[Empty comment from Monorail migration]

### et...@gmail.com (2023-03-15)

Friendly ping

### do...@chromium.org (2023-03-28)

Hey permissions folks, friendly security marshall here. This is our 6th oldest open high severity security bug, and it's getting awfully close to a year of being open. Is there a way we can get some movement on the audit here? Thanks!

### hk...@google.com (2023-03-28)

I'm working on the fix, targeting upcoming branch point M114. Sorry for the delay.

### jd...@chromium.org (2023-03-28)

[Comment Deleted]

### jd...@chromium.org (2023-03-28)

[Comment Deleted]

### me...@chromium.org (2023-04-11)

hkamila: Curious if you had a chance to look at this yet? Thanks!

### et...@gmail.com (2023-05-17)

hello, any update?

### hk...@google.com (2023-05-19)

Thanks for your patience, this is still in my plate. I have a cl in progress I didn't get around to finishing yet, but I'll aim to send it for review next week. I set an "next action" as a reminder to give an update. 

### en...@chromium.org (2023-06-09)

I looked into this briefly. The three UAFs outlined in this bug and the UAFs in the two de-duped bugs are all due to the same root cause, namely, that `PermissionAuditingServiceFactory::BuildServiceInstanceFor` posts the after-start-up task to `PermissionAuditingService::StartPeriodicCullingOfExpiredSessions` incorrectly to the `background_task_runner`, instead of the UI thread, i.e. `base::SequencedTaskRunner::GetCurrentDefault()`. We then snowball from there, and start doing nonsensical things starting the `timer_` on the background thread pool [2] instead of UI thread, because `Start()` it uses the current default task runner by default; accessing weak pointers on the wrong thread [3]; and posting from the background thread pool to the background thread pool [4], even though the next queued task might be the DeleteSoon on the `db_`.

All of these are consequences of `PermissionAuditingService` methods running on the background thread pool, which should never happen.

We should first land a quick fix to `BuildServiceInstanceFor` so that it uses the right task runner for the delayed task. Then, as suggested above, instead of rolling our own implementation of `base::SequenceBound`, which is essentially what we do today, we should migrate to just using `base::SequenceBound`. We might also want to add a `base::SequenceChecker` to `PermissionAuditingService` itself. If we already have an implementation to migrate this to `base::SequenceBound`, we might even skip the first step.

In terms of severity -- as it was pointed out by other security shepherds -- it seems to me that this requires a very well-timed shutdown very close to startup. Since a general shutdown bug is high, I think the timing restrictions make this a medium severity bug.

[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/permissions/permission_auditing_service_factory.cc;l=62;drc=8dec793f15aab029b66c7d345697f20bfc5619b8
[2] https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:components/permissions/permission_auditing_service.cc;l=47;drc=d9095892389e9b1be3b9068feb1330d87f35c61e
[3] https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:components/permissions/permission_auditing_service.cc;l=50;drc=d9095892389e9b1be3b9068feb1330d87f35c61e
[4] https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:components/permissions/permission_auditing_service.cc;l=112;drc=d9095892389e9b1be3b9068feb1330d87f35c61

### et...@gmail.com (2023-06-09)

[Comment Deleted]

### et...@gmail.com (2023-06-09)

I have noticed that the fix for this vulnerability requires a significant amount of time. If there are currently no plans to address and fix it, and if there are no plans to ship this feature to the stable version, would it be possible to completely remove the relevant code in order to resolve this vulnerability?
In addition, this issue involves multiple vulnerabilities in different RCAs, please consider this when rewarding :)
Thanks

### gi...@appspot.gserviceaccount.com (2023-06-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b45f52fceb999a2c069c5abf867d041c914b46d1

commit b45f52fceb999a2c069c5abf867d041c914b46d1
Author: Kamila <hkamila@google.com>
Date: Fri Jun 16 14:19:44 2023

Fix threading PermissionAuditingService.

In PermissionAuditingService, the after start-up task should be
posted to the UI thread as opposed to the background thread pool.

Bug: 1342896
Change-Id: I44d344884f18e37ae4058179d760f7d828b49afc
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4620687
Commit-Queue: Kamila Hasanbega <hkamila@google.com>
Auto-Submit: Kamila Hasanbega <hkamila@google.com>
Reviewed-by: Balazs Engedy <engedy@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1158813}

[modify] https://crrev.com/b45f52fceb999a2c069c5abf867d041c914b46d1/chrome/browser/permissions/permission_auditing_service_factory.cc


### et...@gmail.com (2023-06-30)

Could you please mark it as Fixed so it can enter the reward process. Thanks :)


### hk...@google.com (2023-07-04)

Yes. Thanks! 

### [Deleted User] (2023-07-04)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-04)

[Empty comment from Monorail migration]

### am...@google.com (2023-07-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-07-19)

Congratulations Nan Wang and Guang Gong! The VRP Panel has decided to award you $3,000 for this report of a security bug, mitigated by race condition and shutdown, limiting attacker control. Included in the reward amount is also a $1,000 bisect bonus. While there were two UAFs, as per https://crbug.com/chromium/1342896#c42, there was a single root cause, so we have assessed this as a single issue. 
Thank you for your efforts and reporting this issue to us.  

### am...@google.com (2023-07-22)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-10-10)

This issue was migrated from crbug.com/chromium/1342896?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1392107, crbug.com/chromium/1400581]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060213)*

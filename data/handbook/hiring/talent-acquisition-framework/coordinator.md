---
title: "Candidate Experience Specialist Responsibilities"
description: "This page is an overview of the processes, and systems that the Candidate Experience Team is responsible for."
---

The CES team utilizes [GitLab Service Desk](https://docs.gitlab.com/ee/user/project/service_desk/) and ModernLoop to track all incoming requests to the CES team. If you are a GitLab team member and you have a request or question for the Candidate Experience team, email `ces@gitlab.com` and an issue will automatically be created within the CES Service Desk. Please see the [alignment page](/handbook/hiring/) to learn more about which CES team member will be working on your requests. Our team leverages ModernLoop for interview scheduling, seamlessly connecting with our existing calendar and ATS.

#### How the CES Team will run the Service Desk

1. Under this [CES Service Desk Project](https://gitlab.com/gl-talent-acquisition/ces-service-desk) set up the proper notifications
   - Click on the bell icon on the top right next to Star and Clone
   - Go to Custom Settings
   - Check "Issue is Created"
   - Close out the window
1. On the left-side menu bar click Issues
   - This is where all our incoming CES emails will create an issue. You'll get an alert when someone sends an email to the CES email alias. Any "emails" that need to be addressed will be an open issue listed within this project.
1. Each CES will begin their workday by triaging issues within the Service Desk and their personal Board by adding the appropriate label to the issue.
   1. Click on the new Issue
   1. If unassigned, assign it to yourself or the responsible CES on the right-side toolbar
   1. Read the Issue message
   1. Labeling - each issue will need to be labeled with at least one appropriate label.
   1. If you need to respond to the "email" by adding comments to the issue, be sure to enter comments as you would an email to the candidate. Always assume that a candidate could be included in any email.
   1. If no action is needed and the issue has been solved, you may close it. Do not close issues until you have resolved the problem you are solving.
1. Board Creation - to view and manage assigned issues in one place
   1. Under “Plan” on left hand menu, click “Issue Boards”
   1. Click name of Team Member that is the current board view (e.g. “Alice”)
   1. Click “Create new Board”
   1. Title new board as the name of the new team member or appropriate board label
   1. Uncheck “show closed list”
   1. Next to “Scope” click “Expand”
   1. Under “Assignee” section, click “Edit” and choose the appropriate assignee
   1. Click “Create Board” to create the board
   1. To add columns/specific label list, click “+ New List” next to open issues column
   1. Under “Scope”, ensure that “Label” is selected”
   1. Under “Value,” choose the appropriate label for the desired list
   1. To change the order of the lists on the board, click and drag the lists

### Team Interviews

- When a candidate is ready for a team interview, the recruiter will request availability in ModernLoop. Once availability is requested, it will create a task for CES to schedule.
  - If there are shorter timelines for roles as defined by the hiring team, CES needs to be made aware of those timelines for when interviews need to be scheduled. We will default to scheduling interviews at a minimum of [48 hours](/handbook/hiring/interviewing/) out to leave time for interviewer prep.
  - Reminder: When tagging `@ces` in Greenhouse, do not tag anyone other than the team in the same ping as it will add those users to the Service Desk project.
- If no response is received within 24 hours, CES will send a follow up request for availability and set the due date of the issue to 24 hours after the next email to check for availability again.
  - After the 2nd email to the candidate with no response, the CES will make the Recruiter aware of the no response and no longer attempt to receive availability.
- After availability is received, CES will schedule interviews based on the interview plans in Greenhouse/ModernLoop.
  - CES will be using the Zoom integration with ModernLoop for interviews
  - After the candidate has provided the availability, as an optional step the CES team members can send the Candidate First Touch Email from Greenhouse if there are scheduling challenges.
- This email is sent to inform the candidates that their interview scheduling is in the process and to ensure better engagement with the candidates.
- If CES sees an alert to merge applicant profiles, and those profiles are a match (candidates' email address, phone number, or resume matches), they will merge the applicant profiles. Visit [the Candidate Hygiene section of the home page](/handbook/hiring/) for instructions.
- CES will send interview confirmations via ModernLoop
- CES will not automatically schedule next interviews based off of scorecards
  - The Recruiter or Hiring Manager will need to follow the same scheduling procedures as above in ModernLoop to request scheduling assistance on the next round of interviews.
  - Any candidates who receive a no or definitely not scorecard should be discussed with the Recruiter and the Hiring Manager before declining.

#### Technical Interview Scheduling

Certain positions require technical interviews (i.e. Ruby on Rails, Golang, Frontend, etc) where candidates are asked to demonstrate their knowledge and skills. Technical interview requests can be identified within the scorecard title in ModernLoop as recruiters will utilize the following format: "Technical interview, level & coding language pool - 90 mins".

**Important to Note:**

- These interviews are 90 minutes in duration
- Candidates must submit a GitLab username *before* CES can schedule their interview
- Interviewers and candidates need time to prepare prior to the interview, therefore interviews will be scheduled 3.5-4  business days out as the merge request will be sent by the interviewer 3 working days (or 72 hours) before the interview.
- Interviewers must be the same job level or above to the candidate.  An interviewer can not interview a candidate for a higher job level than theirs.

To schedule a technical interview, CES should follow the process outlined below:

- When a candidate successfully reaches the Team Interview stage the recruiter will send the availability request email to the candidate. This action will initiate a scheduling task for the CES in ModernLoop.
  - If the candidate did not submit a GitLab username during the application or screening stage, the recruiter will also send the GitLab Username Form (this will be found in the Team Interview Stage or Evergreen stage). This generates an email to the candidate requesting they fill out the form with their GitLab Username.
- CES will receive a separate ticket to the CES service desk:
  - The completed GitLab Username form. This will only come into the service desk once the candidate replies to the email, and the username will automatically be added to the Details tab of the candidate's profile under Details > Other. CES should check that the GL username is valid and ensure that the GL username is in a URL format.
  - CES will add the tag "GL Username received" to the candidate's technical scheduling task in ModernLoop.
- Once CES has received and confirmed that the candidate's GL username is valid, the CES team member can proceed with scheduling the interview in ModernLoop.
  - Note: when you send the interview invite to the interviewer, select the template 'Technical Interview with MR'.
- CES will then send the candidate their confirmation through ModernLoop as well.
  - When emailing the candidate their interview confirmation, CES will select the appropriate (Ruby, Golang) ModernLoop email template. This provides the candidate with additional information about what they can expect for their technical interview.

**No Work Submitted on the MR 24 hours Before Interview?**

- If the candidate has not submitted any work on the MR 24 hours before the scheduled interview, the interviewer will notify the CES team.
- The CES team member will cancel the interview, and email the candidate the 'Email to candidate - MR Not submitted' template in Greenhouse. CES will also leave a note on the candidate's Greenhouse profile notifying the recruiter.
- CES will not reschedule the interview until they have received direction from the recruiter.

#### Executive Interview Scheduling

The process below outlines the steps to be followed by the CES team in scheduling executive interviews while partnering with the Executive Business Administrator(EBA) team and executive recruiters. The Candidate Experience team and EBA team will adhere to a 24 hour working day SLA response time for scheduling interviews. Interview requests coming from Executive recruiters are to be scheduled in the executive calendar only.

1. The recruiter will create a scheduling task in ModernLoop and which will populate into the CES "My Tasks" list in ModernLoop

- CES refers to the EBA cheat sheet doc for executive interviewer preferences and contacts the respective EBA with interview details in the #EBA-team-interview-requests channel.
- To request an interview in this channel, click “Workflow” and fill in the appropriate information in each field.

1. CES adds the "Pending EBA" label and Slack link to the EBA scheduling task to the interview task in ModernLoop while awaiting response.

 **Note: Follow up SLA is 24 hours to check for time conflicts delaying scheduling. If the times do not match, CES may contact the candidate
   requesting more availability or suggest some times that works for the interviewer.**

1. Once the EBA confirms the best time and date for the interview. CES sends the interview confirmation email through ModernLoop to the candidate.

1. CES will schedule the interview through ModernLoop & send the calendar invite to the interviewer. Make sure the invite is always marked private.
1. CES notifies EBA of scheduled interviews in the original slack message with a green check mark emoji and close the ticket.

This process not only applies to executive requisitions, but any reqs or interviews that include executive team members supported by EBAs. Please note that not every executive team member has EBA support and they may be scheduled directly in ModernLoop following the usual CES scheduling [process](coordinator/#team-interviews).

**Note:**

- If the candidate needs to reschedule, notify the appropriate EBA in the slack channel and share the candidate's updated availability and greenhouse profile.
- The EBA and CES team will communicate any interview changes or concerns in the slack channel. Other requests such as flagging an offer, completing an interview scorecard, or regarding the executive's schedule may be communicated in this channel as well.

#### Candidate accessibility and accommodation request process

At GitLab, we are committed to fostering an inclusive environment where everyone has the opportunity to contribute. The following steps outline the workflow for the team to process any accessibility and accommodation requests submitted by candidates.

1. **Google Form Submission**

- Candidate submits an accommodation request form from either:
  - Candidate portal - Accommodation request form access is provided at phone screen stage through the portal and remains available throughout the interview process.
  - Initial interview availability email.

1. **CES Notification & Initial Review**

CES will receive a notification as soon as the candidate submits the accommodation form. During initial review, CES will use the matrix below to determine if the accommodation is Level 1 or Level 2.

| Category | Level 1 - Standard<br>(CES handles directly - acknowledgment within 24 hours) | Level 2 - Complex<br>(TMR + Legal - acknowledgment within 24 hours - Follow up with decision within 24-48 hours) |
|----------|-----------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------|
| **Technology Accommodations** | ✓ Closed captioning | ✓ Custom software needs |
| **Interview Accommodations** | ✓ Multi-day interviews<br>✓ Extended time for interviews | ✓ Resource allocation beyond standard offerings |
| **Other** | Not applicable | ✓ Unique or complex accommodation needs<br>✓ Requests requiring policy interpretation<br>✓ Resource allocation beyond standard offerings |

1. **Send candidate acknowledgement email**

- Within 24 hours and regardless of level, CES will send the candidate the 'Accommodation Request Acknowledgment Email' (select the template from GH based on the level of the request.)

1. **Greenhouse Coordination Transfer**

- In the Candidates GH profile, Set the "Application Coordinator" to the designated accommodation-handling CES. This will ensure Modernloop auto-routes all future scheduling tasks, maintaining consistent support and zero missed accommodations.

1. **Tagging & Documentation**

- CES will then add an accommodation tag in Greenhouse as well as an internal note in ModernLoop (ML) for tracking. Note will be kept generic to maintain candidate privacy.

1. **Standard Accommodation Implementation**

- For Level 1 accommodations, during scheduling, CES will include the accommodation next to "accommodation requested:" in the interviewer's invite using TE snippets, 'zoomclose' for closed captioning and 'adtime' for extended time.
- If the candidate has requested a multi-day interview, CES will schedule the interviews accordingly.
- The SLA for overall accommodation implementation is 24 hours.

1. **Non-Standard Request Escalation**

- For Level 2 requests, CES will escalate the request in a dedicated private Slack channel.
- The team will create an implementation strategy, secures approvals for policy exceptions, documents the decision rationale, and informs the candidate of the final plan via email.
- If the accommodation can be supported, CES will update the ML interviewer invite as well to reflect the accommodation request and how it will be implemented.
- The SLA for overall accommodation implementation is 48 hours, including consultation with TMR/Legal and candidate notification.

1. **Interviewer Communication & Confirmation**

- After scheduling, CES will DM interviewers about the accommodation (both Level 1 & 2 if supported) and ensure they have the necessary support to conduct a successful interview.

Note: CES will maintain internal tracking of all interviewer communications and confirmations for accountability and follow-up purposes. The tracking sheet is linked in the CES team repo for reference.

#### ModernLoop

ModernLoop is the scheduling tool that the Candidate Experience Team uses to book
interviews.

## Logging in to ModernLoop

To log in select the ModernLoop tile in Okta and use SSO.

Please ensure you have the [ModernLoop Chrome Extension](https://modernloop.zendesk.com/hc/en-us/articles/18013814809236-ModernLoop-Chrome-Extension) installed on your Chrome Browser.

## How to schedule interviews via ModernLoop

- Go to 'My Tasks' using the task bar on the left
- In the 'Action required' bucket, click on the candidate who has the label 'ready to Schedule'
- A side window will open, scroll down and click the 'Schedule now' button.  The page will open to the candidate's availability.  On the right press 'Next: Setup Interviews' button.
- Check the information for the required interview to schedule (time, interviewer, scorecard etc), then click 'Next: Find Schedules'
- ModernLoop will create a list of interview options.  To see an interviewers calendar you can click on the interviewer or the 'view' option on the top right of the card.
- To select a schedule option click on 'use schedule'on the top right corner of the option card.
- The location will be automatically selected as Zoom and a zoom room selected. Please check with the CES team to understand which Zoom room to use. Each CES member is assigned a particular zoom room to use when scheduling to avoid overbooking a room.
- The calenders section when scheduling in ModernLoop refer to the internal calendars that will populate once an interview is scheduled. The are 'Candidate Interview Calendar' for candidate events and 'Interview calendar' for Internal events. These calendars should auto-populate in this section.
- Select the Email to candidate template from dropdown list.
- If the interview requires a brief, you can include this by selecting 'Add attachment'
- For the interviewer invite, select the correct template from the dropdown list
- Review all details and then press 'Confirm and send'
- If you only wish to send the invites to the interviewers before sending the candidate invite, select 'Send internal only'.  This will send the interviewer invites and move the candidate into the Pending section of My tasks.  When you wish to send the candidate invite you can go into the candidate profile and click 'finish and Send'.

## How to schedule internal interviews

- When receiving a scheduling task in ModernLoop from a recruiter for an internal candidate, confirm that the 'internal candidate' tag has been applied to the task.
- If it is missing, add the "internal candidate" tag to the ModernLoop task yourself for tracking purposes.
- Unlike with external candidates, recruiters do not request availability from internal candidates via email. Instead, they create a scheduling task for CES to arrange interviews directly, without waiting for candidate-submitted availability.
- The recruiters will inform the candidate that CES will be making use of their GitLab calendar to schedule the interview.
- CES should proceed directly to scheduling the calls without waiting for candidate availability submission.
- Access the Google Calendar to view both the interviewer's and internal team member's calendars in tandem.
- Once a suitable time slot has been identified, schedule the interview and send the internal candidate confirmation in ModernLoop.

## How to add or replace an interviewer for a scheduled interview

- If you wish to replace or add an extra interviewer to a scheduled interview, in 'My tasks' go to scheduled, click on the scheduled interview.  
- When the side page opens with the interview details, click on the 3 dots on the interview tile and select 'Edit Interview'.  
- To add an interviewer select 'add interviewer' and type in the name of the new interviewer.
- To remove an interviewer select the three dots next to their name and select remove interviewer.

## How to set up Interviewer Modules (Interviewer pools & training plans)

A module in ModernLoop is an interviewer pool, which also allows for trainees to move through shadows/reverse shadows.  

To set up a module take the following steps:

- Go to Modules on the task bar on the left
- Click on 'New Module'
- Give the Module a name, select the training plan (typically 2 shadow and one reverse shadow), and select role-by-role, then create
- Click on add interviewers and then type in the names of the Trained interviewers for the module.  Then select fully trained and the interviewers will be added to the module.
- To add the trainees click on 'Add interviewers' in the top right corner.  Type in the names of the trainee interviewers and then select 'Trainee'

To delete a Module, click into the Module, then go to settings and delete module.

To assign a module to an interview plan:

- Go to jobs and select the job which you want to use the interviewer module for.
- Select the stage tab and select the interview stage required.  
- The interview plan will pull up the interviews in this stage from Greenhouse.  Click on 'Add Interviewer' and then in the box type the name of the module you want to use.  

## How to schedule a technical interview

- If the technical interview requires a interviewer module, check in the job interview plan that the correct interviewer module is selected.  
- Continue to schedule the interview using the same steps as for a 1:1 interview.
- For the candidate email select the template 'Technical Interview - Candidate confirmation' and add in the technical instructions using the correct text expander snippet.
- For interviews which have an MR, select the 'Technical Interview with MR' for internal invites for interviewers.
- If there is a shadow interviewer from a Module, ModernLoop will automatically add in a paragraph to let the interviewers know who is the lead and who is the shadow.
- Select finish and send.

## How to update Organization wide settings

NOTE: Only Admins can change organizational settings.
Organizational settings can be found in the menu on the left hand side of the homepage.

### If a Candidate Withdraws from the Hiring Process

If a candidate emails the CES Service Desk stating they would like to withdraw from the interview process, the CES should respond to the candidate's email (not the Service Desk ticket) and cc the recruiter (if the recruiter isn't already on the email). The CES response should not say anything definite as there may be a chance for the recruiter to reel the candidate back in. A basic response is below:

> Hi `Candidate Name`, thank you for your email. I have cc'd your recruiter in this email and if there are any additional questions, they will be in touch.

The CES should also tag the Recruiter in the Greenhouse profile of the candidate who withdrew.

The only exception to this should be for executive roles. Please just forward the withdrawal email to the Executive Recruiter and they will handle any follow-up.

### Non-Disclosure Agreements

To send a Non-Disclosure Agreement (NDA) to a candidate, Recruiters should ping @ces in Greenhouse.
CES can then log into DocuSign, select "start" and "use a template", and then access shared templates.
Once the NDA has been returned, upload the document in the "details" section of Greenhouse. Download this document from DocuSign as separate files, and only use the NDA itself (the summary is not necessary).

### Background Screenings

GitLab will obtain references and complete a criminal [records check](/handbook/people-group/contracts-probation-periods/#background-screenings) with employment verifications.

- If the candidate is located in Belgium and the role is not Grade 9 or higher, the CES or Recruiter (whoever kicks off the reference check process) should send the job requisition to the legal team via the #legal Slack channel during Reference/Background screening phase to determine whether or not the role is a position of trust.
- The recruiter should select "Email the team" and send the "CES Start Contract Request" email to CES* to initiate the offer letter and background screening processes after the verbal offer has been made.
- The Candidate Experience Specialist will [initiate a background screening](/handbook/people-group/contracts-probation-periods/#background-screenings) and start the contract process for the candidate.
- Background screening results will be received by the Senior Background Check Specialist and escalated to Team Member Relations and Legal where appropriate

For additional information on reviewing Background screenings see [this page](/handbook/people-group/contracts-probation-periods/#background-screenings).

#### Initiating a Background Screening through Greenhouse

1. Log in to [Greenhouse](https://app2.greenhouse.io/dashboard) and go to the candidate's profile.
1. Click the `Application` tab.
1. Click `Export to Sterling`.
1. Click `Complete Report`, which will redirect you to the Sterling website.
1. Click `Invite`, and then follow the steps below starting at the second step.
1. If the candidate is located in New York City and you have already initiated Step 1, please order NYC Step 2 instead of a traditional US check.

#### Initiating a Background Screening through Sterling Talent Solutions

1. Log in to [Sterling](https://secure.sterlingdirect.com/login/Default.aspx) and E-invite the candidate by inputting their email address.
1. Under "Applicant Information" enter in the candidate's first and last name, as well as their email address to confirm.
1. Select the candidate’s location. You will need to include City and State for US candidates.
1. Next, select "GitLab" from the "Job Position" drop down menu.
1. Next, select the name of the country where the candidate is located. If the country is not listed, choose `Global Screening`
1. Finally, scroll to the bottom of the page and click "Send"
1. Make a note in the Greenhouse profile that the Background Screening has been started

### Reference Check Forms

Prior to giving an offer, Recruiters are required to request references and other offer-related information by sending a form in the Reference Check stage. There are a few versions of this form available on every job based on the country where the candidate is located. When CES receives a form in the Service Desk, there are 3-4 fields to look at: NYC status, PIAA (Employee Invention Assignment Agreement), Outside Work disclosure, and TMRG requests.

**NYC Location**

USA Reference Check forms only:
It's important to note that the USA Reference Check form should be sent to the candidate and Step 1 should be completed before presenting a verbal offer. If the candidate selects "Yes" to indicate that they are located in NYC or its 5 boroughs (They will be listed as Brooklyn, Bronx, New York (Manhattan), Queens, or Staten Island), you will need to complete a two-step background screening process:

Please note that Long Island is not part of NYC and this process does not apply to residents there.

1. CES service desk receives a ticket indicating that the candidate has submitted Reference Check Process Information - USA form. CES notes that the candidate has selected "Yes" for the NYC location question.
1. CES will add the text expander snippet **refchecktodo** into the ticket to help guide them through the process. CES will add the "NYC BGC" label.
1. CES will go to [https://sterlingcheck.app/dashboard/#/dashboard/](https://sterlingcheck.app/dashboard/#/dashboard/). It is important to use this version of Sterling because it allows us to edit the email template that is delivered with the check.
   - Select **NYC Step 1** screening package. You will need to fill out the Location of Employment field as San Francisco, and the Projected Salary field with the candidate's salary (this range can be found in the "Approvals" tab of the candidate's GH profile). Click "next".
   - On the next page, under "Email Content", in the drop down, select "NYC Step 1" template.
   - Scroll to the bottom of the page and input the candidate's full name and email address. Send Invite.
1. CES will add the "Pending" label and due date on the ticket. Create a follow-up reminder in Greenhouse 1 business day out to check if there is an ETA.
   - Once an ETA is set in Sterling, create another follow up reminder in greenhouse for that ETA date. Please note that the results may come in earlier than the ETA.
   - Please contact the Senior Background Check Specialist for any BGC escalations. e.g "Status: Unperformable" or "Status: Consider"
1. This process has been added due to NYC law, which separates the employment verification from the criminal check. Keep an eye on the status of the Step 1 screening results in Sterling. While we are waiting for Step 1 to be cleared, the recruiter can provide the candidate the verbal offer, begin creating the offer in Greenhouse and going through the approval stages. Recruiters can send the contract request ticket to CES when they are ready, **although, CES *cannot* send a written contract to the candidate until Step 1 has been cleared.**
    **Tip:** when the CES desk receives the contract ticket, add the NYC BGC label immediately to remind yourself and your team members that this candidate is undergoing the NYC two-step background screening process.
    - When checking BGCs in Sterling initiated by other team members, be sure to select "Entire Organization" in the top left section of the [Sterling dashboard](https://sterlingcheck.app/dashboard/#/dashboard/).
1. Once the recruiter has sent CES a contract ticket, CES will then complete **NYC Step 2** of the background screening through the Greenhouse integration. Once in Sterling, select the NYC Step 2 screening package and send.
    **Troubleshooting Tip:** If you receive an "expired" error when initiating Step 2 through the Greenhouse Sterling integration, you can navigate to the [Sterling Direct dashboard](https://secure.sterlingdirect.com/sys/). On the right hand side, under "E-Invite Applicant to Background Check", enter in the candidate's email address and select "Invite".
    - Fill in the applicant's information
    - Under "Order Information", select GitLab as the Job Position and under "Screening Package" select NYC Step 2.
    - Then scroll to the bottom right of the page and select Send.

**Outside Work and PIAA Process**

In the form, you will find that candidates are required to disclose whether or not they have any outside work, side projects, Inventions, etc. If they state "none" or "n/a", you can skip this step. If the candidate discloses any information in either the Outside Work section or the PIAA section, CES will take the following steps:

1. CES will visit the [TA Candidate PIAA and Outside Work Disclosure Group](https://gitlab.com/groups/gl-ta-candidate-disclosures)
1. CES will click "New Project" in the upper right corner of the page
1. Select "Create from template"
1. Select "Group (1)" tab and click on the blue button "Use Template"
1. For Project Name - create a title as the Candidate Name
1. Leave all other fields as is and click "Create Project"
   - NOTE: Once the project is created, you will then be brought to a page where you can create an issue within that project. This is where we will provide all information about the disclosure and loop in HMs, TMR, the Recruiter and Director.
1. Click on "Issues" on the left side of the page and select "New Issue."
1. For Issue Name - create a title using the candidates full name along with the type of disclosure received.
1. Under the Description drop-down - select piaa_outside work_discussion template
1. Fill in all pertinent information.
   - Candidate Name along with the Greenhouse Link
   - Copy/Paste the disclosure made by the candidate underneath the CES checkbox
1. Assign the issue to yourself, and at the bottom, click "Create Issue"
1. Once the issue is created, click on "Manage" in the left toolbar and select "Members".
1. Click "Invite Members" - type in HM's name, Director's name, and recruiter name; leave them as a Guest and click "Invite" (These will only be invited in at the "issue" level and therefore will only be able to see the issue they are tagged in. They will not have visibility into the other projects created)
   - IMPORTANT NOTE: For ALL disclosures, Director Level approval is ALWAYS required.
1. Go back into the issue, click Edit and in the info box tag the recruiter, HM & Director, then click save
   - These team members will be notified by email when tagged.
1. In the Comment section of the issue request participants review the disclosure(s) by using TE snippet "discreview"
1. CES will remove the appropriate label once confirmed approvals are received in the comments.
1. If Legal review and approval is required, TMR will invite the appropriate Legal member into the issue and request their review
1. Once fully approved, please add the "Fully Approved" label and close the issue.
1. Proceed to the candidate's GH profile and select "Email (Candidate's Name). Select the "Disclosure Confirmation" template, copy/paste the disclosure the candidate made into the blank space, and Send. The email will CC you and the recruiter.
1. Download the email from your inbox and upload into the "Pre Hire Documents & Changes" folder in the candidate's Workday profile.

**TMRG Conversations**

Our hiring process includes an **optional** step where candidates can request to meet with a TMRG team member. We will offer this to a candidate when they complete their interview process before an offer is made. Whether or not the candidate decides to take us up on this offer will have no impact on our overall hiring decision.

All current TMRGs have agreed to take part in this process. You can find the group list [here](/handbook/company/culture/inclusion/tmrg-tmag/).

When a candidate requests to meet with a TMRG team member via the Reference Check Form, the Candidate Experience Specialist will do the following:

1. Reach out to TMRG volunteers for this call in the dedicated #candidate_tmrg-call slack channel.
    - Select Shortcuts button - looks like a plus sign with lightening bolt
    - Fill in appropriate details
       - Which TMRG would this canidate like to speak with?
       - Where is the candidate located?
       - What role is this candidate interviewing for
       - Click Submit
1. Once submitted, the request will ask volunteers to reply with their Calendly link and LinkedIN Profile (optional) for us to share with the candidate.
1. Once a volunteer has been found the Candidate Experience Specialist will email the candidate the 'TMRG - Reviewed' email template in Greenhouse. The CES will update the template with the Team Members name, Calendly Link and LinkedIN profile if provided and then send to candidate.
1. If a volunteer has not been found within 24 hours the CES team member will reach out to the TMRG in their dedicated TMRG Slack Channel.
1. If a volunteer still has not been found within 24 hours of the second request, the CES will reach out to the [TMRG lead(s)](/handbook/company/culture/inclusion/tmrg-tmag/) and request assistance with scheduling. If a volunteer has not been found within 3 business days of the request, the CES will ask the TMRG lead to take part in the conversation.

As a GitLab team member taking part in these calls, we advise you to start with a short introduction to you and your role here at GitLab. From here, we advise you to let the candidate lead the conversation as the goal is for you to answer their questions and offer insight into how we work.

These calls don't require you to submit a scorecard in Greenhouse. If a candidate mentions something that you see as a red flag (e.g. they outline a past action of theirs that goes against our values) or shares something that would help us set them up for success, we advise you to share the details of this with the hiring manager for the role they're interviewing for. It will be the responsibility of the Hiring Manager to review this and decide whether we need to alter the hiring or offer process for the candidate.

### Send contract

[See Candidate Experience Specialist Contract Processes section of the handbook](/handbook/hiring/)

The [Candidate Experience Specialists](/job-description-library/people-group/candidate-experience) will prepare the contract. While the Candidate Experience Specialist will prioritize a contract above other tasks, the expected turn around on the task is 1 business day. If the contract is time-sensitive, please provide context for the rush. If the Candidate Experience Specialist cannot meet the 1 business day they will inform the recruiter and CES manager via Greenhouse and will provide context.

Recruiters should make themselves familiar with the basic knowledge of the contract processes that can be found on the [CES Contract Processes](/handbook/hiring/) page and the [Contracts, Probation Periods & PIAA](/handbook/people-group/contracts-probation-periods/) page, as well as the [Employment Contracts](https://internal.gitlab.com/handbook/people-group/people-operations/people-connect/employment_contracts/) page in the internal handbook.

1. Check all aspects of the offer:

- Do we have the new team members' legal name in their profile?
  - Check the candidate’s Reference Check form to confirm their legal name is correctly reflected in GH
  - It is extremely important to enter the team member's full legal name (as much as it is known before visually seeing a legal ID). Full legal name should be provided for the [background screening](/handbook/people-group/contracts-probation-periods/#background-screenings) process. It is important to be as accurate as possible, including the person's full legal name as well as any accents used for their name.
- Is the new team members' address listed on the details page?
- What [contract type and entity](/handbook/hiring/) are required based upon location and offer details?
- Is all necessary information (start date, salary, location, etc.) up to date?
- Is the start date one that is not a "no start date" and provides an adequate amount of time for People Connect and IT to have sufficient notice? Ideally, we are providing 10 days notice, but the teams can work with less if we let them know.
- Has the [signatory](/handbook/hiring/) been determined by the Candidate Experience Specialist and updated?
- Has the Entity been selected based on the New Hire's location? If the job title has Federal or PubSec included, please check with the Recruiter if they set up the contract as Inc rather than Federal LLC to confirm.

1. [Generate the contract within Greenhouse](/handbook/hiring/) using a template based on the details found in the offer package, paying attention to whether OTE, draw, and bonuses are included in the offer details.
1. Contact the recruiter or new team member to gather any missing pieces of information (note: candidate’s address can be found in their Reference Check Form).
1. If the contract was created outside of Greenhouse, ensure that the contract has been reviewed and approved by a member of the Legal team.
1. [Stage the contract in DocuSign from within Greenhouse](/handbook/hiring/) to email the correct signing parties. In the “To” field, type the name and select the pre-determined signatory. CC the recruiter and the hiring manager in the CC field.
1. **Before marking the candidate as hired** the Candidate Experience Specialist will reject the candidate from any other active roles including roles for which they are a prospect (without sending a rejection email). *NOTE: If this step is skipped, the profile will not be exported to Workday when the candidate is marked as hired.*
1. **Before marking the candidate as hired** on all candidates, the CES will make sure that the profiles were merged (for internal candidates, this will be indicated if the candidate shows their original `Hired` inactive role). [View candidate merge instructions in the Candidate Hygiene section](/handbook/hiring/).  *NOTE: If this step is skipped, it will create problems with privacy and increases the possibility of a new hire seeing their own Greenhouse profile.*
1. **Before marking the candidate as hired** the CES will ping the recruiter and give them 24 hours to contact/reject all other active candidates. Once this is complete, the CES can proceed with hiring in GH (if candidates are still present in req, select the "keep open" option when setting candidate to hired. This will trigger a new opening to ensure candidates are still present in req)
1. **Before marking the candidate as hired** the CES will verify if the listed Recruiter and Coordinator in the `Details` >  `Source & Responsibility` section of the candidate's profile is correct to ensure accuracy in reporting.
1. The CES will mark the candidate as "Hired" in Greenhouse: *when prompted, select the option to close the req.* Please note, the new hire's Workday profile will be generated automatically.
1. The Candidate Experience Specialist will email the new team member the Welcome Email from Greenhouse with a cc to IT Ops, the Hiring Manager and the Recruiter.  Send the appropriate Welcome Email based on the candidate’s location and whether the candidate will need to procure a laptop themselves.

   - Instructions on the [Laptop Ordering Process](/handbook/security/corporate/end-user-services/laptop-management/laptop-ordering//) are included with this email.

1. Should the start date change after the welcome email is sent please see the required steps [here](/handbook/hiring/).
1. Exception to the start date and onboarding date alignment: If a new team member requires a specific start date for legal reasons (cannot have break in employment) but onboarding on that specific day is restricted (because of Public Holiday, Family & Friends Day, etc.), the Candidate Experience Specialist can notify the People Connect Team in the private Slack channel `people-connect_ces`. The Contract, Greenhouse and Workday should reflect the same start date regardless of the actual onboarding date.  

The last part of the Candidate Experience Specialist's responsibilities with a candidate is to hire them into the system and pass them on to People Connect. The hire-in process includes more complexities, so CES created the following guidelines to clarify start date exceptions and confidentiality around new hires.

**SETTING GREENHOUSE REMINDERS** - CES make use of the due date feature in the GitLab issue to keep track of the start date and maintain consistent communication with the recruiters to ensure the candidates in the requisition are cleared completely. CES can make use of the "Need to hire into Workday" label and set due dates in the GitLab issue to track as well.

The People Connect team has an SLA period of 10 working days to onboard an entity/PEO-based team member. In the event of an exception, the minimum notice required for the People Connect team is 5 working days.

**PROACTIVE COMMUNICATION**- It's essential that CES promptly notify in the #peopleconnect-ces slack channel when they experience a delay or issues with the contracts generated and mark a team member as hired. If there's an urgent hire with less than 10 days to the start date, please use the TE snippet “Itlaprequest” in the people-connect_ces channel to confirm that a laptop can be delivered on time. Only after receiving this confirmation can we confirm the start date with the recruiter.

**NEW HIRE EXCEPTIONS** - For any confidential hires that necessitate a public announcement, please inform Alissa Meeks or Melody Patel about the specific scenario. Additionally, loop them in any communication related to the role to keep them in the loop. This will also be considered as an exception.

**VERIFYING GLOBAL HOLIDAYS** - CES should verify whether the proposed start date coincides with a holiday in the new hire's location. It is the responsibility of the recruiter to check with the Hiring Manager to ensure that the new team member has a support/ onboarding buddy on the first day of onboarding.

**START DATE EXCEPTION EMAIL FOR URGENT HIRES** - This email seeks a required explanation and business justification for the proposed changes in the start date. The People Connect team will review this on a case-by-case basis. Urgent hires refer to situations where the HM requests an earlier start date than the previously agreed upon one, and the new start date does not adhere to the standard 10 working day SLA period for candidate onboarding. **Important**: an exception will not be made without a minimum of 5 working day notice to the People Connect team.

Prominent reasons for urgent hires are Critical Skill Gap / New business opportunities, Equity vesting grant options and Unexpected departures or backfills. CES can access this email under the "Email the team" option in the candidates' Greenhouse profile.

### CES Contract Processes

Assuming that the [hiring process](/handbook/hiring) went smoothly, now it is time to prepare the applicable contracts. Once the verbal offer is made, an issue will be created via the "email team" option in Greenhouse. The CES will send the contract to the applicant, using DocuSign in Greenhouse. On rare occasions, the CES may have to create the contract outside of Greenhouse using Google Docs; if this is the case, the CES needs to have a manager review the contract for accuracy before sending it out for signature.

First, be sure to validate the following:

1. The candidate has been moved to the "offer" stage before sending the contract. CES can adjust this, but it's important to inform the Recruiter because this is a step that should be done when they are ready to make their verbal offer.
1. The start date is not a no-start day, and is more than 10 days from your sent date. People Connect requires at least 5 days to process a new hire, but requests 10 days when possible. Recruiters need to be prepared for the time it takes for both parties to sign the contract as well as reject all remaining candidates and should prepare for this.
1. The candidate lives in a country we are able to hire in. The SSOT for all country hiring is [here](https://comp-calculator.gitlab.net/hiring_status/index).
1. The currency listed in the offer package in Greenhouse should normally be the local currency of the new team member unless approved by Total Rewards. This needs to be confirmed and approved by Total Rewards prior to making the offer, as any changes to the currency will require complete reapproval in Greenhouse, regardless if it is the same amount just in a different currency.
1. Confirm [through which entity the team member would be employed or contracted](/handbook/people-group/employment-solutions#team-member-types-at-gitlab). If the title of the position includes "Public Sector" and they are located in the US, they may need a Federal contract. The Recruiter should confirm with the PBP if there's any questions.
1. If the candidate is located in *Belgium* the CES or Recruiter should be aware of two further things to address: i. there are strict language/translation requirements in Belgium so the CES or Recruiter should confirm which region of Belgium the candidate is located in and let legal know, to ensure the right contract, in the right language is used, and so that a translation can be arranged if necessary; and ii. if the role is *not* Grade 9 or higher, the CES or Recruiter should send a link to the role and the job requisition to the legal team via the #legal Slack channel once the candidate is at offer stage (before anything is sent out!) to determine whether or not the role is a position of trust.
1. The recruiter should select "Email the team" and send the "CES Start Contract Request" email to CES* to initiate the offer letter and background check processes after the verbal offer has been made.

### Entity Contract Signatories

This chart reflects the available signatories for each of GitLab's entities. They are listed in order of preferred signatory first. This chart should only be used for new hire contracts where GitLab has entities. This is not for internal moves such as [contract renewals](/handbook/people-group/contracts-probation-periods/#contract-renewals), [job change letters](/handbook/people-group/contracts-probation-periods/#job-change-letter), or [relocations](/handbook/people-group/relocation/).

| Entity | Signatory |
|-------- | -----|
| GitLab Inc | All Recruiting Leads (Jake Foster, Marissa Farris), Jess Dallmar, Rob Allen, Other People Group Team Members who are employed by Inc. and of the appropriate grade to sign the document. JCLs can be signed by Morgan Wilkins  |
| GitLab Federal LLC    |       Bob Stevens     |
| GitLab BV Belgium, Dutch & English | Marissa Farris, Jake Foster|
| GitLab BV, Netherlands | Marissa Farris, Jake Foster|
| GitLab Canada Corp | Simon Mundy, Rich Song |
| GitLab France S.A.S. | Jake Foster, Rob Allen |
| GitLab GK, Japan | Jess Dallmar, Rob Allen & Jack Connors Backup: Simon Mundy|
| GitLab GmbH | Marissa Farris, Rob Allen |
| GitLab Iberia S.L (Spain) | Jake Foster, Rob Allen. Backups: Jim Gladen & Simon Mundy |
| GitLab Ireland LTD | Marissa Farris, Rob Allen, Jake Foster, Jack Connors |
| GitLab Israel LTD | Jim Gladen, Simon Mundy|
| GitLab IT BV | Marissa Farris, Jake Foster, Jack Connors |
| GitLab PTY Ltd, Australia | Jess Dallmar & Rob Allen, Jack Connors. Backup: Jim Gladen|
| GitLab PTY Ltd, New Zealand | Jess Dallman & Rob Allen, Jack Connors. Backup: Jim Gladen|
| GitLab South Korea | Jess Dallmar, Jack Connors & Rob Allen |
| GitLab Singapore PTE. LTD. | Jess Dallmar, Jack Connors & Rob Allen. Backup: Simon Mundy |
| GitLab UK Ltd | Marissa Farris, Jake Foster, Rob Allen |
| JCLs | Choose signatory from the list above. For the US, Morgan Wilkins can also sign. |
| PEOs | The Candidate Experience Specialist processing the offer. For JCLs, choose Morgan Wilkins or Marissa Farris |

### How to add a contract into Greenhouse

1. In the internal GitLab Handbook, you'll navigate to [this link](https://internal.gitlab.com/handbook/people-group/people-operations/people-connect/employment_contracts/) as a SSOT for all contract templates. Only the People Group, Finance, and Legal should have access to this folder.
1. Navigate to the correct entity of the contract you're attempting to update on the handbook page.
1. Click the link to the contract you're wanting to upload and it will open the Google Document.
1. Navigate to `File`, click `Download` and select `Microsoft Word`.
1. Log in to Greenhouse and go to "[Configure](https://app2.greenhouse.io/configure)" by clicking the gear at the top right corner, then choose "[Offer Templates](https://app2.greenhouse.io/account/offer_letter_templates)".
1. Navigate to and click the `Upload New` button (located underneath All Offer Sections).
1. Enter the template name (The convention is typically "GitLab `Entity` `employment-type`, `with/without bonus`", e.g. `GitLab Inc full-time, with variable bonus/commission`).
1. Click `Choose File` and choose the document you've downloaded and click `Save Template`.
1. Greenhouse will upload the document and it will appear at the bottom of the page. There will be a `Test` button next to it; click this, and it will validate that all of the Greenhouse tokens are correctly inputted. If there are any errors, it will notify you. You will then need to go back to the template in Google Docs and correct the errors, redownload it, and reupload it to Greenhouse (after deleting the original one with mistakes). If all of the tokens are functioning properly, there will be green checkmarks, and you're ready to use this template for contracts!
    1. Check all of the token/fields to ensure they are formatted correctly (`{{ }}`). For each of the fields with curly brackets (`{ }`) in the template on Google Drive, find and replace that field (including the curly brackets) with the corresponding Greenhouse tokens (including the curly bracket). For example, `{Contributor Name}` in the Drive template will be replaced with `{{CANDIDATE_NAME}}`.
1. To delete a contract template from Greenhouse, click the three dots `...` to the right of the template name, then click delete and confirm.

The SSOT for the contract templates are on [this handbook page updated by Legal and People Connect](https://internal.gitlab.com/handbook/people-group/people-operations/people-connect/employment_contracts/). Any updates to contracts will be done there first, and then the talent acquisition team needs to be pinged to be made aware of the changes so they can update the corresponding Greenhouse template.

These steps are executed by the **People Connect and Legal teams** when contracts are being updated, but for reference, if any changes need to be made to the templates, these tasks can be referenced below:

   1. Some fields that are not necessarily clear are the compensation fields as there are separate fields for the *vacancy* and for the *candidate*; we want the candidate fields for the contract, so in Greenhouse, the appropriate token for salary is `{{CURRENCY}}`, bonus is `{{BONUS_AMOUNT}}`, and stock options is `{{STOCK_OPTIONS}}`. Another field that is easily confused is the title; the `{{JOB_NAME}}` is the name of the vacancy, which is not always necessarily the same as the title the candidate will have; to make sure it is always correct and includes the appropriate level and specialty for the candidate, use the token `{{FULL_TITLE__INCLUDING_LEVEL_AND_SPECIALTY_}}`.
   1. The one exception to the curly bracket find and replace process is the Belgian contract. The fields that need to be edited are highlighted.
   1. When removing optional clauses, take care that the paragraph / section numbering still makes sense.
   1. Double check that each field that needs to be filled out is replaced with a Greenhouse token. Sometimes it is not always obvious, as the curly bracket might be regular brackets by mistake.
   1. For each signature section, the following tokens **must** be on their own line in the document, with nothing else on the line: `{{CANDIDATE_SIGNATURE}}`, `{{CANDIDATE_SIGNATURE_DATE}}`, `{{COMPANY_SIGNATURE}}`, and `{{COMPANY_SIGNATURE_DATE}}`. Find each signature page, then hit enter to create the new line after the "Signature", "Name", "Title", and "Date" sections, then copy the corresponding Greenhouse tokens. These can be easy to miss, so double check each signature section has the appropriate Greenhouse tokens, each on their own line.
   1. Most contracts will have various versions that need to created, e.g. one that contains bonus language for variable bonus/commission, director/executive bonuses, or signing bonuses. Best practice is to create the contract containing all of the additional information and title it accordingly, then once you are done go to "File" in Google Docs and choose "Make a copy". Then remove the information as needed and rename the new document and continue the steps below. You can view other documents in the Greenhouse Templates folder for examples.
   1. For contract templates with variable bonus/commission plans, replace all paragraphs with the token `{{VARIABLE_BONUS_TYPE_OFFER_SECTION}}` which will tell Greenhouse to automatically choose the correct bonus type based on the offer package created in Greenhouse.
   1. To change or update a contract that has already been created and uploaded into Greenhouse, return to the corresponding Google Drive doc in the "Greenhouse Templates" folder, open the templates that need to be updated (there may be multiple that need to be changed, since there are different varieties of each contract to accommodate bonus structures, full-time/part-time, etc.), then update each accordingly. If you need to add new tokens to accommodate the change, be sure to follow step 5.3 in the above instructions. Once you have finished making any updates, click "File" in Google Docs, then "Download as" and "Microsoft Word (.docx)". Then go back to the "[Offer Templates](https://app2.greenhouse.io/account/offer_letter_templates)" section in Greenhouse. Find the contract that you are replacing, copy the name of it so you can maintain consistency, then click the three dots `...` to the right of the template name, then click delete and confirm. Then click "Upload New", paste the name of the template, and upload the new version. Click "Test" to validate that everything translated correctly (per step 9 above), and you are ready to use the new template.

### How to Send a Family Member Relationship Acknowledgment

Consistent with GitLab's policy governing Hiring Significant Others or Family Members, GitLab is committed to a policy of employment and advancement based on **qualifications and merit** and does not discriminate in favor of or in opposition to the employment of significant others or family members. Any new hire that has a family member relationship that is currently employed at GitLab must sign [this acknowledgment](https://docs.google.com/document/d/1IseZy4zJZMgP0VCAsGqCP3I6sfnavGdD81THnqljaPI/edit?usp=sharing) along with the GitLab team member. This process is done in conjunction with sending out the contract.

1. If you have not been notified by the recruiter that there is a family relationship in play, there is now a field in the 'Offer Details' that will show whether a relationship exists. There should also be a *Family Member* tag on their profile. It, however, will not show who that family member is.
1. The Recruiter will post the name of the family member in the Private Notes within the Greenhouse profile. If not there, the CES will reach out to the recruiter to find out who the current GitLab team member is.
1. Once the family member is identified, you will send the [Family Member Relationship Acknowledgment](https://docs.google.com/document/d/1IseZy4zJZMgP0VCAsGqCP3I6sfnavGdD81THnqljaPI/edit?usp=sharing) via DocuSign to the new hire as well as the GitLab team member for signing.
1. Drag and drop the Family Member Relationship Acknowledgement form on DocuSign.
1. Add recipients using the following order:

- #1 GitLab Team Member (needs to sign)
- #2 New Hire (needs to sign)
- #3 CES (receives a copy)

1. After all parties have signed, upload a copy into the new hire's Workday profile.
1. Upload Family Member Relationship Acknowledgement form into Workday.
   - Sign into Workday
   - Search the new hire's name
   - Click on the Personal Link on left side of screen
   - Select "Documents"
   - Select "Add"
   - Click "Select Files" and choose appropriate saved PDF
   - Select "OK"
   - Under "Document Category" select "Pre-hire documents & Changes"
   - Under "Comment" write "Family Member Relationship Acknowledgement"
   - Click "Ok" to upload
   - Repeat same steps above this time finding the GitLab team member in Workday
1. Lastly, please open a General People Team request in HelpLab asking them to upload the acknowledgement into the exisiting family members Workday profile. You will need to attach the acknowledgement in the request and provide them the team members name.

### How to Update a Start Date After the Contract is Signed

To change a start date after a **GitLab entity** contract has been signed and the new team member has been "hired" in GreenHouse the Candidate Experience Specialist will complete the following steps:

1. Once the recruiter notifies CES of the start date change, CES should send the “Start Date Change Confirmation” template in Greenhouse under “email the team” and ensure all necessary fields are filled in.
1. After receiving confirmation from both the Hiring Manager and the New Hire, save the confirmation email as a PDF file for upload into Workday.

1. Update GreenHouse:
   - Offer Details
   - Click the edit pencil next to the start date
   - Select the new Start Date
   - Save
   - In the "Make a Note" section in Greenhouse state the old start date and the new state date, and tag the person on FP&A (typically the second approver) who approved the offer.
   - Save
1. Update Entity Payroll Provider (Netherlands) of any changes to the start date via the email templates in Greenhouse.
1. Update the People Connect Team in Slack Workflow.
    - Open private Slack channel `#peopleops-alerts-private`
    - Click Shortcuts button in the bottom left corner (looks like a lightning bolt)
    - Click "New Start Date        Workflow"
    - Fill in Team Member Name with the New Hire Name
    - Fill in Original Start Date (YYYY-MM-DD)
    - Fill in New Start Date (YYYY-MM-DD)
    - Fill in Reason For Change. This is to inform the People Connect Team of the reason for the new date (i.e. Public Holiday, New Hire request, Hiring Manager request, etc.).
    - Optional: Fill in Any other changes.
    - Click Submit
1. Upload start date change comms into Workday.
   - Sign into Workday
   - Search the new team member's name
   - Click on the Personal Link on left side of screen
   - Select "Documents"
   - Select "Add"
   - Click "Select Files" and choose appropriate saved PDF
   - Select "OK"
   - Under "Document Category" select "Pre-Hire Documents & Changes"
   - Under "Comment" write "Start Date Change"
   - Click "Ok" to upload

To change a start date after a **PEO** contract has been signed and the new team member has been "hired" in GreenHouse the Candidate Experience Specialist will complete the following steps:

1. Confirm the start date via email with the new team member, the recruiter, the hiring manager, and the Candidate Experience Specialist.
1. Forward the email to the contact at the PEO.
1. The PEO will generate a new contract and send to the new team member.
   - The Candidate Experience Specialist will need to follow-up with the PEO contact to ensure the new contract is signed.
1. Update GreenHouse:
   - Offer Details
   - Click the edit pencil next to the start date
   - Select the new Start Date
   - Save
   - In the "Make a Note" section in Greenhouse state the old start date and the new state date
   - Save
1. Update the People Connect Team in Slack Workflow.
    - Open private Slack channel `#peopleops-alerts-private`
    - Click Shortcuts button in the bottom left corner (looks like a lightning bolt)
    - Click "New Start Date        Workflow"
    - Fill in Team Member Name with the New Hire Name
    - Fill in Original Start Date (YYYY-MM-DD)
    - Fill in New Start Date (YYYY-MM-DD)
    - Fill in Reason For Change. This is to inform the People Connect Team of the reason for the new date (i.e. Public Holiday, New Hire request, Hiring Manager request, etc.).
1. Upload start date change comms into Workday.
   - Sign into Workday
   - Search the new team member's name
   - Click on the Personal Link on left side of screen
   - Select "Documents"
   - Select "Add"
   - Click "Select Files" and choose appropriate saved PDF
   - Select "OK"
   - Under "Document Category" select "Pre-Hire Documents & Changes"
   - Under "Comment" write "Start Date Change"
   - Click "Ok" to upload

### How to Update a Start Date for an internal candidate after the Job Change Letter is Signed

To change a start date after a Job Change Letter (JCL) has been signed and the internal team member has been "hired" in GreenHouse, the Candidate Experience Specialist will complete the following steps:

1. Once the start date change request comes through, CES will advise the recruiter to collaborate with the hiring manager or PBP to raise a HelpLab ticket for the People Connect team to make these changes in Workday.
The hiring manager or PBP should provide confirmation of the new start date via the HelpLab ticket.
1. CES can update GreenHouse:
   - Go to Offer Details
   - Click the edit pencil next to the start date
   - Select the new Start Date
   - Save
   - In the "Make a Note" section in Greenhouse, state the old start date and the new state date, and tag the person on FP&A (typically the second approver) who approved the offer.
   - Save

### How to Update a Start Date After a French or Spain contract has been signed

   Please follow the normal start date change [process](/handbook/hiring/), thereafter, please follow the following steps:

   1. Make a copy of this Start Date Amendment [letter](https://docs.google.com/document/d/1qpxTi6nPrT4KXDi87tDAWm49D9NZNvTS/edit)
   1. Edit all the highlighted details and save the document on your desktop
   1. In Docusign, create a new envelope and set the signing order as follows:
      - 1 - GitLab France or Spain Signatory (sign)
      - 2 - The candidate (sign)
      - 3 - Alessio Spaggiari (copy)
   1. Use the TextExpander ‘StartdateFS’ in the body of the email in Docusign
   1. Request the signatory in the contracts Slack Channel `#contracts-to-sign` to sign the letter
   1. Once the document has been signed, load it onto the candidate's profile in WorkDay

### How to Void a Contract Before a Candidate Signs

In rare cases, we may rescind our offer before a candidate signs the contract. Work with the Recruiter, Hiring Manager, People Business Partner, VP of Talent Acquisition, and Contract Employment Counsel on ensuring uniform communication. Once the candidate has been informed verbally and via email by the talent acquisition team, follow these steps:

1. Ensure the email is exported into the Activity Feed in Greenhouse.
1. Void the contract in DocuSign utilizing the same communication that was emailed.
1. Reject the candidate in Greenhouse. Be sure to select 'Reject and Don't Send Email.'

### How to Void a Contract when the candidate declines the offer and not marked as hired in the system

In cases where the candidate has declined the offer verbally or via email to the talent acquisition team or CES, follow these steps once the recruiter confirms it is okay to void the contract:

1. Go to the docusign portal, under the " waiting for others" tab, click on the candidate's name whose contract needs to be voided.
1. Under "More" tab, click "Void". Enter the reason for voiding the contract e.g "Candidate declined offer" then click on Void.
1. Go to the candidate's Greenhouse profile, make a note saying the contract is voided by copying the recruiter. This will prompt the recruiter to reject the candidate in GH if it hasn't been done.

### How to Resend a Contract After Being Marked as Hired

There are certain times when a contract needs to get resent to the candidate after they have been hired into the system, should that happen. Follow the steps below:

1. If the req is already closed, tag the Enablement team in the greenhouse profile explaining the situation and that the req needs to be reopened to resend a contract.
1. Unhire the candidate in Greenhouse. (If the position is Closed, Enablement will need to assist with this step).
1. Resend the correct contract and follow standard steps for doing this.
1. Once you receive the contract back, **before** marking the candidate as hired in Greenhouse - ping the People Connect team in the `#peopleop-alerts-private` slack channel and explain exactly what the change was. The updated details will not update Workday and will need to be manually corrected by the People Connect Team.
1. Upload the new contract to their Workday profile.
1. Ping the People Connect Team and let them know the contract has been updated and the details in Workday can be corrected.

For Talent Acquisition Enablement:

1. Once notified by the CES team, copy the Job Approval Chain and add it to the Approval Details Notes section. Include the names of the approvers, the dates approved, and the reason as to why the requisition is being re-opened. Tag the Finance Business Partner, CES, and Recruiter in this note.
1. From the Approvals page, select 'Edit Job & Openings'
1. Duplicate the Opening that needs to be re-opened.
1. Bypass approvals in the Job Approval section to change the Job Status from Draft to Open.
1. Inform CES once the req is open.
1. When the revised contract is uploaded by the CES, verify if the core fields on the offer remain the same. If it remains the same, bypass offer approvals and inform the CES once completed.
1. Once the CES team marks the candidate as hired in Greenhouse, close the duplicated opening and save changes.

### How to Keep Candidates Informed of Any Delays in the PEO Contract Process

Occasionally, there can be delays between the candidate receiving the PEO New Hire Document issued by the CES team and the official contract from a PEO. This delay can result in a nervous wait for the candidate. We must keep anyone who has not received their full contract from our PEO informed of any delays outside of the PEO SLAs.

The Candidate Experience Specialist who initiated the contract process is expected to follow up with the PEO every 24-48 hours until the contract is sent and will note of follow-up dates in the [PEO Tracker](https://docs.google.com/spreadsheets/d/1gSOVTJ1Yv-YsSaliJwKVf-1H0vBZXxb5NWFiqCwT-uo/edit#gid=0). This communication should be sent in Greenhouse, so that the communication is captured in the activity feed. If there are any extreme circumstances that will result in a contract getting to the candidate outside of the PEO SLA's, the CES will also note those in the PEO Tracker. Recruiter is expected to keep the candidate updated on the progress of their contract every 24-48 hours until the candidate receives their contract. A simple message that explains the delay is all that is necessary. As a Candidate Experience Specialist or Recruiter, you're encouraged to utilize the Greenhouse reminder feature to manage these updates and log the email in Greenhouse.

## Amended Contracts

Contract amendments or modifications are processed by the Candidate Experience Specialist if the team member has not started or by the People Connect Team member if they have.

### Amendments prior to starting with GitLab

If an amendment needs to be made and the previous contract was never active, the Candidate Experience Specialist should:

- Ask People Connect in the `people-exp_ces` Slack channel to delete the previous contract from Workday.
- Upload the updated contract in the Documents section of the team member Workday profile, using the 'Contracts and Changes' document category.

*Note: It is essential that People Connect Team members are informed of all changes, as various fields must be updated in Workday.*

### Amendments to contracts for new hires with planned relocations

1. Candidate Experience Specialist will ensure that there is verbiage clearly stating the terms of the compensation changes for relocation after the new hire's start date and ensure that the Total Rewards team has approved both compensations.
1. If you are unsure about the Total Rewards approval, CES will ping the Total Rewards team in the Approval Notes.
    - Navigate to the bottom of the candidate's GH profile
    - See "Approval Notes"
    - Click "Leave a Note"
    - Tag the Total Rewards team member who approved in a note to confirm that both compensation values have been approved
    - Tag the Recruiter as CC
1. Once Total Rewards has confirmed both have been reviewed and approved, generate the appropriate contract
1. Download the Word version of the contract and upload into Google Drive for editing. Don't click to open the doc, just transfer it into Drive so it doesn't impact formatting.
    - Navigate to Google Drive
    - Click "New" in the upper corner of the left toolbar
    - Select "File Upload"
    - Select the contract
1. Add lines at the top of the document for categories to include Compensation for the relocation
    - Example for relocation from ID to CA:
        - CA Compensation: $ USD
        - ID Compensation: $ USD
1. Update Section 10 Location verbiage:
    - Original
        - 10. Location. Your employment with GitLab is conditioned upon your permanent legal residence being near Boise, ID. If your permanent legal residence changes from that location you must notify the Company prior to any such changes. Changes to your permanent legal residence could result in a change to your compensation, benefits, and in some circumstances, termination of your employment.
    - Updated
        - 10. Location. Your employment with GitLab is conditioned upon your permanent legal residence being near Boise, ID and you've disclosed a planned move to San Francisco, CA on or around January 1st, 2021. If your permanent legal residence changes from those locations you must notify the Company prior to any such changes. Changes to your permanent legal residence could result in a change to your compensation, benefits, and in some circumstances, termination of your employment.
1. Delete out all signature tokens from the document, because they will otherwise show up as text in DocuSign.
1. Save and download the contract as a PDF
1. Upload in GH by selecting "Upload Replacement"
1. Stage contract as normal
1. Add tokens back in after changing signing order
1. Send
1. When the contract is completed, message People Connect to make sure they note the relocation.

### Amendments after starting with GitLab

A contractor requests a modification to their contract due to a name change/company incorporation (Example: The individual recently incorporated a company, and would like to invoice GitLab through their company versus individually)

- The People Connect Team member should log the requested change in the Documents section of the team member Workday profile, using the 'Contracts and Changes' document category.
- The People Connect Team member should draft the new contract using the appropriate template in the [Employment Contracts](https://internal.gitlab.com/handbook/people-group/people-operations/people-connect/employment_contracts/) internal handbook page. ***Please remember to always make a copy of the template before editing.***

*Important: Employment contracts cannot be backdated. If a team member requests to backdate a contract for invoicing purposes, an addendum should be added to the contract stating: "As the Contractor has not invoiced GitLab for payment since their start date on `contractor start date`, GitLab will pay the Contractor for this period of time in accordance with the Contractor's base compensation". The start date on the new contract should always reflect the date the contract is staged for signatures.*

- The People Connect Team member should stage the contract in DocuSign to be signed by both the team member and the Director of People Operations.
- Once siged by both parties, the contract should be uploaded to the Documents section of the team member Workday profile, using the 'Contracts and Changes' document category.

### How to Unhire a Candidate After Contract is Signed

If for some reason a candidate declines an offer after they have been hired into the system, whoever receives that information needs to make sure `@ces` is tagged in the Greenhouse profile and is made aware that the candidate will no longer be starting at GitLab. Please note that the steps below are assuming that the person will not be working for GitLab; if you are hoping to just amend their offer after they've been marked as hired, please view the Resend process above.

If they have been hired in Greenhouse and exported to Workday, the team will need to follow these steps:

1. Unhire the candidate in Greenhouse if the req is still open by clicking the "unhire" button on the candidate's offer. If the req is closed, ask Enablement to unhire.
1. Ask the Recruiter to reject them in Greenhouse; add reasons in notes, you may add the email that was sent by the candidate. Click 'reject and don't send email'.
1. Cancel any scheduled emails in Greenhouse.
1. If they were hired via a PEO, inform the contact person at the PEO of this change immediately, ideally before onboarding starts. If they are in a country that uses outside payroll, we will need to inform the payroll company as well.
1. Message IT, People Connect, and the Sr. Background Check Specialist in the #people-ops-ces channel to let them know to cancel any laptop orders, onboarding issues, background checks, and remove from Workday.
1. If the Recruiter has not already tagged the FP&A approver in the Greenhouse notes, please tag them to let them know that the candidate has withdrawn.
1. If the Recruiter has not done so already, add a candidate tag of `Rescinded Acceptance` to the candidate's profile.

**Enablement steps:**

1. Make a note on the Approvals tab and tag each job approver who approved the job last. Note the date approved and let them know that no action is needed, that you are not adding additional headcount, and that you will be reapproving on their behalf as they have already approved.
1. Open a draft opening through the Approvals tab with "TEMP" in all empty mandatory fields.
1. Approve on behalf of Total Rewards (job approval step 1).
1. Mark the candidate unhired on their candidate profile.
1. Remove the temporary opening on the approvals page. This will happen in two steps: first, you'll need to close the opening (using the same process you used to open it), save, and then go back in again to delete the record of the opening. There is a bug in Greenhouse that impacts pop-ups during this stage, so you may need to resize your browser if you're not seeing confirmation messages.
1. Approve the final approvals on behalf of those who originally approved.
1. Inform any involved parties of the unhiring status who will be taking next steps.

## Job Change Letter

When a team member applies for and receives a new position through Greenhouse, a Job Change Letter is prepared in lieu of a new contract using DocuSign. The Candidate Experience Specialist will prepare the letter. This document is signed by the Director, Total Rewards or the Sr. Director, Global People Operations or the Chief People Officer and the team member through DocuSign. Using the Offer through DocuSign - Job Change Letter template in Greenhouse the letter is cc'd to peopleops@gitlab.com team for processing.

Effective dates for a job change letter should be the first (1st) of the month or the sixteenth (16th). For Sales or Sales Development team members, they can only be the first of the month. These effective dates do not need to be on a business day and should be adhered to payroll purposes.
Please note that JCLs cannot be used if a team member is moving from the Federal, LLC. entity into any other entity **or** any entity that is not Federal, LLC into the Federal, LLC. entity. In those cases, a new contract **must** be issued as there are tax implications to this entity.

If the team member is making a lateral move where there is no change in compensation, then the start date can be any day of the month.

When generating a job change letter for a PEO, the steps remains the same as outlined below. However, select the JCL template that does not include RSUs, and send the RSU details via DocuSign email.

The Candidate Experience Specialist needs to merge any additional candidate profiles before marking as hired. If the profiles are not merged, it will create a duplicate and mess with the employment bot sync to Workday. The signed letter is uploaded into Workday under the Contracts and Changes folder on the Documents Tab by the Total Rewards Analyst.

When an internal transition is taking place and the start date for that JCL is amended, please ensure to update the People Connect team via Slack in the `#people-connect_ces` channel of the new start date.

If a team member goes through a promotion through WorkDay versus Greenhouse, a [Job Change Letter](/handbook/people-group/promotions-transfers/#job-change-letter) is prepared by the Total Rewards team as listed on their handbook page.

CES: Follow the instructions below on how to create and send a job change letter.

1. Confirm that the start date is either on the 1st or 16th of the month. For Sales or Sales Development, the start date should be the 1st. This is for payroll purposes and does not need to be on a business day.
1. The signatory matches the appropriate entity. If the candidate is located in the US (including Federal), Morgan Wilkins can be a signatory. If the candidate is employed through a PEO, Morgan Wilkins and Marissa Ferber can be signatories (this process is subject to change)
1. Next, Click Generate
1. Select Job Change Letter template in Greenhouse:
    - Job Change Letter - OTE/with RSU's
    - Job Change Letter - No OTE/with RSU's
    - Job Change Letter w/ OTE, no RSU's
    - Job Change Letter, No OTE, No RSU's

JCLs should be treated like contracts, where RSUs are only features in US ones and all other countries should have text within the DocuSign email instead.

1. Click on Send through DocuSign
1. You will be redirected to DocuSign.
1. On the top left of the screen, click where it says the candidate's name, then click "Edit Recipients". Change the order of recipients to reflect the following order:
    - #1 is Director, Total Rewards (needs to sign)
    - #1 is Recruiter (receives a copy)
    - #1 Hiring Manager (receives a copy)
    - #2 Candidate (needs to sign)
    - #3 People Ops (receives a copy)
    - #3 Nitin Upadhyay and Julia Demina (receives a copy)
    - This ensures that the contract goes to the GitLab signatory to sign first, as well as the recruiter for a Cc and once signed by them it will go to the People Experience for an update of records.
1. Then click "Done".
1. When the JCL is signed, ensure that you merge profiles before Hiring to avoid creating duplicate profile

## Contractor Conversions

A contractor conversion is when a GitLab contractor is moving into a permanent position. Recruiters should communicate to their CES partner that a candidate is going through a contractor conversion process. You can confirm this by checking that the "source" says Contractor Conversion, which will show up on the requisition. CES team members will follow the same steps as a regular contract, however there are a few nuances to note:

1. **Reference Check Forms:** You will need to ensure the candidate has completed the reference check form. You may need to remind recruiters that this is required when contractors transition to a permanent position. The candidate does not need to provide references again however, they will need to disclose outside work and PIAA.
1. **Start Dates:** You may find that start dates with contractor conversions have quicker turnaround times so there are no gaps between a contract end date and a new hires' start date (i.e. a request to start in less than 10 business days, or to start on a non-start date).
1. **Background Checks:** Please check with the Senior Background Check Specialist in the backgroundcheck-ces Slack channel to confirm if you need to initiate a new background check. If there is no gap between the contract and the permanent position, you may not need to initiate a new background check.
1. **Mark as Hired:** After you mark a candidate as hired in Greenhouse, you will need to leave a comment notifying People Connect in the [peopleops-alerts](https://gitlab.enterprise.slack.com/archives/CLTBQ9XC7) Slack channel that it is a contractor conversion.
1. **Laptop/IT:** For all contractor conversions, CES will need to confirm with IT Ops via the [people-connect_CES](https://gitlab.enterprise.slack.com/archives/GJT1K944Q) Slack channel whether the candidate will need a new laptop or not.
    - If they do not need a new laptop, CES will remove the "Ordering your laptop" section from the Welcome email to the candidate.

## Rehires

In the event that a former team member is rehired with the company, they will still go through the normal interviewing process and standard onboarding. Once the contract is signed, CES should ensure that there are no profiles left to merge and that `Former Team Member` is selected as a candidate tag on the right hand side of their profile. They should have their old hire record on their Greenhouse account.

Please let People Connect know in #peopleops-alerts-private if a rehire is happening.

## Process for GitLab team-members in the Netherlands

In this location, a temporary contract (tijdelijk contract) is for 12 months, with a pre-determined end date. A dismissal procedure is not required to terminate a temporary contract at the end of its duration. However communication about the extension of the contract must happen at the latest 1 month before the actual contract end date (aanzegtermijn).

It is common for Dutch employers to offer a second temporary contract when the first expires, but it's not guaranteed. As a Dutch employer, this is standard procedure for GitLab. As of 2015-07-01, employees who have worked with an employer on temporary contracts for at least two years are entitled to an indefinite contract if the work agreement continues, and this is known as the chain rule (ketenregeling).

The process for New Hires is as follows:

1. The offer is made by the recruiter per the [hiring process](/handbook/hiring).
1. If the date of birth is not filled out and cannot be found in a reference check form, the Candidate Experience Specialist can use the emails the email template Contract Info Request - the Netherlands from GreenHouse and send to the candidate.
1. Ensure the start date is on a Monday, unless Monday is a holiday or the non-Monday date is legally required.
1. The Candidate Experience Specialist will stage the contract for signature via DocuSign, CC the hiring manager, and CC the HRSavvy group email. This will ensure our payroll provider in this location can start their onboarding, well ahead of ours.
1. Please note that you should *not* be running a criminal background check for the Netherlands, because they'll be doing a different process (Certificate of Good Conduct/VoGS) instead. Please select the Netherlands background check package which only includes employment verification and an extended global sanctions search.

The People Operation Specialist are in charge of [contract renewals](/handbook/people-group/contracts-probation-periods/#contract-renewals). The process the **end of the first 12-month GitLab BV Netherlands temporary contract** is listed in their [Netherlands Renewal Process](/handbook/people-group/contracts-probation-periods/#netherlands-renewal-process) section of the [Contracts, Probation Periods & PIAA](/handbook/people-group/contracts-probation-periods/) handbook page.

*GitLab IT BV contracts should only be used for contractors. All Netherlands **employees** should be issued the GitLab BV contract.*

## Process for GitLab Team Members in Australia or New Zealand

GitLab has an entity in this location. All team members in this location are employees.
Always ensure the start date is on a Monday, unless Monday is a holiday or the non-Monday date is legally required.

## Process for GitLab Team Members in Ireland, the UK or Singapore

GitLab has an entity in this location. The UK, Ireland and Singapore payroll are now processed through Papaya. There is an updated “Offer Through DocuSign” email templates to group these countries together.
Papaya will follow up with the team members in these locations regarding their payroll.

Please note that Northern Ireland is under the United Kingdom, so if you see an address that includes UK you should hold and verify on google maps where the candidate is located and whether a different contract and background check are needed.

## Process for GitLab Team Members in South Korea, or France

GitLab has entities in Singapore, South Korea, and France. All team members in this location are employees, but payroll will be processed through Global Upside. Please be sure to select the correct docusign email template so they will be CC'ed as the final step of the offer process.

Reminder: France requires contracts to be individually drafted by the Legal team. There is a [SSOT document](https://docs.google.com/spreadsheets/d/1HQxOwt30v1qffulaZay61aj_A5edQgb_zfBrhoq0CgA/edit#gid=0) where we keep track of these requests.

Always ensure the start date is on a Monday, unless Monday is a holiday or the non-Monday date is legally required.

## Creating a French and Spain Offer

1. You will receive a req to create a French or Spain Offer.
1. In Greenhouse, click on Job setup, then hiring team, then add Sarah Rogers & Darren Burr to the job granting them the Job Admin: FPA and Legal permissions, then save.
1. Ensure the start date is on a Monday, unless Monday is a holiday or the non-Monday date is legally required.
1. Send a Slack message to the Legal Team in [ces_legal_contracts](https://gitlab.slack.com/archives/C05R0R495L6) requesting assistance with the offer. When making the request in the channel, please indicate the candidate's name and include the link to the GH profile
1. One of the Legal Team members will respond with the following information:
    - The GreenHouse Offer Template that you should use
    - The wording that should be added to the template (including information on where the wording should be placed). This wording will be placed as provided by Legal on both the English & French sides in English.
    - If the offer does not include draw language, Legal will confirm which part of the offer template should be removed.

Once this information has been received, please go onto GH and follow the steps below:

1. Click on the settings icon
1. Select 'Offer Templates' on the left-hand side
1. Search for the Template as advised by Legal
1. Click on the three dots on the right-hand side of the template you will be using and select the 'download' tab
1. Open the document in Google Docs
1. Make all the changes as advised by the Legal Team and save the document
1. Go back to the offer templates page on GH
1. Click on 'Upload New' on the right-hand side
1. Upload the amended document
1. Then follow the normal offer creation process in GH and select your uploaded document as the offer template for this offer.
1. Please remember to delete this template once you have completed the process and the offer has been signed by the signatory & the candidate

## Creating an Israel offer

When you receive a request to make an offer in Israel, please take the following steps.

1. In Greenhouse, click on Job setup, then hiring team, then add Sarah Rogers & Darren Burr to the job granting them the Job Admin: FPA and Legal permissions, then save.
1. The start dates for Israel team members can be a Sunday, given that their work week is Sunday through Thursday. Please let the People Connect Team know that the start date would be a Sunday.
1. Send a message to the Legal Team the in ces_legal_contracts slack channel requesting assistance with the offer. When making the request in the channel, please indicate the candidate’s name, include the link to the GH profile & request them to give the compensation breakdown as well as let you know what contract template to use.
1. One of the Legal Team members will respond with the following information:
   - The GreenHouse Offer Template that you should use
   - The compensation breakdown & CES to add the ID number in Exhibit A
   - The language that should be added to the template (including where on the contract the wording should be placed).

Once this information has been received, please go into GH and follow the steps below:

1. Click on the settings icon
1. Select 'Offer Templates' on the left-hand side
1. Search for the Template as advised by Legal
1. Click on the three dots on the right-hand side of the template you will be using and select the 'download' option
1. Open the document in Google Docs
1. Make all the changes as advised by the Legal Team and save the document
1. Go back to the offer templates page on GH
1. Click on 'Upload New' on the right-hand side
1. Upload the amended document using a title with the candidates initials (this is so you can identify the template when you go to generate the contract)
1. Then follow the normal offer creation process in GH and select your uploaded document as the offer template for this offer.
1. Please remember to delete this template once you have completed the process and the offer has been signed by the signatory & the candidate

Once after the candidate has signed the offer, please send the "New Hire Welcome Email" where there is a laptop request form. GitLab can ship laptops to Israel and there is no need for the team member to self procure laptops anymore for Israel.

## CXC (NOTE: HIRING IS CURRENTLY PAUSED HERE: Please speak with Enablement before sending offer letters)

GitLab is working in partnership with [CXC Global](https://www.cxcglobal.com/) to employ GitLab team-members located in **Poland**, **Ukraine**, **Romania**, **Russia**, **Serbia**, & **Slovenia**. The actual employment contracts will be sent and issued by CXC and are in accordance with local labor law. CXC also handles the processing and payment of payroll and associated taxes and compliance in each of the countries on behalf of GitLab. The contracts themselves are between the individual and CXC.

CXC provides a 12 month contract in these locations, and this can be extended. They are only able to support contractors that have an established entity/company in these countries (listed above). The offer details will be provided to CXC by GitLab's hiring team.

To create the contract:

1. Offer is made by the recruiter per the [hiring process](/handbook/hiring).
1. The Candidate Experience Specialist emails the new team member the Contract Info Request - CXC from GreenHouse.
    - Click "Email CANDIDATE NAME"
    - Select "Contract Info Request-CXC" from dropdown.
    - CC Recruiter
    - Click "Send Email"
1. Ensure the start date is on a Monday, unless Monday is a holiday or the non-Monday date is legally required.
1. The Candidate Experience Specialist will check if there is a probationary period.
    - Go to [Probationary Periods for Team Members Employed by a PEO](/handbook/people-group/contracts-probation-periods/#probation-period) and check the candidate's country.
    - Select the duration of the probationary period (if any) in the "Offer Details" dropdown. If there isn't one, select "N/A" in that field.
1. The Candidate Experience Specialist will check if the contract is indefinite or fixed.
    - If the contract is indefinite, select "Indefinite" from the dropdown in "Offer Details".
    - If the contract is fixed, select "Fixed Contract" from the dropdown in "Offer Details" and enter the end date under "End Date".
1. Once the additional information is received, The Candidate Experience Specialist will generate the PEO form out of GreenHouse.
    - Click "Generate"
    - Select "PEO New Hire Template" from the dropdown
    - Click "Generate"
1. The Candidate Experience Specialist will stage the form for their own signature via DocuSign, the new team member and the appropriate CXC contact. Contact details can be found in 1password => People Operations Vault => Entity & Co-employer HR Contacts.
1. The Candidate Experience Specialist should add the candidate to the [PEO Tracking Sheet](https://docs.google.com/spreadsheets/d/1gSOVTJ1Yv-YsSaliJwKVf-1H0vBZXxb5NWFiqCwT-uo/edit#gid=0) and keep track of communication between GitLab.
1. CXC will then prepare the SOW and contract.
1. CXC will then reach out to the candidates directly to coordinate the contract signing and onboarding to CXC's payroll.
1. Kindly allow a duration of one week for CXC to complete their process. This might mean that a two week notice period to start at GitLab, could increase to three weeks, its important to communicate this duration to new hires in this location.
1. CXC will inform the Candidate Experience Specialist when the contract is signed.
1. The Candidate Experience Specialist will mark the candidate as hired.
1. The CES will adjust the 'Accepted' date to match the 'Sent' date.
1. The Candidate Experience Specialist will now mark the candidate as hired.

## Preparing Employment Agreements for GitLab team members employed via Global Expansion (GX)

GitLab is working in partnership with Global Expansion to employ GitLab team-members located in:

- Mexico
- Costa Rica
- Kenya
- South Africa
- UAE
- Latvia
- Philippines
- Austria
- Chile

1. The Offer is made by the recruiter per the hiring process
1. If the Nationality field is not filled out and cannot be found in the Reference Check form, CES sends “Contract Info Request-Global Upside” email to the new hire to collect additional details
1. Ensure the start date is on a Monday, unless Monday is a holiday or the non-Monday date is legally required
1. The Candidate Experience Specialist will check if there is a probationary period.
1. Go to [Probationary Periods for Team Members Employed by a PEO](/handbook/people-group/contracts-probation-periods/#probation-period) and check the candidate’s country.
1. Select the duration of the probationary period (if any) in the “Offer Details” dropdown. If there isn’t one, select “N/A” in that field
1. The Candidate Experience Specialist will check if the contract is indefinite or fixed
1. If the contract is indefinite, select “Indefinite” from the dropdown in “Offer Details”
1. If the contract is fixed, select “Fixed Contract” from the dropdown in “Offer Details” and enter the end date under “End Date”
1. Once additional details are obtained, update the offer details to reflect all information. The CES should be the signatory
1. Generate “PEO Template!” in Offer Documents to Send through DocuSign
1. Choose template Offer through DocuSign -GX - Global Expansion -To User, Self (CES) -Sign and complete
1. Log in to the GX 1 Platform using the CES Team log in credentials (you can find this information in the CES desk repository)
1. Click + New Employee (pink button) on the landing page
1. Click the "+" icon on the left hand side of the gray bar
1. Add personal information of new hire to required fields
    - Legal Last Name
    - Legal First Name
    - Email
    - Contact Number
    - To Country
1. Add Position details
    - Job Title
    - Intended Start Date
    - Contract Duration
    - Projected End Date (if contract is fixed)
1. Add CES name and contact information to the Signatory fields
1. To "Line Manager" fields, add the hiring manager's information
1. Use the information on [Probationary Periods for Team Members Employed by a PEO](/handbook/people-group/contracts-probation-periods/#probation-period) to add employee & employer notice periods as well as probation period.
1. Add benefits information:
    - Medical Benefits: Use Country guide information located in CES Repository to complete the two fields
    - Employment Retirement Insurance: Use Country guide information located in CES Repository. If nothing is noted in the guide for the country, select “Not Applicable”
    - Benefits Policy Duration: Select "auto renew" for contract duration
    - If you see three check boxes for Visa & background screening: ONLY FOR UAE - Select YES (Visa only) and ALWAYS Select "No" for the background screenings for all countries
1. GX Compensation
    - Monthly Basic Salary: Enter the number “1” (you are not expected to calculate this). Add the candidate’s annual salary to the additional notes section, making sure to include the currency
    - Local currency: Click the down arrow next to field and search for the country. You can also view the currency in the candidate’s greenhouse offer.
1. If you have all the details populated,  click Initiate New Employee (or Save and Submit Later if you are missing data)
1. GX will then review the details and compose the employee’s contract. They will then email ces@gitlab.com when it is complete and ask us to review. You will need to log into the GX platform FIRST, and then click the link in the email sent by GX
1. Review all details of the contract to confirm accuracy
    - If there are items missing, you have the ability to write feedback notes and send back to GX. Click the drop down and select “REJECT - the following changes are required” and submit
    - If everything looks good, click the drop down and select “APPROVE - I am happy with this employment contract” and submit
1. GX will also be sending a 1 page docusign to ces@gitlab.com where we need to confirm employment details again. Please review and sign the document if accurate. Docusign will auto populate a signature of “GL CES Team” but you can adjust and add your name in front of that title. Add your title and send
1. GX will then release the employment contract to the candidate and notify us via email as soon as it is signed. We may also receive an email to our desk when they manually upload the contract to their portal, but these can be ignored if you have heard from them already
1. Proceed with sending the correct Welcome Email
1. Before making the candidate as hired in GH, please make sure all other candidates have been rejected. Once that is done, mark the candidate as hired in Greenhouse, adjust the ‘Accepted’ date to match the ‘Sent’ date, and close the req

## Preparing Employment Agreements for GitLab team members employed via Global Upside

GitLab is working in partnership with [Global Upside](https://www.safeguardglobal.com/) for employing GitLab team-members located in:

- India

The process for creating and sending an agreement is as follows:

1. The Offer is made by the recruiter per the [hiring process](/handbook/hiring).
1. If the Nationality field is not filled out and cannot be found in the Reference Check form, CES sends "Contract Info Request-Global Upside" email to the new hire to collect additional details.
1. Ensure the start date is on a Monday, unless Monday is a holiday or the non-Monday date is legally required.
1. The Candidate Experience Specialist will check if there is a probationary period.
    - Go to [Probationary Periods for Team Members Employed by a PEO](/handbook/people-group/contracts-probation-periods/#probation-period) and check the candidate's country.
    - Select the duration of the probationary period (if any) in the "Offer Details" dropdown. If there isn't one, select "N/A" in that field.
1. The Candidate Experience Specialist will check if the contract is indefinite or fixed.
    - If the contract is definite, select "Indefinite" from the dropdown in "Offer Details".
    - If the contract is fixed, select "Fixed Contract" from the dropdown in "Offer Details" and enter the end date under "End Date".
1. Once additional details are obtained, update the offer details to reflect all information. The CES should be the signatory.
1. Generate "PEO New Hire Template" in Offer Documents to Send through DocuSign
1. Choose template *Offer through DocuSign -Global Upside*
    -To User, Self (CES)
    -Sign and complete
1. Download the completed Statement of Work in PDF form to upload it into Egnyte.
    -Make sure the downloaded file is titled with new hire's full name
1. Once in Egnyte, navigate to *"/Shared/GPS/Active Clients/GitLab/IN/HR/Employee Master/Client Upload/New Employee Information"*
1. Click *Upload* to place new hire's statement of work in this folder
1. Inform the Global Upside team (gitlabHR@globalpeoservices.com) of any new hires by sending email template *Email to Global Upside* under "Email the Team" in Greenhouse to let them know that a new SOW was uploaded into Egnyte and the employee's name.
1. The Candidate Experience Specialist should add the candidate to the [PEO Tracking Sheet](https://docs.google.com/spreadsheets/d/1gSOVTJ1Yv-YsSaliJwKVf-1H0vBZXxb5NWFiqCwT-uo/edit#gid=0) and keep track of communication between GitLab.
1. Once Global Upside has drafted up the contract, they will place it in Egnyte and email the CES to review and approve.
    -CES should double-check that the contract reflects all the correct information that we sent to them.
1. Once the contract is signed by the new hire, Global Upside will notify the CES.
1. Proceed with marking them as hired in Greenhouse, adjusting the 'Accepted' date to match the 'Sent' date, sending the welcome email, and making sure all other candidates have been rejected prior to marking as hired and closing the req.

## Remote.com

GitLab has partnered with [Remote.com](https://remote.com/) to hire in Brazil, Denmark, Switzerland, Italy, Sweden, Luxembourg and Hungary. The actual employment contracts will be sent and issued by Remote and are in accordance with local labor law.  The offer details will be provided to Remote by GitLab's hiring team.

To create the contract:

1. Offer is made by the recruiter per the [hiring process](/handbook/hiring).
1. If the Nationality field is not filled out and cannot be found in the Reference Check form, CES sends "Contract Info Request-Global Upside" email to the new hire to collect additional details.
    - Click "Email CANDIDATE NAME"
    - Select "Contract Info Request-Remote.com" from dropdown.
    - CC Recruiter
    - Click "Send Email"
1. Ensure the start date is on a Monday, unless Monday is a holiday or the non-Monday date is legally required.
1. The Candidate Experience Specialist will check if there is a probationary period.
    - Go to [Probationary Periods for Team Members Employed by a PEO](/handbook/people-group/contracts-probation-periods/#probation-period) and check the candidate's country.
    - Select the duration of the probationary period (if any) in the "Offer Details" dropdown. If there isn't one, select "N/A" in that field.
1. The Candidate Experience Specialist will check if the contract is indefinite or fixed.
    - If the contract is indefinite, select "Indefinite" from the dropdown in "Offer Details".
    - If the contract is fixed, select "Fixed Contract" from the dropdown in "Offer Details" and enter the end date under "End Date".
1. The CES will change the signatory to themselves to stage the offer for their signature.
1. Once the additional information is received, The Candidate Experience Specialist will generate the PEO form out of GreenHouse.
    - Click "Generate"
    - Select "PEO New Hire Template" from the dropdown
    - Click "Generate"
1. The Candidate Experience Specialist will choose template *Offer through DocuSign -Remote.com* and will copy gitlab@remote.com on the email.
1. In DocuSign, the CES will update the signing order to CES/Signatory as number 1 to sign and all other copied individuals as number 2, to receive a copy.
1. CES will send PEO template and sign once it is received in their inbox.
1. Once PEO template is signed, CES can upload candidate into the Remote.com platform (see more details instructions on how to do so, below).
1. Remote will prepare the New Employee Contract and will inform the Candidate Experience Specialist when the contract is sgined.
1. Once  CES receives confirmation that the candidate has signed the Remote.com contract (can be viewed in portal), they will continue steps as normal - send Welcome Email and mark the candidate as hired.
1. The CES will adjust the 'Accepted' date to match the 'Sent' date.

## How to add the New Hire to the Remote platform

1. Log into the [Remote](https://employ.remote.com/dashboard) platform
1. Click the onboarding tab on the left side of the page
1. Click 'add new employee' on the top right corner of the page
1. Click 'employee'
1. You be will be on the 'employment eligibility' page - fill in the candidates details and click continue
1. You will now be on the 'basic information' page - fill in the candidates details and click continue
1. You be will be on the 'contract details' page - fill in the contract details

Kindly note the following when filling in this section:

1. Contract Duration: Most contracts will be indefinite, unless specified by the Recruiter
    - Probation Period: Use the default or minimum options specified by Remote. Please utilize the [Probation Section](/handbook/people-group/contracts-probation-periods/#probation-period) of the handbook to determine probation.
    - For Mexico: When adding a team member to the Remote platform you should select 30 days as a Christmas bonus, not 15.
1. Type of employee: Full time
1. Annual Gross salary: as stated in the offer details in GH
1. Annual leave: Is usually the statutory minimum. You can also utilize the [General & Entity Specific Benefits page](/handbook/total-rewards/benefits/general-and-entity-benefits/remote-com/)
   - Mexico you can input 20 days
1. Is this employee approved for outside employment: No
1. Signing bonus: as stated in the offer details in GH
1. Other Bonus: Do not include guaranteed draw. If asked, please loop in Marissa. Remote does not currently have enough of an in-depth understanding of our bonus structure to be able to include this information.
1. Commission: No
1. Equity Compensation: Do not include.
1. Number of paid time off days: Select the statutory minimum recommended days as mentioned by Remote, if there is an option, select the lowest number (this should be the statutory minimum)
1. Role Description: Copy/paste the job description within the job family. Make sure you're only including the specific role they have, and you can skip the fillers at the beginning and end.
1. Training requirement: Leave blank
1. Supervisor Name: as stated in the offer details in GH
1. Experience level: There will be different versions of these choices based on the country you are selecting. Choose the one that most closely matches your position, and ask the recruiter for recommendations if you're unsure.
1. Work Address: Select Yes
1. Benefits - Select the following per country:

| Country | Benefit plan |
|---------|--------------|
| Denmark | Standard |
| Hungary | Standard |
| Luxembourg | Premium |
| Brazil | Omint Plan (should be added for you) |
| Italy | Premium |
| Switzerland | None |
| Sweden | None |

1. Life Insurance Coverage - For Mexico Hires, Please select "Life/ADD Insurance of 350 MXN (~18 USD)". For more details on benefits for team members who are contracted through Remote. Click [here](/handbook/total-rewards/benefits/general-and-entity-benefits/remote-com/#brazil-).
If there are any questions, these should be directed to help@remote.com.
1. Click on the benefits acknowledgement and continue
1. You be will be on the 'billing cycle' page.
1. Click on monthly billing cycle and click continue.
1. You will now be able to review all the candidate and contract details, you are able to edit them should you wish.
1. Once you have reviewed, and everything is in order, click 'invite now'.
1. Please select the option to "add this employee to a single employee plan"
1. Your candidate has been submitted successfully. You are able to see the progress on the Remote homepage.

## How to add the New Hire to the Papaya platform

1. Log into the [Papaya](https://gitlab.papayaglobal.com/backoffice/org/1826/dashboard) platform
1. Click the 'add worker' tab on the top right side of the page
1. Click 'create new request' under the EOR worker block
1. Select the candidates country on the drop down
1. Click next
1. You be will be on the 'worker details' page - fill in the candidates details
1. Please ignore the following: Company ID
1. Click next
1. You will now be on the 'employment terms' page - fill in the details
1. Please ignore the following: expected end date in the case of an indefinite contract & the organizational attributes
1. Click continue
1. You will be on the 'contract compensation' page - fill in the contract details
1. Please ignore the following: allowances & miscellaneous
1. Under contract terms, select the mandatory requirements by local law tabs for all
1. Click next
1. You will be on the 'initial employment terms letter' page - fill in the contract details
1. Should papaya send the candidate the initial employment terms letter prior to the contract - click 'yes'
1. Click next
1. You will now be able to review all the candidate and contract details, you are able to edit them should you wish.
1. Select all the term of the consent clause
1. When should papaya contact the worker - select 'as soon as possible'
1. Click submit
1. Your candidate has been submitted successfully. You will be redirected to the papaya homepage
1. Once you submit the candidate, an alert will be sent to Papaya to inform them of the new project
1. Amit Bengal - AmitBe@papayaglobal.com (Customer Success Manager at Papaya who looks after GitLab) will reach out to the CES to confirm that they have received the alert. Amit should ask for permission to contact the candidate directly - please confirm this ASAP. Papaya will validate the information submitted into the platform and reach out to CES or the candidate should there be any immediate questions regarding the contract information shared
1. An offer overview (Offer Template) with the basic offer details will be sent to CES to approve (resembles our PEO Template) - once approved, a welcome email will be sent to the candidate - accompanied by the offer template. The Welcome Email will introduce the PEO to the candidate.
1. At this stage, the candidate is also requested to verify their information and provide documents needed to complete the request.
1. Once the candidate has verified their information and provided the required documents, Papaya sends the offer draft to the Local Team (a contact person in the candidates country) to review the contract against the in-country laws - Duration: 48 hours
1. The Local Team then sends the offer to Papaya's Legal Team once they have done their part. The Legal Team then approves the final offer. - Duration: 24 hours
1. The approved offer will then be uploaded onto the Papaya Platform under hidden documents. CES will be informed to go and approve the final draft before it can be issued to the candidate.
1. Should there be any questions or amendments that need to be made, depending on their complexity, they could have to be directed back to the Local Team (48 hours), then back to the Legal Team  (24 hours), before making its way back to us again.
1. Once CES approves the offer, Papaya will extend it to the candidate.
1. Should there be any questions or amendments that need to be made, depending on their complexity, they could have to be directed to the Local Team (48 hours), then back to the Legal Team (24 hours), before making its way back to us again for reapproval, then issued to the candidate again.
1. Once the candidate accepts, Papaya will inform us.

## Advance Funds process for locations GitLab can not order laptops

There are a handful of countries, listed [here](/handbook/security/corporate/end-user-services/laptop-management/laptop-ordering//) where new hires will need to procure their own laptop before their start date.

1. The CES team member will identify that the new hire is located in one of these countries, and will send the New Hire Welcome Email - Brazil, Costa Rica, Chile, Armenia, or Ukraine template.
1. This email uses a different Google form than the regular Welcome Email. The new hire will be presented with two options and be asked to select their preference:
    - Purchase and expense for reimbursement through NAVAN on their first day at GitLab
    - Request advanced funds to self-procure
1. IT will receive an issue in their [IT Equipment Order Processing](https://gitlab.com/gitlab-com/it/end-user-services/issues/it-equipment-order-processing/-/issues/?sort=closed_at_desc&state=opened&first_page_size=100) desk with the new hire's selection. If the candidate has requested advanced funds, IT will then tag AP within the issue and provide approval for the laptop purchase. AP will gather the new hire's banking details and release the funds.

**GitLab and New Hire:**

1. Once the verbal offer has been made by the recruiter [hiring process](/handbook/hiring) complete the [Template-GitLab China Employee Offer letter](https://docs.google.com/document/d/1c69dG9TuAB0MgiKj_gLDuHTHpzjocvEAm2okUOKqRIs/edit#) as per How to use this page to prepare a contract.
1. CIIC require a Chinese version of a [Letter of Employment Intent](https://docs.google.com/document/d/1BEHvveYUJkS1xwyd037P_zzitOSotF_68Kbi-c7k8hY/edit).
1. Complete the Letter of Intents with all of the information required/known. This should be completed in [English](https://docs.google.com/document/d/1b3fHqHzXhhoJeskUN-Km9vTLeuszysWPj8PlvXm45ug/edit) first then translated into Chinese using Google Translate.
1. Once this has been done send the GitLab (Chinese & English) versions of the Letter of Employment Intent to the new hire for their review, completion and signature using DocuSign. Ensure that Peopleops and CIIC are copied.
1. Once everything has been signed, print and FedEx the Chinese and English Letter of Intents to CIIC. The address can be found in the PEO China folder > China Employment Options > CIIC in the Google Drive.
1. The Candidate Experience Specialist should add the candidate to the [PEO Tracking Sheet](https://docs.google.com/spreadsheets/d/1gSOVTJ1Yv-YsSaliJwKVf-1H0vBZXxb5NWFiqCwT-uo/edit#gid=0) and keep track of communication between GitLab.
1. The PEO will inform the Candidate Experience Specialist when the contract is signed.
1. The Candidate Experience Specialist will mark the candidate as hired.
1. The CES will adjust the 'Accepted' date to match the 'Sent' date.
1. The Candidate Experience Specialist will now mark the candidate as hired.

**GitLab & CIIC:**

1. GitLab has a Secondment Agreement in place with CIIC, this may need to be updated but CIIC will confirm.
1. Once CIIC have received the documents they will prepare a payment notice and send this to GitLab (peopleops) for payment. This must be paid upfront and may need CFO approval.
1. After CIIC receive payment they will reach out to the new hire to complete a Labor Contract.

**CIIC & New Hire**

Once the Labor Contract has been signed by both CIIC and the new hire the individual can now commence their work with GitLab.

## Employment Agreements for GitLab team members in Germany

From 1 January 2025, the wet-ink signature requirement in Germany has been removed, so that offers can be issued with e-signature via DosuSign (steps set out below). Germany payroll are now all processed through Papaya.

1. CES will ensure that the start date is either a Monday, or the 1st or 16th of the month
1. Please use the signatories listed against the German Entity as per this [table](/handbook/hiring/)
1. Send the offer through Greenhouse and DocuSign. Use the "send through Docusign" template and add the RSU information into the body of the email.
1. Initiate the background check. Please use the Germany Package from the drop down in Sterling.

Candidates in Germany have the right to ask for a wet signature contract.  (Process to be added)

## Employment Agreements for GitLab team members in Japan

GitLab has an entity in Japan (GitLab GK) and use the GitLab GK contracts in this location. All team members in this location are employees.

Always ensure the start date is on a Monday, unless Monday is a holiday or the non-Monday date is legally required.

## Intern Employment Contracts

GitLab participates in hiring interns within the INC entity as well as the Code2College program. Code2College is the FIRST and ONLY program that places high school students into paid, technical internships.

The Intern contract template will be used for both C2C interns and all other interns hired into GitLab. However there are some different necessary steps when processing a C2C intern. Processes are described below.

1. When the offer decision is made, Emerging Talent Coordinator/Recruiter will create offer in GH profile and request approvals as normal.
1. Once approved, CES to send the contract using the "INC Intern" template in GH. Some important details needed in the offer details will be the hourly rate of pay and the end date of the contract (since this is not an indefinite contract). Please ensure these details are in the offer before generating.
1. After the offer is sent, CES will initiate the background check by selecting the Comprehensive Criminal Check with Employment. **IMPORTANT NOTE - If this is a C2C (Code2College) intern - you will only need to select the Comprehensive Criminal Check in Sterling. Employment check is not needed as most C2C interns will be minors.**
1. Because most interns from C2C are minors, at the time the BGC is initiated, CES will also need to send the [Parental Consent Form](https://docs.google.com/document/d/1J0xundRL___Hhg0zNkt7KTMMEgTv63U5rseqTlmv8ok/edit) to the interns guardian.

   - This form can be send via DocuSign
   - Please add appropriate tokens
   - Please set up distribution as follows (guardian email can be recieved from Emerging Talent Coordinator):
      1. Guardian - Needs to sign
      1. Emerging Talent Coordinator - receives a copy

1. Once the offers are signed by the candidate, CES will send the GitLab Inc Intern Welcome Email. **Note: GitLab will provide laptops to these interns. The Welcome Email asks them to fill out form ASAP**
1. Once the req is cleared, CES can mark the Intern as hired.
1. CES will ping People Connect in the #peopleops-alerts slack channel to let them know they just hired in an Intern. **please indicate if they are C2C in your messaging to them**
1. Once Intern is hired into the system - they will move to the responsibility of People Connect who will create onboarding issues and communicate information about the TaNewKi call.
1. If you are notified that the C2C intern requires a "youth work permit", please send form over to People Connect. They will be required to fill out the "employer" portion and submit to the intern/guardians.

## Employment Agreements for GitLab team members located everywhere else (IT BV contractor agreements)

1. Review the [Hiring Status](/handbook/people-group/employment-solutions#country-hiring-guidelines) of the location you are working with. If the location has not been evaluated yet, we issue a IT BV contractor agreement.
1. If the candidate would like to use their own entity for the contractor agreement update the offer details with the Contractor Name and Address. You will use the IT BV Contractor Agreement - C2C in these cases.
1. Generate IT BV Contractor Agreement - Independent or the IT BV Contractor Agreement - C2C
1. Select Send with DocuSign
1. Select the "Offer through DocuSign-IT BV" email template
1. Update the "To" field to include the GitLab signatory and include the hiring manager in CC field
1. Select Preview on DocuSign
1. Once in DocuSign, update the signing order as you would with other contracts and hit send

## Adding Relocation Verbiage to Entity Contracts

1. Candidate Experience Specialist will ensure that there is verbiage clearly stating the terms of the compensation changes for relocation after the new hire's start date.
1. CES will ping the Total Rewards team in the Approval Notes.
    - Navigate to the bottom of the candidate's GH profile
    - See "Approval Notes"
    - Click "Leave a Note"
    - Tag Brittany Rohde in a note to confirm that both compensation values have been approved
    - Tag the Recruiter as CC
1. Once Total Rewards has confirmed both have been reviewed, generate the appropriate contract
1. Download the Word version of the contract and upload into Google Drive for editing
    - Navigate to Google Drive
    - Click "New" in the upper corner of the left toolbar
    - Select "File Upload"
    - Select the contract
1. Add lines at the top of the document for categories to include Compensation for the relocation
    - Example for relocation from ID to CA:
        - CA Compensation: $ USD
        - ID Compensation: $ USD
1. Update Section 10 Location verbiage:
    - Original
        - 10. Location. Your employment with GitLab is conditioned upon your permanent legal residence being near Boise, ID. If your permanent legal residence changes from that location you must notify the Company prior to any such changes. Changes to your permanent legal residence could result in a change to your compensation, benefits, and in some circumstances, termination of your employment.
    - Updated
        - 10. Location. Your employment with GitLab is conditioned upon your permanent legal residence being near Boise, ID and you've disclosed a planned move to San Francisco, CA on or around January 1st, 2021. If your permanent legal residence changes from those locations you must notify the Company prior to any such changes. Changes to your permanent legal residence could result in a change to your compensation, benefits, and in some circumstances, termination of your employment.
1. Delete out all Tokens
1. Save and download the contract
1. Upload in GH by selecting "Upload Replacement"
1. Ping the `Contracts-to-sign` channel in Slack and let the recruiter know that you are sending a contract staged for a future relocation
1. Stage contract as normal
1. Add tokens back in after changing signing order
1. Send

### Employment Offboarding

When team members depart GitLab, People Connect will create an offboarding issue. The CES team is responsible for completing tasks under the `@gitlab-com/gl-ces` section. Please note that offboarding issues are time sensitive and should be completed by the due date set on the issue. Completion of these tasks also ensure GitLab remains compliant.

1. Go to [Employment Issues](https://gitlab.com/gitlab-com/team-member-epics/employment/-/issues) where the offboarding issues can be found. In the search bar, filter issues by the "CES: To Do" label and work on the issues by due date. Once you open up an offboarding issue, navigate to the `@gitlab-com/gl-ces` section and complete the following steps.
1. Open Google calendar, select the "Interview Calendar", and type in the team member's name in the search bar at the top. Ensure the team member offboarding isn't in any active interviews.If the team member appears in an active interview,advise the respective CES team member to work with their recruiters to replace the interviewer.Any interviews that have been grayed out on the calendar, have passed already.
1. If the offboarding team member is from an engineering department, CES to check the hiring repo both [backend](https://gitlab.com/gitlab-com/people-group/hiring-processes/-/blob/master/Engineering/Frontend/2-TechnicalInterview/Interviewers.md),[frontend](https://gitlab.com/gitlab-com/people-group/hiring-processes/-/blob/master/Engineering/Backend/Interviewers.md?plain=0#rubyrails-technical-interviewers) and [Platform POOL](https://gitlab.com/gitlab-com/people-group/hiring-processes/-/tree/master/Engineering/Infrastructure/Platforms?ref_type=heads) to remove the departing interviewer from the pool.
CES can make changes through a merge request e.g "Removed John Doe from list of ruby on rails technical interviewers". CES must only use the merge rights to remove offboarding interviewers from the hiring repo and not make any other significant changes to it.

1. Check for reqs that the team member might be on by searching the team member's name under `Users` in Greenhouse. When searching the team member's name, select the profile with the team member's GitLab email address; this will navigate to their Greenhouse profile settings.
    If you encounter a team member's name listed as "Job Admin: Hiring Manager" with Open job reqs, please following steps:
    - Copy and paste the job req title into a new Greenhouse window and search
    - Select the correct job req by ensuring the req#s match (i.e. 7458)
    - Select Job Set up and navigate to the Hiring Team section
    - Please ensure that the hiring manager position has been filled by another team member. If the hiring manager section is empty or still shows the team member who is offboarding, reach out to the CES coordinator listed and advise the CES team member to work with the recruiter to find a replacement hiring manager & update interview plans.
    - No action is required if the offboarding team member is listed as "Job Admin: Hiring Manager", for a req title which is "Closed", "Draft", or "Template" in it.
1. Once all steps have been completed, navigate to the right hand side of the offboarding issue, remove the "CES: To Do" label, disable notifications, and leave a comment/ notify "Recruiting Ops". (e.g @ destinyreyes ces tasks done)

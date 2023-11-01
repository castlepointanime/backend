# Creation workflow

1. 20231031232049-envelope-created.json: Contract is first generated.
2. 20231031232106-recipient-sent.json: An email is sent to the signer.
3. 20231031232108-envelope-sent.json: The envelope has been sent to the signer.

* Signer fills out the form, but doesn't click "Finish" yet

4. 20231031232209-recipient-delivered.json: Signer finished fields

* Signer clicks "Finish"

5. 20231031232305-recipient-completed.json: Signer finished all fields

* These are for the approver

6. 20231031232307-recipient-sent.json: An email is sent to the approver.
7. 20231031232411-recipient-delivered.json: Approver has finished fields (aka approver has finished signing)
8. 20231031232414-envelope-delivered.json: Envelope is being made
9. 20231031232433-recipient-completed.json: Approver has finished all fields
10. 20231031232435-envelope-completed.json: Contract has been made

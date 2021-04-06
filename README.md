
# demo video for week 9:  
*IAM roles and policy tightening.  How to understand, do, and keep your hair.*     

Transcript & slides are below.  Please click this demo video to hear it with sound.   

![demo](https://user-images.githubusercontent.com/38410965/111993516-18082000-8aed-11eb-882c-b870193c33aa.mp4)

#

> *Hello everyone and thank you for watching this video on my final project which replicates project 4. This has been a great project to toy around with different AWS languages and tools.*  

### IAM roles and policy tightening  
### How to understand, do, and keep your hair  
Steve Depp  
MSDS 498 section 61  

**Demo Video 9**  

**Project 4**  

**DynamoDB —> EventBridge —>  Lambda —> SQS —> Lambda —> AWS comprehend —> S3**  
fang —> 5minutetimer —> serverlessproducer —> producer —> producerai —> comprehend —> fangsentiment-depp  

<img width="423" alt="Al Data Engineering" src="https://user-images.githubusercontent.com/38410965/112216488-efb91800-8bf7-11eb-8dd0-b8b17eccfc1c.png">

#

> *Now, my infra is working from build to ...* 

### Working infra  

- [x] make S3 bucket  
- [x] build lambda layers  

<img width="682" alt="Collecting boto3" src="https://user-images.githubusercontent.com/38410965/112215687-07dc6780-8bf7-11eb-90b5-f91a5833e99c.png">

#

> *... tear down with monitoring and logging and linting, but I needed to ensure that data is secure in transit and that IAM roles are as tight as possible.  This demo video is about the latter.   I would like to show you how I learned about IAM roles and policies and how to tighten those up so that the bits of my infra are given only permissions needed to do their jobs.  In my architecture ...*

### Working infra

- [x] deploy infrastructure  
- [x] add items to DynamoDB table  
- [x] tear down  

<img width="682" alt="Successfully packaged artifacts" src="https://user-images.githubusercontent.com/38410965/112215773-23e00900-8bf7-11eb-8df7-1cac2513e03a.png">

#

> *... I have 2 lambdas that perform all the actions. So, the only permissions I need to give out are to the Lambdas.  Here you see the Lambda 'serverlessroducer' gets names from a DynamoDB table and puts those names in an SQS queue and Lambda function 'producerai' gets the names from SQS queue and deletes them from SQS queue, and then one by one the Lambda asks AWS Comprehend to perform some ML on the name, and finally sends that result to an S3 bucket.  In this  demo we will focus only on the 'serverlessproducer' Lambda but the method for editing IAM policies and experimenting with tests is the same for the any Lamnda.*   

### Tighten up IAM

**ServerlessProducer**  
  - gets names from a DynamoDB table  
  - puts those names in an SQS Queue  

	**DynamoDB —> EventBridge —>  Lambda —> SQS —>**  
	fang —> 5minutetimer —> serverlessproducer —> producer —>  

**ProducerAI**   
- gets names from SQS Queue  
- deletes them from the SQS Queue  
- performs some machine learning on them  
- sends that result to S3  

	**SQS —> Lambda —> AWS comprehend —> S3**     
	producer —> producerai —> comprehend —> fangsentiment-depp

<img width="423" alt="Al Data Engineering" src="https://user-images.githubusercontent.com/38410965/112215930-512cb700-8bf7-11eb-9319-e7868954ceaa.png">

#

> *I found the best way to see what Lambdas need  is to look at Lambda code.  Here, we see this Lambda 'serverlessproducer' needs to scan a DynamoDB table and get the URL for an SQS queue and then send that queue a message.   All that runs fine when the Lambda is given a role that has administrative permissions that are detailed in a policy, but the idea is that your infrastructure is always vulnerable to benign abuse by nice people and malicious abuse by people that seek to take advantage of your infrastructure’s open doors.   The best way to find out exactly the permissions that your Lambdas need is via the IAM console*   

### ServerlessProducer - IAM - start with code to see permissions needed  

**ServerlessProducer**   
- gets names from a DynamoDB table: scan  
- puts those names in an SQS Queue: get_queue / send_message  

	**DynamoDB —> EventBridge —>  Lambda —> SQS —>**   
	fang —> 5minutetimer —> serverlessproducer —> producer —>

<img width="734" alt="lambda_function py" src="https://user-images.githubusercontent.com/38410965/112215979-61dd2d00-8bf7-11eb-9f78-1e0bfb090f08.png">

#

> *As mentioned, the steps include first getting your infra running with admin policies, which give your Lambdas free run of the ship.  Make sure it works.  Then use the IAM console to strip the unneeded permissions away.   So, here’s the Lambda with a role called 'LambdaExecutionRole2'. That means that when the Lambda function 'serverlessproducer' takes any action [pause] it takes on the role of LambdaExecutionRole2.  Let's see what that role can do, and exactly what permissions it needs to do the things that 'serverlessproducer' needs to do.*    

### ServerlessProducer - LambdaExecutionRole2 role name  

- [x] click on role name “LambdaExecutionRole2”  

<img width="984" alt="ServerlessProducer" src="https://user-images.githubusercontent.com/38410965/112216074-7a4d4780-8bf7-11eb-9afd-d6e77e7d1f42.png">

#

> *Here, we see that 'LambdaExecutionRole2' has been given a policy or set of permissions called 'AdministrativeAccess' which allows that role to do anything it wants on any resource it wants.  So, if 'serverlessproducer' has role 'LamndaExecutionRole2', it has permissions under 'AdministrativeAccess' policy and can do what ever it wants.  That's a bit too loose so lets delete that by clicking on the x.*

### ServerlessProducer - LambdaExecutionRole2 role - AdministrativeAccess policy  

ServerlessProducer in the role of “LambdaExecutionRole2”   
has permissions under “AdministrativeAccess” policy  
- [x] do anything on anything: Allow Action * on Resource *  
- [x] delete via “x” on LHS  

<img width="984" alt="Pasted Graphic 9" src="https://user-images.githubusercontent.com/38410965/112216194-98b34300-8bf7-11eb-8eee-d702adfd42d8.png">

#

> *We detach.*

### ServerlessProducer - LambdaExecutionRole2 role - new policy  

- [x] Detach  

<img width="984" alt="Summary" src="https://user-images.githubusercontent.com/38410965/112216799-4cb4ce00-8bf8-11eb-975b-63f674554a62.png">

#

> *We click on 'Add inline policy', which essentially means: make a custom policy that you can edit later as you test it out.*  

### ServerlessProducer - LambdaExecutionRole2 role - new policy  

- [x] click on “Add inline policy”  

<img width="984" alt="Summary" src="https://user-images.githubusercontent.com/38410965/112216850-5c341700-8bf8-11eb-9894-2582294c40b8.png">

#

> *We choose a service.*

### ServerlessProducer - LambdaExecutionRole2 role - new policy  

- [x] click on “Choose a service”  

<img width="984" alt="Create policy" src="https://user-images.githubusercontent.com/38410965/112216906-6d7d2380-8bf8-11eb-9f0d-35d142611e39.png">

#

> *Start typing DynamoDB and then click on 'DynamoDB', ...*  

### ServerlessProducer - LambdaExecutionRole2 role - new policy. 

- [x] start typing “dyn” and click DynamoDB  

<img width="984" alt="Create policy" src="https://user-images.githubusercontent.com/38410965/112216959-7ff75d00-8bf8-11eb-9bb6-98e2ad66346e.png">

#

> *... click on 'Read', and ...*  

### ServerlessProducer - LambdaExecutionRole2 role - new policy  

- [x] click on the arrow “Read” and  

<img width="984" alt="Create policy" src="https://user-images.githubusercontent.com/38410965/112217084-a1584900-8bf8-11eb-9029-23af7fd35e80.png">

#

> *... click on 'Scan' which is what we need 'serverlessproducer' in its 'LamndaExecutionRole2' role to do.*  

### ServerlessProducer - LambdaExecutionRole2 role - new policy  

- [x] click on “scan”   
- [x] notice the warnings in orange and click on arrow “Resources” to investigate  

<img width="984" alt="Pasted Graphic 17" src="https://user-images.githubusercontent.com/38410965/112217164-b339ec00-8bf8-11eb-859d-1ffdc7022856.png">

#

> *Click the checkbox next to 'ANY in this account' for both 'index' and 'table' components of your DynamoDB*  

### ServerlessProducer - LambdaExecutionRole2 role - new policy

- [x] click on “Any in this account” for “index” and “table”  

<img width="984" alt="Create policy" src="https://user-images.githubusercontent.com/38410965/112220793-06ae3900-8bfd-11eb-9783-d90bc95e0e30.png">

#

> *By doing that, you're asking AWS to find your existing assets that these policies would apply to.   It finds your DynamoDB table and its index.  Done with DynamoDB, and we think 'serverlessproducer' Lambda has the access it needs.*  

### ServerlessProducer - LambdaExecutionRole2 role - new policy

AWS is telling you that you should assign specific resources / assets to these permissions.  
AWS will not add this policy if you do not add a specific resource or all resources.   

- [x] click on “Any in this account”    

AWS finds the DynamoDB resources in your accounts and applies “scan” to them.   
If AWS cannot find a resource and you don’t know the resource, you can click “All resources” and get a benign warning.    

<img width="984" alt="Create policy" src="https://user-images.githubusercontent.com/38410965/112220999-49701100-8bfd-11eb-9dcf-90c90bb9e7c7.png">

#

> *Now, lets do another service [pause] at the bottom here.*   

### ServerlessProducer - LambdaExecutionRole2 role - new policy

- [x] click on “Service”

<img width="984" alt="Create policy" src="https://user-images.githubusercontent.com/38410965/112221087-673d7600-8bfd-11eb-8c4d-2a70cd7a8f35.png">

#

> *Type 'SQS' and select SQS*  

### ServerlessProducer - LambdaExecutionRole2 role - new policy

- [x] start typing “sqs” and click SQS

<img width="984" alt="Create policy" src="https://user-images.githubusercontent.com/38410965/112221140-79b7af80-8bfd-11eb-88d2-002fe113b844.png">

#

> *Same as before: we will click on the actions that 'serverlessproducer' needs to perform on SQS.  [pause] Click on 'Read' and 'Write'*   

### ServerlessProducer - LambdaExecutionRole2 role - new policy

- [x] click on the arrow “Read”  

With your architecture you might experiment with “Read” or “Tagging” depending on your code’s needs.  
For example, ProducerAI  

<img width="984" alt="Pasted Graphic 25" src="https://user-images.githubusercontent.com/38410965/112221191-8936f880-8bfd-11eb-9c41-7a42b92b45a6.png">

#

> *'Read' allows us to get the URL of the SQS queue [pause] and 'Write' allows us to send a message*  

### ServerlessProducer - LambdaExecutionRole2 role - new policy

- [x] click on the arrow “Read” and click “GetQueueURL”  
- [x] click on the arrow “Write” and click “SendMessage”   

With your architecture you might experiment with “Tagging” depending on your code’s needs.  
The lambda “ProduceAI” needs permissions to “GetQueueAttributes” and ”DeleteMessage”.  

- [x] click on the arrow “Write” and click “SendMessage”.  

<img width="984" alt="Pasted Graphic 27" src="https://user-images.githubusercontent.com/38410965/112221257-9a800500-8bfd-11eb-968c-d6ccfee93576.png">

#

> *As with DynamoDB, click the check box for 'Any in this account' to let AWS identify Resources. Then, click on 'Review policy'.*   

### ServerlessProducer - LambdaExecutionRole2 role - new policy

- [x] click on “Any in this account”
- [x] click on “Review policy”

<img width="984" alt="Pasted Graphic 28" src="https://user-images.githubusercontent.com/38410965/112221332-ae2b6b80-8bfd-11eb-9a85-d88157eda20e.png">

#

> *Name it and 'Create'.*  

### ServerlessProducer - LambdaExecutionRole2 role - LambdaTighter policy

- [x] give the policy a name “LambdaTighter”  
- [x] click “Create policy”  

<img width="984" alt="Create policy" src="https://user-images.githubusercontent.com/38410965/112221364-ba172d80-8bfd-11eb-8737-e0266b0246b7.png">

#

> *If you want to edit or see the policy, click on the arrow next to its name, ...*  

### ServerlessProducer - LambdaExecutionRole2 role - LambdaTighter policy

- [x] click on arrow “LambdaTighter” to see the policy in json format  

<img width="984" alt="Summary" src="https://user-images.githubusercontent.com/38410965/112221442-d2874800-8bfd-11eb-804e-0746aa787077.png">

#

> *... click 'Edit policy'.*  

### ServerlessProducer - LambdaExecutionRole2 role - LambdaTighter policy

- [x] click on “Edit policy” to see and edit the policy in json format  

<img width="984" alt="Summary" src="https://user-images.githubusercontent.com/38410965/112221492-e2069100-8bfd-11eb-8c69-b799e601220c.png">

#

> *This page would let us edit via the same menu functions used earlier.  Here, I choose the JSON tab because its quicker to see what permissions you’ve given the role.*   

### ServerlessProducer - LambdaExecutionRole2 role - LambdaTighter policy

Here you can edit with the menus used so far or directly in JSON format.     
- [x] click on ”JSON”

<img width="984" alt="Edit LamndaTighter" src="https://user-images.githubusercontent.com/38410965/112221545-f3e83400-8bfd-11eb-8ca1-7125d0b6e64f.png">

#

> *These 2 lines are superfluous.*   

### ServerlessProducer - LambdaExecutionRole2 role - LambdaTighter policy

These two lines just mean that the policy was produced using the menu driven method we employed.  

<img width="984" alt="Edit LamndaTighter" src="https://user-images.githubusercontent.com/38410965/112221630-0c584e80-8bfe-11eb-9c6c-6ac9c7f5906e.png">

#

> *Here, we see that 'serverlessproducer' acting in role of 'LamndaExecutionRole2' is allowed ...*   

### ServerlessProducer - LambdaExecutionRole2 role - LambdaTighter policy

This policy will “Allow” …

<img width="984" alt="Edit LamndaTighter" src="https://user-images.githubusercontent.com/38410965/112221673-1c702e00-8bfe-11eb-8f9f-9c48ab9cb946.png">

#

> *... to do 4 actions ...*   

### ServerlessProducer - LambdaExecutionRole2 role - LambdaTighter policy

… to do these four “Actions” …

<img width="984" alt="Edit LamndaTighter" src="https://user-images.githubusercontent.com/38410965/112221738-31e55800-8bfe-11eb-9eff-42ac948f8f5a.png">

#

> *... on 3 resources.*   

### ServerlessProducer - LambdaExecutionRole2 role - LambdaTighter policy

… these “Resources” …   
- [ ] add / edit / delete any lines you like here and ”Review” and “Save” your updates.   
- [ ] or “Cancel” to return   

<img width="984" alt="Edit LamndaTighter" src="https://user-images.githubusercontent.com/38410965/112221806-43c6fb00-8bfe-11eb-9be3-d21cd1fee7a1.png">

#

> *Let's see if that is enough or too much by returning to the Lambda function, ...*

### ServerlessProducer - LambdaExecutionRole2 role - LambdaTighter policy

LmabdaExecutionRole2 now has a tighter IAM policy limiting it to 4 actions on 3 identified assets.    
- [x] click on “ServerlessProducer - Lambda” tab and test it out.

<img width="984" alt="Summary" src="https://user-images.githubusercontent.com/38410965/112221989-8557a600-8bfe-11eb-8563-99da069393ee.png">

#

> *... and testing it out.  Here, mine succeeds, but I had to hunt and peck to get the policies just tight enough to restrict 'serverlessproducer' to just the actions it needs.*   

### ServerlessProducer - IAM policy - test it out!

Yay!

<img width="984" alt="ServerlessProducer" src="https://user-images.githubusercontent.com/38410965/112222039-943e5880-8bfe-11eb-9121-ea44936b4253.png">

#

> *One note is that for your Lambdas need to contribute to moinotirng and logging, you need to give them  permission to write to CloudWatch and ...*  

### ServerlessProducer - IAM policy - monitoring & logging

- [x] “Allow” “Action” “cloudwatch” for * “Resources”

<img width="984" alt="Pasted Graphic 40" src="https://user-images.githubusercontent.com/38410965/112222089-a4563800-8bfe-11eb-9806-faeb3dde1c34.png">

#

> *... permission to write to logs.*

### ServerlessProducer - IAM policy - monitoring & logging

- [x] “Allow” “Action” “logs” for * “Resources”

<img width="984" alt="Pasted Graphic 41" src="https://user-images.githubusercontent.com/38410965/112222144-b59f4480-8bfe-11eb-9b6c-df83724b560d.png">

#

> *To review, when youre working with a cloud service provider, the architecture you design requires tool A to talk to tool B and tool B to change something about tool C.  Put another way, the infra ALLOWS tool A to talk with tool B and ALLOWS tool B to change something about tool C.  [pause].   You want to give A, B, and C permissions to do those things but nothing more.  That way, if for some reason you are worried about behaviors of people, you know which doors you have left unlocked. To do this, start with the code; then, go to the IAM console and then test out in the Lamnda Console.  The only hair pull was related to AWS Comprehend. Anyone who has an answer please ...*

### Review - It is kinda fun

- [x] look at lambda_handler code for actions that AWS assets need to take
- [x] use AWS IAM console to experiment with different policy actions and resources
- [x] test your lambda function 

#

### One hair pull

I could not figure out how to set up IAM policy for “AWS comprehend”.   
Every time I used this method to tighten permissions even slightly resulted in a test failure.    
Tightening to “detect_sentiment” was a no go; so I set “Action” to *    
It is possible there is a very long lag for permissions set up in the ML arena.   
 
<img width="912" alt="Pasted Graphic 42" src="https://user-images.githubusercontent.com/38410965/112222220-d23b7c80-8bfe-11eb-9b2b-7b7d48175b98.png">

#

> *... let me know.  Otherwise, I've given AWS Comprehend carte blanche with this policy line.  Thank you.*

### Hair pull

AWS comprehend gets carte blanche.

<img width="774" alt="Effect Allow" src="https://user-images.githubusercontent.com/38410965/112222251-e0899880-8bfe-11eb-9a30-2d34fb43981a.png">






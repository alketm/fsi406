# Creating the lambda functions that will process data from the stream

1 - Go to the Lambda service

2 - Click on 'Create function'
  - Select 'Author from scratch'
  - give it the name fsi406-mavg-1
  - select as runtime 'python3.8'
  - Leave the permissions as default - a new role name fsi406-mavg-1-role-${random} will be created

3 - Click on 'Create function'

4 - On the next window, replace the template code with the code from fsi406-mavg-1.py

5 - Change function timeout (in the 'Basic Settings' section) to 30 seconds

6 - Click 'Save'

7 - Repeat for function fsi406-mavg-5 - but make sure to re-use the role we created earlier

8 - Go to IAM and update the IAM role by adding the CloudWatchFullAccess policy

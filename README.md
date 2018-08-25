# LaTeX Jenkins Manage
This repository contains a python script and instructions below that will help users to check that pull requests of LaTeX documents will successfully build. This is useful for organisations that maintain large documentation repositories written in LaTeX.

The steps are as follows:
1) Set up Jenkins and install all standard plugins.
2) Add Environment Injector Plugin and GitHub Pull Request Builder Plugin.
3) Set up a bot GitHub account with its own email.
4) Give the bot ssh access to the repository with the LaTeX that your organisation is working on.
5) Add the bot to the email configuration on Jenkins - smtp server etc. This will allow Jenkins to send emails.
6) Set up a GitHub project on Jenkins and link to repository using the bot for ssh access.
7) Tick GitHub Pull Request Builder box and the webhooks box within that in the Jenkins project.
8) Set up GitHub to send webhooks to Jenkins.
9) Jenkins should now be able to detect pull requests issued in the GitHub repository. You may have to whitelist the organisation/GitHub that have access to the repository also.

Now we have the steps relating directly to running the build.
1) Add an execute shell with the following command in it 'echo LAST = $(git log -1 --pretty=format:'%ae') > propsfile.txt'. This will pick up the email of the pull request issuer.
2) Add 'Inject environment variables' and set the 'Properties File Path' to propsfile.txt. This makes the issuer email an environment variable.
3) And another shell to run the python script.
4) Now in Post-build actions add an email notification and set the recepiants to ${LAST}.
5) Add a set GitHub commit status (universal) with settings as desired.

Note that for the email of the pull request issuer to be picked up the privacy email option on GitHub has to be unchecked. This is found in email settings.

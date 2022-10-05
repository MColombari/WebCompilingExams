<h1>Web Compiling Exams</h1>

This is a web application, made to manage and correct online exams for the course of OOP (Object-Oriented Programming).
Is made in flash and runs in a docker.
The docker image can be seen [here](https://hub.docker.com/repository/docker/mcolombari/final_webapp/).

These are few of the application functionalitì:
 - Compile and Run Java/Python program.
 - Answer multiple option and open questions.
 - Manage and student during the exam.
 - “Auto” corrects student answers at the end of the exam, and lets the administrator grade it.

The following are instruction to run this app.
Download application:
 - Download docker image with this [link](https://hub.docker.com/repository/docker/mcolombari/final_webapp/) or this command:
   - "docker pull mcolombari/final_webapp:latest".
 - If supported you can just run "run.sh" script.
 - Otherwise you can run this command (change application path):
         docker run -it -p 5000:5000 -v *APPLICATION_PATH*/config.yaml:/app/config.yaml \
                             -v *APPLICATION_PATH*/log.txt:/app/log.txt \
                             -v *APPLICATION_PATH*/exam:/app/exam \
                             -v *APPLICATION_PATH*/questions:/app/questions \

Application Management:
- "config.yaml" is a configuration file that let the admin to:
    - Set a countdown for the test, it's a positive integer number that indicate the maximum ammount of minutes to complete the test.
      - to disable the countdown set the value to "0".
    - Points taken in case of wrong answer in multiple option question, this can be a floating value.
      - every correct option is considered ad "1" points.
    - Difficulty, type and number of questions.
- The "questions" directory contains all the question that can be submitted, they are divided for type and category.
    - Open and multiple option questions: for each category theres only one file containing all the questions,
      inside that file they are organized in paragraph by difficulty.
      for each paragraph a weight can be defined, must be a integer arbitrary number.
      - How the file is parsed:
        - Empy line are ignored.
        - Line with "--" define the difficulty of the following questions.
        - Line with " define the question.
        - Line with "+" or "-" define a possible option (for multiple option questions):
          - "+": the option is right.
          - "-": the option is wrong.
    - Programming questions (java / python): for each category there are multiple file, one for every question,
      the information about the question MUST be in the first and following row of the file, the question text can be
      written in multiple row.
        - Python: For testing we are using "unittest" library, very similar to "JUnit".
          User's solution will be wrote in "RunningFile" so to import class/function you must import from that file.
        - Java: For testing no library is used, so the tests output must be formatted in the following way:
            - First row contains only "." e "F" character, "." for every successful test and "F" for every failed test.
            - The content of the following row will be shown in "terminal output".
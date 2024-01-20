import textwrap

student_accept_html = """\
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Enchird</title>
</head>

<body>
    <main style="max-width: 600px; padding: 40px; color: #1F201F; font-family: Inter; line-height: 24px;">
        <p>Dear <strong>{first_name} {last_name}</strong></p>

        <div>
            <p style="margin-block: 30px;">
                I hope this email finds you well. On behalf of the <strong>{faculty}</strong> at
                , I am delighted to inform you that your application to pursue a degree in <strong>{department}</strong> has been
                accepted.
                Congratulations! We are excited to welcome you to our academic community.
            </p>

            <p style="margin-block: 30px;">
                We understand that choosing the right institution and program is very important.
                Your acceptance is a testament to your hard work, dedication, and academic achievements. We
                believe that you will contribute positively to our vibrant learning environment and make the most of the
                opportunities available in the <strong>{department}</strong> program.

            </p>

            <p style="margin-block: 30px;">
                To facilitate a smooth transition into your academic journey, please find attached important information
                regarding the next steps, including:

            </p>
        </div>

        <ol>
            <li>
                <p>
                    <strong>Orientation Details:</strong> Dates, times, and locations for the orientation sessions to
                    help you get acquainted with the faculty, staff, and fellow students..
                </p>
            </li>

            <li>
                <p>
                    <strong>Registration Process:</strong>
                    Instructions on how to complete the registration process, including course selection and any
                    required documentation.



                </p>
            </li>

            <li>
                <p><strong>Important Dates:</strong> Key dates for the upcoming semester, such as the start of classes,
                    examination periods, and other significant events.

                </p>
            </li>
        </ol>

        <div>
            <p style="margin-block: 30px;">If you have any questions or need further assistance, feel free to reach out
                to our <strong>[Admissions Office/Student Services]</strong> at <strong>[contact email/phone
                    number]</strong>. We are here to support you
                and ensure a seamless transition into your academic journey.

            </p>

            <p style="margin-block: 30px;">
                Once again, congratulations on your acceptance to the {department} program at <strong>[University
                    Name]</strong>. We look forward to meeting you and wish you every success in your academic pursuits.


            </p>
        </div>

        <div>
            <p style="margin-block: 30px;">Best regards,</p>

            <div>
                <p style="margin: 0; margin-block-end: 4px;"><strong>[Your Full Name]</strong></p>
                <p style="margin: 0; margin-block-end: 4px;"><strong>[Your Title]</strong> </p>
                <p style="margin: 0; margin-block-end: 4px;"><strong>{faculty}</strong> </p>
                <p style="margin: 0; margin-block-end: 4px;"><strong>[University Name]</strong> </p>
                <p style="margin: 0; margin-block-end: 4px;"><strong>[Contact Information]</strong> </p>
            </div>
        </div>


        <div style=" margin-block: 35px;">
            <div style="margin-block: 24px;">
                <h4 style="font-size: 20px; color: black; font-weight: bold; margin: 0; margin-block-end: 10px;">
                    Please use the temporary password below to log into your student dashboard.</h4>
                <button
                    style="width: 100%; padding-block: 24px; background-color: #2218A7; border: 0; border-radius: 4px; color:white; cursor: pointer;">
                    TEMP PASSWORD: {password}</button>
            </div>
        </div>

        <div style="text-align: center; font-size: 20px;">
            <p style="margin: 0; margin-block-end: 10px;"><a href=""
                    style="color:black; font-weight: bold; ">Enchird</a></p>
            <p style="margin: 0; margin-block-end: 10px;">Brings you closer to learning</p>
            <p style="margin: 0; margin-block-end: 10px;">Copyright &copy; 2024</p>
        </div>
    </main>
</body>

</html>

"""



student_reject_html = """\
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Enchird</title>
</head>

<body>
    <main style="max-width: 600px; padding: 40px; color: #1F201F; font-family: Inter; line-height: 24px;">
        <p>Dear <strong>{first_name} {last_name}</strong></p>

        <div>
            <p style="margin-block: 25px;">
                I hope this email finds you well. I am writing to inform you of the admissions decision for your
                application to the <strong>{department}</strong> program at [University Name]. After careful
                consideration, we
                regret to inform you that your application has not been successful.

            </p>

            <p style="margin-block: 25px;">
                We understand that this news may be disappointing, and we want to express our appreciation for the time
                and effort you invested in your application to <strong>[University Name]</strong>. The admissions
                process is highly
                competitive, and unfortunately, we are unable to offer a place in the <strong>{department}
                    </strong> program at this time.
            </p>

            <p style="margin-block: 25px;">We encourage you to explore alternative educational opportunities and
                consider other institutions that
                align with your academic and personal goals. If you have any specific feedback on your application or
                would like guidance on potential areas for improvement, please do not hesitate to reach out to our
                <strong>[Admissions Office]</strong> at <strong>[contact email/phone number]</strong>.
            </p>

        </div>

        <div>
            <p style="margin-block: 25px;">
                Remember that this decision does not define your capabilities or potential for success. Many successful
                individuals have faced initial setbacks and found new paths that ultimately led to fulfilling and
                rewarding experiences.
            </p>
            <p style="margin-block: 25px;">
                We appreciate your interest in <strong>[University Name]</strong>, and we wish you the very best in your
                academic and
                personal endeavors. If you have any questions or need further assistance, please feel free to contact
                our <strong>[Admissions Office/Student Services]</strong>.
            </p>
            <p style="margin-block: 25px;">
                Thank you for considering <strong>[University Name]</strong>, and we extend our best wishes for your
                future endeavors.

            </p>
        </div>

        <div>
            <p style="margin-block: 20px;">Kind regards,</p>

            <div>
                <p style="margin: 0; margin-block-end: 4px;"><strong>[Your Full Name]</strong></p>
                <p style="margin: 0; margin-block-end: 4px;"><strong>[Your Title]</strong> </p>
                <p style="margin: 0; margin-block-end: 4px;"><strong>{faculty}</strong> </p>
                <p style="margin: 0; margin-block-end: 4px;"><strong>[University Name]</strong> </p>
                <p style="margin: 0; margin-block-end: 4px;"><strong>[Contact Information]</strong> </p>
            </div>
        </div>


        <div style="text-align: center; font-size: 16px; margin-top: 35px;">
            <p style="margin: 0; margin-block-end: 10px;"><a href=""
                    style="color:black; font-weight: bold; ">Enchird</a></p>
            <p style="margin: 0; margin-block-end: 10px;">Brings you closer to learning</p>
            <p style="margin: 0; margin-block-end: 10px;">Copyright &copy; 2024</p>
        </div>
    </main>
</body>

</html>
  
  
"""




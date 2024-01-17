student_accept_html = """\
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <link rel="stylesheet" href="css/globals.css" />
    <link rel="stylesheet" href="css/styleguide.css" />
    <link rel="stylesheet" href="css/style.css" />
  </head>
  <body>
    <div class="email-template">
      <div class="frame-wrapper">
        <div class="frame">
          <div class="enchird-logo-wrapper">
            <div class="enchird-logo">
              <img class="icon-book-saved" src="img/type=desktop.png" />
            </div>
          </div>
          <div class="div">
            <div class="frame-2">
              <p class="subject-notification">
                <span class="span">Subject: </span>
                <span class="text-wrapper-2"
                  >Notification of Admissions Decision for [Field of Studies] Program <br
                /></span>
                <span class="span"><br />Dear </span>
                <span class="text-wrapper-3">{{ user.first_name }}</span>
                <span class="span"
                  >, <br />
                  <br />I hope this email finds you well. On behalf of the
                </span>
                <span class="text-wrapper-3">[Faculty/Department Name]</span>
                <span class="span"> at </span>
                <span class="text-wrapper-3">[University Name]</span>
                <span class="span">, I am delighted to inform you that your application to pursue </span>
                <span class="text-wrapper-3">[Field of Studies]</span>
                <span class="span">
                  has been successful. Congratulations! We are excited to welcome you to our academic community. <br />
                  <br />Your acceptance is a testament to your hard work, dedication, and academic achievements. We
                  believe that you will contribute positively to our vibrant learning environment and make the most of
                  the opportunities available in the
                </span>
                <span class="text-wrapper-3">[Field of Studies]</span>
                <span class="span">
                  program. <br />
                  <br />To facilitate a smooth transition into your academic journey, please find attached important
                  information regarding the next steps, including: <br />
                  <br
                /></span>
                <span class="text-wrapper-3">Orientation Details</span>
                <span class="span"
                  >: Dates, times, and locations for the orientation sessions to help you get acquainted with the
                  faculty, staff, and fellow students. <br />
                  <br
                /></span>
                <span class="text-wrapper-3">Registration Process</span>
                <span class="span"
                  >: Instructions on how to complete the registration process, including course selection and any
                  required documentation. <br />
                  <br
                /></span>
                <span class="text-wrapper-3">Important Dates</span>
                <span class="span"
                  >: Key dates for the upcoming semester, such as the start of classes, examination periods, and other
                  significant events. <br />
                  <br />If you have any questions or need further assistance, feel free to reach out to our</span
                >
                <span class="text-wrapper-3">
                  [Admissions Office/Student Services] at [contact email/phone number].</span
                >
                <span class="span">
                  We are here to support you and ensure a seamless transition into your academic journey. <br />
                  <br />Once again, congratulations on your acceptance to the
                </span>
                <span class="text-wrapper-3">[Field of Studies]</span>
                <span class="span"> program at </span>
                <span class="text-wrapper-3">[University Name]</span>
                <span class="span"
                  >. We look forward to meeting you and wish you every success in your academic pursuits. <br />
                  <br />Best regards, <br />
                  <br
                /></span>
                <span class="text-wrapper-3"
                  >[Your Full Name] <br />[Your Title] <br />[Faculty/Department Name] <br />[University Name]
                  <br />[Contact Information]</span
                >
              </p>
              <div class="frame-3">
                <p class="p">Please follow this link to setup your account profile</p>
                <div class="button-desktop"><div class="button-component">Setup My Profile</div></div>
              </div>
            </div>
            <div class="auto-layout-vertical">
              <div class="text-wrapper-4">Enchird</div>
              <p class="text-wrapper-5">Brings you closer to learning.</p>
              <div class="text-wrapper-5">Copyright © 2024</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </body>
</html>


"""


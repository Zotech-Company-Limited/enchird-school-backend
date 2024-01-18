import textwrap

student_accept_html = textwrap.dedent("""\
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8"/>
    <style>
      @import url("https://cdnjs.cloudflare.com/ajax/libs/meyer-reset/2.0/reset.min.css");
      @import url("https://fonts.googleapis.com/css?family=Kurale:400|Inter:400,700|Barlow:700");

      * {
        box-sizing: border-box;
      }

      html,
      body {
        margin: 0px;
        height: 100%;
      }

      /* a blue color as a generic focus style */
      button:focus-visible {
        outline: 2px solid #4a90e2 !important;
        outline: -webkit-focus-ring-color auto 5px !important;
      }

      a {
        text-decoration: none;
      }

      .email-template {
        background-color: #ffffff;
        display: flex;
        flex-direction: row;
        justify-content: center;
        width: 100%;
      }

      .email-template .frame-wrapper {
        background-color: var(--enchird-whiteenchird-white-1);
        width: 788px;
        height: 2393px;
      }

      .email-template .frame {
        display: flex;
        flex-direction: column;
        width: 659px;
        align-items: flex-start;
        gap: 48px;
        position: relative;
        top: 63px;
        left: 65px;
      }

      .email-template .enchird-logo-wrapper {
        position: relative;
        width: 232px;
        height: 55px;
      }

      .email-template .enchird-logo {
        display: flex;
        width: 609px;
        height: 55px;
        align-items: center;
        gap: 14px;
        position: relative;
      }

      .email-template .icon-book-saved {
        position: relative;
        width: 240px;
        height: 60px;
        margin-left: -2px;
      }

      .email-template .text-wrapper {
        position: relative;
        width: fit-content;
        margin-top: -10.5px;
        margin-bottom: -8.5px;
        font-family: "Kurale-Regular", Helvetica;
        font-weight: 400;
        color: var(--enchird-primaryenchird-primary-1);
        font-size: 50px;
        letter-spacing: 0;
        line-height: normal;
      }

      .email-template .div {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        gap: 70px;
        position: relative;
        align-self: stretch;
        width: 100%;
        flex: 0 0 auto;
      }

      .email-template .frame-2 {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        gap: 36px;
        position: relative;
        align-self: stretch;
        width: 100%;
        flex: 0 0 auto;
      }

      .email-template .subject-notification {
        position: relative;
        align-self: stretch;
        margin-top: -1px;
        font-family: "Inter-Regular", Helvetica;
        font-weight: 400;
        color: var(--enchird-blackenchird-black-2);
        font-size: 24px;
        letter-spacing: 0;
        line-height: 36px;
      }

      .email-template .span {
        font-family: "Inter-Regular", Helvetica;
        font-weight: 400;
        color: #1e201e;
        font-size: 24px;
        letter-spacing: 0;
        line-height: 36px;
      }

      .email-template .text-wrapper-2 {
        font-family: "Inter-Bold", Helvetica;
        font-weight: 700;
      }

      .email-template .text-wrapper-3 {
        font-family: "Inter-SemiBold", Helvetica;
        font-weight: 600;
      }

      .email-template .frame-3 {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        gap: 16px;
        position: relative;
        align-self: stretch;
        width: 100%;
        flex: 0 0 auto;
      }

      .email-template .p {
        position: relative;
        width: fit-content;
        margin-top: -1px;
        font-family: "Inter-Bold", Helvetica;
        font-weight: 700;
        color: #000000;
        font-size: 24px;
        text-align: center;
        letter-spacing: 0;
        line-height: normal;
      }

      .email-template .button-desktop {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 16px;
        padding: 24px 32px;
        position: relative;
        align-self: stretch;
        width: 100%;
        flex: 0 0 auto;
        background-color: var(--enchird-primaryenchird-primary-1);
        border-radius: 4px;
        overflow: hidden;
      }

      .email-template .button-component {
        position: relative;
        width: fit-content;
        margin-top: -1px;
        font-family: var(--bodytext-regular-18-font-family);
        font-weight: var(--bodytext-regular-18-font-weight);
        color: var(--enchird-whiteenchird-white-1);
        font-size: var(--bodytext-regular-18-font-size);
        letter-spacing: var(--bodytext-regular-18-letter-spacing);
        line-height: var(--bodytext-regular-18-line-height);
        font-style: var(--bodytext-regular-18-font-style);
      }

      .email-template .auto-layout-vertical {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 10px;
        position: relative;
        align-self: stretch;
        width: 100%;
        flex: 0 0 auto;
      }

      .email-template .text-wrapper-4 {
        position: relative;
        width: 82px;
        margin-top: -1px;
        font-family: "Barlow-Bold", Helvetica;
        font-weight: 700;
        color: #000000;
        font-size: 24px;
        text-align: center;
        letter-spacing: 0;
        line-height: normal;
        text-decoration: underline;
      }

      .email-template .text-wrapper-5 {
        position: relative;
        width: fit-content;
        font-family: "Inter-Regular", Helvetica;
        font-weight: 400;
        color: #000000;
        font-size: 24px;
        text-align: center;
        letter-spacing: 0;
        line-height: normal;
      }
    </style>
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
                <span class="text-wrapper-2">Notification of Admissions Decision for [Field of Studies] Program <br /></span>
                <span class="span"><br />Dear </span>
                <span class="text-wrapper-3">{{ user.first_name }}</span>
                <span class="span">, <br /><br />I hope this email finds you well. On behalf of the</span>
                <span class="text-wrapper-3">[Faculty/Department Name]</span>
                <span class="span"> at </span>
                <span class="text-wrapper-3">[University Name]</span>
                <span class="span">, I am delighted to inform you that your application to pursue </span>
                <span class="text-wrapper-3">[Field of Studies]</span>
                <span class="span"> has been successful. Congratulations! We are excited to welcome you to our academic community. <br /><br />Your acceptance is a testament to your hard work, dedication, and academic achievements. We believe that you will contribute positively to our vibrant learning environment and make the most of the opportunities available in the</span>
                <span class="text-wrapper-3">[Field of Studies]</span>
                <span class="span"> program. <br /><br />To facilitate a smooth transition into your academic journey, please find attached important information regarding the next steps, including: <br /><br /></span>
                <span class="text-wrapper-3">Orientation Details</span>
                <span class="span">: Dates, times, and locations for the orientation sessions to help you get acquainted with the faculty, staff, and fellow students. <br /><br /></span>
                <span class="text-wrapper-3">Registration Process</span>
                <span class="span">: Instructions on how to complete the registration process, including course selection and any required documentation. <br /><br /></span>
                <span class="text-wrapper-3">Important Dates</span>
                <span class="span">: Key dates for the upcoming semester, such as the start of classes, examination periods, and other significant events. <br /><br />If you have any questions or need further assistance, feel free to reach out to our</span>
                <span class="text-wrapper-3">[Admissions Office/Student Services] at [contact email/phone number].</span>
                <span class="span"> We are here to support you and ensure a seamless transition into your academic journey. <br /><br />Once again, congratulations on your acceptance to the</span>
                <span class="text-wrapper-3">[Field of Studies]</span>
                <span class="span"> program at </span>
                <span class="text-wrapper-3">[University Name]</span>
                <span class="span">. We look forward to meeting you and wish you every success in your academic pursuits. <br /><br />Best regards, <br /><br /></span>
                <span class="text-wrapper-3">[Your Full Name] <br />[Your Title] <br />[Faculty/Department Name] <br />[University Name] <br />[Contact Information]</span>
              </p>
              <div class="frame-3">
                <p class="p">Please follow this link to set up your account profile</p>
                <div class="button-desktop"><div class="button-component">Set up My Profile</div></div>
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

""")


      ******************************************************************
      * Author: Clair Marchesani
      * Date: 22 May 2016
      * Purpose: Self-Study / Demonstration
      * Tectonics: cobc
      * URL: https://github.com/DillonDepeel/Cobol-Programming-Collection/blob/main/Cobol%20Utilities/Phonebook.cbl
      ******************************************************************
       IDENTIFICATION DIVISION.
       PROGRAM-ID. PHONEBOOK.
       AUTHOR CLAIR MARCHESANI
       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT BOOK ASSIGN TO "PHONEBOOK.DAT"
           ORGANIZATION IS SEQUENTIAL
           FILE STATUS IS FS.
       DATA DIVISION.
       FILE SECTION.
       FD BOOK.
       01 BOOKENTRY.
           88 ENDOFFILE    VALUE HIGH-VALUES.
           02 NAME.
               03 FIRSTNAME        PIC X(10).
               03 LASTNAME         PIC X(10).
           02 PHONENUMBER.
               03 PREFIX           PIC 9(5).
               03 RESTOFNUMBER     PIC 9(7).
       WORKING-STORAGE SECTION.
       01 FS                       PIC 99.
       01 YESNOANSWER              PIC X.
       01 WS-BOOKENTRY.
           02 WS-NAME.
               03 WS-FIRSTNAME        PIC X(10).
               03 WS-LASTNAME         PIC X(10).
           02 WS-PHONENUMBER.
               03 WS-PREFIX           PIC 9(5).
               03 WS-RESTOFNUMBER     PIC 9(12).
       PROCEDURE DIVISION.
       MAIN-PROCEDURE.
            DISPLAY "Enter Surname."
            ACCEPT WS-LASTNAME
            OPEN INPUT BOOK
            IF FS(1:1) IS NOT ZERO THEN
                CLOSE BOOK
                IF WS-LASTNAME EQUALS SPACES THEN STOP RUN END-IF
                DISPLAY "Adding a new entry"
                PERFORM ADD-ENTRY-PROCEDURE
            END-IF
            READ BOOK
               AT END SET ENDOFFILE TO TRUE
            END-READ
            PERFORM UNTIL ENDOFFILE
               IF LASTNAME EQUALS WS-LASTNAME THEN
                   DISPLAY SPACE
                   DISPLAY FIRSTNAME SPACE LASTNAME
                   DISPLAY "Number" SPACE PREFIX SPACE RESTOFNUMBER
               END-IF
               READ BOOK
                   AT END SET ENDOFFILE TO TRUE
               END-READ
            END-PERFORM
            CLOSE BOOK
            DISPLAY "Add new entry?"
            ACCEPT YESNOANSWER
            IF YESNOANSWER EQUALS 'Y' THEN PERFORM ADD-ENTRY-PROCEDURE.
            CLOSE BOOK
            STOP RUN.

       ADD-ENTRY-PROCEDURE.
            OPEN EXTEND BOOK
            MOVE WS-LASTNAME TO LASTNAME
            DISPLAY "Enter first name for person " WS-LASTNAME
            ACCEPT FIRSTNAME
            DISPLAY "Enter Phone Number Prefix"
            ACCEPT PREFIX
            DISPLAY "Enter rest of phone number"
            ACCEPT RESTOFNUMBER
            WRITE BOOKENTRY
            CLOSE BOOK
            STOP RUN.

       END PROGRAM PHONEBOOK.
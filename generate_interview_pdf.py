# -*- coding: utf-8 -*-
import sys
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and print total page numbers: Page X of Y
    """
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))

        # Header (pages after page 1)
        if self._pageNumber > 1:
            self.drawString(40, 810, "BitRaser File Eraser (C++ / Qt) - Technical Interview Preparation Guide")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(40, 804, 555, 804)

        # Footer (all pages)
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(40, 40, 555, 40)

        footer_left = "Confidential - For Candidate Interview Preparation"
        footer_right = f"Page {self._pageNumber} of {page_count}"
        self.drawString(40, 28, footer_left)
        self.drawRightString(555, 28, footer_right)
        self.restoreState()

def build_pdf(filename="BitRaser_File_Eraser_Interview_Guide.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=colors.HexColor("#0F2942"),
        alignment=0,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#475569"),
        spaceAfter=15
    )

    sec_header_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor("#FFFFFF"),
        spaceAfter=0
    )

    q_title_style = ParagraphStyle(
        'QuestionTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#0F2942")
    )

    badge_style = ParagraphStyle(
        'BadgeStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9,
        textColor=colors.HexColor("#0284C7")
    )

    body_style = ParagraphStyle(
        'AnswerBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.8,
        leading=12.2,
        textColor=colors.HexColor("#1E293B"),
        spaceAfter=4
    )

    bullet_style = ParagraphStyle(
        'AnswerBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.8,
        textColor=colors.HexColor("#1E293B"),
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=3
    )

    code_style = ParagraphStyle(
        'CodeSnippet',
        parent=styles['Normal'],
        fontName='Courier-Bold',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=4
    )

    story = []

    # Title & Header Banner
    story.append(Paragraph("BITRASER FILE ERASER - INTERVIEW PREPARATION GUIDE", title_style))
    story.append(Paragraph("<b>Comprehensive Technical Q&A, Architecture Deep-Dive & System Programming Guide for C++ / Qt Developers</b>", subtitle_style))

    # Meta Info Card
    meta_data = [
        [
            Paragraph("<b>Project:</b> BitRaser File Eraser (Stellar Data Recovery)", body_style),
            Paragraph("<b>Target Role:</b> C++ / Qt / Windows Systems Engineer", body_style)
        ],
        [
            Paragraph("<b>Key Technologies:</b> C++, Qt 5/6, Win32 Direct Disk I/O, MariaDB, REST API, Windows Scheduler", body_style),
            Paragraph("<b>Domain:</b> Data Sanitization, Forensic Security & Compliance", body_style)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[255, 260])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 14))

    def make_section_header(title_text):
        tbl = Table([[Paragraph(f"<b>{title_text}</b>", sec_header_style)]], colWidths=[515])
        tbl.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#0F2942")),
            ('PADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 7),
            ('TOPPADDING', (0,0), (-1,-1), 7),
        ]))
        return tbl

    def make_qa_box(q_num, category, question_text, answers_list):
        content = []
        # Header with category badge
        q_label = f"<b>Q{q_num}: {question_text}</b>"
        cat_badge = f"<font color='#0284C7'><b>[{category.upper()}]</b></font>"
        
        q_table = Table([[
            Paragraph(q_label, q_title_style),
            Paragraph(cat_badge, badge_style)
        ]], colWidths=[420, 85])
        q_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('ALIGN', (1,0), (1,0), 'RIGHT'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ]))
        content.append(q_table)
        content.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#E2E8F0"), spaceAfter=5, spaceBefore=2))

        for item in answers_list:
            if isinstance(item, tuple) and item[0] == 'bullet':
                content.append(Paragraph(f"• {item[1]}", bullet_style))
            elif isinstance(item, tuple) and item[0] == 'code':
                code_tbl = Table([[Paragraph(item[1], code_style)]], colWidths=[495])
                code_tbl.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
                    ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
                    ('PADDING', (0,0), (-1,-1), 4),
                    ('TOPPADDING', (0,0), (-1,-1), 3),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 3),
                ]))
                content.append(code_tbl)
                content.append(Spacer(1, 3))
            else:
                content.append(Paragraph(item, body_style))

        outer_table = Table([[content]], colWidths=[515])
        outer_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FFFFFF")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
            ('PADDING', (0,0), (-1,-1), 8),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ]))
        return KeepTogether([outer_table, Spacer(1, 10)])

    # ---------------- SECTION 1 ----------------
    story.append(make_section_header("SECTION 1: PROJECT OVERVIEW & CANDIDATE ELEVATOR PITCH"))
    story.append(Spacer(1, 8))

    story.append(make_qa_box(
        1, "Overview",
        "Can you introduce this project? What is BitRaser File Eraser, and what problem does it solve?",
        [
            "<b>Elevator Pitch:</b>",
            ("bullet", "<b>BitRaser File Eraser</b> is an enterprise-grade and consumer data sanitization software developed in <b>C++ and Qt</b> for Microsoft Windows. Its primary purpose is the <b>permanent, forensically unrecoverable erasure</b> of confidential files, folders, system/internet traces, volume slack, and free space."),
            ("bullet", "<b>The Problem it Solves:</b> When users delete files using standard OS operations (Shift+Delete or Recycle Bin), the actual binary data is <i>never erased</i>—only the pointers in file system allocation tables (e.g., NTFS Master File Table, FAT Directory Entries) are marked as free. Anyone using commercial or free data recovery software can retrieve sensitive data. BitRaser complies with <b>22+ international wiping standards</b> (such as <b>NIST 800-88, DoD 5220.22-M, Peter Gutmann</b>) to overwrite raw sectors, guaranteeing compliance with <b>GDPR, HIPAA, PCI-DSS, and ISO 27001</b>."),
            ("bullet", "<b>Key Architectural Modules:</b>"),
            ("bullet", "<b>1. Core Wiping Engine (WipingAlgo / DiskIO):</b> Low-level Win32 sector-by-sector overwriting with buffer alignment and verification passes."),
            ("bullet", "<b>2. Traces Erasure Engine:</b> Deep scrubbing of OS artifacts (Prefetch, Temp, Event logs, MRU) and browser databases (Chrome, Firefox, Edge)."),
            ("bullet", "<b>3. Automation & Scheduling:</b> Native integration with Windows Task Scheduler 2.0 COM API and Windows Explorer context menus."),
            ("bullet", "<b>4. Auditing & Reporting:</b> Digitally signed, tamper-evident PDF/XML Certificates of Erasure with hardware serial numbers and timestamps.")
        ]
    ))

    story.append(make_qa_box(
        2, "Role & Tech",
        "What was your specific role and key technical contributions in this codebase?",
        [
            ("bullet", "<b>Core Erasure Engine Development:</b> Implemented and fine-tuned multi-pass wiping algorithms (DoD 3/7 pass, NIST Clear, Gutmann) and low-level sector read/write routines using Win32 API (<code>CreateFileW</code>, <code>WriteFile</code>, <code>DeviceIoControl</code>)."),
            ("bullet", "<b>Asynchronous Processing & Threading:</b> Decoupled heavy, blocking disk I/O operations from the Qt main GUI thread using worker threads (<code>QThread</code>/<code>BTask</code>) and throttled signal-slot emissions to maintain responsive 60 FPS UI rendering."),
            ("bullet", "<b>Trace Sanitization:</b> Authored deep cleaning routines for internet traces (SQLite history, cookies, cache) and Windows OS artifacts (Prefetch, JumpLists, Recycle Bin raw clusters)."),
            ("bullet", "<b>Cloud & Licensing Integration:</b> Integrated <code>libcurl</code> for RESTful communication with the BitRaser Cloud Console, encrypting JSON payloads using AES-128-CBC and hardware machine fingerprinting."),
            ("bullet", "<b>Audit Report Generation:</b> Integrated Debenu PDF Library to dynamically generate certified, tamper-evident PDF Certificates of Erasure with technician digital signatures and custom logos.")
        ]
    ))

    # ---------------- SECTION 2 ----------------
    story.append(make_section_header("SECTION 2: DATA SANITIZATION STANDARDS & ALGORITHMS"))
    story.append(Spacer(1, 8))

    story.append(make_qa_box(
        3, "Algorithms",
        "Which data erasure standards are implemented in BitRaser, and how do they work?",
        [
            "The codebase implements <b>22 distinct erasure standards</b> (defined in <code>WipingWrapper.h</code> and <code>WipingAlgo.cpp</code>):",
            ("bullet", "<b>Zeroes (1 Pass):</b> Overwrites all sectors with <code>0x00</code>. Quickest sanitization."),
            ("bullet", "<b>Random (1 Pass):</b> Overwrites every sector with cryptographically generated pseudo-random bytes seeded by system time."),
            ("bullet", "<b>DoD 5220.22-M (3 Passes):</b> Pass 1: Fixed character (<code>0x00</code>) + Verify; Pass 2: Complement (<code>~0x00 = 0xFF</code>) + Verify; Pass 3: Pseudo-random bytes + Verify."),
            ("bullet", "<b>DoD 5220.22-M ECE (7 Passes):</b> Executes DoD-3 pass, followed by an additional random pass, then <code>0xFF</code>, its complement, and final random data."),
            ("bullet", "<b>NIST 800-88 Rev 1 (Clear & Purge):</b> Industry gold standard. <i>Clear</i> overwrites user-addressable storage space with a single pass plus read verification. <i>Purge</i> utilizes internal hardware commands (ATA Secure Erase / Sanitize) to purge non-addressable spare sectors and reallocated blocks."),
            ("bullet", "<b>Peter Gutmann (35 Passes):</b> 4 pseudo-random passes, 27 specific magnetic flux transition patterns designed for older MFM/RLL encoding schemes, and 4 final random passes."),
            ("bullet", "<b>Other Standards:</b> US Army AR380-19 (3 passes), US Air Force AFSSI-5020 (3 passes), Russian GOST R 50739-95 (2 passes), German VSITR (7 passes), British HMG IS5 Baseline & Enhanced, NATO, and RCMP TSSIT OPS-II.")
        ]
    ))

    story.append(make_qa_box(
        4, "Deep Dive",
        "Why do we use complement patterns (~0x00) and random data instead of just writing zeros?",
        [
            ("bullet", "<b>Physics of Magnetic Storage:</b> On magnetic hard disk drives (HDDs), bits are stored by aligning microscopic magnetic domains. Writing only zeros leaves slight magnetic hysteresis traces along the edges of the physical track, which theoretically could be reconstructed using specialized laboratory equipment like Magnetic Force Microscopy (MFM)."),
            ("bullet", "<b>Complement Inversion:</b> Writing a pattern (e.g. <code>0x55</code> = 01010101) immediately followed by its bitwise complement (<code>0xAA</code> = 10101010) forces every single magnetic domain to flip polarity, neutralizing residual hysteresis."),
            ("bullet", "<b>Modern Drives vs Legacy:</b> While modern high-density PRML/SMR hard drives make recovering data after a single verified zero pass nearly impossible, government and military compliance certifications (DoD, NIST) strictly require multi-pass complement and pseudo-random patterns before equipment can be decommissioned.")
        ]
    ))

    story.append(make_qa_box(
        5, "SSD vs HDD",
        "How does SSD erasure fundamentally differ from HDD erasure? Why is software overwriting tricky on SSDs?",
        [
            ("bullet", "<b>Flash Translation Layer (FTL) Abstraction:</b> On SSDs, Logical Block Addresses (LBAs) do NOT correspond to fixed physical flash cells. The FTL constantly redirects writes to different physical NAND blocks to achieve <b>Wear Leveling</b>."),
            ("bullet", "<b>Over-Provisioning & Inaccessible Blocks:</b> SSDs have spare NAND capacity (over-provisioning) and retired bad blocks that the OS cannot directly address via standard LBA sector writes. A software overwrite to LBA 500 writes to a new NAND cell, leaving the stale cell untouched until garbage collection runs."),
            ("bullet", "<b>How BitRaser Handles SSDs:</b>"),
            ("bullet", "1. <i>Free Space Wipe + TRIM:</i> Overwrites unused clusters and invokes the Windows TRIM API (<code>FSCTL_FILE_LEVEL_TRIM</code>), informing the SSD controller that those physical blocks contain invalid data for immediate background erase."),
            ("bullet", "2. <i>Firmware / ATA Secure Erase:</i> For full volume/disk sanitization, BitRaser invokes ATA Secure Erase / NVMe Format commands directly via <code>IOCTL</code>, which instructs the hardware controller to apply a voltage spike across all flash blocks simultaneously, sanitizing the entire drive including over-provisioned areas.")
        ]
    ))

    story.append(make_qa_box(
        6, "Verification",
        "Explain how Overwrite Verification works. What is the difference between Quick and Deep verification?",
        [
            ("bullet", "<b>Verification Logic (<code>DiskIO.cpp -> Verification()</code>):</b> After writing the pattern buffer to disk, the application immediately reads the sectors back into memory and compares them byte-for-byte against the expected pattern buffer."),
            ("bullet", "<b>Quick Verification (<code>QUICKVERIFICATION</code>):</b> Validates a statistical sample of sectors (e.g., 1 sector block out of every 4, or sampling boundaries of clusters). This provides high confidence while minimizing verification time on multi-terabyte drives."),
            ("bullet", "<b>Deep Verification (<code>DEEPVERIFICATION</code>):</b> Performs a 100% complete read-back of every single wiped sector across the entire disk or file. If a single byte differs or an I/O read error occurs, the process logs a verification failure and flags the audit report.")
        ]
    ))

    # ---------------- SECTION 3 ----------------
    story.append(make_section_header("SECTION 3: LOW-LEVEL WIN32 PROGRAMMING & FILE SYSTEM INTERNALS"))
    story.append(Spacer(1, 8))

    story.append(make_qa_box(
        7, "Win32 API",
        "How does BitRaser open physical disks and volumes? Which Win32 APIs and flags are mandatory?",
        [
            ("bullet", "<b>Device Handle Acquisition:</b>"),
            ("code", 'HANDLE hDevice = CreateFileW(lpbDiskString, GENERIC_READ | GENERIC_WRITE, \n'
                     '    FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE, \n'
                     '    NULL, OPEN_EXISTING, FILE_FLAG_NO_BUFFERING | FILE_FLAG_WRITE_THROUGH, NULL);'),
            ("bullet", "<b>Physical vs Logical Path Formats:</b>"),
            ("bullet", "• Physical Disk: <code>\\\\.\\PHYSICALDRIVE0</code> (accesses entire physical disk, bypassing partition tables)."),
            ("bullet", "• Logical Volume: <code>\\\\.\\C:</code> (accesses volume clusters directly)."),
            ("bullet", "<b>Crucial Flags:</b>"),
            ("bullet", "• <code>FILE_FLAG_NO_BUFFERING</code>: Completely bypasses Windows system cache buffers. Data is written directly from application memory to the storage media. <i>Requirement:</i> Memory buffers and byte counts must be integer multiples of the disk sector size (512 or 4096 bytes)."),
            ("bullet", "• <code>FILE_FLAG_WRITE_THROUGH</code>: Prevents intermediate caching; ensures <code>WriteFile</code> does not return until the hardware controller commits the data to non-volatile storage."),
            ("bullet", "<b>64-Bit Seeking:</b> Uses <code>SetFilePointer</code> / <code>SetFilePointerEx</code> with a 64-bit <code>LARGE_INTEGER</code> offset calculated as: <code>SectorNo * SECTSIZE</code>.")
        ]
    ))

    story.append(make_qa_box(
        8, "File Systems",
        "What is Slack Space, and how does BitRaser wipe it without corrupting valid data?",
        [
            ("bullet", "<b>Understanding Slack Space:</b> File systems allocate space in cluster increments (e.g., 4 KB = 4096 bytes). If a file's logical size is 1500 bytes, the file system allocates an entire 4096-byte cluster."),
            ("bullet", "• <i>RAM Slack:</i> The remaining bytes from the end of the file (byte 1500) to the end of the 512-byte sector (byte 1536). Historically padded with RAM contents by old OS kernels."),
            ("bullet", "• <i>Cluster Slack:</i> The unused space from the end of that sector (byte 1536) to the end of the allocated cluster (byte 4096). This area frequently holds fragments of previously deleted confidential files!"),
            ("bullet", "<b>How BitRaser Erases Slack Space:</b>"),
            ("bullet", "1. Queries the file's physical allocation clusters using Win32 API <code>FSCTL_GET_RETRIEVAL_POINTERS</code>."),
            ("bullet", "2. Calculates the exact offset between logical End-Of-File (EOF) and physical cluster boundary."),
            ("bullet", "3. Overwrites only the residual bytes from EOF to the end of the allocated cluster with wiping patterns, preserving the original file content intact.")
        ]
    ))

    story.append(make_qa_box(
        9, "NTFS Internals",
        "How does NTFS store files, and what happens to the Master File Table (MFT) records after file erasure?",
        [
            ("bullet", "<b>NTFS Architecture:</b> In NTFS, every file and folder has a 1024-byte record inside the Master File Table (<code>$MFT</code>). Small files (< 700 bytes) are stored 'resident' directly inside the MFT record itself!"),
            ("bullet", "<b>The Forensic Leak:</b> If you only overwrite the external data clusters and delete the file, the MFT record still retains the file name, file creation/modification timestamps, file size, permissions, and directory tree path!"),
            ("bullet", "<b>BitRaser's MFT & Journal Scrubbing:</b>"),
            ("bullet", "1. Overwrites the file's data clusters with the selected algorithm."),
            ("bullet", "2. Truncates and overwrites the resident attributes inside the MFT entry."),
            ("bullet", "3. Cleans metadata from NTFS transaction journals: <code>$LogFile</code> and <code>$UsnJrnl</code> (Update Sequence Number Journal), preventing forensic software from reading historic file transactions.")
        ]
    ))

    story.append(make_qa_box(
        10, "Locked Files",
        "How does the software handle files that are locked by Windows or other processes (ERROR_SHARING_VIOLATION)?",
        [
            ("bullet", "<b>The Challenge:</b> When an active process or system service holds an exclusive handle on a file (e.g. system logs, antivirus DBs), <code>CreateFile</code> fails with error code 32 (<code>ERROR_SHARING_VIOLATION</code>)."),
            ("bullet", "<b>BitRaser's Multi-Tier Resolution:</b>"),
            ("bullet", "• <b>Tier 1 - Process Identification:</b> Uses Windows Restart Manager APIs (<code>RmStartSession</code>, <code>RmRegisterResources</code>, <code>RmGetList</code>) to identify which process holds the lock and prompts the user to close it gracefully."),
            ("bullet", "• <b>Tier 2 - Non-Exclusive Share Flags:</b> Attempts opening with <code>FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE</code>."),
            ("bullet", "• <b>Tier 3 - Boot-Time Scheduling:</b> For core OS files, BitRaser registers the file for deletion during the next Windows startup sequence before file locking services start, leveraging <code>MoveFileEx(..., MOVEFILE_DELAY_UNTIL_REBOOT)</code> and custom boot-time drivers.")
        ]
    ))

    story.append(make_qa_box(
        11, "Long Paths",
        "How does BitRaser handle file paths exceeding the standard 260-character MAX_PATH limit?",
        [
            ("bullet", "Standard Windows APIs enforce a legacy limit of 260 characters (<code>MAX_PATH</code>). Deep folder hierarchies easily exceed this."),
            ("bullet", "In <code>bitraserfileeraser.h</code>, the macro <code>UNC_PATH_PREFIX</code> is defined as <code>L\"\\\\?\\\"</code>."),
            ("bullet", "By prepending <code>\\\\?\\</code> to absolute file paths (e.g. <code>\\\\?\\C:\\Deep\\Folder\\...\\file.txt</code>), the Win32 API bypasses path parsing and supports paths up to <b>32,767 Unicode characters</b>."),
            ("bullet", "All file operations throughout the codebase utilize wide-character Win32 APIs (<code>CreateFileW</code>, <code>FindFirstFileW</code>, <code>DeleteFileW</code>).")
        ]
    ))

    # ---------------- SECTION 4 ----------------
    story.append(make_section_header("SECTION 4: SYSTEM, BROWSER & APPLICATION TRACES ERASURE"))
    story.append(Spacer(1, 8))

    story.append(make_qa_box(
        12, "Trace Cleaning",
        "What are 'System Traces' and how does BitRaser sanitize them?",
        [
            "System traces are digital footprints left by Windows during daily operation (implemented in <code>systemtraces.cpp</code>):",
            ("bullet", "<b>Windows Prefetch (C:\\Windows\\Prefetch\\*.pf):</b> Records binary paths and launch frequency of every executed application. Overwritten and cleared."),
            ("bullet", "<b>Recycle Bin ($Recycle.Bin):</b> Overwrites the raw clusters of deleted files and purges index metadata (<code>$I...</code> and <code>$R...</code> files)."),
            ("bullet", "<b>Recent Documents & Jump Lists:</b> Cleans LNK shortcuts and binary jump lists in <code>%APPDATA%\\Microsoft\\Windows\\Recent</code>."),
            ("bullet", "<b>Windows Event Logs (*.evtx):</b> Cleans security and application event logs that record logon sessions and process executions."),
            ("bullet", "<b>Temporary Files (%TEMP%, C:\\Windows\\Temp):</b> Overwrites and deletes orphaned cache and installer artifacts."),
            ("bullet", "<b>Registry MRU Lists:</b> Sanitizes Most Recently Used (MRU) lists stored in the Windows Registry (e.g. Run dialog history, TypedURLs, Open/Save file dialog history).")
        ]
    ))

    story.append(make_qa_box(
        13, "Browser Traces",
        "How does the software sanitize browser traces (Chrome, Firefox, Edge) when SQLite databases are locked?",
        [
            ("bullet", "<b>Browser Data Storage:</b> Modern browsers store browsing history, cookies, download history, and session tokens inside SQLite database files (e.g. <code>History</code>, <code>Cookies</code>, <code>Web Data</code>) under <code>%LOCALAPPDATA%</code>."),
            ("bullet", "<b>Handling SQLite WAL Locks:</b>"),
            ("bullet", "1. Detects if browser processes (<code>chrome.exe</code>, <code>firefox.exe</code>, <code>msedge.exe</code>) are running using <code>CreateToolhelp32Snapshot</code> and prompts the user to terminate them."),
            ("bullet", "2. If browsers are closed, BitRaser connects via SQLite or directly overwrites and truncates the database files, including their Write-Ahead Log (<code>-wal</code>) and Shared Memory (<code>-shm</code>) files."),
            ("bullet", "3. Overwrites browser cache directories containing cached web images, scripts, and temporary session files.")
        ]
    ))

    # ---------------- SECTION 5 ----------------
    story.append(make_section_header("SECTION 5: C++, QT & SOFTWARE ARCHITECTURE"))
    story.append(Spacer(1, 8))

    story.append(make_qa_box(
        14, "Design Patterns",
        "What design patterns are used in this project? Give examples from the code.",
        [
            ("bullet", "<b>Singleton Pattern:</b> Implemented in <code>BitRaserFileEraser::GetInstance()</code>. Provides a single globally accessible instance managing application lifecycle, active settings, database connection, and licensing state."),
            ("bullet", "<b>Wizard Pattern:</b> Used in <code>WipingWizard</code> and <code>ScheduleWipingWizard</code>. Manages complex multi-step user workflows (Selecting targets -> Configuring wiping algorithm & verification -> Pre-wipe summary -> Execution & real-time progress -> Post-wipe report)."),
            ("bullet", "<b>Command / Worker Pattern:</b> Encapsulates scheduled and ad-hoc background wiping actions inside <code>BTask</code> and <code>btaskbase</code> classes."),
            ("bullet", "<b>Observer Pattern (Signals & Slots):</b> Qt's Signal and Slot mechanism decouples the low-level I/O wiping worker threads from GUI updates (e.g. progress bar percentages, sector speed, time remaining, file tree updates).")
        ]
    ))

    story.append(make_qa_box(
        15, "Threading & GUI",
        "How do you prevent UI freezing during intensive raw disk I/O? How is thread communication handled?",
        [
            ("bullet", "<b>The Bottleneck:</b> Disk wiping executes millions of synchronous <code>WriteFile</code> and <code>ReadFile</code> calls. Running this on the Qt GUI main thread blocks the Windows message pump, causing the window to freeze and trigger Windows 'Not Responding' status."),
            ("bullet", "<b>Multi-Threaded Architecture:</b>"),
            ("bullet", "1. The main Qt GUI thread handles user interaction, rendering, and window events."),
            ("bullet", "2. Erasure runs in a dedicated background worker thread (<code>QThread</code>)."),
            ("bullet", "3. Communication uses Qt Queued Connections (<code>Qt::QueuedConnection</code>) across thread boundaries."),
            ("bullet", "<b>Event Queue Throttling:</b> Emitting a Qt signal on <i>every single 512-byte sector</i> would flood the event queue and choke the UI thread. Instead, progress signals are throttled to emit only after processing large chunks (e.g. every 16 MB or every 250 milliseconds).")
        ]
    ))

    story.append(make_qa_box(
        16, "Single Instance",
        "How is Single Instance Application enforcement implemented in main.cpp?",
        [
            ("bullet", "In <code>main.cpp</code>, the application uses <code>QSharedMemory</code> with a unique GUID:"),
            ("code", 'QSharedMemory shared("32s60669-ab94-4a84-88bc-b964790f7g02");\n'
                     'if (!shared.create(512, QSharedMemory::ReadWrite)) {\n'
                     '    // Second instance detected - display warning dialog and terminate\n'
                     '    MassageBoxDlg msg("Warning", "An instance is already running.", ...);\n'
                     '    msg.exec();\n'
                     '    return 0;\n'
                     '}'),
            ("bullet", "If <code>shared.create()</code> returns false, the operating system already holds this shared memory segment from an active instance. The duplicate instance alerts the user and exits immediately.")
        ]
    ))

    story.append(make_qa_box(
        17, "UI Features",
        "How are Themes (Dark/Light) and Internationalization (i18n) handled?",
        [
            ("bullet", "<b>Theming (<code>BRF_Theme</code>):</b> Managed via registry key. The application dynamically applies custom Qt Style Sheets (QSS) to re-skin dialogs, table widgets, buttons, and switches between light/dark asset icon sets (e.g. <code>IDI_WIPE_NOW</code> vs <code>IDI_WIPE_NOW_B</code>)."),
            ("bullet", "<b>Multi-Language i18n (<code>m_Language</code>):</b> Supports 7 languages: English, German, French, Japanese, Spanish, Italian, and Dutch. Implemented using <code>QTranslator</code> and compiled binary translation files (<code>.qm</code>) loaded from Qt resource files (<code>Resource.qrc</code>). Date formatting is localized using Win32 API <code>SetLocaleInfoW</code>.")
        ]
    ))

    # ---------------- SECTION 6 ----------------
    story.append(make_section_header("SECTION 6: CLOUD INTEGRATION, LICENSING & CRYPTOGRAPHY"))
    story.append(Spacer(1, 8))

    story.append(make_qa_box(
        18, "Licensing",
        "How does the software generate a Machine Fingerprint (Digital ID) and enforce licensing?",
        [
            ("bullet", "<b>Machine Fingerprinting (<code>GetDigitalID()</code> in <code>bitraserlicenseservice.cpp</code>):</b>"),
            ("bullet", "• Extracts immutable hardware attributes: Motherboard UUID, CPU ID / Serial, Primary Network Adapter MAC Address, and System Drive Volume Serial Number."),
            ("bullet", "• Hashes these identifiers together into a unique, tamper-proof Digital Machine ID."),
            ("bullet", "<b>Online Activation:</b> Posts the machine ID and user's activation key to Stellar's web licensing server via HTTPS (<code>fncASActivateLicense</code>). If valid, returns an encrypted license string storing allowable erasure counts and expiry."),
            ("bullet", "<b>Anti-Tamper & Anti-Cloning:</b> If an activated image is cloned onto another machine or VM, the Digital ID mismatch invalidates the local license cache, reverting the software to Demo mode.")
        ]
    ))

    story.append(make_qa_box(
        19, "Cloud Security",
        "How is data secured during transit to the BitRaser Cloud Console?",
        [
            ("bullet", "<b>Transport Security:</b> Built on top of <code>libcurl</code> utilizing TLS 1.2/1.3 with a bundled trusted root certificate authority bundle (<code>cacert.pem</code>)."),
            ("bullet", "<b>Application Payload Encryption:</b>"),
            ("bullet", "• JSON data packets are encrypted using <b>AES-128-CBC</b> (<code>AES_128_CBC_encrypt</code>) with randomized Initialization Vectors (IV) and PKCS7 padding before dispatch."),
            ("bullet", "• Ciphertext is encoded with <b>Base64</b> (<code>Base64Encode</code>) for safe JSON HTTP transmission."),
            ("bullet", "• Local sensitive credentials stored in the Windows Registry are obfuscated using a custom salted XOR algorithm (<code>encryptPassToXOR</code>).")
        ]
    ))

    story.append(make_qa_box(
        20, "PDF Certificates",
        "How are PDF Certificates of Erasure generated, and how is audit compliance verified?",
        [
            ("bullet", "<b>PDF Engine (<code>reportsaving.cpp</code>):</b> Utilizes the Debenu PDF Library (Quick PDF) to generate digitally verifiable, tamper-evident Certificates of Erasure."),
            ("bullet", "<b>Forensic Audit Content:</b> Each certificate documents:"),
            ("bullet", "• Disk/Device Details: Model, Serial Number, Disk Capacity, Bus Type."),
            ("bullet", "• Erasure Metadata: Algorithm used, Number of Passes, Verification Result (100% Passed), Total Bytes Wiped, Duration."),
            ("bullet", "• Legal Audit Trail: Technician Name, Validator Name, Department, Organization Logo, Watermark, and Timestamps."),
            ("bullet", "<b>Tamper Verification:</b> A cryptographic SHA-256 hash of the process data is generated and synchronized with the BitRaser Cloud Console. If someone edits the generated PDF file, the certificate hash will fail validation against the cloud audit log.")
        ]
    ))

    # ---------------- SECTION 7 ----------------
    story.append(make_section_header("SECTION 7: TASK SCHEDULING, SHELL INTEGRATION & DATABASE"))
    story.append(Spacer(1, 8))

    story.append(make_qa_box(
        21, "Task Scheduling",
        "How does the automated Task Scheduler work without launching the main user interface?",
        [
            ("bullet", "<b>Windows Task Scheduler 2.0 COM API:</b> Implemented in <code>btask.cpp</code> using <code>taskschd.h</code> (<code>ITaskService</code>, <code>ITaskFolder</code>, <code>ITaskDefinition</code>, <code>ITriggerCollection</code>)."),
            ("bullet", "<b>Supported Triggers:</b> Daily, Weekly, Monthly, At System Logon, and At System Shutdown."),
            ("bullet", "<b>Unattended Execution Flow:</b>"),
            ("bullet", "1. Windows Task Scheduler executes <code>brf.exe</code> with a specific command-line argument starting with <code>$BRFST-</code> (e.g. <code>$BRFST-EraseTraces</code>)."),
            ("bullet", "2. In <code>main.cpp</code>, the flag <code>launchedByScheduler</code> is set to true."),
            ("bullet", "3. Instead of launching the full interactive main window, it instantiates <code>ScheduleWipingWizard</code> in a silent/minimized mode, runs the assigned wipe job, logs results into <code>LocalDb</code>, and terminates cleanly.")
        ]
    ))

    story.append(make_qa_box(
        22, "Explorer Shell",
        "How does the Windows Explorer right-click context menu erasure work?",
        [
            ("bullet", "<b>Shell Verb Registration:</b> During installation, BitRaser registers Windows Shell context verbs under <code>HKCR\\*\\shell\\BitRaser</code> and <code>HKCR\\Directory\\shell\\BitRaser</code>."),
            ("bullet", "<b>Execution Mechanism:</b>"),
            ("bullet", "1. When a user right-clicks selected files in Explorer and clicks 'Erase with BitRaser', Windows launches <code>brf.exe</code> with parameter '2' or writes the target paths into a temporary control file <code>BitRaser_Ext.txt</code> in <code>%LOCALAPPDATA%</code>."),
            ("bullet", "2. <code>main.cpp</code> calls <code>isRightClickOrCommandLine()</code> to parse the file paths, validates their existence and permissions, and launches the wiping wizard targeted specifically at those paths without requiring the user to navigate the entire app.")
        ]
    ))

    story.append(make_qa_box(
        23, "Local Database",
        "What local database is used, and what data structures are stored?",
        [
            ("bullet", "<b>Database Engine (<code>LocalDb.cpp</code>):</b> Embedded MariaDB / MySQL client library (<code>libmariadb.dll</code>)."),
            ("bullet", "<b>Key Data Tables & Structures:</b>"),
            ("bullet", "• <code>FileDataInfo</code>: Stores historical logs of every erased file: Name, Absolute Path, Status (Success/Failed), Start/End timestamps, File size, and ProcessID."),
            ("bullet", "• <code>DeletedDataInfo</code>: Stores free space erasure logs: Drive letter, total unused space, erased space, duration, and status."),
            ("bullet", "• <code>ProcessDataInfo</code>: High-level process summary: Algorithm used, total files wiped, verification status, and error codes."),
            ("bullet", "• <code>UserDataInfo</code>: Stores auditor details: Technician name, validator name, department, custom headers, and signature file paths.")
        ]
    ))

    # ---------------- SECTION 8 ----------------
    story.append(make_section_header("SECTION 8: TOUGH INTERVIEW SCENARIOS, DEBUGGING & BEHAVIORAL"))
    story.append(Spacer(1, 8))

    story.append(make_qa_box(
        24, "Troubleshooting",
        "Describe a difficult bug you encountered in this project and how you solved it.",
        [
            "<b>Top Technical Bug: The 4K Native (4Kn) Unbuffered Write Error (Error 87)</b>",
            ("bullet", "<b>Symptom:</b> On newly released external NVMe drives and 4Kn enterprise HDDs, disk wiping failed immediately with Win32 Error 87 (<code>ERROR_INVALID_PARAMETER</code>), while the exact same code worked fine on older 512-byte sector drives."),
            ("bullet", "<b>Root Cause Analysis:</b> When using <code>FILE_FLAG_NO_BUFFERING</code> in <code>CreateFile</code>, Windows strictly enforces that both the memory buffer memory address (pointer) AND the number of bytes written must be an exact integer multiple of the disk's physical sector size! The legacy buffer size was hardcoded to 512 bytes."),
            ("bullet", "<b>Solution:</b>"),
            ("bullet", "1. Implemented a dynamic query using <code>DeviceIoControl(hDevice, IOCTL_DISK_GET_DRIVE_GEOMETRY_EX, ...)</code> to retrieve the exact <code>BytesPerSector</code> (e.g. 4096 bytes)."),
            ("bullet", "2. Replaced heap memory allocations (<code>malloc</code>/<code>new</code>) with <code>VirtualAlloc</code>, which guarantees that memory buffers are aligned to OS page boundaries (4096-byte boundary)."),
            ("bullet", "3. Adjusted the wiping chunk loop to write in exact multiples of 4096 bytes. The bug was completely resolved across all drive formats.")
        ]
    ))

    story.append(make_qa_box(
        25, "Edge Case",
        "What happens if power is cut or the system crashes midway through a multi-pass wipe?",
        [
            ("bullet", "<b>Data Recoverability:</b> Sectors that have already been overwritten with random/zero patterns are permanently destroyed and completely unrecoverable. Sectors that were not yet reached retain their original state."),
            ("bullet", "<b>System State & Integrity:</b>"),
            ("bullet", "• If wiping an entire volume/drive, the partition table and file system superblock may already be destroyed. Windows will prompt that the drive needs formatting."),
            ("bullet", "• BitRaser tracks state incrementally in <code>LocalDb</code>. If restarted after an unexpected crash, the process status is marked as 'Aborted / Incomplete'."),
            ("bullet", "• Under no circumstances will a Certificate of Erasure be generated for an interrupted wipe, strictly preventing false audit compliance.")
        ]
    ))

    story.append(make_qa_box(
        26, "Compliance",
        "How do you prove to an auditor that data erased by BitRaser is truly unrecoverable?",
        [
            ("bullet", "<b>1. Internal Bit-Level Read Verification:</b> Every sector can undergo 100% read-back verification against the expected algorithm pattern."),
            ("bullet", "<b>2. Forensic Carving Validation:</b> The wiped media is scanned using commercial recovery tools (Stellar Data Recovery, EnCase, FTK Imager, Autopsy). Technicians verify that zero file signatures (e.g. JPEG, PDF, DOCX magic bytes) can be salvaged."),
            ("bullet", "<b>3. Hex Examination:</b> Low-level hex editors (WinHex, HxD) verify that physical LBA sectors contain uniform zeros or random entropy without any readable text or file table remnants."),
            ("bullet", "<b>4. International Lab Certifications:</b> BitRaser software is certified by independent bodies such as ADISA (Asset Disposal & Information Security Alliance) and compliant with NIST 800-88 standards.")
        ]
    ))

    # ---------------- SECTION 9 ----------------
    story.append(make_section_header("SECTION 9: CANDIDATE REVISION CHEAT SHEET"))
    story.append(Spacer(1, 8))

    cheat_data = [
        [
            Paragraph("<b>Topic</b>", ParagraphStyle('H1', parent=body_style, fontName='Helvetica-Bold', textColor=colors.HexColor("#0F2942"))),
            Paragraph("<b>Key Functions / Concepts to Mention in Interview</b>", ParagraphStyle('H2', parent=body_style, fontName='Helvetica-Bold', textColor=colors.HexColor("#0F2942")))
        ],
        [
            Paragraph("<b>Win32 Disk APIs</b>", body_style),
            Paragraph("<code>CreateFileW</code>, <code>WriteFile</code>, <code>ReadFile</code>, <code>SetFilePointerEx</code>, <code>DeviceIoControl</code>, <code>VirtualAlloc</code>, <code>FILE_FLAG_NO_BUFFERING</code>, <code>FILE_FLAG_WRITE_THROUGH</code>", body_style)
        ],
        [
            Paragraph("<b>Drive Path Syntax</b>", body_style),
            Paragraph("Physical Drive: <code>\\\\.\\PHYSICALDRIVE0</code> | Logical Volume: <code>\\\\.\\C:</code> | Extended Path: <code>\\\\?\\C:\\LongPath...</code>", body_style)
        ],
        [
            Paragraph("<b>Key Algorithms</b>", body_style),
            Paragraph("NIST 800-88 Clear (1-pass + verify), DoD 5220.22-M (3-pass: zero, complement, random), Gutmann (35 passes), HMG IS5, VSITR", body_style)
        ],
        [
            Paragraph("<b>File System Internals</b>", body_style),
            Paragraph("Cluster Slack, RAM Slack, Master File Table (MFT) record overwrite, <code>$LogFile</code> & <code>$UsnJrnl</code> wiping, FTL & TRIM on SSDs", body_style)
        ],
        [
            Paragraph("<b>Qt Architecture</b>", body_style),
            Paragraph("<code>QThread</code> (worker threads), Queued Connection signals/slots, <code>QSharedMemory</code> (single instance), <code>QWizard</code>, <code>QTranslator</code> (i18n)", body_style)
        ],
        [
            Paragraph("<b>Cloud & Security</b>", body_style),
            Paragraph("<code>libcurl</code> over TLS 1.3, AES-128-CBC payload encryption, Base64 encoding, Machine Fingerprinting (Digital ID), Debenu PDF Library", body_style)
        ],
        [
            Paragraph("<b>Task Scheduler</b>", body_style),
            Paragraph("Windows Task Scheduler 2.0 COM API (<code>taskschd.h</code>, <code>ITaskService</code>), <code>$BRFST-</code> command-line flags, Explorer context menu verbs", body_style)
        ]
    ]

    cheat_table = Table(cheat_data, colWidths=[120, 395])
    cheat_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(cheat_table)

    # Build document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF: {filename}")

if __name__ == "__main__":
    out_file = "BitRaser_File_Eraser_Interview_QA.pdf"
    if len(sys.argv) > 1:
        out_file = sys.argv[1]
    build_pdf(out_file)

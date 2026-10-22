"""
Semester-wise subject list for every demo course.

Subject codes are <prefix><semester><nn>, e.g. BCA101 is the first semester-1 subject of BCA
and LAW1003 the third semester-10 subject of BALLB.
"""
from .models import Subject

# Subjects whose name contains one of these are practical/project work and carry fewer credits
PRACTICAL_KEYWORDS = ("Project", "Internship", "Seminar", "Dissertation", "Training", "Report", "Lab",
                      "Moot Court", "Practice School")

ENGINEERING_SEM_1 = ("Engineering Mathematics I", "Engineering Physics", "Programming for Problem Solving",
                     "Engineering Graphics")

# Course code -> (subject code prefix, one tuple of subject names per semester)
SYLLABUS = {
    "BCA": ("BCA", [
        ("Programming in C", "Mathematical Foundations", "Digital Electronics", "Fundamentals of Computers", "Communicative English"),
        ("Data Structures", "Object Oriented Programming with C++", "Discrete Mathematics", "Computer Organization", "Environmental Studies"),
        ("Database Management Systems", "Operating Systems", "Java Programming", "Computer Networks", "Statistics and Probability"),
        ("Software Engineering", "Web Programming", "Python Programming", "Design and Analysis of Algorithms", "Numerical Methods"),
        ("Cloud Computing", "Data Mining", "Mobile Application Development", "Computer Graphics", "Mini Project"),
        ("Artificial Intelligence", "Cyber Security", "Machine Learning", "Internet of Things", "Major Project"),
    ]),
    "BSCIT": ("BIT", [
        ("Web Technologies", "Imperative Programming", "Digital Logic", "Operating Systems Fundamentals", "Discrete Mathematics"),
        ("Object Oriented Programming", "Microprocessor Architecture", "Web Programming", "Numerical and Statistical Methods", "Green Computing"),
        ("Python Programming", "Data Structures", "Computer Networks", "Database Management Systems", "Applied Mathematics"),
        ("Core Java", "Embedded Systems", "Computer Oriented Statistical Techniques", "Software Engineering", "Computer Graphics and Animation"),
        ("Software Project Management", "Internet of Things", "Advanced Web Programming", "Artificial Intelligence", "Enterprise Java"),
        ("Software Quality Assurance", "Security in Computing", "Business Intelligence", "Geographic Information Systems", "Project Implementation"),
    ]),
    "BEEC": ("EC", [
        ("Basic Electronics",) + ENGINEERING_SEM_1,
        ("Engineering Mathematics II", "Engineering Chemistry", "Basic Electrical Engineering", "Elements of Mechanical Engineering", "Technical English"),
        ("Network Analysis", "Electronic Devices", "Digital System Design", "Signals and Systems", "Engineering Mathematics III"),
        ("Analog Circuits", "Microcontrollers", "Control Systems", "Electromagnetic Field Theory", "Probability and Random Processes"),
        ("Digital Signal Processing", "Analog and Digital Communication", "Linear Integrated Circuits", "Computer Organization", "Environmental Studies"),
        ("VLSI Design", "Embedded Systems", "Microwave Engineering", "Information Theory and Coding", "Mini Project"),
        ("Wireless Communication", "Optical Fiber Communication", "Antenna and Wave Propagation", "Image Processing", "Internship"),
        ("Satellite Communication", "Network Security", "Internet of Things", "Project Work", "Technical Seminar"),
    ]),
    "BEEE": ("EE", [
        ("Circuit Theory",) + ENGINEERING_SEM_1,
        ("Engineering Mathematics II", "Engineering Chemistry", "Basic Electronics", "Elements of Mechanical Engineering", "Technical English"),
        ("Electric Circuit Analysis", "Analog Electronic Circuits", "Digital System Design", "Transformers and Generators", "Engineering Mathematics III"),
        ("Electric Motors", "Electromagnetic Field Theory", "Power Generation and Economics", "Operational Amplifiers", "Electrical Measurements and Instrumentation"),
        ("Transmission and Distribution", "Control Systems", "Power Electronics", "Signals and Systems", "Environmental Studies"),
        ("Power System Analysis", "Microcontrollers", "Electrical Machine Design", "Renewable Energy Sources", "Mini Project"),
        ("Power System Protection", "High Voltage Engineering", "Electric Drives", "Utilization of Electrical Power", "Internship"),
        ("Smart Grid Technology", "Electric Vehicles", "Power Quality", "Project Work", "Technical Seminar"),
    ]),
    "BEME": ("ME", [
        ("Engineering Mechanics",) + ENGINEERING_SEM_1,
        ("Engineering Mathematics II", "Engineering Chemistry", "Basic Electrical Engineering", "Workshop Practice", "Technical English"),
        ("Mechanics of Materials", "Basic Thermodynamics", "Material Science", "Manufacturing Processes", "Engineering Mathematics III"),
        ("Applied Thermodynamics", "Fluid Mechanics", "Kinematics of Machines", "Machine Drawing", "Metal Cutting and Forming"),
        ("Dynamics of Machines", "Design of Machine Elements I", "Turbomachines", "Management and Entrepreneurship", "Environmental Studies"),
        ("Heat Transfer", "Design of Machine Elements II", "Finite Element Analysis", "Computer Integrated Manufacturing", "Mini Project"),
        ("Control Engineering", "Computer Aided Design", "Automobile Engineering", "Operations Research", "Internship"),
        ("Robotics", "Additive Manufacturing", "Energy Engineering", "Project Work", "Technical Seminar"),
    ]),
    "BECV": ("CV", [
        ("Surveying",) + ENGINEERING_SEM_1,
        ("Engineering Mathematics II", "Engineering Chemistry", "Basic Electrical Engineering", "Elements of Civil Engineering", "Technical English"),
        ("Strength of Materials", "Fluid Mechanics", "Building Materials and Construction", "Engineering Geology", "Engineering Mathematics III"),
        ("Analysis of Determinate Structures", "Concrete Technology", "Advanced Surveying", "Hydraulics and Hydraulic Machines", "Building Planning and Drawing"),
        ("Design of RC Structures", "Geotechnical Engineering", "Transportation Engineering", "Water Supply Engineering", "Environmental Studies"),
        ("Design of Steel Structures", "Foundation Engineering", "Wastewater Engineering", "Hydrology and Irrigation", "Mini Project"),
        ("Estimation and Costing", "Prestressed Concrete", "Construction Management", "Remote Sensing and GIS", "Internship"),
        ("Earthquake Engineering", "Bridge Engineering", "Pavement Design", "Project Work", "Technical Seminar"),
    ]),
    "BCOM": ("BCOM", [
        ("Financial Accounting", "Business Economics", "Principles of Management", "Business Communication", "Business Mathematics"),
        ("Advanced Financial Accounting", "Corporate Administration", "Banking Law and Practice", "Business Statistics", "Environmental Studies"),
        ("Corporate Accounting", "Cost Accounting", "Business Law", "Marketing Management", "Income Tax I"),
        ("Advanced Corporate Accounting", "Advanced Cost Accounting", "Company Law", "Financial Management", "Income Tax II"),
        ("Management Accounting", "Auditing", "Goods and Services Tax", "Entrepreneurship Development", "Investment Management"),
        ("Accounting for Government", "International Business", "Financial Markets and Services", "E-Commerce", "Project Report"),
    ]),
    "BBA": ("BBA", [
        ("Principles of Management", "Financial Accounting", "Business Economics", "Business Communication", "Quantitative Methods"),
        ("Organizational Behaviour", "Cost Accounting", "Macroeconomics", "Business Environment", "Environmental Studies"),
        ("Marketing Management", "Human Resource Management", "Financial Management", "Business Statistics", "Corporate Law"),
        ("Production and Operations Management", "Management Accounting", "Research Methodology", "Business Ethics", "Income Tax"),
        ("Strategic Management", "Entrepreneurship Development", "Consumer Behaviour", "Investment Management", "Summer Internship"),
        ("International Business", "Supply Chain Management", "Digital Marketing", "Banking and Insurance", "Project Report"),
    ]),
    "BSCPHY": ("PHY", [
        ("Mechanics", "Mathematical Physics I", "Calculus", "Inorganic Chemistry", "English I"),
        ("Properties of Matter", "Waves and Oscillations", "Differential Equations", "Organic Chemistry", "English II"),
        ("Thermal Physics", "Electricity and Magnetism", "Mathematical Physics II", "Analytical Chemistry", "Environmental Studies"),
        ("Optics", "Analog Electronics", "Mathematical Physics III", "Physical Chemistry", "Computational Physics"),
        ("Quantum Mechanics", "Atomic and Molecular Physics", "Digital Electronics", "Statistical Mechanics", "Solid State Physics"),
        ("Nuclear and Particle Physics", "Electromagnetic Theory", "Astrophysics", "Material Science", "Physics Project"),
    ]),
    "BSCCHE": ("CHE", [
        ("Inorganic Chemistry", "Organic Chemistry I", "Physical Chemistry I", "Mathematics for Chemists", "English I"),
        ("Atomic Structure and Bonding", "Organic Chemistry II", "Chemical Thermodynamics", "Physics for Chemists", "English II"),
        ("Chemistry of s and p Block Elements", "Stereochemistry", "Chemical Kinetics", "Analytical Chemistry", "Environmental Studies"),
        ("Coordination Chemistry", "Organic Reaction Mechanisms", "Electrochemistry", "Industrial Chemistry", "Polymer Chemistry"),
        ("Organometallic Chemistry", "Spectroscopy", "Quantum Chemistry", "Biochemistry", "Instrumental Methods of Analysis"),
        ("Bioinorganic Chemistry", "Medicinal Chemistry", "Green Chemistry", "Surface Chemistry", "Chemistry Project"),
    ]),
    "BSCMAT": ("MAT", [
        ("Calculus", "Algebra I", "Analytical Geometry", "Physics I", "English I"),
        ("Differential Equations", "Algebra II", "Vector Calculus", "Physics II", "English II"),
        ("Real Analysis I", "Group Theory", "Theory of Equations", "Probability and Statistics", "Environmental Studies"),
        ("Real Analysis II", "Ring Theory", "Partial Differential Equations", "Numerical Analysis", "Discrete Mathematics"),
        ("Linear Algebra", "Complex Analysis", "Mechanics", "Graph Theory", "Linear Programming"),
        ("Metric Spaces", "Number Theory", "Fourier Series and Transforms", "Mathematical Modelling", "Mathematics Project"),
    ]),
    "BSCBT": ("BT", [
        ("Cell Biology", "Biochemistry I", "Microbiology I", "Chemistry for Biologists", "English I"),
        ("Genetics", "Biochemistry II", "Microbiology II", "Biostatistics", "English II"),
        ("Molecular Biology", "Immunology", "Plant Biotechnology", "Bioinstrumentation", "Environmental Studies"),
        ("Genetic Engineering", "Animal Biotechnology", "Enzyme Technology", "Bioinformatics", "Biosafety and Bioethics"),
        ("Industrial Biotechnology", "Environmental Biotechnology", "Medical Biotechnology", "Genomics and Proteomics", "Bioprocess Engineering"),
        ("Pharmaceutical Biotechnology", "Food Biotechnology", "Intellectual Property Rights", "Nanobiotechnology", "Biotechnology Project"),
    ]),
    "BAENG": ("ENG", [
        ("British Poetry", "History of English Literature", "Introduction to Literary Forms", "Indian History", "Kannada I"),
        ("British Drama", "Indian Writing in English", "Phonetics and Spoken English", "Political Science", "Kannada II"),
        ("British Fiction", "American Literature", "Literary Criticism", "Sociology", "Environmental Studies"),
        ("Shakespeare", "Romantic Poetry", "Linguistics", "Women's Writing", "Creative Writing"),
        ("Victorian Literature", "Modern British Literature", "Postcolonial Literature", "Translation Studies", "Literature and Film"),
        ("Contemporary Literary Theory", "World Literature", "Dalit Literature", "Cultural Studies", "Dissertation"),
    ]),
    "BAECO": ("ECO", [
        ("Microeconomics", "Indian Economy", "Mathematics for Economics", "Political Science", "Kannada I"),
        ("Macroeconomics", "Economic History of India", "Statistics for Economics", "Sociology", "Kannada II"),
        ("Intermediate Microeconomics", "Money and Banking", "Public Finance", "Indian Constitution", "Environmental Studies"),
        ("Intermediate Macroeconomics", "International Economics", "Development Economics", "Econometrics", "Agricultural Economics"),
        ("Environmental Economics", "Labour Economics", "Industrial Economics", "Indian Public Policy", "Financial Economics"),
        ("Economics of Growth", "Urban Economics", "Health Economics", "Karnataka Economy", "Research Project"),
    ]),
    "BAPSY": ("PSY", [
        ("Introduction to Psychology", "Biological Psychology", "Statistics for Psychology", "Sociology", "English I"),
        ("Cognitive Psychology", "Developmental Psychology", "Psychological Testing", "Political Science", "English II"),
        ("Social Psychology", "Personality Theories", "Research Methods in Psychology", "Indian Constitution", "Environmental Studies"),
        ("Abnormal Psychology", "Health Psychology", "Counselling Psychology", "Positive Psychology", "Experimental Psychology Lab"),
        ("Clinical Psychology", "Organizational Psychology", "Educational Psychology", "Psychology of Gender", "Psychometrics"),
        ("Forensic Psychology", "Community Psychology", "Psychotherapy", "Neuropsychology", "Dissertation"),
    ]),
    "BAJMC": ("JMC", [
        ("News Reporting", "Introduction to Mass Communication", "History of Journalism", "Communication Skills", "Kannada I"),
        ("News Editing", "Photojournalism", "Media Laws and Ethics", "Indian Society and Culture", "Kannada II"),
        ("Radio Journalism", "Advertising", "Development Communication", "Indian Constitution", "Environmental Studies"),
        ("Television Journalism", "Public Relations", "Feature Writing", "Media Research", "Graphic Design"),
        ("Digital Journalism", "Documentary Production", "Corporate Communication", "Film Studies", "Internship"),
        ("Investigative Journalism", "Social Media Management", "Media Management", "Business Journalism", "Project Work"),
    ]),
    "BHM": ("HM", [
        ("Food Production", "Food and Beverage Service", "Front Office Operations", "Accommodation Operations", "Communication Skills"),
        ("Food Production II", "Food and Beverage Service II", "Front Office II", "Housekeeping II", "Nutrition and Food Science"),
        ("Advanced Food Production", "Bar Operations", "Hotel Accounting", "Hospitality Law", "Environmental Studies"),
        ("Industrial Training", "Training Report", "Hotel Engineering", "Tourism Management", "Computer Applications in Hospitality"),
        ("Quantity Food Production", "Food and Beverage Management", "Rooms Division Management", "Hospitality Marketing", "Human Resource Management"),
        ("International Cuisine", "Event Management", "Facility Planning", "Food Safety and Quality", "Financial Management"),
        ("Bakery and Confectionery", "Revenue Management", "Entrepreneurship in Hospitality", "Research Methodology", "Strategic Management"),
        ("Hotel Operations Management", "Customer Relationship Management", "Sustainable Hospitality", "Project Work", "Seminar"),
    ]),
    "BDES": ("FD", [
        ("Fashion Illustration", "Elements of Design", "History of Fashion", "Textile Science", "Communication Skills"),
        ("Pattern Making", "Garment Construction", "Colour Theory", "Fibre to Fabric", "Environmental Studies"),
        ("Advanced Pattern Making", "Draping", "Surface Ornamentation", "Fashion Merchandising", "Computer Aided Design"),
        ("Traditional Indian Textiles", "Fashion Forecasting", "Apparel Production", "Knitwear Design", "Craft Documentation"),
        ("Fashion Styling", "Menswear Design", "Fashion Marketing", "Textile Testing", "Internship"),
        ("Couture Design", "Accessory Design", "Sustainable Fashion", "Fashion Photography", "Visual Merchandising"),
        ("Portfolio Development", "Fashion Business Management", "Design Research", "Kidswear Design", "Fashion Retail"),
        ("Design Collection", "Entrepreneurship in Fashion", "Fashion Law", "Graduation Project", "Seminar"),
    ]),
    "BALLB": ("LAW", [
        ("Law of Contracts", "Legal Methods", "Political Science I", "Sociology I", "General English"),
        ("Specific Contracts", "Law of Torts", "Political Science II", "Economics I", "Legal English"),
        ("Constitutional Law I", "Family Law I", "History I", "Economics II", "Environmental Studies"),
        ("Constitutional Law II", "Family Law II", "Jurisprudence", "History II", "Political Science III"),
        ("Criminal Law", "Property Law", "Administrative Law", "Sociology II", "Labour Law I"),
        ("Criminal Procedure Code", "Company Law", "Public International Law", "Labour Law II", "Law of Evidence"),
        ("Civil Procedure Code", "Interpretation of Statutes", "Environmental Law", "Taxation Law", "Human Rights Law"),
        ("Alternative Dispute Resolution", "Intellectual Property Law", "Banking Law", "Competition Law", "Cyber Law"),
        ("Drafting Pleading and Conveyancing", "Professional Ethics", "Insurance Law", "Land Laws", "Moot Court"),
        ("Private International Law", "Women and Criminal Law", "Penology and Victimology", "Internship", "Dissertation"),
    ]),
    "BPHARM": ("PHA", [
        ("Pharmaceutics", "Human Anatomy and Physiology I", "Pharmaceutical Analysis I", "Pharmaceutical Inorganic Chemistry", "Communication Skills"),
        ("Human Anatomy and Physiology II", "Pharmaceutical Organic Chemistry I", "Biochemistry", "Pathophysiology", "Computer Applications in Pharmacy"),
        ("Pharmaceutical Organic Chemistry II", "Physical Pharmaceutics I", "Pharmaceutical Microbiology", "Pharmaceutical Engineering", "Environmental Sciences"),
        ("Pharmaceutical Organic Chemistry III", "Medicinal Chemistry I", "Physical Pharmaceutics II", "Pharmacology I", "Pharmacognosy and Phytochemistry I"),
        ("Medicinal Chemistry II", "Industrial Pharmacy I", "Pharmacology II", "Pharmacognosy and Phytochemistry II", "Pharmaceutical Jurisprudence"),
        ("Medicinal Chemistry III", "Pharmacology III", "Herbal Drug Technology", "Biopharmaceutics and Pharmacokinetics", "Pharmaceutical Biotechnology"),
        ("Instrumental Methods of Analysis", "Industrial Pharmacy II", "Pharmacy Practice", "Novel Drug Delivery System", "Practice School"),
        ("Biostatistics and Research Methodology", "Social and Preventive Pharmacy", "Pharmacovigilance", "Cosmetic Science", "Project Work"),
    ]),
}


def add_syllabus(course, faculty=None):
    """Create the course's missing syllabus subjects (existing codes are left untouched). Returns how many were added."""
    if course.code not in SYLLABUS:
        return 0
    prefix, semesters = SYLLABUS[course.code]
    existing = set(Subject.objects.filter(code__startswith=prefix).values_list("code", flat=True))
    new_subjects = [
        Subject(code=code, name=name, course=course, semester=sem, faculty=faculty,
                credits=2 if any(k in name for k in PRACTICAL_KEYWORDS) else 4)
        for sem, names in enumerate(semesters[:course.total_semesters], start=1)
        for n, name in enumerate(names, start=1)
        if (code := f"{prefix}{sem}{n:02d}") not in existing
    ]
    Subject.objects.bulk_create(new_subjects)
    return len(new_subjects)

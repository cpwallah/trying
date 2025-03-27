import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Button, Scale, messagebox, ttk, Entry, Frame, IntVar, Checkbutton, Scrollbar, Text, Toplevel, PhotoImage
from PIL import Image, ImageDraw, ImageFont, ImageTk
from fpdf import FPDF
from datetime import datetime
import openai
from termcolor import colored

openai.api_key = "API_KEY_OPENAI"

# Questions
questions = {
    "Openness to experience": [
        "Mujhe Nayi Jghon Kaa Pataa Lganaa Pasnd Hai. ",
        "Mujhe Vibhinn Sanskritiyon Aur Jiivn Ke Triikon Ke Baare Mein Jaanne Mein Dilchaspii Hai.",
        "Mujhe Ne Vichaaron Aur Drishtikonon Kaa Pataa Lganaa Pasnd Hai.",
        "Main Klaa Aur Rchnaatmktaa Se Aakarssit Huun.",
        "Mujhe Amuurt Vichaaron Aur Saiddhaantik Avdhaaranaaon Par Charcha Karnaa Pasnd Hai.",
        "Mujhe Vividh Aur Vividh Vissyon Ke Baare Mein Padhanaa Pasnd Hai",
        "Mujhe Sangrahalyon Aur Klaa Pradrshniyon Kaa Dauraa Karnaa Pasnd Hai. ",
        "Mujhe Drshn Aur Amuurt Vichaaron Mein Dilchaspii Hai.",
        "Mujhe Klaatmk Abhivykti Ke Vibhinn Ruupon Ke Saath Prayog Karnaa Pasnd Hai.",
        "Mujhe Samasyaon Ko Hal Karne Ke Vaiklpik Triikon Ke Baare Mein Sochnaa Pasnd Hai.",
        "Main Sthaapit Maandndon Aur Niymon Par Sawal Uthaanaa Pasnd Kartaa Huun.",
        "Mujhe Maanv Kssmataa Ki Khoj Mein Dilchaspii Hai.",
         
    ],
    "Awareness": [
        "Main Ek Sangthit Aur Anushaasit Vykti Huun.",
        "Mujhe Yojnaa Banaanaa Aur Lakshya Nirdhaarit Karnaa Pasnd Hai",
        "Main Samay Kaa Paabnd Huun Aur Main Apnii Pratibddhtaaon Ko Puuraa Kartaa Huun",
        "Main Jo Kaam Kartaa Huun Uski Gunvttaa Ki Parwah Kartaa Huun.",
        "Mujhe Sthaapit Niymon Aur Viniymon Kaa Paaln Karnaa Pasnd Hai.",
        "Mujhe Sab Kuchh Niyntran Mein Rakhnaa Pasnd Hai.",
        "Jab Chiijen Avyvsthit Yaa Aniyojit Hotii Hain To Main Ashj Mhsuus Kartaa Huun.",
        "Mujhe Suuchiyaan Banaanaa Aur Apne Kaaryon Par Nazar Rakhnaa Pasnd Hai.",
        "Main Hameshaa Apnaa Sarvshressth Pradrshn Karne Kaa Prayaas Kartaa Huun.",
        "Yah Mujhe Pareshaan Kartaa Hai Jab Any Log Apnii Pratibddhtaaon Ko Nahin Rakhte Hain.",
        "Mujhe Apne Kaaryon Aur Nirnyon Ke Liye Jimmedaar Honaa Pasnd Hai.",
        "Mujhe Mhtwakaankssii Lakshya Nirdhaarit Karnaa Aur Unhen Praaapt Karne Ke Liye Kadii Mehnt Karnaa Pasnd Hai."
    ],
    "Extraversion": [
        "Main Saamaajik Paristhitiyon Mein Shj Mhsuus Kartaa Huun Aur Mujhe Ne Logon Se Milnaa Pasnd Hai.",
        "Mujhe Dhyaan Kaa Kendr Bannaa Pasnd Hai.",
        "Mujhe Saarvjnik Ruup Se Bolnaa Aur Prastutiyaa Denaa Pasnd Hai.",
        "Main Saamaajik Sthitiyon Mein Oorjaawan Aur Utsaahit Mhsuus Kartaa Huun.",
        "Mujhe Doston Ke Saath Baahar Jaanaa Aur Sakriy Saamaajik Jiivn Pasnd Hai.",
        "Mujhe Ek Tiim Ke Ruup Mein Kaam Karnaa Aur Duusaron Ke Saath Shyog Karnaa Pasnd Hai.",
        "Mujhe Ek Smuuh Yaa Tiim Mein Netaa Bannaa Pasnd Hai.",
        "Mujhe Apnii Vyktigt Shaili Aur Upasthiti Ke Saath Dhyaan Aakarssit Karnaa Pasnd Hai.",
        "Main Ajnbiyon Se Baat Karne Mein Shj Mhsuus Kartaa Huun.",
        "Mujhe Saamaajik Kaarykramon Aur Smuuh Gatividhiyon Mein Bhaag Lenaa Pasnd Hai.",
        "Mujhe Logon Aur Showr Se Ghiraa Rhnaa Pasnd Hai.",
        "Jab Main Lnbe Samay Tak Akelaa Rhtaa Huun To Main Oob Yaa Bechaun Mhsuus Kartaa Huun."
    ],
    "Affability": [
        "Mujhe Any Logon Ki Bhaavnaaon Ki Parwah Hai.",
        "Mujhe Logon Ki Madad Karnaa Pasnd Hai Jab Unhen Bhaavnaatmk Smrthn Ki Aavshyktaa Hotii Hai.",
        "Main Mushkil Paristhitiyon Mein Duusaron Ko Dekhkar Ashj Mhsuus Kartaa Huun.",
        "Main Khud Ko Koee Ayesaa Vykti Maantaa Huun Jo Dyaalu Aur Shaanubhuutipuurn Hai.",
        "Mujhe Ek Tiim Ke Ruup Mein Kaam Karne Aur Lakshyaon Ko Praaapt Karne Ke Liye Duusaron Ke Saath Shyog Karne Mein Majaa Aataa Hai.",
        "Mujhe Duusaron Kaa Saamanaa Karnaa Pasnd Nahin Hai Aur Main Sangharsson Se Bchne Ki Koshish Kartaa Huun.",
        "Mujhe Duusaron Ke Liye Ehsaan Karnaa Aur Unki Dekhbhaal Karnaa Pasnd Hai.",
        "Mujhe Saamaajik Baatchiit Aur Ne Dost Banaane Mein Majaa Aataa Hai.",
        "Main Duusaron Ke Saath Achchhe Sanbndh Banaae Rakhne Kaa Prayaas Kartaa Huun.",
        "Main Duusaron Ki Bhalaaee Ki Parwah Kartaa Huun Aur Jitnaa Ho Sake Madad Karne Ki Koshish Kartaa Huun.",
        "Mujhe Duusaron Ko Slaah Aur Smrthn Denaa Pasnd Hai.",
        "mujhe apne praiyjnon ke saath samay bitaanaa aur unki dekhbhaal karnaa pasnd hai",
        "mujhe un chiijon ko karne mein majaa aataa hai jo duusaron ko khush karte hain."
    ],
    "Emotional Stability": [
        "Main Aasaanii Se Tnaavgrst Aur Chintit Mhsuus Kartaa Huun.",
        "Main Aksar Abhibhuut Mhsuus Kartaa Huun.",
        "Main Aksar Udaas Yaa Udaas Mhsuus Kartaa Huun.",
        "Mujhe Binaa Kisii Achchhe Kaaran Ke Dr Lga.",
        "Main Us Sthiti Ke Baare Mein Chintit Thaa Jismein Main Ghbaraa Saktaa Thaa Aur Khud Ko Bevkuuph Banaa Saktaa Thaa.",
        "Main Un Chiijon Ke Baare Mein Chintaa Kartaa Huun Jo Mere Niyntran Se Baahar Hain.",
        "Mere Liye Aaraam Karnaa Aur Samasyaon Ke Baare Mein Sochnaa Bnd Karnaa Mushkil Hai.",
        "Main Un Sthitiyon Ke Baare Mein Chintit Thaa Jinmein Main Ghbaraa Saktaa Thaa Aur Ghbaraa Saktaa Thaa Aur Khud Ko Muurkh Banaa Saktaa Thaa.",
        "Mujhe Is Baat Ki Bahut Chintaa Hai Ki Duusare Log Mere Baare Mein Kyaa Sochte Hain.",
        "Aalochnaa Aur Nkaaraatmk Tippniyaan Mujhe Sakaaraatmk Logon Se Adhik Prabhaavit Kartii Hain.",
        "Main Apne Kaushl Aur Kssmataaon Ke Baare Mein Asurkssit Mhsuus Kartaa Huun.",
        "Main Gltiyaa Karne Aur Jo Main Kartaa Huu Usmein Asphl Hone Se Drtaa Huu.",
        "Mujhe Lga Ki Mere Paas Aage Dekhne Ke Liye Kuchh Bhii Nahin Hai.",
        "Mujhe Lga Ki Jivn Kaa Arth Km Thaa."
    ]
}

answers = {}
current_question = 0

# user_name = ""
# user_age = ""
data={"user_name":None,"user_age":None}
# Questions and answers and other functions remain the same...

def accept_terms_and_conditions():
    def proceed():
        if var.get():
            terms_window.destroy()
            collect_name_and_age()
        else:
            messagebox.showwarning("Terms and Conditions", "Select the checkbox to continue.")

    terms_window = Tk()
    terms_window.title("Términos y Condiciones")
    terms_window.configure(bg="#f5f5f5")
    terms_window.attributes('-fullscreen', True)

    # Frame to contain the Text and Scrollbar
    frame = Frame(terms_window, bg="#f5f5f5")
    frame.pack(pady=20, padx=20, expand=True, fill="both")

    scrollbar = Scrollbar(frame)
    scrollbar.pack(side="right", fill="y")

    terms_display = Text(frame, wrap="word", yscrollcommand=scrollbar.set, font=("Helvetica", 10), height=20, width=80)
    terms_display.pack(side="left", expand=True, fill="both")

    # Insert formatted text
    #terms_display.tag_configure("title", font=("Arial", 18, "bold"))
    terms_display.tag_configure("title", font=("Georgia", 28, "bold"), foreground="ivory", background="darkslateblue")
    terms_display.tag_configure("bold", font=("Helvetica", 14, "bold"))
    terms_display.tag_configure("normal", font=("Helvetica", 14))

    terms_display.insert("1.0", "\n\n\t\t\t\t\t\t\t\t\t\t\t\tSWASTH\n\n\t\t\t\t\t\t\tPsychological Profiling App for Mental Health\n", "title")
    terms_display.insert("end", "\n\n1. Background/Problem Statement: ", "bold")
   
#change in roman 
    terms_display.insert("end", "Isakaa uddeshy sanjnaanaatmke vywahaarik aur bhaavnaatmk klyaan hai. sakaaraatmk maansik swasthy ek vykti ko apnii puurii kssmataa kaa ehsaas karnee svsth triike se jiivn ke tnaav kaa saamanaa karnee kaam par apnii utpaadktaa mein sudhaar karne aur apne smudaay aur smaaj ko wapas dene ki anumati detaa hai.\n\n", "normal")
    terms_display.insert("end", "2. Need: ", "bold")
    terms_display.insert("end", "Maansik swasthy ke muddon se juujh rahe sabhi vyktiyon ko aksar madad ke liye duusaron tak phunchne ki aavshyktaa ho saktii hai. jab kie phaisle kaa saamanaa karne ke dr ke kaarane ve aksar apne muddon ko botalabnd kar dete hain aur inkaar mein rhte hain jisse unkaa maansik swasthy aur bigd jaataa hai.\n\n", "normal")
    terms_display.insert("end", "3. Working: ", "bold")
    terms_display.insert("end", "Upyogkartaa vishisst prashnon ke saath bot ke saath chait karne mein sakssm hogae jisake liye bot nigraanii karega ki upyogkartaa kaise pratikriyaa de raha hai aur bhaavnaaon kaa pataa lgane ke upyog se shreniyon ke ek set ke aadhaar par aur eaaee ko yoge abhyaase praerk viidiyo ke viidiyo link pradaan karne ke liye upyogkartaa ko bdhaawa dene aur use vartmaan muud se apne maansik swasthy ko behtr banaane mein madad karne ke liye.\n\n", "normal")
    terms_display.insert("end", "4. Modules: ", "bold")
    terms_display.insert("end", "pranaali mein isake up.modyuul ke saath ek pramukh modyuul shaamil hai. upyogkartaa vyktigt vivran kaa upyog karke pnjiikarn kar saktaa haie naam aur umr kaa upyog karke apne vyktigt khaate mein lawgin kar saktaa hai aur chaitbot kaa upyog kar saktaa hai.\n\n", "normal")
    terms_display.insert("end", "5. Chatbot: ", "bold")
    terms_display.insert("end", "Chaitbot vyktiyon ki bhaavnaaon kaa pataa lganee paanch alag.alag shreniyon mein bhaavnaaon kaa vrgiikarn aur aatm muulyaankn ke liye ek sanklit report pradaan karne shit saamntii pradaan kartaa hai.\n\n", "normal")
    terms_display.insert("end", "6. Hardware Requirements: ", "bold")
    terms_display.insert("end", "MacOS Sierra and above, Windows 7 or higher with I3 processor system or higher and minimum 4GB RAM. \n\n", "normal")
    terms_display.insert("end", "7. Limitations: ", "bold")
    terms_display.insert("end", "Glt input sanklit report ko prabhaavit karenge. aapko shii vivran bharne ki slaah dii jaatii hai\n\n", "normal")
    terms_display.insert("end", "8. Application: ", "bold")
    terms_display.insert("end", " Is pranaali kaa upyog kisii bhii upyogkartaa dwaraa vibhinn prashnon ke liye 1-7 ke paimaane par apnii bhaavnaaon ko chihnit karne ke liye kiyaa jaa saktaa hai jo use apne tnaav str kaa vishlessn karne mein madad kar saktaa hai aur knpnii kamandr sanklit report ke aadhaar par mhtvpuurn kadam uthaa sakte hain jisse vykti ko apne maansik tnaav / sankt / avsaad ko door karne aur uski maansik bhalaaee aur smgr dksstaa bdhaane mein madad mil saktii hai\n\n", "normal")
    terms_display.insert("end", "9. Usage: ", "bold")
    terms_display.insert("end", "Aap pariikssn saajhaa kar sakte haine lekin aap isakaa vyaavsaayik upyog nahin kar sakte hain yaa vyutpnn kaary nahin kar sakte hain.\n\n", "normal")
    terms_display.insert("end", "10. Warning: ", "bold")
    terms_display.insert("end", "Ek sakriy maansik swasthy sankt ke maadhym se rhne wale vykti ;jhaan unke vichaar yaa vywahaar anishchit yaa bekaabuu lagte hainddh yaa aatmghaatii vichaaron kaa anubhv karne wale log is staindalon sv.shaaytaa SWASTH ayep ke liye sabse achchhe ummiidwar nahin ho sakte haine aur is sophtveyr kaa upyog peshevr madad ke viklp ke ruup mein nahin kiyaa jaanaa chaahie. ydi aap yaa aapkaa koee parichit sangharss kar raha haie to turnt maansik swasthy peshevr se madad lenaa mhtvpuurn hai.\n\n", "normal")
    terms_display.insert("end", "11. Note: ", "bold")
    terms_display.insert("end", "Yah pariyojnaa 2025 mein 39 maaunten diviijn signl rejimeint dwaraa viksit ki gayi hai aur yah staindalon mod mein kaam karegii.\n\n", "normal")
    terms_display.insert("end", "12. Updates: ", "bold")
    terms_display.insert("end", "Sophtveyr ke adytn hone yaa koee modyuul yaa kaarykssmataa jodne ke liye kripyaa 39 MDSR se sanpark karen. vartmaan modyuul mein yogdaan ke liye kripyaa yahaan mel karen  swaininegi@gmail.com\n\n", "normal")
    terms_display.insert("end", "13. Third parties: ", "bold")
    terms_display.insert("end", "Ye shrten tiisare pkss ke laabhaarthiyon ko adhikaar pradaan nahin kartii hain. kevl in shrton ke pkss hii in shrton ko laaguu kar sakte hain\n\n", "normal")
    terms_display.insert("end", "    Disclaimer: ", "bold")
    terms_display.insert("end", "39 emdiiesaar dwaraa pradaan kiyaa gayaa SWASTH aavedn kevl suuchnaatmk aur sv.muulyaankn uddeshyon ke liye hai. yah ek naidaanik upkarn nahin hai aur peshevr chikitsaa slaahe nidaan yaa upchaar ko pratisthaapit nahin kartaa hai. parinaamon kaa upyog chikitsaa nirny lene yaa kisii bhii upchaar yojnaa ko bdlne ke aadhaar ke ruup mein nahin kiyaa jaanaa chaahie. aapaat sthiti ke maamle meine apne kssetr mein ek laaisens praaapt maansik swasthy pradaataa yaa aapaatakaalin sewaon se sanpark karen. SWASTH eplikeshn aur isake nirmaataa prashnottrii parinaamon ke aadhaar par kie ge kisii bhii nirny ke liye jimmedaar nahin hain. is prashnottrii mein aapki bhaagiidaarii svaichchhik haie aur aage bdhkare aap sviikaar karte hain ki parinaam peshevr maansik swasthy muulyaankn kaa viklp nahin hain.\n\n", "normal")
    
    terms_display.insert("end", "    Terms and Conditions: \n\n", "bold")
    terms_display.insert("end", "1.  Acceptance of Terms: ", "bold")
    terms_display.insert("end", "SWASTH eplikeshn kaa upyog aur upyog karke aap in niymon aur shrton se baadhy hone ke liye shamt hain. ydi aap shamt nahin hain to aapko is sophtveyr kaa upyog nahin karnaa chaahie\n\n", "normal")
    terms_display.insert("end", "2.  Intended Use: ", "bold")
    terms_display.insert("end", "SWASTH  eplikeshn kevl saamaany suuchnaa ke uddeshyon ke liye dijaain kiyaa gayaa hai. Isakaa uddeshy kisii bhii maansik swasthy sthiti kaa nidaan upchaar yaa ilaaj karnaa nahin hai. upyogkartaaon ko kisii bhii chikitsaa yaa manovaijnaanik chintaaon ke liye ek yogy peshevr se paraamrsh karnaa chaahie.\n\n", "normal")
    terms_display.insert("end", "3.  Privacy & Data Collection: ", "bold")
    terms_display.insert("end", "SWASTH upyogkartaa anubhv ko bdhaane aur sewaon mein sudhaar karne ke liye anaam detaa ektr kar saktaa hai. ham aapki shamti ke binaa tiisare pkss ke saath vyktigt jaankaarii saajhaa nahin karte hain siway jab kanoondwaraa aavshyk ho. ham detaa kaise ektr aur upyog karte hain isake vivran ke liye kripyaa hamaarii gopniiytaa niiti dekhen\n\n", "normal")
    terms_display.insert("end", "4.  No Liability: ", "bold")
    terms_display.insert("end", "SWASTH prashnottrii parinaamon ki stiiktaa yaa vishvsniiytaa ki garntii nahin detaa hai. ham kisii bhii bhaavnaatmk sankte glt vyaakhyaae yaa prashnottrii parinaamon ke aadhaar par ki gayi kaarrwaiyon ke liye jimmedaar nahin hain. upyogkartaa is sophtveyr ke upyog ke liye puurii zimmedari lete hain.\n\n", "normal")
    terms_display.insert("end", "5.  Modifications: ", "bold")
    terms_display.insert("end", "SWASTH kisii bhii samay in shrton ko apadet karne kaa adhikaar surkssit rakhtaa hai. parivartnon ke baad sophtveyr kaa nirntr upyog nayi shrton ki sviikriti ko ingit kartaa hai.\n\n", "normal")
    terms_display.insert("end", "6.  Contact Information: ", "bold")
    terms_display.insert("end", "In shrton ke baare mein kisii bhii prashn ke liye kripyaa hamse swaininegi@gmail.com par sanpark karen\n\n", "normal")
    
    
    terms_display.insert("end", "Is upkarn kaa upyog karkee upyogkartaa in niymon aur shrton aur upkarn ke upyog se sanbndhit kisii bhii any notis yaa pratibndh se baadhy hone ke liye shamt hotaa hai.\n", "bold")
    terms_display.insert("end", "Developer Details: ", "bold")
    terms_display.insert("end", "Capt Swaini Negi, 39 MDSR\n\n", "bold")
 
#end changes
 
    terms_display.configure(state="disabled")
    scrollbar.config(command=terms_display.yview)

    var = IntVar()
    check_button = Checkbutton(terms_window, text="I have understood the requirements and usage of SWASTH app", variable=var, bg="#f5f5f5", font=("Helvetica", 10))
    check_button.pack(pady=10)

    Button(terms_window, text="Proceed", command=proceed, bg="#4caf50", fg="white", relief="flat", font=("Helvetica", 10)).pack(pady=10)

    terms_window.mainloop()


# Window to store name and age
def collect_name_and_age():
    def submit():
        global user_name, user_age
        global data
        user_name = name_entry.get().strip()  # Eliminar espacios en blanco al principio y al final
        user_age = age_entry.get().strip()
        data={"user_name":user_name,"user_age":user_age}

        # Validate that the fields are not empty
        if not user_name or not user_age:
            messagebox.showwarning("Missing information", "Please fill out all fields before continuing.")
            return

        # Validate that age is a number
        if not user_age.isdigit():
            messagebox.showwarning("Invalid age", "Please enter a valid age (numbers only).")
            return

        user_info_window.destroy()

    user_info_window = Tk()
    user_info_window.title("Enter your Name and Age")
    user_info_window.configure(bg="#f5f5f5")
    
    # Full screen mode
    user_info_window.attributes('-fullscreen', True)

    # Central frame to group elements and center them
    center_frame = Frame(user_info_window, bg="#f5f5f5")
    center_frame.place(relx=0.5, rely=0.5, anchor="center")

    title_label = Label(center_frame, text="Basic Information: Identify yourself", bg="#f5f5f5", font=("Arial", 20, "bold"))
    title_label.pack(pady=30)

    name_frame = Frame(center_frame, bg="#f5f5f5")
    name_frame.pack(pady=15, fill="x")
    name_label = Label(name_frame, text="           Name:", bg="#f5f5f5", font=("Arial", 14), width=14)
    name_label.grid(row=0, column=0, padx=(0, 20))
    name_entry = Entry(name_frame, font=("Arial", 12), width=40)
    name_entry.grid(row=0, column=1, padx=(20, 0))

    age_frame = Frame(center_frame, bg="#f5f5f5")
    age_frame.pack(pady=15, fill="x")
    age_label = Label(age_frame, text="           Age:", bg="#f5f5f5", font=("Arial", 14), width=14)
    age_label.grid(row=0, column=0, padx=(0, 20))
    age_entry = Entry(age_frame, font=("Arial", 12), width=40)
    age_entry.grid(row=0, column=1, padx=(20, 0))

    submit_button = Button(center_frame, text="Submit", command=submit, bg="#4caf50", fg="white", relief="flat", font=("Arial", 14, "bold"), width=20)
    submit_button.pack(pady=40)

    user_info_window.mainloop()


def next_question():
    save_answer()
    global current_question
    total_questions = sum(len(v) for v in questions.values())
    if current_question < total_questions - 1:  # Make sure we don't exceed the total number of questions
        category_index = current_question // 12
        category = list(questions.keys())[category_index]
        question = questions[category][current_question % 12]
        question_label.config(text=question)
        current_question += 1
    else:
        messagebox.showinfo("SWASTH", "You have completed all the questions! Press FINISH/ RESTART")

def confirm_exit():
    response = messagebox.askyesno("Confirm exit", "Are you sure you want to close the program?")
    if response:
        summary_window.destroy()  # Close the summary window
        root.destroy()  # Close the main window

def save_as_pdf():
    generate_graph()  # First generate the graph and save it as an image
    summary_text = "Summary of your answers:\n\n"
    for category, scores in answers.items():
        avg_score = sum(scores) / len(scores)
        summary_text += f"{category}: {avg_score:.2f}/7\n"
    generate_pdf_with_summary(summary_text)  # Then generate the PDF with the summary and the graph image
    generate_pdf_overall_summary(summary_text) # overall summary

def save_answer():
    global current_question, answers
    category_index = current_question // 12
    if category_index >= len(questions):  # Make sure we don't exceed the number of categories
        return
    category = list(questions.keys())[category_index]
    answer = scale.get()
    if category not in answers:
        answers[category] = []
    answers[category].append(answer)


def generate_summary():
    global summary_window
    summary_window = Tk()
    summary_text = f"SWASTH: Report: Name: {data["user_name"]}\nAge: {data["user_age"]}"
    summary_window.title("SWASTH: Report")
    
    # Calculate the summary (average of responses for each category)
    summary_text = f"Summary of your answers:Name: {data["user_name"]}\nAge: {data["user_age"]}"
    for category, scores in answers.items():
        avg_score = sum(scores) / len(scores)
        summary_text += f"{category}: {avg_score:.2f}/7\n"
    print("In generate summary:",data["user_name"],data["user_age"])
    Label(summary_window, text=summary_text, font=("Arial", 12)).pack(pady=20)
    
    Button(summary_window, text="Save as PDF", command=save_as_pdf).pack(pady=10)
    Button(summary_window, text="Close", command=confirm_exit).pack(pady=10)

def get_openai_summary(answers):
    # Convert responses to text
    # text = "\n".join([f"{cat}: {sum(answers[cat]) / len(answers[cat])}" for cat in answers])

    # # Ask OpenAI for a detailed analysis 
    # prompt_text = f"""
    # Based on the following Personality Test results, it provides a detailed analysis to help the recruiter understand the candidate's characteristics:
    # {text}
    # """

    # messages = [{"role": "system", "content": "You are analyzing results from a Personality Test."},
    #             {"role": "user", "content": prompt_text}]
    
    # response = openai.ChatCompletion.create(
    #   model="gpt-3.5-turbo",
    #   messages=messages
    # )

    # #The model's response will be in the last message sent by "assistant"
    # return response.choices[0].message['content'].strip()


    text = "\n".join([f"{cat}: {sum(answers[cat]) / len(answers[cat]):.2f}" for cat in answers])

    # Ask OpenAI for a detailed analysis
    prompt_text = f"""
    Based on the following Personality Test results, provide a detailed analysis to help the recruiter understand the candidate's characteristics:
    
    {text}
    """

    messages = [
        {"role": "system", "content": "You are analyzing results from a Personality Test."},
        {"role": "user", "content": prompt_text}
    ]
    
    try:
        client = openai.OpenAI()  # ✅ Corrected: Use the new OpenAI client
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        # ✅ Corrected: Extract response using new API format
        return response.choices[0].message.content.strip()

    except openai.OpenAIError as e:
        return f"Error: {str(e)}"

class MyPDF(FPDF):
    def header(self):
        # background image path
        background_image = "media/background.png"

        # Get the dimensions of the image (in mm)
        image_width, image_height = self.get_image_dimensions(background_image)

        # Calculate x and y coordinates to center the image
        x_centered = (self.w - image_width) * 0.5
        y_centered = (self.h - image_height) * 0.5

        # Add background image on each page, centered
        self.image(background_image, x=x_centered, y=y_centered, w=image_width)

    def get_image_dimensions(self, image_path):
        # Use the PIL library to obtain the image dimensions in pixels
        with Image.open(image_path) as img:
            width_px, height_px = img.size

        # Convert pixel dimensions to millimeters (assuming 96 DPI)
        width_mm = width_px * 25.4 / 96
        height_mm = height_px * 25.4 / 96

        return width_mm, height_mm

def generate_pdf_with_summary(summary):
    pdf = MyPDF()
    pdf.add_page()

    pdf.set_font("Arial", 'B', size=16)  # Bold font and size 16

    # PDF Title
    pdf.cell(0, 10, "Analysis of the Personality Test", ln=True, align="C")

    # Write name and age on PDF
    pdf.set_font("Arial", size=12)  # Write name and age on PDF
    pdf.cell(0, 10, f"Name: {user_name}", ln=True)
    pdf.cell(0, 10, f"Age: {user_age}", ln=True)
    # Get the current date and time
    current_date_time = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
    pdf.cell(0, 10, f"Date and Time: {current_date_time}", ln=True)  # Add to PDF
    pdf.ln(10)

    # Get OpenAI analysis


    # openai_analysis = get_openai_summary(answers)
    # pdf.multi_cell(0, 10, openai_analysis)

    # Add the chart image
    image_path = "personalidad.png"  # Chart Image Path
    pdf.image(image_path, x=10, y=None, w=190)  # Adjust the size (w) according to your needs

    # Guardar el PDF
    filename = "analisis_test_personalidad.pdf"
    pdf.output(filename)
    messagebox.showinfo("Analysis generated", f"The analysis has been saved as  {filename}")
    
    
    
def generate_pdf_overall_summary(summary):
    pdf = MyPDF()
    pdf.add_page()

    pdf.set_font("Arial", 'B', size=16)  # Bold font and size 16

    # PDF Title
    pdf.cell(0, 10, "Analysis of the Personality Test", ln=True, align="C")

    # Write name and age on PDF
    #pdf.set_font("Arial", size=12)  # Write name and age on PDF
    #pdf.cell(0, 10, f"Name: {user_name}", ln=True)
    #pdf.cell(0, 10, f"Age: {user_age}", ln=True)
    # Get the current date and time
    current_date_time = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
    pdf.cell(0, 10, f"Date and Time: {current_date_time}", ln=True)  # Add to PDF
    pdf.ln(10)

    # Get OpenAI analysis


    # openai_analysis = get_openai_summary(answers)
    # pdf.multi_cell(0, 10, openai_analysis)

    # Add the chart image
    image_path = "personalidad.png"  # Chart Image Path
    pdf.image(image_path, x=10, y=None, w=190)  # Adjust the size (w) according to your needs

    # Guardar el PDF
    filename = "compiledreport.pdf"
    pdf.output(filename)
    messagebox.showinfo("Analysis generated", f"The analysis has been saved as  {filename}")


def generate_graph():
    labels = [cat for cat in questions.keys() if cat in answers]
    scores = [sum(answers[cat]) / len(answers[cat]) for cat in labels]
    num_vars = len(labels)
    
    # Radar Chart Settings
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    scores += scores[:1]  # Add the first score at the end to close the circle
    angles += angles[:1]  # Add the first angle to the end to close the circle

    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
    
    # Custom colors
    fill_color = '#2899c0'
    line_color = '#ca4124'
    label_color = '#c09660'
    
    # Main chart
    ax.fill(angles, scores, color=fill_color, alpha=0.6)  # Fill color
    ax.plot(angles, scores, color=line_color, linewidth=3)  # Color de la línea
    
    # Label and Title Settings
    ax.set_yticks(range(1, 8))
    ax.set_yticklabels(range(1, 8), fontsize=12, color=label_color)  # Scoring Label Color
    ax.set_xticks(angles[:-1])  # We exclude the last angle which is the repeated one
    ax.set_xticklabels(labels, fontsize=14, fontweight='bold', color=label_color)  # Color de las etiquetas de categoría
    
    # Añadir líneas de cuadrícula y configurar el fondo
    ax.grid(color='grey', linestyle='--', linewidth=0.5, alpha=0.6)
    ax.set_facecolor('whitesmoke')  # Color de fondo del gráfico
    #summary_text = f"SWASTH: Report: Name: {data["user_name"]}\nAge: {data["user_age"]}"
    summary_text = f"SWASTH Report"
    # Establecer el título
    ax.set_title(summary_text, size=20, y=1.1, color=line_color, fontweight='bold')  # Color y tamaño del título
    
    plt.tight_layout()
    
    # Guardar la imagen del gráfico
    image_path = "personalidad.png"
    fig.savefig(image_path, dpi=300, bbox_inches='tight')  # Aumentar la resolución y ajustar el tamaño

def update_progressbar():
    total_questions = sum(len(v) for v in questions.values())
    percentage_complete = (current_question / total_questions) * 100
    progress_bar['value'] = percentage_complete

def reset_test():
    # Ventana emergente de confirmación
    response = messagebox.askyesno("Confirm restart", "Are you sure you want to restart the test?")
    if not response:
        return  # Si el usuario selecciona 'No', no haremos nada y saldremos de la función

    global answers, current_question
    answers = {}  # Reiniciar las respuestas
    current_question = 0  # Reiniciar el contador de preguntas
    question_label.config(text="Press Next to start the test.")  # Reiniciar el texto de la etiqueta de pregunta
    scale.set(0)  # Reiniciar la escala

# Recopilar nombre y edad antes de comenzar el test
accept_terms_and_conditions()

# Ventana principal
root = Tk()
root.title("Personality test")
root.attributes('-fullscreen', True)
root.configure(bg="#f5f5f5")

# Cargar y ajustar la única imagen que se usará
original_image = Image.open("media/front.png")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
resized_image = original_image.resize((screen_width, screen_height), Image.LANCZOS)
front_image = ImageTk.PhotoImage(resized_image)

# Marco centrado
center_frame = Frame(root, bg="#f5f5f5")
center_frame.place(relx=0.5, rely=0.5, anchor='center')

question_label = Label(center_frame, text="Press Next to start the test.", bg="#f5f5f5", font=("Helvetica", 14), fg="#333333")
question_label.pack(pady=20)

# Fondo de la ventana (único layer)
front_label = Label(root, image=front_image, bg="#f5f5f5")
front_label.place(relx=0.5, rely=0.5, anchor='center')
front_label.lower()  # Enviar la etiqueta al fondo

# Escala y etiquetas
scale_frame = Frame(center_frame, bg="#f5f5f5")
scale_frame.pack(pady=10)

left_reference_label = Label(scale_frame, text="I don't identify myself", bg="#f5f5f5", font=("Helvetica", 10), fg="#555555")
left_reference_label.pack(side="left", padx=5)

scale = Scale(scale_frame, from_=1, to=7, orient="horizontal", bg="#e0e0e0", sliderlength=30, width=15, highlightthickness=0)
scale.pack(side="left", pady=20)

right_reference_label = Label(scale_frame, text="I totally identify", bg="#f5f5f5", font=("Helvetica", 10), fg="#555555")
right_reference_label.pack(side="left", padx=5)

# Botones
button_frame = Frame(center_frame, bg="#f5f5f5")
button_frame.pack(pady=10)

next_button = Button(button_frame, text="Next", command=lambda: [next_question(), update_progressbar()], bg="#4caf50", fg="white", relief="flat", font=("Helvetica", 10))
next_button.pack(side="left", padx=5)

finish_button = Button(button_frame, text="Finish", command=generate_summary, bg="#ff5722", fg="white", relief="flat", font=("Helvetica", 10))
finish_button.pack(side="left", padx=5)

reset_button = Button(button_frame, text="Restart", command=lambda: [reset_test(), update_progressbar()], bg="#607d8b", fg="white", relief="flat", font=("Helvetica", 10))
reset_button.pack(side="left", padx=5)

# Barra de progreso
progress_bar = ttk.Progressbar(center_frame, orient="horizontal", length=600, mode="determinate", style="TProgressbar")
progress_bar.pack(pady=20)

root.mainloop()

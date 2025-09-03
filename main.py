from flask import Flask, render_template, request

app = Flask(__name__)

# Helper to convert list of (title, link) to list of dicts
def to_dict_list(tuples):
    return [{"title": title, "link": link} for title, link in tuples]

# Full books dictionary with 15 suggestions per option, and extended language and author categories
books = {
    "age": {
        "10-15":
        to_dict_list([
            ("Harry Potter", "https://www.goodreads.com/book/show/3.Harry_Potter"),
            ("Percy Jackson", "https://www.goodreads.com/book/show/123675190-the-lightning-thief?ac=1&from_search=true&qid=nP58INHDXo&rank=1"),
            ("Charlotte's Web", "https://www.goodreads.com/book/show/24178.Charlotte_s_Web"),
            ("Wonder", "https://www.goodreads.com/book/show/11387515-wonder"),
            ("Diary of a Wimpy Kid", "https://www.goodreads.com/book/show/389627.Diary_of_a_Wimpy_Kid"),
            ("The Tale of Despereaux", "https://www.goodreads.com/book/show/37190.The_Tale_of_Despereaux"),
            ("The Giver", "https://www.goodreads.com/book/show/3636.The_Giver"),
            ("Coraline", "https://www.goodreads.com/book/show/17061.Coraline"),
            ("Holes", "https://www.goodreads.com/book/show/38709.Holes"),
            ("The Lightning Thief", "https://www.goodreads.com/book/show/28187.The_Lightning_Thief")
        ]),
        "16-25": to_dict_list([
            ("The Hunger Games", "https://www.goodreads.com/book/show/2767052"),
            ("The Fault in Our Stars", "https://www.goodreads.com/book/show/11870085"),
            ("Eleanor & Park", "https://www.goodreads.com/book/show/15745753-eleanor-park"),
            ("Looking for Alaska", "https://www.goodreads.com/book/show/99561.Looking_for_Alaska"),
            ("Red Queen", "https://www.goodreads.com/book/show/22328546-red-queen"),
            ("To All the Boys I’ve Loved Before", "https://www.goodreads.com/book/show/15749186-to-all-the-boys-i-ve-loved-before"),
            ("Paper Towns", "https://www.goodreads.com/book/show/6442769-paper-towns"),
            ("They Both Die at the End", "https://www.goodreads.com/book/show/33385229-they-both-die-at-the-end"),
            ("Legend", "https://www.goodreads.com/book/show/9275658-legend"),
            ("Divergent", "https://www.goodreads.com/book/show/13335037-divergent")
        ]),
        "26-40": to_dict_list([
            ("Atomic Habits", "https://www.goodreads.com/book/show/40121378"),
            ("The Silent Patient", "https://www.goodreads.com/book/show/40097951-the-silent-patient"),
            ("Educated", "https://www.goodreads.com/book/show/35133922-educated"),
            ("The Midnight Library", "https://www.goodreads.com/book/show/52578297-the-midnight-library"),
            ("The Subtle Art of Not Giving a F*ck", "https://www.goodreads.com/book/show/28257707"),
            ("The Alchemist", "https://www.goodreads.com/book/show/865"),
            ("The Book Thief", "https://www.goodreads.com/book/show/19063.The_Book_Thief"),
            ("Where the Crawdads Sing", "https://www.goodreads.com/book/show/36809135-where-the-crawdads-sing"),
            ("Verity", "https://www.goodreads.com/book/show/59344312-verity"),
            ("The Four Agreements", "https://www.goodreads.com/book/show/6596.The_Four_Agreements")
        ]),
        "40+": to_dict_list([
            ("The Alchemist", "https://www.goodreads.com/book/show/865"),
            ("Becoming", "https://www.goodreads.com/book/show/38746485"),
            ("Tuesdays with Morrie", "https://www.goodreads.com/book/show/6900.Tuesdays_with_Morrie"),
            ("The Kite Runner", "https://www.goodreads.com/book/show/77203.The_Kite_Runner"),
            ("A Man Called Ove", "https://www.goodreads.com/book/show/18774964-a-man-called-ove"),
            ("Educated", "https://www.goodreads.com/book/show/35133922-educated"),
            ("Sapiens", "https://www.goodreads.com/book/show/23692271-sapiens"),
            ("The Power of Now", "https://www.goodreads.com/book/show/6708.The_Power_of_Now"),
            ("The Art of Happiness", "https://www.goodreads.com/book/show/38210.The_Art_of_Happiness"),
            ("Stillness Is the Key", "https://www.goodreads.com/book/show/44525305-stillness-is-the-key")
        ])
    },
    "genre": {
        "fantasy": to_dict_list([
            ("Harry Potter", "https://www.goodreads.com/book/show/3.Harry_Potter"),
            ("The Hobbit", "https://www.goodreads.com/book/show/5907.The_Hobbit"),
            ("The Name of the Wind", "https://www.goodreads.com/book/show/186074.The_Name_of_the_Wind"),
            ("Mistborn", "https://www.goodreads.com/book/show/68428.Mistborn"),
            ("Throne of Glass", "https://www.goodreads.com/book/show/7896527-throne-of-glass"),
            ("Eragon", "https://www.goodreads.com/book/show/113436.Eragon"),
            ("The Cruel Prince", "https://www.goodreads.com/book/show/26032825-the-cruel-prince"),
            ("A Court of Thorns and Roses", "https://www.goodreads.com/book/show/16096824-a-court-of-thorns-and-roses"),
            ("Six of Crows", "https://www.goodreads.com/book/show/23437156-six-of-crows"),
            ("Shadow and Bone", "https://www.goodreads.com/book/show/10194157-shadow-and-bone")
        ]),
        "mystery": to_dict_list([
            ("Gone Girl", "https://www.goodreads.com/book/show/19288043-gone-girl"),
            ("The Girl with the Dragon Tattoo", "https://www.goodreads.com/book/show/2429135.The_Girl_with_the_Dragon_Tattoo"),
            ("Big Little Lies", "https://www.goodreads.com/book/show/19486412-big-little-lies"),
            ("The Silent Patient", "https://www.goodreads.com/book/show/40097951-the-silent-patient"),
            ("The Da Vinci Code", "https://www.goodreads.com/book/show/968.The_Da_Vinci_Code"),
            ("Before I Go to Sleep", "https://www.goodreads.com/book/show/9736930-before-i-go-to-sleep"),
            ("In the Woods", "https://www.goodreads.com/book/show/237209.In_the_Woods"),
            ("The Couple Next Door", "https://www.goodreads.com/book/show/28815474-the-couple-next-door"),
            ("Behind Closed Doors", "https://www.goodreads.com/book/show/29437949-behind-closed-doors"),
            ("Sharp Objects", "https://www.goodreads.com/book/show/66559.Sharp_Objects")
        ]),
        "romance": to_dict_list([
            ("Pride and Prejudice", "https://www.goodreads.com/book/show/1885.Pride_and_Prejudice"),
            ("Me Before You", "https://www.goodreads.com/book/show/17347634-me-before-you"),
            ("The Notebook", "https://www.goodreads.com/book/show/15931.The_Notebook"),
            ("It Ends with Us", "https://www.goodreads.com/book/show/27362503-it-ends-with-us"),
            ("The Fault in Our Stars", "https://www.goodreads.com/book/show/11870085-the-fault-in-our-stars"),
            ("Twilight", "https://www.goodreads.com/book/show/41865.Twilight"),
            ("The Kiss Quotient", "https://www.goodreads.com/book/show/36199084-the-kiss-quotient"),
            ("The Hating Game", "https://www.goodreads.com/book/show/25883848-the-hating-game"),
            ("Beach Read", "https://www.goodreads.com/book/show/52867387-beach-read"),
            ("Red, White & Royal Blue", "https://www.goodreads.com/book/show/41150487-red-white-royal-blue")
        ]),
        "science fiction": to_dict_list([
            ("Dune", "https://www.goodreads.com/book/show/44767458-dune"),
            ("Ender's Game", "https://www.goodreads.com/book/show/375802.Ender_s_Game"),
            ("Neuromancer", "https://www.goodreads.com/book/show/22328.Neuromancer"),
            ("The Martian", "https://www.goodreads.com/book/show/18007564-the-martian"),
            ("Fahrenheit 451", "https://www.goodreads.com/book/show/13079982-fahrenheit-451"),
            ("Ready Player One", "https://www.goodreads.com/book/show/9969571-ready-player-one"),
            ("The Hunger Games", "https://www.goodreads.com/book/show/2767052-the-hunger-games"),
            ("Snow Crash", "https://www.goodreads.com/book/show/830.Snow_Crash"),
            ("Project Hail Mary", "https://www.goodreads.com/book/show/54493401-project-hail-mary"),
            ("Cinder", "https://www.goodreads.com/book/show/11235712-cinder")
        ]),
        "horror": to_dict_list([
            ("It", "https://www.goodreads.com/book/show/830502.It"),
            ("The Shining", "https://www.goodreads.com/book/show/11588.The_Shining"),
            ("Bird Box", "https://www.goodreads.com/book/show/18498558-bird-box"),
            ("The Haunting of Hill House", "https://www.goodreads.com/book/show/89717.The_Haunting_of_Hill_House"),
            ("Pet Sematary", "https://www.goodreads.com/book/show/30701802-pet-sematary"),
            ("Mexican Gothic", "https://www.goodreads.com/book/show/53152636-mexican-gothic"),
            ("The Exorcist", "https://www.goodreads.com/book/show/323361.The_Exorcist"),
            ("Misery", "https://www.goodreads.com/book/show/10614.Misery"),
            ("Home Before Dark", "https://www.goodreads.com/book/show/50833559-home-before-dark"),
            ("The Only Good Indians", "https://www.goodreads.com/book/show/52180399-the-only-good-indians")
        ]),
        "biography": to_dict_list([
            ("The Diary of a Young Girl", "https://www.goodreads.com/book/show/48855.The_Diary_of_a_Young_Girl"),
            ("Steve Jobs", "https://www.goodreads.com/book/show/11084145-steve-jobs"),
            ("Becoming", "https://www.goodreads.com/book/show/38746485-becoming"),
            ("Long Walk to Freedom", "https://www.goodreads.com/book/show/318431.Long_Walk_to_Freedom"),
            ("Educated", "https://www.goodreads.com/book/show/35133922-educated"),
            ("I Am Malala", "https://www.goodreads.com/book/show/17851885-i-am-malala"),
            ("Bossypants", "https://www.goodreads.com/book/show/9418327-bossypants"),
            ("When Breath Becomes Air", "https://www.goodreads.com/book/show/25899336-when-breath-becomes-air"),
            ("Alexander Hamilton", "https://www.goodreads.com/book/show/16130.Alexander_Hamilton"),
            ("The Wright Brothers", "https://www.goodreads.com/book/show/22609391-the-wright-brothers")
        ]),
        "historical fiction": to_dict_list([
            ("The Book Thief", "https://www.goodreads.com/book/show/19063.The_Book_Thief"),
            ("All the Light We Cannot See", "https://www.goodreads.com/book/show/18143977-all-the-light-we-cannot-see"),
            ("The Nightingale", "https://www.goodreads.com/book/show/21853621-the-nightingale"),
            ("The Tattooist of Auschwitz", "https://www.goodreads.com/book/show/38359036-the-tattooist-of-auschwitz"),
            ("Beneath a Scarlet Sky", "https://www.goodreads.com/book/show/32487617-beneath-a-scarlet-sky"),
            ("The Help", "https://www.goodreads.com/book/show/466702.The_Help"),
            ("The Guernsey Literary and Potato Peel Pie Society", "https://www.goodreads.com/book/show/13636.The_Guernsey_Literary_and_Potato_Peel_Pie_Society"),
            ("Water for Elephants", "https://www.goodreads.com/book/show/43624.Water_for_Elephants"),
            ("The Pillars of the Earth", "https://www.goodreads.com/book/show/5043.The_Pillars_of_the_Earth"),
            ("Atonement", "https://www.goodreads.com/book/show/7305.Atonement")
        ]),
        "non-fiction": to_dict_list([
            ("Sapiens", "https://www.goodreads.com/book/show/23692271-sapiens"),
            ("Educated", "https://www.goodreads.com/book/show/35133922-educated"),
            ("Becoming", "https://www.goodreads.com/book/show/38746485-becoming"),
            ("The Immortal Life of Henrietta Lacks", "https://www.goodreads.com/book/show/6493208-the-immortal-life-of-henrietta-lacks"),
            ("Unbroken", "https://www.goodreads.com/book/show/8664359-unbroken"),
            ("The Wright Brothers", "https://www.goodreads.com/book/show/22609391-the-wright-brothers"),
            ("Into the Wild", "https://www.goodreads.com/book/show/1845.Into_the_Wild"),
            ("Born a Crime", "https://www.goodreads.com/book/show/29780253-born-a-crime"),
            ("Quiet", "https://www.goodreads.com/book/show/8520610-quiet"),
            ("The Power of Habit", "https://www.goodreads.com/book/show/12609433-the-power-of-habit")
        ]),
        "thriller": to_dict_list([
            ("The Girl on the Train", "https://www.goodreads.com/book/show/22557272-the-girl-on-the-train"),
            ("The Da Vinci Code", "https://www.goodreads.com/book/show/968.The_Da_Vinci_Code"),
            ("Gone Girl", "https://www.goodreads.com/book/show/19288043-gone-girl"),
            ("The Silent Patient", "https://www.goodreads.com/book/show/40097951-the-silent-patient"),
            ("Shutter Island", "https://www.goodreads.com/book/show/184603.Shutter_Island"),
            ("Before I Go to Sleep", "https://www.goodreads.com/book/show/9736930-before-i-go-to-sleep"),
            ("Dark Places", "https://www.goodreads.com/book/show/12397845-dark-places"),
            ("The Reversal", "https://www.goodreads.com/book/show/7751338-the-reversal"),
            ("The Woman in the Window", "https://www.goodreads.com/book/show/25489010-the-woman-in-the-window"),
            ("I Am Watching You", "https://www.goodreads.com/book/show/28278712-i-am-watching-you")
        ]),
        "popularity": to_dict_list([
            ("Where the Crawdads Sing", "https://www.goodreads.com/book/show/36809135-where-the-crawdads-sing"),
            ("The Midnight Library", "https://www.goodreads.com/book/show/52578297-the-midnight-library"),
            ("The Vanishing Half", "https://www.goodreads.com/book/show/51791252-the-vanishing-half"),
            ("Circe", "https://www.goodreads.com/book/show/36809180-circe"),
            ("Normal People", "https://www.goodreads.com/book/show/41057279-normal-people"),
            ("Anxious People", "https://www.goodreads.com/book/show/39921296-anxious-people"),
            ("Little Fires Everywhere", "https://www.goodreads.com/book/show/34273292-little-fires-everywhere"),
            ("The Night Circus", "https://www.goodreads.com/book/show/9361589-the-night-circus"),
            ("Educated", "https://www.goodreads.com/book/show/35133922-educated"),
            ("The Song of Achilles", "https://www.goodreads.com/book/show/11554013-the-song-of-achilles")
        ]),
        "self-help": to_dict_list([
            ("The Power of Now", "https://www.goodreads.com/book/show/6708.The_Power_of_Now"),
            ("Atomic Habits", "https://www.goodreads.com/book/show/40121378-atomic-habits"),
            ("The Subtle Art of Not Giving a F*ck", "https://www.goodreads.com/book/show/28257707-the-subtle-art-of-not-giving-a-f-ck"),
            ("How to Win Friends and Influence People", "https://www.goodreads.com/book/show/4865.How_to_Win_Friends_and_Influence_People"),
            ("You Are a Badass", "https://www.goodreads.com/book/show/12722928-you-are-a-badass"),
            ("Think and Grow Rich", "https://www.goodreads.com/book/show/30186948-think-and-grow-rich"),
            ("The Four Agreements", "https://www.goodreads.com/book/show/6596.The_Four_Agreements"),
            ("Mindset", "https://www.goodreads.com/book/show/40745.Mindset"),
            ("Can't Hurt Me", "https://www.goodreads.com/book/show/40297953-can-t-hurt-me"),
            ("Dare to Lead", "https://www.goodreads.com/book/show/33590271-dare-to-lead")
        ]),
        "comedy": to_dict_list([
            ("Bossypants", "https://www.goodreads.com/book/show/9418327-bossypants"),
            ("Good Omens", "https://www.goodreads.com/book/show/12067.Good_Omens"),
            ("The Hitchhiker's Guide to the Galaxy", "https://www.goodreads.com/book/show/386162.The_Hitchhiker_s_Guide_to_the_Galaxy"),
            ("Yes Please", "https://www.goodreads.com/book/show/20910157-yes-please?from_search=true&from_srp=true&qid=jPID4bWGZF&rank=1"),
            ("Catch-22", "https://www.goodreads.com/book/show/168668.Catch_22"),
            ("Is Everyone Hanging Out Without Me?", "https://www.goodreads.com/book/show/10335308-is-everyone-hanging-out-without-me?ref=nav_sb_ss_2_8"),
            ("Hyperbole and a Half", "https://www.goodreads.com/book/show/17571564-hyperbole-and-a-half?ref=nav_sb_ss_1_10"),
            ("The Rosie Project", "https://www.goodreads.com/book/show/16181775-the-rosie-project?ref=nav_sb_ss_1_17"),
            ("Me Talk Pretty One Day", "https://www.goodreads.com/book/show/4137.Me_Talk_Pretty_One_Day?ref=nav_sb_noss_l_11"),
            ("Lamb: The Gospel According to Biff, Christ's Childhood Pal", "https://www.goodreads.com/book/show/28881.Lamb?ref=nav_sb_ss_2_9")
        ]),
        "classics": to_dict_list([
            ("To Kill a Mockingbird", "https://www.goodreads.com/book/show/2657.To_Kill_a_Mockingbird"),
            ("Pride and Prejudice", "https://www.goodreads.com/book/show/1885.Pride_and_Prejudice"),
            ("The Great Gatsby", "https://www.goodreads.com/book/show/4671.The_Great_Gatsby"),
            ("1984", "https://www.goodreads.com/book/show/5470.1984"),
            ("Moby Dick", "https://www.goodreads.com/book/show/153747.Moby_Dick_or_the_Whale"),
            ("Jane Eyre", "https://www.goodreads.com/book/show/10210.Jane_Eyre"),
            ("Wuthering Heights", "https://www.goodreads.com/book/show/6185.Wuthering_Heights"),
            ("The Catcher in the Rye", "https://www.goodreads.com/book/show/5107.The_Catcher_in_the_Rye"),
            ("Little Women", "https://www.goodreads.com/book/show/1934.Little_Women"),
            ("Frankenstein", "https://www.goodreads.com/book/show/18490.Frankenstein")
        ]),
    },
    "mood": {
        "happy": to_dict_list([
            ("The Rosie Project by Graeme Simsion", "https://www.goodreads.com/book/show/16181775-the-rosie-project"),
            ("Eleanor Oliphant Is Completely Fine by Gail Honeyman", "https://www.goodreads.com/book/show/31434883-eleanor-oliphant-is-completely-fine"),
            ("Bridget Jones's Diary by Helen Fielding", "https://www.goodreads.com/book/show/227443.Bridget_Jones_s_Diary"),
            ("The Hundred-Year-Old Man Who Climbed Out of the Window and Disappeared by Jonas Jonasson", "https://www.goodreads.com/book/show/13167681"),
            ("A Man Called Ove by Fredrik Backman", "https://www.goodreads.com/book/show/18774964-a-man-called-ove"),
            ("The House in the Cerulean Sea by TJ Klune", "https://www.goodreads.com/book/show/45047384-the-house-in-the-cerulean-sea"),
            ("Good Omens by Neil Gaiman & Terry Pratchett", "https://www.goodreads.com/book/show/12067.Good_Omens"),
            ("The Flatshare by Beth O’Leary", "https://www.goodreads.com/book/show/36478784-the-flatshare"),
            ("The Switch by Beth O'Leary", "https://www.goodreads.com/book/show/45134200-the-switch"),
            ("My Grandmother Asked Me to Tell You She’s Sorry by Fredrik Backman", "https://www.goodreads.com/book/show/23604559-my-grandmother-asked-me-to-tell-you-she-s-sorry")
        ]),
        "sad": to_dict_list([
            ("The Fault in Our Stars by John Green", "https://www.goodreads.com/book/show/11870085-the-fault-in-our-stars"),
            ("A Little Life by Hanya Yanagihara", "https://www.goodreads.com/book/show/22822858-a-little-life"),
            ("Me Before You by Jojo Moyes", "https://www.goodreads.com/book/show/15507958-me-before-you"),
            ("The Book Thief by Markus Zusak", "https://www.goodreads.com/book/show/19063.The_Book_Thief"),
            ("They Both Die at the End by Adam Silvera", "https://www.goodreads.com/book/show/33385229-they-both-die-at-the-end"),
            ("If I Stay by Gayle Forman", "https://www.goodreads.com/book/show/4374400-if-i-stay"),
            ("Bridge to Terabithia by Katherine Paterson", "https://www.goodreads.com/book/show/2835.Bridge_to_Terabithia"),
            ("Tuesdays with Morrie by Mitch Albom", "https://www.goodreads.com/book/show/6900.Tuesdays_with_Morrie"),
            ("The Perks of Being a Wallflower by Stephen Chbosky", "https://www.goodreads.com/book/show/22628.The_Perks_of_Being_a_Wallflower"),
            ("Where the Red Fern Grows by Wilson Rawls", "https://www.goodreads.com/book/show/10365.Where_the_Red_Fern_Grows")
        ]),
        "motivated": to_dict_list([
            ("Can’t Hurt Me by David Goggins", "https://www.goodreads.com/book/show/41721428-can-t-hurt-me"),
            ("Atomic Habits by James Clear", "https://www.goodreads.com/book/show/40121378-atomic-habits"),
            ("Grit by Angela Duckworth", "https://www.goodreads.com/book/show/27213329-grit"),
            ("Mindset by Carol S. Dweck", "https://www.goodreads.com/book/show/40745.Mindset"),
            ("The Power of Now by Eckhart Tolle", "https://www.goodreads.com/book/show/6708.The_Power_of_Now"),
            ("You Are a Badass by Jen Sincero", "https://www.goodreads.com/book/show/15843166-you-are-a-badass"),
            ("The 7 Habits of Highly Effective People by Stephen R. Covey", "https://www.goodreads.com/book/show/36072.The_7_Habits_of_Highly_Effective_People"),
            ("The Subtle Art of Not Giving a F*ck by Mark Manson", "https://www.goodreads.com/book/show/28257707-the-subtle-art-of-not-giving-a-f-ck"),
            ("Start With Why by Simon Sinek", "https://www.goodreads.com/book/show/7108725-start-with-why"),
            ("Deep Work by Cal Newport", "https://www.goodreads.com/book/show/25744928-deep-work")
        ]),
        "romantic": to_dict_list([
            ("Pride and Prejudice by Jane Austen", "https://www.goodreads.com/book/show/1885.Pride_and_Prejudice"),
            ("The Notebook by Nicholas Sparks", "https://www.goodreads.com/book/show/15931.The_Notebook"),
            ("Outlander by Diana Gabaldon", "https://www.goodreads.com/book/show/10964.Outlander"),
            ("Me Before You by Jojo Moyes", "https://www.goodreads.com/book/show/15507958-me-before-you"),
            ("It Ends with Us by Colleen Hoover", "https://www.goodreads.com/book/show/27362503-it-ends-with-us"),
            ("Red, White & Royal Blue by Casey McQuiston", "https://www.goodreads.com/book/show/41150487-red-white-royal-blue"),
            ("The Hating Game by Sally Thorne", "https://www.goodreads.com/book/show/25883848-the-hating-game"),
            ("Beach Read by Emily Henry", "https://www.goodreads.com/book/show/52867387-beach-read"),
            ("The Time Traveler’s Wife by Audrey Niffenegger", "https://www.goodreads.com/book/show/18619684-the-time-traveler-s-wife"),
            ("The Kiss Quotient by Helen Hoang", "https://www.goodreads.com/book/show/36577586-the-kiss-quotient")
        ]),
        "adventurous": to_dict_list([
            ("Life of Pi by Yann Martel", "https://www.goodreads.com/book/show/4214.Life_of_Pi"),
            ("Into the Wild by Jon Krakauer", "https://www.goodreads.com/book/show/1845.Into_the_Wild"),
            ("The Alchemist by Paulo Coelho", "https://www.goodreads.com/book/show/865.The_Alchemist"),
            ("Around the World in Eighty Days by Jules Verne", "https://www.goodreads.com/book/show/54479.Around_the_World_in_Eighty_Days"),
            ("The Hobbit by J.R.R. Tolkien", "https://www.goodreads.com/book/show/5907.The_Hobbit"),
            ("Wild by Cheryl Strayed", "https://www.goodreads.com/book/show/12262741-wild"),
            ("The Call of the Wild by Jack London", "https://www.goodreads.com/book/show/1852.The_Call_of_the_Wild"),
            ("Into Thin Air by Jon Krakauer", "https://www.goodreads.com/book/show/1898.Into_Thin_Air"),
            ("Treasure Island by Robert Louis Stevenson", "https://www.goodreads.com/book/show/295.Treasure_Island"),
            ("Journey to the Center of the Earth by Jules Verne", "https://www.goodreads.com/book/show/32829.Journey_to_the_Center_of_the_Earth")
        ]),
        "curious": to_dict_list([
            ("Sapiens by Yuval Noah Harari", "https://www.goodreads.com/book/show/23692271-sapiens"),
            ("Thinking, Fast and Slow by Daniel Kahneman", "https://www.goodreads.com/book/show/11468377-thinking-fast-and-slow"),
            ("Cosmos by Carl Sagan", "https://www.goodreads.com/book/show/55030.Cosmos"),
            ("A Short History of Nearly Everything by Bill Bryson", "https://www.goodreads.com/book/show/21.A_Short_History_of_Nearly_Everything"),
            ("Astrophysics for People in a Hurry by Neil deGrasse Tyson", "https://www.goodreads.com/book/show/32191710-astrophysics-for-people-in-a-hurry"),
            ("Guns, Germs, and Steel by Jared Diamond", "https://www.goodreads.com/book/show/1842.Guns_Germs_and_Steel"),
            ("The Selfish Gene by Richard Dawkins", "https://www.goodreads.com/book/show/61535.The_Selfish_Gene"),
            ("A Brief History of Time by Stephen Hawking", "https://www.goodreads.com/book/show/3869.A_Brief_History_of_Time"),
            ("The Gene by Siddhartha Mukherjee", "https://www.goodreads.com/book/show/27276428-the-gene"),
            ("The Sixth Extinction by Elizabeth Kolbert", "https://www.goodreads.com/book/show/17910054-the-sixth-extinction")
        ]),
        "scared": to_dict_list([
            ("It by Stephen King", "https://www.goodreads.com/book/show/830502.It"),
            ("The Haunting of Hill House by Shirley Jackson", "https://www.goodreads.com/book/show/89717.The_Haunting_of_Hill_House"),
            ("Bird Box by Josh Malerman", "https://www.goodreads.com/book/show/18498558-bird-box"),
            ("Mexican Gothic by Silvia Moreno-Garcia", "https://www.goodreads.com/book/show/53152636-mexican-gothic"),
            ("The Shining by Stephen King", "https://www.goodreads.com/book/show/11588.The_Shining"),
            ("The Exorcist by William Peter Blatty", "https://www.goodreads.com/book/show/179780.The_Exorcist"),
            ("The Silence of the Lambs by Thomas Harris", "https://www.goodreads.com/book/show/23807.The_Silence_of_the_Lambs"),
            ("Dracula by Bram Stoker", "https://www.goodreads.com/book/show/17245.Dracula"),
            ("Coraline by Neil Gaiman", "https://www.goodreads.com/book/show/17061.Coraline"),
            ("The Turn of the Screw by Henry James", "https://www.goodreads.com/book/show/12948.The_Turn_of_the_Screw")
        ]),
        "relaxed": to_dict_list([
            ("The Little Prince by Antoine de Saint-Exupéry", "https://www.goodreads.com/book/show/157993.The_Little_Prince"),
            ("The Wind in the Willows by Kenneth Grahame", "https://www.goodreads.com/book/show/5659.The_Wind_in_the_Willows"),
            ("Anne of Green Gables by L.M. Montgomery", "https://www.goodreads.com/book/show/8127.Anne_of_Green_Gables"),
            ("The Secret Garden by Frances Hodgson Burnett", "https://www.goodreads.com/book/show/2998.The_Secret_Garden"),
            ("Winnie-the-Pooh by A.A. Milne", "https://www.goodreads.com/book/show/99107.Winnie_the_Pooh"),
            ("My Family and Other Animals by Gerald Durrell", "https://www.goodreads.com/book/show/17150.My_Family_and_Other_Animals"),
            ("Under the Tuscan Sun by Frances Mayes", "https://www.goodreads.com/book/show/11107.Under_the_Tuscan_Sun"),
            ("The Enchanted April by Elizabeth von Arnim", "https://www.goodreads.com/book/show/151469.The_Enchanted_April"),
            ("Big Magic by Elizabeth Gilbert", "https://www.goodreads.com/book/show/24453082-big-magic"),
            ("The Art of Happiness by Dalai Lama", "https://www.goodreads.com/book/show/38210.The_Art_of_Happiness")
        ]),
        "bored": to_dict_list([
            ("The Martian by Andy Weir", "https://www.goodreads.com/book/show/18007564-the-martian"),
            ("Ready Player One by Ernest Cline", "https://www.goodreads.com/book/show/9969571-ready-player-one"),
            ("The Da Vinci Code by Dan Brown", "https://www.goodreads.com/book/show/968.The_Da_Vinci_Code"),
            ("The Girl with the Dragon Tattoo by Stieg Larsson", "https://www.goodreads.com/book/show/2429135.The_Girl_with_the_Dragon_Tattoo"),
            ("The Maze Runner by James Dashner", "https://www.goodreads.com/book/show/6186357-the-maze-runner"),
            ("Gone Girl by Gillian Flynn", "https://www.goodreads.com/book/show/19288043-gone-girl"),
            ("Catching Fire by Suzanne Collins", "https://www.goodreads.com/book/show/6148028-catching-fire"),
            ("Percy Jackson and the Olympians by Rick Riordan", "https://www.goodreads.com/series/43790-percy-jackson-and-the-olympians"),
            ("City of Bones by Cassandra Clare", "https://www.goodreads.com/book/show/256683.City_of_Bones"),
            ("The Hunger Games by Suzanne Collins", "https://www.goodreads.com/book/show/2767052-the-hunger-games")
        ])
    },
    "author": {
        "j.k. rowling": to_dict_list([
            ("Harry Potter and the Sorcerer’s Stone", "https://www.goodreads.com/book/show/3"),
            ("Harry Potter and the Chamber of Secrets", "https://www.goodreads.com/book/show/15881"),
            ("Harry Potter and the Prisoner of Azkaban", "https://www.goodreads.com/book/show/5"),
            ("Harry Potter and the Goblet of Fire", "https://www.goodreads.com/book/show/6"),
            ("Harry Potter and the Order of the Phoenix", "https://www.goodreads.com/book/show/2"),
            ("Harry Potter and the Half-Blood Prince", "https://www.goodreads.com/book/show/1"),
            ("Harry Potter and the Deathly Hallows", "https://www.goodreads.com/book/show/136251"),
            ("Fantastic Beasts and Where to Find Them", "https://www.goodreads.com/book/show/41899"),
            ("The Casual Vacancy", "https://www.goodreads.com/book/show/13497818"),
            ("The Cuckoo's Calling", "https://www.goodreads.com/book/show/16160797")
        ]),
        "george orwell": to_dict_list([
            ("1984", "https://www.goodreads.com/book/show/5470.1984"),
            ("Animal Farm", "https://www.goodreads.com/book/show/7613.Animal_Farm"),
            ("Homage to Catalonia", "https://www.goodreads.com/book/show/13891.Homage_to_Catalonia"),
            ("Down and Out in Paris and London", "https://www.goodreads.com/book/show/97587.Down_and_Out_in_Paris_and_London"),
            ("The Road to Wigan Pier", "https://www.goodreads.com/book/show/21433.The_Road_to_Wigan_Pier"),
            ("Burmese Days", "https://www.goodreads.com/book/show/7145.Burmese_Days"),
            ("Keep the Aspidistra Flying", "https://www.goodreads.com/book/show/37796.Keep_the_Aspidistra_Flying"),
            ("Coming Up for Air", "https://www.goodreads.com/book/show/60917.Coming_Up_for_Air"),
            ("A Clergyman's Daughter", "https://www.goodreads.com/book/show/31544.A_Clergyman_s_Daughter"),
            ("Essays", "https://www.goodreads.com/book/show/398169.Essays")
        ]),
        "jane austen": to_dict_list([
            ("Pride and Prejudice", "https://www.goodreads.com/book/show/1885.Pride_and_Prejudice"),
            ("Sense and Sensibility", "https://www.goodreads.com/book/show/14935.Sense_and_Sensibility"),
            ("Emma", "https://www.goodreads.com/book/show/15736888-emma"),
            ("Mansfield Park", "https://www.goodreads.com/book/show/141150.Mansfield_Park"),
            ("Northanger Abbey", "https://www.goodreads.com/book/show/19341.Northanger_Abbey"),
            ("Persuasion", "https://www.goodreads.com/book/show/233756.Persuasion"),
            ("Lady Susan", "https://www.goodreads.com/book/show/49533.Lady_Susan"),
            ("Love and Friendship", "https://www.goodreads.com/book/show/62748.Love_and_Friendship"),
            ("Juvenilia", "https://www.goodreads.com/book/show/16552749-juvenilia"),
            ("The Watsons", "https://www.goodreads.com/book/show/25458203-the-watsons")
        ]),
        "stephen king": to_dict_list([
            ("The Shining", "https://www.goodreads.com/book/show/11588.The_Shining"),
            ("It", "https://www.goodreads.com/book/show/830502.It"),
            ("Carrie", "https://www.goodreads.com/book/show/10535.Carrie"),
            ("Misery", "https://www.goodreads.com/book/show/2767052-misery"),
            ("Pet Sematary", "https://www.goodreads.com/book/show/46145.Pet_Sematary"),
            ("The Stand", "https://www.goodreads.com/book/show/149267.The_Stand"),
            ("Doctor Sleep", "https://www.goodreads.com/book/show/11815871-doctor-sleep"),
            ("Salem's Lot", "https://www.goodreads.com/book/show/81962.Salem_s_Lot"),
            ("11/22/63", "https://www.goodreads.com/book/show/10223637-11-22-63"),
            ("The Green Mile", "https://www.goodreads.com/book/show/10928.The_Green_Mile")
        ]),
        "agatha christie": to_dict_list([
            ("Murder on the Orient Express", "https://www.goodreads.com/book/show/853510"),
            ("And Then There Were None", "https://www.goodreads.com/book/show/16299.And_Then_There_Were_None"),
            ("The Murder of Roger Ackroyd", "https://www.goodreads.com/book/show/16115.The_Murder_of_Roger_Ackroyd"),
            ("Death on the Nile", "https://www.goodreads.com/book/show/853519"),
            ("The ABC Murders", "https://www.goodreads.com/book/show/92404.The_ABC_Murders"),
            ("Evil Under the Sun", "https://www.goodreads.com/book/show/853513"),
            ("The Mysterious Affair at Styles", "https://www.goodreads.com/book/show/8683.The_Mysterious_Affair_at_Styles"),
            ("A Murder is Announced", "https://www.goodreads.com/book/show/853538"),
            ("Crooked House", "https://www.goodreads.com/book/show/853523"),
            ("The Body in the Library", "https://www.goodreads.com/book/show/92406.The_Body_in_the_Library")
        ]),
        "mark twain": to_dict_list([
            ("The Adventures of Tom Sawyer", "https://www.goodreads.com/book/show/2457.The_Adventures_of_Tom_Sawyer"),
            ("Adventures of Huckleberry Finn", "https://www.goodreads.com/book/show/2956.Adventures_of_Huckleberry_Finn"),
            ("The Prince and the Pauper", "https://www.goodreads.com/book/show/31250.The_Prince_and_the_Pauper"),
            ("Life on the Mississippi", "https://www.goodreads.com/book/show/21851.Life_on_the_Mississippi"),
            ("A Connecticut Yankee in King Arthur's Court", "https://www.goodreads.com/book/show/6849.A_Connecticut_Yankee_in_King_Arthur_s_Court"),
            ("The Innocents Abroad", "https://www.goodreads.com/book/show/15646.The_Innocents_Abroad"),
            ("Roughing It", "https://www.goodreads.com/book/show/35413.Roughing_It"),
            ("The Mysterious Stranger", "https://www.goodreads.com/book/show/13255.The_Mysterious_Stranger"),
            ("The $30,000 Bequest", "https://www.goodreads.com/book/show/13006.The_30_000_Bequest"),
            ("Personal Recollections of Joan of Arc", "https://www.goodreads.com/book/show/13248.Personal_Recollections_of_Joan_of_Arc")
        ]),
        "charles dickens": to_dict_list([
            ("A Tale of Two Cities", "https://www.goodreads.com/book/show/1953.A_Tale_of_Two_Cities"),
            ("Great Expectations", "https://www.goodreads.com/book/show/2623.Great_Expectations"),
            ("Oliver Twist", "https://www.goodreads.com/book/show/730.Oliver_Twist"),
            ("David Copperfield", "https://www.goodreads.com/book/show/766.David_Copperfield"),
            ("Bleak House", "https://www.goodreads.com/book/show/1023.Bleak_House"),
            ("Hard Times", "https://www.goodreads.com/book/show/3142.Hard_Times"),
            ("Little Dorrit", "https://www.goodreads.com/book/show/700.Little_Dorrit"),
            ("The Old Curiosity Shop", "https://www.goodreads.com/book/show/872.The_Old_Curiosity_Shop"),
            ("Nicholas Nickleby", "https://www.goodreads.com/book/show/3716.Nicholas_Nickleby"),
            ("The Pickwick Papers", "https://www.goodreads.com/book/show/2919.The_Pickwick_Papers")
        ]),
        "ernest hemingway": to_dict_list([
            ("The Old Man and the Sea", "https://www.goodreads.com/book/show/2165.The_Old_Man_and_the_Sea"),
            ("A Farewell to Arms", "https://www.goodreads.com/book/show/3354.A_Farewell_to_Arms"),
            ("For Whom the Bell Tolls", "https://www.goodreads.com/book/show/15517.For_Whom_the_Bell_Tolls"),
            ("The Sun Also Rises", "https://www.goodreads.com/book/show/3876.The_Sun_Also_Rises"),
            ("To Have and Have Not", "https://www.goodreads.com/book/show/40486.To_Have_and_Have_Not"),
            ("Islands in the Stream", "https://www.goodreads.com/book/show/105812.Islands_in_the_Stream"),
            ("Death in the Afternoon", "https://www.goodreads.com/book/show/215715.Death_in_the_Afternoon"),
            ("Green Hills of Africa", "https://www.goodreads.com/book/show/215716.Green_Hills_of_Africa"),
            ("The Garden of Eden", "https://www.goodreads.com/book/show/1038702.The_Garden_of_Eden"),
            ("In Our Time", "https://www.goodreads.com/book/show/3385.In_Our_Time")
        ]),
        "dan brown": to_dict_list([
            ("The Da Vinci Code", "https://www.goodreads.com/book/show/968.The_Da_Vinci_Code"),
            ("Angels & Demons", "https://www.goodreads.com/book/show/960.Angels_Demons"),
            ("Inferno", "https://www.goodreads.com/book/show/914.Inferno"),
            ("The Lost Symbol", "https://www.goodreads.com/book/show/34950467-the-lost-symbol"),
            ("Origin", "https://www.goodreads.com/book/show/37580290-origin"),
            ("Digital Fortress", "https://www.goodreads.com/book/show/49413.Digital_Fortress"),
            ("Deception Point", "https://www.goodreads.com/book/show/349503.Deception_Point"),
            ("Wild Symphony", "https://www.goodreads.com/book/show/43222622-wild-symphony"),
            ("Robert Langdon Series", "https://www.goodreads.com/series/41127-robert-langdon"),
            ("The Solomon Key", "https://www.goodreads.com/book/show/3019968-the-solomon-key")
        ]),
        "haruki murakami": to_dict_list([
            ("Norwegian Wood", "https://www.goodreads.com/book/show/11297.Norwegian_Wood"),
            ("Kafka on the Shore", "https://www.goodreads.com/book/show/4929.Kafka_on_the_Shore?ref=nav_sb_ss_1_5"),
            ("1Q84", "https://www.goodreads.com/book/show/10427827-1q84"),
            ("The Wind-Up Bird Chronicle", "https://www.goodreads.com/book/show/11298.The_Wind_Up_Bird_Chronicle"),
            ("Dance Dance Dance", "https://www.goodreads.com/book/show/16778.Dance_Dance_Dance"),
            ("Hard-Boiled Wonderland and the End of the World", "https://www.goodreads.com/book/show/10069.Hard_Boiled_Wonderland_and_the_End_of_the_World"),
            ("South of the Border, West of the Sun", "https://www.goodreads.com/book/show/7802.South_of_the_Border_West_of_the_Sun"),
            ("After Dark", "https://www.goodreads.com/book/show/5483.After_Dark"),
            ("Men Without Women", "https://www.goodreads.com/book/show/33652490-men-without-women?ref=nav_sb_ss_1_17"),
            ("Colorless Tsukuru Tazaki and His Years of Pilgrimage", "https://www.goodreads.com/book/show/41022133-colorless-tsukuru-tazaki-and-his-years-of-pilgrimage?ref=nav_sb_ss_1_10")
        ])
    },
    "language": {
        "english": to_dict_list([
            ("To Kill a Mockingbird", "https://www.goodreads.com/book/show/2657"),
            ("1984", "https://www.goodreads.com/book/show/5470.1984"),
            ("The Catcher in the Rye", "https://www.goodreads.com/book/show/5107"),
            ("The Great Gatsby", "https://www.goodreads.com/book/show/4671"),
            ("Pride and Prejudice", "https://www.goodreads.com/book/show/1885"),
            ("Jane Eyre", "https://www.goodreads.com/book/show/10210"),
            ("The Hobbit", "https://www.goodreads.com/book/show/5907"),
            ("Wuthering Heights", "https://www.goodreads.com/book/show/6185"),
            ("Little Women", "https://www.goodreads.com/book/show/1934"),
            ("Of Mice and Men", "https://www.goodreads.com/book/show/890")
        ]),
        "hindi": to_dict_list([
            ("Godaan", "https://www.goodreads.com/book/show/312496"),
            ("Raag Darbari", "https://www.goodreads.com/book/show/853097"),
            ("Gunahon Ka Devta", "https://www.goodreads.com/book/show/17939153"),
            ("Kamayani", "https://www.goodreads.com/book/show/12154345"),
            ("Maila Anchal", "https://www.goodreads.com/book/show/18581939"),
            ("Pinjar", "https://www.goodreads.com/book/show/19722578"),
            ("Tamas", "https://www.goodreads.com/book/show/3248596"),
            ("Gaban", "https://www.goodreads.com/book/show/18310880"),
            ("Nirmala", "https://www.goodreads.com/book/show/8681326"),
            ("Panchatantra", "https://www.goodreads.com/book/show/6141235")
        ]),
        "french": to_dict_list([
            ("Les Misérables", "https://www.goodreads.com/book/show/24280"),
            ("The Little Prince", "https://www.goodreads.com/book/show/157993"),
            ("The Count of Monte Cristo", "https://www.goodreads.com/book/show/7126"),
            ("Madame Bovary", "https://www.goodreads.com/book/show/2175"),
            ("Germinal", "https://www.goodreads.com/book/show/12201"),
            ("The Stranger", "https://www.goodreads.com/book/show/49552"),
            ("Swann’s Way", "https://www.goodreads.com/book/show/18749"),
            ("The Red and the Black", "https://www.goodreads.com/book/show/52297"),
            ("The Plague", "https://www.goodreads.com/book/show/11989"),
            ("Manon Lescaut", "https://www.goodreads.com/book/show/933714")
        ]),
        "spanish": to_dict_list([
            ("Don Quixote", "https://www.goodreads.com/book/show/3836"),
            ("One Hundred Years of Solitude", "https://www.goodreads.com/book/show/320"),
            ("Love in the Time of Cholera", "https://www.goodreads.com/book/show/9712"),
            ("The House of the Spirits", "https://www.goodreads.com/book/show/9337"),
            ("Like Water for Chocolate", "https://www.goodreads.com/book/show/69685"),
            ("The Shadow of the Wind", "https://www.goodreads.com/book/show/1232"),
            ("Ficciones", "https://www.goodreads.com/book/show/9245"),
            ("Chronicle of a Death Foretold", "https://www.goodreads.com/book/show/63032"),
            ("The Tunnel", "https://www.goodreads.com/book/show/162092"),
            ("Zorro", "https://www.goodreads.com/book/show/77285")
        ]),
        "german": to_dict_list([
            ("Faust", "https://www.goodreads.com/book/show/14590"),
            ("All Quiet on the Western Front", "https://www.goodreads.com/book/show/35569795"),
            ("The Trial", "https://www.goodreads.com/book/show/17690"),
            ("Siddhartha", "https://www.goodreads.com/book/show/52036"),
            ("Perfume", "https://www.goodreads.com/book/show/343"),
            ("Steppenwolf", "https://www.goodreads.com/book/show/16631"),
            ("The Magic Mountain", "https://www.goodreads.com/book/show/77664"),
            ("The Sorrows of Young Werther", "https://www.goodreads.com/book/show/19441"),
            ("Thus Spoke Zarathustra", "https://www.goodreads.com/book/show/51893"),
            ("The Neverending Story", "https://www.goodreads.com/book/show/27712")
        ]),
        "japanese": to_dict_list([
            ("Norwegian Wood", "https://www.goodreads.com/book/show/11297"),
            ("Kafka on the Shore", "https://www.goodreads.com/book/show/4929"),
            ("The Tale of Genji", "https://www.goodreads.com/book/show/11293"),
            ("Battle Royale", "https://www.goodreads.com/book/show/57891"),
            ("Snow Country", "https://www.goodreads.com/book/show/140325"),
            ("The Sailor Who Fell from Grace with the Sea", "https://www.goodreads.com/book/show/77695"),
            ("Kitchen", "https://www.goodreads.com/book/show/50144"),
            ("In the Miso Soup", "https://www.goodreads.com/book/show/57129"),
            ("Out", "https://www.goodreads.com/book/show/79665"),
            ("I Am a Cat", "https://www.goodreads.com/book/show/87155")
        ]),
        "russian": to_dict_list([
            ("War and Peace", "https://www.goodreads.com/book/show/656"),
            ("Anna Karenina", "https://www.goodreads.com/book/show/15823480"),
            ("Crime and Punishment", "https://www.goodreads.com/book/show/7144"),
            ("The Brothers Karamazov", "https://www.goodreads.com/book/show/4934"),
            ("The Master and Margarita", "https://www.goodreads.com/book/show/117833"),
            ("Fathers and Sons", "https://www.goodreads.com/book/show/49363"),
            ("Eugene Onegin", "https://www.goodreads.com/book/show/14666"),
            ("Notes from Underground", "https://www.goodreads.com/book/show/17876"),
            ("Doctor Zhivago", "https://www.goodreads.com/book/show/25621"),
            ("Dead Souls", "https://www.goodreads.com/book/show/188061")
        ]),
        "chinese": to_dict_list([
            ("Dream of the Red Chamber", "https://www.goodreads.com/book/show/160689"),
            ("Journey to the West", "https://www.goodreads.com/book/show/241472"),
            ("The Art of War", "https://www.goodreads.com/book/show/10534"),
            ("Wild Swans", "https://www.goodreads.com/book/show/1848"),
            ("To Live", "https://www.goodreads.com/book/show/108233"),
            ("The Three-Body Problem", "https://www.goodreads.com/book/show/20518872"),
            ("Balzac and the Little Chinese Seamstress", "https://www.goodreads.com/book/show/81658"),
            ("Soul Mountain", "https://www.goodreads.com/book/show/87520"),
            ("Red Sorghum", "https://www.goodreads.com/book/show/321208"),
            ("Frog", "https://www.goodreads.com/book/show/23848320")
        ]),
        "arabic": to_dict_list([
            ("The Cairo Trilogy", "https://www.goodreads.com/book/show/79149"),
            ("Season of Migration to the North", "https://www.goodreads.com/book/show/77102"),
            ("Palace Walk", "https://www.goodreads.com/book/show/79149"),
            ("The Prophet", "https://www.goodreads.com/book/show/2547"),
            ("Girls of Riyadh", "https://www.goodreads.com/book/show/268236"),
            ("In the Eye of the Sun", "https://www.goodreads.com/book/show/578991"),
            ("The Map of Love", "https://www.goodreads.com/book/show/43980"),
            ("Cities of Salt", "https://www.goodreads.com/book/show/359068"),
            ("Frankenstein in Baghdad", "https://www.goodreads.com/book/show/35397013"),
            ("Men in the Sun", "https://www.goodreads.com/book/show/460302")
        ]),
        "korean": to_dict_list([
            ("Please Look After Mom", "https://www.goodreads.com/book/show/8931437"),
            ("The Vegetarian", "https://www.goodreads.com/book/show/25489025"),
            ("Human Acts", "https://www.goodreads.com/book/show/30091914"),
            ("Kim Ji-young, Born 1982", "https://www.goodreads.com/book/show/52239756"),
            ("I’ll Be Right There", "https://www.goodreads.com/book/show/18404183"),
            ("Your Republic is Calling You", "https://www.goodreads.com/book/show/7911823"),
            ("At Dusk", "https://www.goodreads.com/book/show/40957437"),
            ("The Plotters", "https://www.goodreads.com/book/show/39209283"),
            ("No One Writes Back", "https://www.goodreads.com/book/show/15818140"),
            ("The Court Dancer", "https://www.goodreads.com/book/show/37941672")
        ])
    }
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    category = request.form['category']
    option = request.form['option']
    suggestions = books.get(category, {}).get(option, [])
    return render_template('result.html',
                           category=category,
                           option=option,
                           suggestions=suggestions)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)

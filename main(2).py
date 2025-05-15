from flask import Flask, render_template, request

app = Flask(__name__)


# Helper to convert list of (title, link) to list of dicts
def to_dict_list(tuples):
    return [{"title": title, "link": link} for title, link in tuples]


# Book suggestions dictionary with corrected format
books = {
    "age": {
        "10-15":
        to_dict_list([
            ("Harry Potter",
             "https://www.goodreads.com/book/show/3.Harry_Potter"),
            ("Percy Jackson",
             "https://www.goodreads.com/series/45175-percy-jackson"),
            ("Charlotte's Web",
             "https://www.goodreads.com/book/show/24178.Charlotte_s_Web"),
            ("Wonder", "https://www.goodreads.com/book/show/11387515-wonder")
        ]),
        "16-25":
        to_dict_list([
            ("The Hunger Games",
             "https://www.goodreads.com/book/show/2767052"),
            ("The Fault in Our Stars",
             "https://www.goodreads.com/book/show/11870085"),
            ("Eleanor & Park",
             "https://www.goodreads.com/book/show/15745753-eleanor-park"),
            ("Looking for Alaska",
             "https://www.goodreads.com/book/show/99561.Looking_for_Alaska")
        ]),
        "26-40":
        to_dict_list([
            ("Atomic Habits", "https://www.goodreads.com/book/show/40121378"),
            ("The Silent Patient",
             "https://www.goodreads.com/book/show/40097951-the-silent-patient"
             ),
            ("Educated",
             "https://www.goodreads.com/book/show/35133922-educated"),
            ("The Midnight Library",
             "https://www.goodreads.com/book/show/52578297-the-midnight-library"
             )
        ]),
        "40+":
        to_dict_list([
            ("The Alchemist", "https://www.goodreads.com/book/show/865"),
            ("Becoming", "https://www.goodreads.com/book/show/38746485"),
            ("Tuesdays with Morrie",
             "https://www.goodreads.com/book/show/6900.Tuesdays_with_Morrie"),
            ("The Kite Runner",
             "https://www.goodreads.com/book/show/77203.The_Kite_Runner")
        ])
    },
    "genre": {
        "fantasy":
        to_dict_list([
            ("The Hobbit",
             "https://www.goodreads.com/book/show/5907.The_Hobbit"),
            ("Eragon", "https://www.goodreads.com/book/show/113436.Eragon"),
            ("Throne of Glass",
             "https://www.goodreads.com/book/show/7896527-throne-of-glass"),
            ("A Court of Thorns and Roses",
             "https://www.goodreads.com/book/show/16096824-a-court-of-thorns-and-roses"
             )
        ]),
        "mystery":
        to_dict_list([
            ("Gone Girl",
             "https://www.goodreads.com/book/show/19288043-gone-girl"),
            ("The Girl with the Dragon Tattoo",
             "https://www.goodreads.com/book/show/2429135"),
            ("Big Little Lies",
             "https://www.goodreads.com/book/show/19486412-big-little-lies"),
            ("The Da Vinci Code",
             "https://www.goodreads.com/book/show/968.The_Da_Vinci_Code")
        ]),
        "romance":
        to_dict_list([
            ("Pride and Prejudice",
             "https://www.goodreads.com/book/show/1885"),
            ("Me Before You",
             "https://www.goodreads.com/book/show/17347634-me-before-you"),
            ("It Ends With Us",
             "https://www.goodreads.com/book/show/27362503-it-ends-with-us"),
            ("The Notebook",
             "https://www.goodreads.com/book/show/15931.The_Notebook")
        ]),
        "mythology":
        to_dict_list([
            ("The Ramayana",
             "https://www.goodreads.com/book/show/6711206-the-ramayana"),
            ("Norse Mythology",
             "https://www.goodreads.com/book/show/37903770-norse-mythology"),
            ("Mythos", "https://www.goodreads.com/book/show/35074096-mythos"),
            ("The Iliad", "https://www.goodreads.com/book/show/1371.The_Iliad")
        ]),
        "non-fiction":
        to_dict_list([
            ("Sapiens",
             "https://www.goodreads.com/book/show/23692271-sapiens"),
            ("The Subtle Art of Not Giving a F*ck",
             "https://www.goodreads.com/book/show/28257707"),
            ("Educated",
             "https://www.goodreads.com/book/show/35133922-educated"),
            ("The Body",
             "https://www.goodreads.com/book/show/43582376-the-body")
        ]),
        "sci-fi":
        to_dict_list([
            ("Dune", "https://www.goodreads.com/book/show/234225.Dune"),
            ("Ender's Game",
             "https://www.goodreads.com/book/show/375802.Ender_s_Game"),
            ("The Martian",
             "https://www.goodreads.com/book/show/18007564-the-martian"),
            ("Neuromancer",
             "https://www.goodreads.com/book/show/22328.Neuromancer")
        ]),
        "horror":
        to_dict_list([
            ("It", "https://www.goodreads.com/book/show/830502.It"),
            ("The Shining",
             "https://www.goodreads.com/book/show/11588.The_Shining"),
            ("Bird Box",
             "https://www.goodreads.com/book/show/18498558-bird-box"),
            ("The Haunting of Hill House",
             "https://www.goodreads.com/book/show/89717.The_Haunting_of_Hill_House"
             )
        ]),
        "historical":
        to_dict_list([
            ("All the Light We Cannot See",
             "https://www.goodreads.com/book/show/18143977-all-the-light-we-cannot-see"
             ),
            ("The Book Thief",
             "https://www.goodreads.com/book/show/19063.The_Book_Thief"),
            ("The Nightingale",
             "https://www.goodreads.com/book/show/21853621-the-nightingale"),
            ("Wolf Hall",
             "https://www.goodreads.com/book/show/6101138-wolf-hall")
        ]),
        "thriller":
        to_dict_list([
            ("The Girl on the Train",
             "https://www.goodreads.com/book/show/22557272-the-girl-on-the-train"
             ),
            ("Before I Go to Sleep",
             "https://www.goodreads.com/book/show/9736930-before-i-go-to-sleep"
             ),
            ("Behind Closed Doors",
             "https://www.goodreads.com/book/show/29437949-behind-closed-doors"
             ),
            ("The Couple Next Door",
             "https://www.goodreads.com/book/show/28815474-the-couple-next-door"
             )
        ]),
        "self-help":
        to_dict_list([
            ("The 7 Habits of Highly Effective People",
             "https://www.goodreads.com/book/show/36072"),
            ("Think and Grow Rich",
             "https://www.goodreads.com/book/show/30186948-think-and-grow-rich"
             ),
            ("How to Win Friends and Influence People",
             "https://www.goodreads.com/book/show/4865"),
            ("Can't Hurt Me",
             "https://www.goodreads.com/book/show/41721428-can-t-hurt-me")
        ])
    },
    "mood": {
        "happy":
        to_dict_list([
            ("The Little Prince",
             "https://www.goodreads.com/book/show/157993.The_Little_Prince"),
            ("Anne of Green Gables",
             "https://www.goodreads.com/book/show/8127.Anne_of_Green_Gables"),
            ("Matilda", "https://www.goodreads.com/book/show/39988.Matilda"),
            ("Good Vibes, Good Life",
             "https://www.goodreads.com/book/show/42642076-good-vibes-good-life"
             )
        ]),
        "sad":
        to_dict_list([
            ("A Man Called Ove",
             "https://www.goodreads.com/book/show/18774964-a-man-called-ove"),
            ("The Book Thief",
             "https://www.goodreads.com/book/show/19063.The_Book_Thief"),
            ("Five Feet Apart",
             "https://www.goodreads.com/book/show/39939417-five-feet-apart"),
            ("Bridge to Terabithia",
             "https://www.goodreads.com/book/show/2836.Bridge_to_Terabithia")
        ]),
        "anxious":
        to_dict_list([
            ("The Power of Now",
             "https://www.goodreads.com/book/show/6708.The_Power_of_Now"),
            ("Reasons to Stay Alive",
             "https://www.goodreads.com/book/show/25733573-reasons-to-stay-alive"
             ),
            ("The Comfort Book",
             "https://www.goodreads.com/book/show/55660424-the-comfort-book"),
            ("Feel the Fear and Do It Anyway",
             "https://www.goodreads.com/book/show/651153")
        ]),
        "adventurous":
        to_dict_list([
            ("Treasure Island",
             "https://www.goodreads.com/book/show/295.Treasure_Island"),
            ("Life of Pi",
             "https://www.goodreads.com/book/show/4214.Life_of_Pi"),
            ("Around the World in Eighty Days",
             "https://www.goodreads.com/book/show/54479.Around_the_World_in_Eighty_Days"
             ),
            ("Into the Wild",
             "https://www.goodreads.com/book/show/1845.Into_the_Wild")
        ]),
        "hysteria":
        to_dict_list([
            ("The Bell Jar",
             "https://www.goodreads.com/book/show/6514.The_Bell_Jar"),
            ("One Flew Over the Cuckoo's Nest",
             "https://www.goodreads.com/book/show/332613.One_Flew_Over_the_Cuckoo_s_Nest"
             ),
            ("American Psycho",
             "https://www.goodreads.com/book/show/28676.American_Psycho"),
            ("We Have Always Lived in the Castle",
             "https://www.goodreads.com/book/show/861577")
        ]),
        "nostalgia":
        to_dict_list([
            ("Little Women",
             "https://www.goodreads.com/book/show/1934.Little_Women"),
            ("Anne of Avonlea",
             "https://www.goodreads.com/book/show/77390.Anne_of_Avonlea"),
            ("A Tree Grows in Brooklyn",
             "https://www.goodreads.com/book/show/14791.A_Tree_Grows_in_Brooklyn"
             ),
            ("Old Yeller",
             "https://www.goodreads.com/book/show/5477.Old_Yeller")
        ]),
        "hatred":
        to_dict_list([
            ("1984", "https://www.goodreads.com/book/show/5470.1984"),
            ("Lord of the Flies",
             "https://www.goodreads.com/book/show/7624.Lord_of_the_Flies"),
            ("The Handmaid's Tale",
             "https://www.goodreads.com/book/show/38447.The_Handmaid_s_Tale"),
            ("Animal Farm",
             "https://www.goodreads.com/book/show/7613.Animal_Farm")
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
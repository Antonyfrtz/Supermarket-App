# coding: utf8
# Use to add products to database dynamically
import requests

url = "http://localhost:8080/add"
headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'}

products = [
    {
        'name': 'ΟΛΥΜΠΟΣ | Ρόφημα Καρπός Αμύγδαλο',
        'desc': 'Το ΚΑΡΠΟΣ ΑΜΥΓΔΑΛΟ είναι ένα ρόφημα αμυγδάλου το οποίο παράγεται αποκλειστικά από ελληνικά αμύγδαλα. Επιλέγουμε τα καλύτερα αμύγδαλα, σε συνεργασία με τους Έλληνες παραγωγούς και σας προσφέρουμε ένα φυτικό ρόφημα με όλη την υψηλή θρεπτική αξία των ελληνικών καρπών χωρίς προσθήκη ζάχαρης.',
        'catID': 'Dairy',
        'price': '2.29',
        'imageSource': '/images/products/karpos.jpg'
    },
    {
        'name': 'TOTAL | Γιαούρτι Στραγγιστό 5%',
        'desc': 'Γιαούρτι στραγγιστό 5% λιπαρά. Το αγαπημένο στραγγιστό γιαούρτι με την χαρακτηριστική γεύση και βελούδινη υφή.',
        'catID': 'Dairy',
        'price': '3.28',
        'imageSource': '/images/products/product1.jpg'
    },
    {
        'name': 'NIRVANA | Παγωτό Pralines & Cream 650gr',
        'desc': 'Παγωτό καραμέλα με σιρόπι καραμέλας 12,3% και καραμελωμένα πεκάν 8,5%.',
        'catID': 'Dairy',
        'price': '13.47',
        'imageSource': '/images/products/product2.jpg'
    },
    {
        'name': 'THINK BIO | Καρότα Ελληνικά',
        'desc': 'Τα Καρότα Ελληνικά από τη σειρά THINK BIO είναι προϊόντα βιολογικής γεωργίας. Προέρχονται από ελληνικές καλλιέργειες, όπου οι φυτικές προστασίες, η λίπανση και η ανάπτυξη γίνονται με φυσικά και βιολογικά προϊόντα. Τα καρότα περιέχουν πολλές θρεπτικές ουσίες όπως βιταμίνες, αντιοξειδωτικά και ινώδη, που είναι σημαντικά για την υγεία μας.',
        'catID': 'Produce',
        'price': '1.79',
        'imageSource': '/images/products/carrots.jpg'
    },
    {
        'name': 'ΦΡΕΣΚΟΥΛΗΣ | Έτοιμη Σαλάτα Καπριτσιόζα 150g',
        'desc': 'Η Καπριτσιόζα σαλάτα είναι μια έτοιμη σαλάτα λαχανικών, δημοφιλής για την απλότητα και τη γεύση της. Όντας μία από τις πλυμένες φρέσκες σαλάτες του Φρεσκούλη, είναι έτοιμη απλά για να την βάλετε στο πιάτο σας και να την απολαύσετε χωρίς περαιτέρω προεργασία. Κατάλληλη για όλους όσους επιθυμούν να τρέφονται υγιεινά, η συγκεκριμένη σαλάτα μπορεί να αποτελέσει σημαντικό μέρος μιας ολοκληρωμένης διατροφής ενισχύοντας το ανοσοποιητικό σας σύστημα.',
        'catID': 'Vegetables',
        'price': '2.88',
        'imageSource': '/images/products/salad.jpg'
    },
    {
        'name': 'ΒΙΟ | Κολοκύθια Βιολογικής Γεωργίας',
        'desc': 'Το κολοκύθι έχει χαμηλή περιεκτικότητα σε θερμίδες, ενώ παράλληλα προσφέρει στον οργανισμό μας πολύτιμα θρεπτικά συστατικά, όπως φυλλικό οξύ, βιταμίνη Α και κάλιο.',
        'catID': 'Vegetables',
        'price': '1.92',
        'imageSource': '/images/products/kolokythia.jpg'
    },
    {
        'name': 'DOLE | Βιολογικές Μπανάνες Εισαγωγής',
        'desc': 'Η καλλιέργεια γίνεται χωρίς χημικά προϊόντα και συνθετικά λιπάσματα. Οι μέθοδοι καλλιέργειας που χρησιμοποιούμε αποσκοπούν στη βελτίωση της γονιμότητας του εδάφους καθώς και στην καταπολέμηση των παρασίτων και τον περιορισμό των ασθενειών με βιολογικές μεθόδους. Είναι πηγή φυτικών ινών και βιταμίνης C.',
        'catID': 'Fruit',
        'price': '2.48',
        'imageSource': '/images/products/bananas.jpg'
    },
    {
        'name': 'Μάνγκο Συσκευασμένα Εισαγωγής',
        'desc': 'Μάνγκο συσκευασμένα εισαγωγής. Πλούσια γεύση, πλούσιο σε θρεπτικά συστατικά, ελάχιστες θερμίδες.',
        'catID': 'Fruit',
        'price': '2.67',
        'imageSource': '/images/products/mango.jpg'
    },
    {
        'name': 'ΒΙΟ | Πορτοκάλια Βαλέντσια Χυμού',
        'desc': 'Τα πορτοκάλια αποτελούν πλούσια πηγή βιταμίνης C, η οποία λόγω της αντιοξειδωτικής της δράσης, προστατεύει την υγεία της καρδιάς και την εμφάνιση διαφόρων τύπου καρκίνου. Προτιμήστε να τα καταναλώνετε ολόκληρα, αντί για χυμό, καθώς έτσι είναι πλουσιότερα σε φυτικές ίνες. Αν τα στύψετε, μην σουρώσετε το χυμό, γιατί με τον τρόπο αυτό αφαιρείτε φυτικές ίνες.',
        'catID': 'Fruit',
        'price': '2.80',
        'imageSource': '/images/products/oranges.jpg'
    },
    {
        'name': 'ΠΙΝΔΟΣ | Μπούτια Νωπού Κοτόπουλου 800g',
        'desc': 'Μπούτια νωπού ελληνικού κοτόπουλου. Το νόστιμο, ορεινό κοτόπουλο, φρέσκο και μεγαλωμένο σε ορεινό κλίμα. Το νωπό μπούτι είναι το μηριαίο οστούν, το κνημιαίο οστούν, και η περόνη μαζί με το μυϊκό σύστημα που τα περιβάλει. Οι τομές πρέπει να πραγματοποιούνται στις κλειδώσεις. Επίσης περιλαμβάνει ένα κομμάτι της ράχης προσκολλημένο πάνω του, εφόσον το βάρος του δεύτερου μέρους δεν υπερβαίνει το 25% του συνολικού βάρους του κομματιού. Μπορεί να προσφέρεται με ή χωρίς δέρμα.',
        'catID': 'Meat',
        'price': '6.38',
        'imageSource': '/images/products/chicken.jpg'
    },
    {
        'name': 'BARILLA | Τορτελίνι Με Τυρί 250gr',
        'desc': 'Τα Tortellini αποτελούν αναπόσπαστο κομμάτι της Ιταλικής γαστρονομίας. Γεννήθηκαν στην Ιταλική περιοχή της Emilia (πιο συγκεκριμένα στην Bologna και τη Modena).Πλούσια γέμιση από τυρια, είναι το ιδανικό ζυμαρικο για να μετατρέψεις μια απλή συνταγή σε γαστρονομική, προσθέτοντας λίγη κοκκινη σαλτσα ή λευκη και τα αγαπημένα σου λαχανικά.',
        'catID': 'Pasta',
        'price': '2.59',
        'imageSource': '/images/products/tortellini.jpg'
    },
    {
        'name': 'BARILLA | Penne Rigate 500gr',
        'desc': 'Τα ζυμαρικά Penne Rigate προτιμούνται  σε πολλές περιπτώσεις, ως το πιο κλασικό πιάτο στο οικογενειακό τραπέζι. Όλοι απολαμβάνουν το φαγητό τους πάνω από ένα ωραίο αχνιστό πιάτο με μακαρόνια Penne Rigate Barilla με κόκκινη σαλτσα Αrrabbiata ή με ραγού φυσικά με συνοδεία από τριμμενο τυρι. Είναι επίσης ιδανικά για μακαρονοσαλατές ή σαλατα με θαλασσινα.',
        'catID': 'Pasta',
        'price': '1.30',
        'imageSource': '/images/products/penne.jpg'
    },
    {
        'name': 'BARILLA | Farfalle No 65 500 gr',
        'desc': 'Τα μακαρόνια Barilla Farfalle (Φιογκάκια) φτιάχνονται από ένα φύλλο ζύμης που κόβεται σε τετραγωνάκια και "τσιμπιέται" στο κέντρο  η οποία ξαφνιάζει τον ουρανίσκο, μέσω της διαφορετικής υφής του πιο χοντρού κεντρικού τμήματος και των δύο άκρων: μια πραγματική απόλαυση για τους καλοφαγάδες. Από τα πιο χαρούμενα σχήματα στην κουζίνα, τα ζυμαρικά Farfalle, όπως οι πεταλούδες, πετούν από τη μία γεύση στην άλλη, και προσαρμόζονται σε πολλούς διαφορετικούς συνδυασμούς γεύσεων. Εμείς προτείνουμε να τα δοκιμάσετε σε σαλατα με τονο, πιπεριες , λαχανικα και ελαιολαδο συνθέτοντας την πιο μοναδική μακαρονοσαλατα.',
        'catID': 'Pasta',
        'price': '1.31',
        'imageSource': '/images/products/farfalle.jpg'
    },
    {
        'name': 'ΚΤΗΜΑ ΑΛΦΑ | Οίνος Λευκός Ξηρός 750ml',
        'desc': 'ΓΕΜΑΤΟ ΜΕ ΕΞΑΙΡΕΤΙΚΗ ΙΣΟΡΡΟΠΙΑ, ΔΡΟΣΙΑ ΚΑΙ ΦΙΝΕΤΣΑ. ΖΩΗΡΗ ΚΑΙ ΜΑΚΡΑΣ ΔΙΑΡΚΕΙΑΣ ΕΠΙΓΕΥΣΗ. ΑΡΩΜΑΤΑ ΛΕΥΚΩΝ ΛΟΥΛΟΥΔΙΩΝ, ΕΣΠΕΡΙΔΟΕΙΔΩΝ ΚΑΙ ΔΙΑΚΡΙΤΙΚΩΝ ΑΡΩΜΑΤΙΚΩΝ ΒΟΤΑΝΩΝ.',
        'catID': 'Liquor',
        'price': '14.52',
        'imageSource': '/images/products/wine1.jpg'
    },
    {
        'name': 'KELLOGGS | Δημητριακά Krave 410g',
        'desc': 'Τα KRAVE είναι τραγανά μαξιλαράκια με λαχταριστή γέμιση γεύσης πραλίνας φουντουκιού. Είτε για πρωινό, είτε για απογευματινό σνακ, ένα είναι σίγουρο τα KRAVE είναι ΜΙΑΜ ΜΙΑΜ!',
        'catID': 'Sweets',
        'price': '8.05',
        'imageSource': '/images/products/krave.jpg'
    },
    {
        'name': 'ΟΛΥΜΠΟΣ | Γάλα Υψηλής Παστερίωσης 3,7%',
        'desc': 'Το βιολογικό γάλα ΟΛΥΜΠΟΣ συλλέγεται καθημερινά από ελληνικές πιστοποιημένες βιολογικές κτηνοτροφικές μονάδες. Προέρχεται από αγελάδες που τρέφονται με φυτικές βιολογικές τροφές, ακολουθώντας όλους τους κανόνες πιστοποίησης των βιολογικών προϊόντων. Με σεβασμό στη φύση, με γεύση πλούσια, φυσική, παράγουμε ένα 100% βιολογικό γάλα για εσάς αλλά πολύ περισσότερο για τα παιδιά σας. Το βιολογικό γάλα ΟΛΥΜΠΟΣ με 3,7% λιπαρά, παράγεται από 100% ελληνικό φρέσκο γάλα.',
        'catID': 'Dairy',
        'price': '2.33',
        'imageSource': '/images/products/milk1.jpg'
    }
]

for product in products:
    response = requests.post(url, headers=headers, data=product)
    print(response.text)

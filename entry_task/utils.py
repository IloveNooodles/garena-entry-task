# Parser buat json/forms
def is_parse_body_correct(dict, list_of_keys):
    for keys in list_of_keys:
        if keys not in dict:
            return False

    return True


# Django form ini replica models dari djangonya tapi gak harus sama persis ato bisa ada pre processing dan ini udah ada auto validasi dan ada validasinya sendiri di django fieldnya (custom validator)

# data sensitive itu gak perlu di return dan ada beberapa yang engga. Contoh data yang bisa di return itu biasaanya kalo mau nambahin question, nanti postnya updated nambah 1 question nanti updatednya bisa returnn lewat data. Intinya nge save satu request biar user ga perlu get lagi

# JWT itu identifier jadi sensitive information gak usah dimasukin
# referal code boleh semua info yang gak sensitive aja

# uuid uuid4 ini udah fixed length jadi ref_code nya gak bisa lebih pendek. Jadi harus ngecheck expected usernya ada berapa biar nanti ref codenya bisa nyesuain

# ambil sesuatu yg unique obfuscate username aja bahkan bisa, cuma make username doang tapi bisa liat usernamenya apa. Biasanya make cypher jadi di encode si usernamenya jadi challengenya cyphernya harus lebih complicated lagi PIKIR LAGI1!!

# bisa batch update make cron jobs tiap jam di queue juga. Contohyna twitter, leaderboard


# Readibility tuh pinting banget, soalnya harus bisa di baca sama orang lain, jadi ada beberapa, JsonResponse error, email_validation dan tiap function ada goalsnya sendiri yang di describe sama function name, ada beberapa tipe. Kaya misal general, parse request body di utils kalo app specific

# Kalo logicnya app spesific 1 app yg pengen ref code nya 8, tp ad 1 lagi numbers ini bisa ditaro di modelsnya lgsg sesuatu yg gaada behavioural ini GENERAL BGT ditaro di django/www/ ini ada nested django www

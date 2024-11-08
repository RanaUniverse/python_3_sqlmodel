from faker import Faker

fake = Faker()

abc = fake.name()
# abc = fake.word("conjunction")
abc = two_word_name = fake.word("noun") + " " + fake.word("adjective")
abc =            page_number= fake.random_int(100,500,5)
abc =            price_in_inr=fake.random_int(99,999,10)

print(abc)

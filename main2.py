from faker import Faker
import random

fake = Faker()

# abc = fake.word("conjunction")
abc = two_word_name = fake.word("noun") + " " + fake.word("adjective")
abc = page_number = fake.random_int(100, 500, 5)
abc = price_in_inr = fake.random_int(99, 999, 10)

abc1 = two_word = fake.word("adjective") + " " + fake.word("noun") + " Store"
abc2 = two_word = fake.word("adjective") + " " + fake.word("noun") + " Library"
abc3 = two_word = fake.word("adjective") + " " + fake.word("noun") + " Center"

abc = random.choice([abc1, abc2, abc3])

abc = two_word = (
    f"{fake.word('adjective')} {fake.word('noun')} {random.choice(['Store', 'Library', 'Center'])}"
)

abc = two_word = (
    f"{fake.word('adjective')} "
    f"{fake.word('noun')} "
    f"{random.choice(['Store', 'Library', 'Center'])}"
)


print(abc)

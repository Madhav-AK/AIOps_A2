import pandas as pd
import random as random

first_names = ["sujal", "madhav", "raghav", "pulkit", "rohan", "vrishab", "pakshal"]
middle_names = ["kumar", "arun", "jayant", "rohit", "aditya", "ramesh"]
last_names = ["singh", "bhatra", "bhatt", "shetty", "reddy", "iyengar", "jindal", "ambani"]
domains = ["@gmail.com", "@iitm.ac.in", "@yahoo.com", "@hotmail.com", "@outlook.com"]
malformed_domains = ["gmail.", "@yahoo", "@iitm", "@out@look.com", "hotmail@com"]

RANDOM_STATE = 42
random.seed(RANDOM_STATE)

def generate(csv_id, starting_index, n_samples):
    data = []
    for id in range(starting_index, starting_index + n_samples):
        a = random.choice(first_names) 
        b = random.choice(middle_names)
        c = random.choice(last_names)
        d = random.randint(1, 5000)
        phone = random.randint(10**9, 10**10 - 1)
        is_malformed = random.randint(0, 1)
        if is_malformed:
            is_missing = random.randint(0, 3)
            if is_missing in (1, 2, 3):
                e = random.choice(domains)
                email = f"{a}.{b}.{c}.{d}{e}"
                row = [id, a, email, phone, 0]
                row[is_missing] = None
                data.append(row)
            else:
                e = random.choice(malformed_domains)
                email = f"{a}.{b}.{c}.{d}{e}"
                row = [id, a, email, phone, 0]
                data.append(row)
        else:
            e = random.choice(domains)
            email = f"{a}.{b}.{c}.{d}{e}"
            row = [id, a, email, phone, 1]
            data.append(row)

    df = pd.DataFrame(data, columns=['id', 'first name', 'email', 'phone', 'is_valid'])
    df.to_csv(f"data/user_signup_data_{csv_id}.csv", index=False)



if __name__ == "__main__":
    samples_per_record = 100
    for i in range(8):
        generate(i+1, i*samples_per_record, samples_per_record)

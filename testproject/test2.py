import random

def generate_indian_phone_number():
    # Indian phone numbers start with 6, 7, 8, or 9 and are 10 digits long
    first_digit = random.choice(['6', '7', '8', '9'])
    rest_digits = ''.join([str(random.randint(0, 9)) for _ in range(9)])
    return f"+91{first_digit}{rest_digits}"

def generate_vcf_file(filename, num_contacts):
    with open(filename, 'w') as vcf_file:
        for i in range(1, num_contacts + 1):
            name = f"Dummy Contact {i}"
            phone_number = generate_indian_phone_number()
            vcf_file.write("BEGIN:VCARD\n")
            vcf_file.write("VERSION:3.0\n")
            vcf_file.write(f"FN:{name}\n")
            vcf_file.write(f"TEL;TYPE=CELL:{phone_number}\n")
            vcf_file.write("END:VCARD\n")

# Generate a VCF file with 10,000 dummy contacts
generate_vcf_file("dummy_contacts.vcf", 10000)

print("VCF file with 10,000 dummy contacts generated successfully!")
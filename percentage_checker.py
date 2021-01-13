
print('Decrypted text using bombe settings:')
bombe_output = input().replace(" ", "").upper()

print('Actual decrypted text:')
actual_output = input().replace(" ", "").upper()

assert len(bombe_output) == len(
    actual_output), "Length of output and actual decryption should be the same, bombe_output was {} and actual_output was {}".format(len(bombe_output), len(actual_output))

matched_letters = 0
for i in range(len(bombe_output)):
    if (bombe_output[i] == actual_output[i]):
        matched_letters += 1

percentage_match = matched_letters/len(bombe_output) * 100
print('{:.2f}% Matched'.format(percentage_match))

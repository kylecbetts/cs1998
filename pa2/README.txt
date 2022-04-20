Name: Kyle Betts
NetID: kcb82

Challenges Attempted: Tier I, II, III

Tier I:
It is important that these routes have password protection because we don't 
want a user to be able to act on behalf of another user. In order 
to have password protection, we need to collect their password when they 
create an account, which is why we have a password field in the create_user 
endpoint. Next, we don't want a user to see another user's balance using the 
get_user endpoint so we take in a password and confirm the user is the owner 
of the account being accessed. Finally, we don't want a user to send money 
on behalf of another user, so we collect the sender's password on the 
send_money endpoint and confirm the owner of the sending account is 
authorizing the send.

Tier II:
Password hashing is important because we don't want to save plain text 
passwords in our database. If our database is compromised and the passwords 
are plain text, then the user's accounts are not safe, and if they reuse 
passwords on other sites, they can be compromised on other sites as well. 
Hashing is a one way function, meaning plain text can be hashed, but a hashed 
value is not easily converted back to plain text. When a password is provided, 
the hash is taken, and then compared to the value in the database. Even if a 
hacker gets the hash value from the database, they still cannot access a 
user's account since they need the plain text version. 

Tier III:
A rainbow table is a list of precomputed hashes corresponding to the original 
plain text values. These can be used to determine a user's plain text password 
if the hashed values in a database become compromised. For common and simple 
passwords, most of them will be found in a rainbow table, meaning a database's 
compromised hashed values can be converted to original plain text passwords. 
Salting is adding a random and unique string to the front of a user's password 
before it is hashed so that the resulting password is very unique and will 
unlikely appear in a rainbow table. This increases the security in the case 
that the database's hashed passwords are compromised. Iterative hashing is 
hashing the hash of the plain-text password. This once again increases 
originality in the final hash value, and also adds another step of un-hashing 
that would be required to find the plain-text password. Now, if the database's 
hashed password is found, it needs to be un-hashed from a rainbow table, to get 
the first hash value, and that hash value would need to be unhashed from the 
rainbow table to get the original password. Both the first hash value and the 
second hashed value would have to be in the rainbow table to get back the 
original password. This is extremely secure. The password can even be iteratively 
hashed as many times as desired, with more iterations being even more secure since 
each hash computed has to be in the rainbow table to get the original plain text 
password.
INSERT INTO email_vectors 
(email_id, sender, recipient, subject, body, content, date, thread_id, embedding) 
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (email_id) DO NOTHING
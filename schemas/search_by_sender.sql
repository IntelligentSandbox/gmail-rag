SELECT email_id, sender, recipient, subject, body, content, date, thread_id, 1.0 as similarity
FROM email_vectors 
WHERE LOWER(sender) LIKE LOWER(%s)
ORDER BY date DESC 
LIMIT %s